# Notion → Kindle

Automatically pushes Notion pages **and all their subpages** to your Kindle
library as EPUBs.

There is no native Notion→Kindle sync, so this is a 3-stage pipeline:

1. **Extract** — pull a Notion root page and every nested subpage/database via
   the Notion API and flatten it into one Markdown document (each top-level
   subpage becomes a chapter).
2. **Convert** — run Pandoc to produce a reflowable **EPUB** with a table of
   contents. EPUB (not PDF) is what reads well on a Kindle.
3. **Validate** — run [epubcheck](https://www.w3.org/publishing/epubcheck/) on
   each EPUB; a book that fails validation is *not* emailed (the run exits
   non-zero so the failure is visible). Skipped automatically if epubcheck
   isn't installed; force-skip with `SKIP_VALIDATE=1`.
4. **Deliver** — email the EPUB to your `@kindle.com` Send-to-Kindle address.
   It shows up under **Library → Docs** and syncs to all your devices.

A scheduled GitHub Action (`.github/workflows/notion-to-kindle.yml`) runs the
whole thing daily, and you can trigger it manually any time.

## What gets sent

The books are configured in [`books.json`](./books.json). Currently:

| Book | Notion root page |
| --- | --- |
| Project Management & Leadership — Knowledge Base | `37484611-d24c-815c-b3dc-ded7283db09e` |
| Scaling & Operating Frameworks — Reference Library | `36a84611-d24c-81de-ae52-e1c319c95072` |

To add/remove a book, edit `books.json`. The `root_page_id` is the UUID in the
page's URL.

## One-time setup

### 1. Create a Notion integration and share the pages with it

1. Go to <https://www.notion.so/my-integrations> → **New integration**
   (internal). Copy the **Internal Integration Secret** (starts with `ntn_`).
2. Open each root page in Notion → `•••` menu → **Connections** → add your
   integration. Sharing the root page also grants access to its subpages.

### 2. Confirm your Send-to-Kindle setup

- Your Kindle address: **`adrianhills@kindle.com`**
  (Amazon → *Manage Your Content and Devices → Preferences → Personal Document
  Settings* to verify.)
- On that same settings page, make sure your sending address (**`adrianhills@gmail.com`**)
  is in the **Approved Personal Document E-mail List**. Amazon silently drops
  documents from un-approved senders.

### 3. Create a Gmail app password (for sending)

Gmail blocks plain-password SMTP, so create an app password:

1. Enable 2-Step Verification on the Google account.
2. <https://myaccount.google.com/apppasswords> → create one for "Mail".
3. Use the 16-character value as `SMTP_PASS`.

(If you'd rather not use Gmail, any SMTP provider works — set `SMTP_HOST`,
`SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `FROM_EMAIL` accordingly. The
`FROM_EMAIL` you use must be on Amazon's approved-sender list.)

### 4. Add GitHub repository secrets

Repo → **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Value |
| --- | --- |
| `NOTION_TOKEN` | Notion integration secret (`ntn_…`) |
| `KINDLE_EMAIL` | `adrianhills@kindle.com` |
| `SMTP_USER` | `adrianhills@gmail.com` |
| `SMTP_PASS` | Gmail app password |

Optional secrets: `SMTP_HOST`, `SMTP_PORT`, `FROM_EMAIL` (defaults are
`smtp.gmail.com`, `587`, and `SMTP_USER`).

### 5. Run it

- **Automatic:** runs daily at 07:00 UTC (change the `cron` in the workflow).
- **Manual:** repo → **Actions → Notion to Kindle → Run workflow**. Set
  *Build only* to `true` for a dry run that builds the EPUBs (downloadable as a
  workflow artifact) without emailing them.

## Run locally

```bash
pip install -r requirements.txt
brew install pandoc            # or: sudo apt-get install pandoc

export NOTION_TOKEN=ntn_...
export KINDLE_EMAIL=adrianhills@kindle.com
export SMTP_USER=adrianhills@gmail.com
export SMTP_PASS=your_app_password

# Dry run — build EPUBs into ./build without emailing:
SKIP_SEND=1 python notion_to_kindle.py

# Build and send:
python notion_to_kindle.py
```

## Notes & limitations

- **Databases** (Templates Library, Glossary, Source Courses, etc.) are
  rendered by listing each row as a section with its page content. Complex
  database views/filters are not reproduced.
- **Images** are referenced by their Notion-hosted URLs; Pandoc embeds external
  images it can fetch at build time. Notion's signed image URLs can expire, so
  some images may not embed.
- Send-to-Kindle accepts up to **25 files / 50 MB per email**; each book is
  sent as its own message, so this isn't a concern here.
- Notion API calls are throttled to stay under the ~3 requests/second limit, so
  large knowledge bases take a minute or two to build.
