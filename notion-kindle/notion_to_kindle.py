#!/usr/bin/env python3
"""
Notion -> Kindle pipeline.

For each book defined in books.json this script:
  1. Recursively pulls a Notion root page and every nested subpage / database
     via the Notion API and converts it to a single Markdown document, with
     each top-level subpage becoming a chapter.
  2. Runs Pandoc to turn that Markdown into an EPUB (reflowable, with a table
     of contents) — the format Kindle handles best.
  3. Validates the EPUB with epubcheck (if available); a book that fails
     validation is not emailed.
  4. Emails the EPUB to your Send-to-Kindle address so it lands in
     Library -> Docs and syncs to all your devices.

Configuration comes entirely from environment variables (secrets) plus the
non-secret books.json, so nothing sensitive lives in the repo.

Required env vars:
  NOTION_TOKEN   Notion internal-integration token (the page must be shared
                 with the integration).
  KINDLE_EMAIL   Your @kindle.com Send-to-Kindle address.
  SMTP_USER      Mailbox to send from (e.g. your Gmail). Must be on Amazon's
                 approved personal-document sender list.
  SMTP_PASS      App password for that mailbox.

Optional env vars:
  SMTP_HOST      Default: smtp.gmail.com
  SMTP_PORT      Default: 587 (STARTTLS)
  FROM_EMAIL     Default: SMTP_USER
  BOOKS_FILE     Default: books.json (next to this script)
  OUTPUT_DIR     Default: ./build
  SKIP_SEND      If set to "1", build the EPUBs but do not email them.
  EPUBCHECK_JAR  Path to epubcheck.jar (default /usr/share/java/epubcheck.jar).
                 If neither the jar (+ java) nor an `epubcheck` command is found,
                 validation is skipped with a warning.
  SKIP_VALIDATE  If set to "1", skip epubcheck validation.
"""

import json
import os
import shutil
import smtplib
import subprocess
import sys
import time
from email.message import EmailMessage
from pathlib import Path

import requests

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
HERE = Path(__file__).resolve().parent

TOKEN = os.environ.get("NOTION_TOKEN", "")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}

# Gentle throttle so we stay under Notion's ~3 requests/second limit.
REQUEST_PAUSE = 0.34


def _get(url, params=None):
    """GET with basic retry/backoff for rate limits and transient errors."""
    for attempt in range(5):
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        if resp.status_code == 429:
            wait = float(resp.headers.get("Retry-After", 2 ** attempt))
            time.sleep(wait)
            continue
        if resp.status_code >= 500:
            time.sleep(2 ** attempt)
            continue
        resp.raise_for_status()
        time.sleep(REQUEST_PAUSE)
        return resp.json()
    resp.raise_for_status()


def _post(url, payload):
    for attempt in range(5):
        resp = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        if resp.status_code == 429:
            wait = float(resp.headers.get("Retry-After", 2 ** attempt))
            time.sleep(wait)
            continue
        if resp.status_code >= 500:
            time.sleep(2 ** attempt)
            continue
        resp.raise_for_status()
        time.sleep(REQUEST_PAUSE)
        return resp.json()
    resp.raise_for_status()


def get_block_children(block_id):
    """Return all child blocks of a block/page, following pagination."""
    blocks = []
    cursor = None
    while True:
        params = {"page_size": 100}
        if cursor:
            params["start_cursor"] = cursor
        data = _get(f"{NOTION_API}/blocks/{block_id}/children", params=params)
        blocks.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return blocks


def plain_title(props):
    """Pull a human title out of a Notion page's properties object."""
    for value in props.values():
        if value.get("type") == "title":
            return "".join(t.get("plain_text", "") for t in value["title"]) or "Untitled"
    return "Untitled"


def get_page_title(page_id):
    data = _get(f"{NOTION_API}/pages/{page_id}")
    return plain_title(data.get("properties", {}))


def query_database(database_id):
    """Return all row-pages of a database."""
    rows = []
    cursor = None
    while True:
        payload = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor
        data = _post(f"{NOTION_API}/databases/{database_id}/query", payload)
        rows.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return rows


def rich_text_to_md(rich_text):
    out = []
    for span in rich_text:
        text = span.get("plain_text", "")
        if not text:
            continue
        ann = span.get("annotations", {})
        if ann.get("code"):
            text = f"`{text}`"
        else:
            if ann.get("bold"):
                text = f"**{text}**"
            if ann.get("italic"):
                text = f"*{text}*"
            if ann.get("strikethrough"):
                text = f"~~{text}~~"
        href = span.get("href")
        if href:
            text = f"[{text}]({href})"
        out.append(text)
    return "".join(out)


def hashes(level):
    return "#" * max(1, min(level, 6))


def render_blocks(blocks, level, lines):
    """Convert a flat list of Notion blocks to Markdown lines.

    `level` is the current heading depth so that headings and nested subpages
    sit correctly under their parent page.
    """
    for block in blocks:
        btype = block.get("type")
        data = block.get(btype, {}) if btype else {}
        rich = data.get("rich_text", [])
        text = rich_text_to_md(rich) if rich else ""

        if btype == "child_page":
            render_page(block["id"], level + 1, lines, title=data.get("title"))
        elif btype == "child_database":
            render_database(block["id"], level + 1, lines, title=data.get("title"))
        elif btype == "paragraph":
            if text:
                lines.append(text + "\n")
        elif btype in ("heading_1", "heading_2", "heading_3"):
            offset = {"heading_1": 1, "heading_2": 2, "heading_3": 3}[btype]
            lines.append(f"{hashes(level + offset)} {text}\n")
        elif btype == "bulleted_list_item":
            lines.append(f"- {text}")
            _render_children_inline(block, lines, indent="  ")
        elif btype == "numbered_list_item":
            lines.append(f"1. {text}")
            _render_children_inline(block, lines, indent="   ")
        elif btype == "to_do":
            mark = "x" if data.get("checked") else " "
            lines.append(f"- [{mark}] {text}")
        elif btype == "toggle":
            lines.append(f"**{text}**\n")
            _render_children_inline(block, lines, indent="")
        elif btype == "quote":
            lines.append(f"> {text}\n")
        elif btype == "callout":
            icon = (data.get("icon") or {}).get("emoji", "")
            lines.append(f"> {icon} {text}\n".strip() + "\n")
        elif btype == "code":
            lang = data.get("language", "")
            body = "".join(t.get("plain_text", "") for t in rich)
            lines.append(f"```{lang}\n{body}\n```\n")
        elif btype == "divider":
            lines.append("---\n")
        elif btype == "equation":
            lines.append(f"$$\n{data.get('expression', '')}\n$$\n")
        elif btype == "image":
            url = _file_url(data)
            cap = rich_text_to_md(data.get("caption", []))
            if url:
                lines.append(f"![{cap}]({url})\n")
        elif btype == "bookmark":
            url = data.get("url", "")
            if url:
                lines.append(f"[{url}]({url})\n")
        elif btype == "table":
            render_table(block["id"], lines)
        else:
            # Unknown / unsupported block: emit its text if any, else skip.
            if text:
                lines.append(text + "\n")
            if block.get("has_children") and btype not in ("column_list", "column"):
                _render_children_inline(block, lines, indent="")
        # Recurse into structural containers that hold real content.
        if btype in ("column_list", "column") and block.get("has_children"):
            render_blocks(get_block_children(block["id"]), level, lines)


def _render_children_inline(block, lines, indent):
    if not block.get("has_children"):
        return
    children = get_block_children(block["id"])
    sub = []
    render_blocks(children, 6, sub)
    for line in sub:
        for piece in line.split("\n"):
            lines.append(indent + piece if piece else piece)


def _file_url(data):
    f = data.get("external") or data.get("file") or {}
    return f.get("url", "")


def render_table(table_id, lines):
    rows = get_block_children(table_id)
    md_rows = []
    for row in rows:
        if row.get("type") != "table_row":
            continue
        cells = row["table_row"]["cells"]
        md_rows.append([rich_text_to_md(c) for c in cells])
    if not md_rows:
        return
    header = md_rows[0]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")
    for r in md_rows[1:]:
        lines.append("| " + " | ".join(r) + " |")
    lines.append("")


def render_page(page_id, level, lines, title=None):
    if title is None:
        title = get_page_title(page_id)
    lines.append(f"\n{hashes(level)} {title}\n")
    render_blocks(get_block_children(page_id), level, lines)


def render_database(database_id, level, lines, title=None):
    if not title:
        title = "Database"
    lines.append(f"\n{hashes(level)} {title}\n")
    rows = query_database(database_id)
    for row in rows:
        row_title = plain_title(row.get("properties", {}))
        render_page(row["id"], level + 1, lines, title=row_title)


def build_markdown(book):
    """Return a Markdown string for one book, including YAML metadata."""
    root_id = book["root_page_id"].replace("-", "")
    lines = []
    # Render the root page's own intro content at level 1, then its subpages
    # become chapters (also level-1 headings -> Pandoc chapter splits).
    render_blocks(get_block_children(root_id), 1, lines)
    body = "\n".join(lines)

    meta = (
        "---\n"
        f"title: \"{book['title']}\"\n"
        f"author: \"{book.get('author', 'Notion')}\"\n"
        f"lang: en\n"
        f"date: \"{time.strftime('%Y-%m-%d')}\"\n"
        "---\n\n"
    )
    return meta + body


def make_epub(book, markdown_text, output_dir):
    md_path = output_dir / f"{book['filename']}.md"
    epub_path = output_dir / f"{book['filename']}.epub"
    md_path.write_text(markdown_text, encoding="utf-8")
    cmd = [
        "pandoc",
        str(md_path),
        "-o", str(epub_path),
        "--toc",
        "--toc-depth=2",
        "--epub-chapter-level=1",
        "--metadata", f"title={book['title']}",
        "--from", "markdown+pipe_tables+task_lists+tex_math_dollars",
    ]
    subprocess.run(cmd, check=True)
    return epub_path


def validate_epub(epub_path):
    """Validate an EPUB with epubcheck. Returns (ok, detail).

    Skips (ok=True) with a note if no validator is available, so the pipeline
    still runs in environments without epubcheck installed.
    """
    jar = os.environ.get("EPUBCHECK_JAR", "/usr/share/java/epubcheck.jar")
    if shutil.which("java") and Path(jar).is_file():
        cmd = ["java", "-jar", jar, str(epub_path)]
    elif shutil.which("epubcheck"):
        cmd = ["epubcheck", str(epub_path)]
    else:
        return True, "skipped (epubcheck not found)"

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = (result.stdout + result.stderr).strip()
    if result.returncode != 0:
        return False, output
    # epubcheck prints a "Messages: ..." summary line on success; surface it.
    summary = next(
        (ln.strip() for ln in output.splitlines() if "Messages:" in ln), "valid"
    )
    return True, summary


def send_to_kindle(epub_path, book):
    kindle_email = os.environ["KINDLE_EMAIL"]
    smtp_user = os.environ["SMTP_USER"]
    smtp_pass = os.environ["SMTP_PASS"]
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    from_email = os.environ.get("FROM_EMAIL", smtp_user)

    msg = EmailMessage()
    msg["Subject"] = book["title"]
    msg["From"] = from_email
    msg["To"] = kindle_email
    msg.set_content(
        f"Automated delivery of '{book['title']}' from Notion.\n"
        "Sent by the notion-kindle pipeline."
    )
    msg.add_attachment(
        epub_path.read_bytes(),
        maintype="application",
        subtype="epub+zip",
        filename=epub_path.name,
    )

    with smtplib.SMTP(smtp_host, smtp_port, timeout=60) as smtp:
        smtp.starttls()
        smtp.login(smtp_user, smtp_pass)
        smtp.send_message(msg)


def main():
    if not TOKEN:
        sys.exit("NOTION_TOKEN is not set.")

    books_file = Path(os.environ.get("BOOKS_FILE", HERE / "books.json"))
    books = json.loads(books_file.read_text(encoding="utf-8"))

    output_dir = Path(os.environ.get("OUTPUT_DIR", HERE / "build"))
    output_dir.mkdir(parents=True, exist_ok=True)

    skip_send = os.environ.get("SKIP_SEND") == "1"
    skip_validate = os.environ.get("SKIP_VALIDATE") == "1"
    failures = 0

    for book in books:
        print(f"==> Building '{book['title']}'")
        markdown_text = build_markdown(book)
        epub_path = make_epub(book, markdown_text, output_dir)
        size_kb = epub_path.stat().st_size / 1024
        print(f"    EPUB written: {epub_path.name} ({size_kb:.0f} KB)")

        if not skip_validate:
            ok, detail = validate_epub(epub_path)
            if not ok:
                failures += 1
                print(f"    epubcheck FAILED — not emailing this book:\n{detail}")
                continue
            print(f"    epubcheck: {detail}")

        if skip_send:
            print("    SKIP_SEND=1 -> not emailing.")
            continue
        send_to_kindle(epub_path, book)
        print(f"    Emailed to {os.environ['KINDLE_EMAIL']}")

    if failures:
        sys.exit(f"{failures} book(s) failed EPUB validation.")
    print("Done.")


if __name__ == "__main__":
    main()
