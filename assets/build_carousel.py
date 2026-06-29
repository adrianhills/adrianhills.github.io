# -*- coding: utf-8 -*-
# Builds an 8-slide LinkedIn carousel (1080x1350 portrait) as a single print-ready HTML.

OUT = "/Users/adrian/Documents/adrianhills.github.io/assets/carousel/tpm-carousel.html"

# PMI palette
C = {
    "init": "#2563EB", "plan": "#7C3AED", "exec": "#059669",
    "mon": "#D97706", "close": "#DC2626",
    "ink": "#0F172A", "muted": "#64748B", "faint": "#94A3B8",
    "line": "#E2E8F0", "navy": "#0B1220", "navy2": "#111E36",
}

def skill(name, desc, color):
    return f'''<div class="skill">
      <span class="dot" style="background:{color}"></span>
      <span class="sk-name">{name}</span>
      <span class="sk-desc">{desc}</span>
    </div>'''

def phase_block(title, color, items):
    rows = "".join(skill(n, d, color) for n, d in items)
    return f'''<div class="phase">
      <div class="phase-head" style="color:{color}">
        <span class="phase-bar" style="background:{color}"></span>{title}
      </div>
      {rows}
    </div>'''

INIT = [
    ("kickoff", "the 5 questions that make or break a start"),
    ("stakeholder-map", "who needs what, when, and how"),
    ("business-case", "the case that actually moves approvals"),
    ("capacity-plan", "demand vs. availability, before overcommit"),
]
PLAN = [
    ("workback", "schedule built backward from the target date"),
    ("raid", "living risks / assumptions / issues / dependencies"),
    ("dependency-scan", "chains, circular deps, critical-path exposure"),
    ("premortem", "surface failure modes before they happen"),
    ("offsite-plan", "an agenda built around decisions, not talk"),
]
EXEC = [
    ("status-update", "exec-ready status from raw notes, in minutes"),
    ("comms", "one update, reframed for four audiences"),
    ("decision", "options, trade-offs, recommendation, rationale"),
    ("escalate", "what changed, what it costs, the exact ask"),
    ("prd-review", "find gaps before the post-launch retro does"),
    ("slack-formatting", "the right structure for every message type"),
    ("zoom-summary", "decisions + owners + actions from a transcript"),
    ("multi-system-status", "portfolio-level rollups across tracks"),
]
MON = [
    ("watchdog", "early-warning signals before slips happen"),
    ("roadmap-compare", "what moved between two roadmap versions"),
    ("live RAID", "risk tracking that stays current, not stale"),
    ("live dependency-scan", "critical path, continuously checked"),
]
CLOSE = [
    ("retro", "honest reflection that ends in behavior change"),
    ("async-retro", "independent input, zero anchoring bias"),
    ("rca", "root cause and learning, never blame"),
    ("launch-readiness", "a clean go / no-go against a checklist"),
]
CROSS = [
    ("program-expert", "coaching that builds judgment, not dependency"),
    ("tpm-rockstar", "periodic review of senior TPM craft"),
]

def slide(inner, n, dark=False):
    cls = "slide dark" if dark else "slide"
    foot_color = "rgba(255,255,255,.45)" if dark else C["faint"]
    return f'''<section class="{cls}">
    <div class="accent"></div>
    {inner}
    <div class="foot" style="color:{foot_color}">
      <span>adrianhills.github.io</span><span>{n} / 8</span>
    </div>
  </section>'''

# ---- Slide 1: COVER (dark) ----
s1 = slide(f'''
    <div class="cover">
      <div class="eyebrow">AI-NATIVE PROGRAM MANAGEMENT</div>
      <h1>Most TPMs spend <span class="hl">70%</span> of their time on work AI can now do in minutes.</h1>
      <p class="cover-sub">So I built <b>25 tools</b> to prove it.</p>
      <div class="swipe">Swipe&nbsp;→</div>
    </div>''', 1, dark=True)

# ---- Slide 2: INTRO ----
s2 = slide(f'''
    <div class="pad">
      <div class="kicker" style="color:{C['init']}">THE SETUP</div>
      <h2>In two weeks, I built 25 Claude&nbsp;Code skills covering the full program management lifecycle.</h2>
      <p class="lead">From kickoff and capacity planning through escalation, retrospective, and root&nbsp;cause analysis.</p>
      <div class="rule"></div>
      <p class="lead big">The time savings were real.<br><b>But the bigger shift was something else.</b></p>
    </div>''', 2)

# ---- Slide 3: 70/20/10 ----
def bar(pct, label, desc, ai, color, light, width):
    return f'''<div class="frow">
      <div class="fpct" style="color:{color}">{pct}</div>
      <div class="fcard" style="background:{light}">
        <span class="facc" style="background:{color}"></span>
        <div class="flabel" style="color:{color}">{label}</div>
        <div class="fdesc">{desc}</div>
        <div class="ftrack"><span style="width:{width}%;background:{color}"></span></div>
      </div>
      <div class="fbadge" style="color:{color};border-color:{color}">{ai}</div>
    </div>'''
s3 = slide(f'''
    <div class="pad">
      <div class="kicker" style="color:{C['plan']}">THE MENTAL MODEL</div>
      <h2 class="tight">How I think about the&nbsp;TPM&nbsp;role</h2>
      <p class="lead">AI doesn't change the breakdown. It supercharges your impact within each layer.</p>
      <div class="frame">
        {bar("70%","EXECUTION","status · escalation · decisions · dependencies","AI compresses",C['init'],"#EFF6FF",100)}
        {bar("20%","COLLABORATION","alignment · facilitation · cross-functional leadership","AI amplifies",C['plan'],"#F5F3FF",55)}
        {bar("10%","INFLUENCE","trusted voice — without the authority","AI extends",C['exec'],"#F0FDF4",30)}
      </div>
    </div>''', 3)

# ---- Slide 4: PMI MAP ----
def pmi_col(title, color, items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'''<div class="pcol">
      <div class="phead" style="background:{color}">{title}</div>
      <ul style="--c:{color}">{lis}</ul>
    </div>'''
s4 = slide(f'''
    <div class="pad">
      <div class="kicker" style="color:{C['exec']}">THE STRUCTURE</div>
      <h2 class="tight">25 skills, mapped to the 5 PMI process groups</h2>
      <div class="pmi">
        {pmi_col("① INITIATING", C['init'], ["kickoff","stakeholder-map","business-case","capacity-plan"])}
        {pmi_col("② PLANNING", C['plan'], ["workback","raid","dependency-scan","premortem","offsite-plan"])}
        {pmi_col("③ EXECUTING", C['exec'], ["status-update","comms","decision","escalate","prd-review","slack-formatting","zoom-summary","multi-system"])}
        {pmi_col("④ MONITORING", C['mon'], ["watchdog","roadmap-compare","live RAID","live deps"])}
        {pmi_col("⑤ CLOSING", C['close'], ["retro","async-retro","rca","launch-readiness"])}
      </div>
      <div class="crossbar">CROSS-CUTTING · <b>program-expert</b> (coaching) · <b>tpm-rockstar</b> (craft review)</div>
    </div>''', 4)

# ---- Slide 5: Initiating + Planning ----
s5 = slide(f'''
    <div class="pad">
      <div class="kicker" style="color:{C['init']}">START &amp; PLAN</div>
      <h2 class="tight">Setting programs up to win</h2>
      {phase_block("① INITIATING", C['init'], INIT)}
      {phase_block("② PLANNING", C['plan'], PLAN)}
    </div>''', 5)

# ---- Slide 6: Executing + Monitoring ----
s6 = slide(f'''
    <div class="pad">
      <div class="kicker" style="color:{C['exec']}">RUN &amp; WATCH</div>
      <h2 class="tight">Driving execution, surfacing risk</h2>
      {phase_block("③ EXECUTING", C['exec'], EXEC)}
      {phase_block("④ MONITORING", C['mon'], MON)}
    </div>''', 6)

# ---- Slide 7: Closing + Cross-cutting ----
s7 = slide(f'''
    <div class="pad">
      <div class="kicker" style="color:{C['close']}">CLOSE &amp; COACH</div>
      <h2 class="tight">Landing the program — and raising the craft</h2>
      {phase_block("⑤ CLOSING", C['close'], CLOSE)}
      {phase_block("✦ CROSS-CUTTING", C['ink'], CROSS)}
    </div>''', 7)

# ---- Slide 8: CLOSING (dark, stats + CTA) ----
s8 = slide(f'''
    <div class="pad close">
      <div class="eyebrow">THE RESULT</div>
      <div class="stats">
        <div class="stat"><div class="num">2 wks</div><div class="slab">to build the suite</div></div>
        <div class="vline"></div>
        <div class="stat"><div class="num">85%</div><div class="slab">less reporting time</div></div>
        <div class="vline"></div>
        <div class="stat"><div class="num">5</div><div class="slab">PMI groups covered</div></div>
      </div>
      <p class="closeline">The tools don't replace judgment.<br><span class="hl2">They reduce the tax on it.</span></p>
      <div class="cta">Full breakdown in the comments&nbsp;👇<br><b>Follow Adrian Hills</b> for more on AI-native program management.</div>
    </div>''', 8, dark=True)

slides = "\n".join([s1,s2,s3,s4,s5,s6,s7,s8])

HTML = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
  :root {{
    --init:{C['init']}; --plan:{C['plan']}; --exec:{C['exec']}; --mon:{C['mon']}; --close:{C['close']};
    --ink:{C['ink']}; --muted:{C['muted']}; --faint:{C['faint']}; --line:{C['line']};
  }}
  html, body {{ font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; color:var(--ink); }}
  @page {{ size:1080px 1350px; margin:0; }}
  .slide {{
    position:relative; width:1080px; height:1350px; background:#fff;
    page-break-after:always; overflow:hidden;
  }}
  .slide:last-child {{ page-break-after:auto; }}
  .slide.dark {{ background:linear-gradient(160deg,{C['navy']} 0%,{C['navy2']} 100%); color:#fff; }}
  .accent {{ position:absolute; top:0; left:0; right:0; height:8px;
    background:linear-gradient(90deg,var(--init) 0%,var(--plan) 25%,var(--exec) 50%,var(--mon) 75%,var(--close) 100%); }}
  .foot {{ position:absolute; left:72px; right:72px; bottom:54px; display:flex; justify-content:space-between;
    font-size:20px; letter-spacing:.5px; }}
  .pad {{ padding:128px 72px 72px; }}
  .kicker {{ font-size:21px; font-weight:800; letter-spacing:3px; margin-bottom:26px; }}
  .eyebrow {{ font-size:21px; font-weight:800; letter-spacing:4px; color:rgba(255,255,255,.5); }}
  h2 {{ font-size:60px; line-height:1.08; font-weight:800; letter-spacing:-1.2px; margin-bottom:30px; }}
  h2.tight {{ font-size:54px; margin-bottom:22px; }}
  .lead {{ font-size:30px; line-height:1.5; color:var(--muted); font-weight:400; }}
  .lead.big {{ font-size:36px; color:var(--ink); line-height:1.4; }}
  .lead.big b {{ color:var(--init); }}
  .rule {{ height:1px; background:var(--line); margin:44px 0; }}

  /* Cover */
  .cover {{ padding:150px 80px 72px; height:100%; display:flex; flex-direction:column; }}
  .cover .eyebrow {{ margin-bottom:60px; }}
  .cover h1 {{ font-size:84px; line-height:1.06; font-weight:800; letter-spacing:-2px; max-width:900px; }}
  .cover .hl {{ color:#60A5FA; }}
  .cover-sub {{ font-size:40px; margin-top:54px; color:rgba(255,255,255,.82); font-weight:400; }}
  .cover-sub b {{ color:#fff; }}
  .swipe {{ margin-top:auto; font-size:30px; font-weight:700; color:#60A5FA; letter-spacing:.5px; }}

  /* 70/20/10 */
  .frame {{ margin-top:36px; display:flex; flex-direction:column; gap:30px; }}
  .frow {{ display:flex; align-items:center; gap:26px; }}
  .fpct {{ font-size:64px; font-weight:800; width:150px; text-align:right; flex:none; letter-spacing:-2px; }}
  .fcard {{ position:relative; flex:1; border-radius:18px; padding:30px 34px 34px; overflow:hidden; }}
  .facc {{ position:absolute; left:0; top:0; bottom:0; width:8px; }}
  .flabel {{ font-size:20px; font-weight:800; letter-spacing:1.5px; margin-bottom:12px; }}
  .fdesc {{ font-size:26px; color:#334155; margin-bottom:20px; }}
  .ftrack {{ height:8px; border-radius:4px; background:#E2E8F0; overflow:hidden; }}
  .ftrack span {{ display:block; height:100%; border-radius:4px; opacity:.75; }}
  .fbadge {{ flex:none; width:200px; text-align:center; font-size:21px; font-weight:700;
    border:2px solid; border-radius:14px; padding:16px 0; }}

  /* PMI map */
  .pmi {{ display:grid; grid-template-columns:repeat(5,1fr); gap:14px; margin-top:30px; }}
  .pcol {{ background:#F8FAFC; border:1px solid var(--line); border-radius:14px; overflow:hidden; }}
  .phead {{ color:#fff; font-size:17px; font-weight:800; letter-spacing:.5px; padding:16px 12px; text-align:center; }}
  .pcol ul {{ list-style:none; padding:18px 14px; }}
  .pcol li {{ font-size:21px; color:#1E293B; padding:9px 0 9px 18px; position:relative; line-height:1.2; }}
  .pcol li::before {{ content:""; position:absolute; left:0; top:16px; width:7px; height:7px; border-radius:50%; background:var(--c); }}
  .crossbar {{ margin-top:26px; background:var(--ink); color:#fff; border-radius:14px; padding:26px;
    text-align:center; font-size:24px; letter-spacing:.3px; }}
  .crossbar b {{ color:#93C5FD; }}

  /* Skill lists */
  .phase {{ margin-top:34px; }}
  .phase-head {{ font-size:24px; font-weight:800; letter-spacing:1.5px; display:flex; align-items:center; margin-bottom:18px; }}
  .phase-bar {{ display:inline-block; width:34px; height:5px; border-radius:3px; margin-right:16px; }}
  .skill {{ display:flex; align-items:baseline; padding:11px 0; border-bottom:1px solid #F1F5F9; }}
  .dot {{ width:9px; height:9px; border-radius:50%; flex:none; margin-right:18px; transform:translateY(-2px); }}
  .sk-name {{ font-size:26px; font-weight:700; color:var(--ink); width:330px; flex:none; }}
  .sk-desc {{ font-size:23px; color:var(--muted); line-height:1.3; }}

  /* Close slide */
  .close {{ padding:150px 80px 72px; }}
  .stats {{ display:flex; align-items:center; gap:40px; margin:80px 0 70px; }}
  .stat {{ flex:1; text-align:center; }}
  .num {{ font-size:78px; font-weight:800; color:#fff; letter-spacing:-2px; }}
  .slab {{ font-size:22px; color:rgba(255,255,255,.55); letter-spacing:1px; margin-top:8px; }}
  .vline {{ width:1px; height:90px; background:rgba(255,255,255,.18); }}
  .closeline {{ font-size:46px; line-height:1.35; font-weight:700; color:rgba(255,255,255,.92); }}
  .hl2 {{ color:#60A5FA; }}
  .cta {{ margin-top:80px; font-size:30px; line-height:1.5; color:rgba(255,255,255,.75); }}
  .cta b {{ color:#fff; }}
</style></head>
<body>
{slides}
</body></html>'''

with open(OUT, "w") as f:
    f.write(HTML)
print("HTML written:", OUT, "(", len(HTML), "chars )")
