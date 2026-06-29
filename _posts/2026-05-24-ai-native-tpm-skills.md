---
layout: post
title: "25 AI Skills I Built to Run Programs. Here's the Philosophy Behind Them."
date: 2026-05-24
description: "I built 25 Claude Code skills that cover the full program management lifecycle — from kickoff to retrospective. This is why, how they work, and what they actually changed."
tags: [tpm, ai, tools, program-management]
---

I didn't set out to build 25 tools.

I started with one problem: status updates took too long and communicated too little. I wanted to see if AI could help me get to the first draft faster without sacrificing the senior signal — the risk trajectory, the decision needed, the clear ask. It worked. So I kept going.

What I built over the next couple of weeks is a suite of Claude Code skills that covers nearly the entire program management lifecycle — from kickoff and capacity planning through escalation, retrospective, and root cause analysis. Each skill is a structured prompt that does one thing well, integrates with how I already work, and gets out of the way.

This post is about the philosophy behind those tools. What they're designed to do, how they're organized, and what actually changed. These skills have been used across multiple organizations at Intuit — by PMs, TPMs, and other roles — which shaped how broadly I designed them to apply.

---

## The core thesis

I see the role of a senior TPM as something different from filling out templates. It is to compress the time between ambiguous input and clear decision — for engineers, for product managers, for executives.

Here's how I think about the breakdown of that work: roughly 70% is execution — the operational core of moving programs forward. About 20% is team and company collaboration: the leadership, facilitation, and alignment work that keeps cross-functional effort coherent. And 10% is influence without authority — becoming a trusted voice in rooms where you don't have a title to back you up.

AI doesn't change that breakdown. What it does is supercharge your impact within it. When execution gets compressed, you can expand scope and increase velocity without sacrificing quality. The depth of each artifact goes up. The prep work happens faster. And you can do all of it at a level of rigor that used to require more hours than the calendar allowed.

Most program work has a repeatable shape. A kickoff has the same five questions regardless of the program. A status update has the same four components regardless of the team. An escalation needs the same three things to be useful: what changed, what it costs, and what the decision-maker needs to do.

If the shape is repeatable, the scaffolding can be automated. That frees up the judgment work — the part that actually requires experience, context, and relationship — to be the main job rather than something squeezed in between formatting Slack messages and reformatting the same update for four different audiences.

That's the thesis: **AI compresses execution so that orchestration, judgment, and influence become the full job.**

---

## How the skills work

Each skill is a markdown file that gets invoked through Claude Code. When I call it, it pulls the relevant context — program state, stakeholder list, recent signals — and produces a structured output I can use directly or edit lightly before sharing.

The skills don't try to replace judgment. They create the conditions for good judgment to happen faster. A good status update doesn't write itself because the AI generated a draft — it writes itself because the AI forced me to answer the right questions in the right order, and then I applied the context that only I have.

The other principle: one skill, one job. I didn't try to build a Swiss army knife. I built 25 scalpels. Each one has a clear input format, a clear output format, and a clear moment in the program lifecycle where it belongs.

---

## How they map to the PMI process groups

These skills weren't designed in isolation — they follow the structure that program management practitioners have used for decades. Below is how they map across the five PMI process groups.

![AI-Native TPM Skills mapped to PMI Process Groups](/assets/tpm-skills-pmi.svg)

---

## The skills, by category

### Program setup

**kickoff** — Structures the five questions that make or break a program start: what is the outcome and the date, what is fixed versus flexible across scope and resources, who owns decisions, what is the critical path, and what does failure look like. Forces the conversation I need to have anyway, before week two confusion makes it harder.

**workback** — Generates a workback schedule from a target date and milestone list. Surfaces sequencing conflicts and flags where the critical path is thinner than the team thinks.

**capacity-plan** — Maps team capacity against program demand across a planning window. Identifies where commitments exceed availability before the team is already overcommitted.

**stakeholder-map** — Builds a structured map of decision-makers, influencers, and affected parties across a program. Clarifies who needs to know what, at what cadence, and through which channel.

---

### Execution and monitoring

**status-update** — Produces an exec-ready status update from raw program notes. Output is structured: RAG signal, key progress, active risks with owners, decisions needed. Estimated time savings: what used to take 45 minutes now takes under 10.

**multi-system-status-write** — Aggregates status across multiple workstreams or systems into a single coherent narrative. Particularly useful for portfolio-level reporting or programs with parallel tracks.

**watchdog** — Monitors for early warning signals across a program: decision velocity dropping, RAID growing without movement, leading indicators flattening. Surfaces risks before they become slips.

**dependency-scan** — Scans a list of workstreams and milestones, identifies dependency chains, flags circular dependencies, and highlights critical path exposure.

**raid** — Generates and maintains a structured RAID log (Risks, Assumptions, Issues, Dependencies) with owners and needed-by dates. Treats RAID as a living decision tool rather than a static artifact.

---

### Decision-making

**decision** — Structures a decision log entry with options, trade-offs, recommendation, and rationale. Designed to make implicit decisions explicit and create an organizational memory that outlasts Slack threads.

**escalate** — Formats an escalation with the three things that make escalations useful: what changed and when, what it costs if not addressed, and the specific decision or action the recipient needs to take. Escalations that don't end with a clear ask aren't escalations — they're status updates with anxiety.

**premortem** — Runs a structured pre-mortem before a program or launch. Identifies the most likely failure modes, their probability and impact, and the mitigation moves available now. Easier to be honest about failure risks before anyone is defending a plan.

**rca** — Structures a root cause analysis after an incident, miss, or near-miss. Follows the five-why pattern and surfaces systemic factors versus proximate ones. Designed to produce learning, not blame.

---

### Communications and alignment

**comms** — Reformats a single technical update for multiple audiences: engineering Slack, exec summary, customer-facing changelog, and all-hands blurb. One input, four outputs, each calibrated to its audience without requiring four separate drafts.

**slack-formatting** — Formats a Slack message with the right structure for its purpose — decision request, status update, escalation, or FYI. Eliminates the wall-of-text problem.

**zoom-meeting-summary** — Converts raw meeting notes or a transcript into a structured summary: decisions made, action items with owners and dates, open questions. Gets the artifact out of the meeting and into the tracker in under five minutes.

---

### Review and learning

**prd-review** — Reviews a PRD or RFC draft and surfaces gaps: undefined edge cases, missing metrics, unstated assumptions, and internal contradictions. Cheaper to find these in the document than in the post-launch retro.

**retro** — Structures a sprint or program retrospective with prompts calibrated for honest reflection — what worked, what didn't, what would we do differently, and what specific behavior change do we commit to.

**async-retro** — Runs an asynchronous retrospective when the team is distributed or when real-time facilitation would produce anchoring bias. Collects independent responses before synthesis.

**roadmap-compare** — Compares two versions of a roadmap and surfaces what changed, what moved, what disappeared, and what the net impact is on the critical path. Useful for planning cycles and for making scope changes visible.

---

### Business and strategy

**business-case** — Structures a business case with the components that actually move approvals: the problem, the options considered, the recommended path, the investment required, the expected return, and the decision needed by when.

**launch-readiness** — Runs a structured launch readiness review against a configurable checklist: technical readiness, operational readiness, support readiness, comms, rollback plan, and success metrics. Flags gaps before go-live.

**offsite-plan** — Builds an offsite agenda from a set of goals and constraints. Structures time for the conversations that are hard to have in weekly syncs and ensures the output is a decision or alignment, not just a good discussion.

---

### Coaching and program excellence

**program-expert** — A TPM coaching prompt that helps junior or mid-level program managers think through a complex situation at the right altitude. Produces questions, not answers — designed to build judgment, not dependency.

**tpm-rockstar** — Structures a periodic review of TPM craft against the behaviors that actually separate execution from senior altitude: decision quality, dependency surfacing, trade-off clarity, escalation timing, and coaching impact.

---

## What actually changed

The most direct impact: reporting time dropped by roughly 85 percent. Status updates, escalation memos, and stakeholder communications that used to take the better part of a morning now take minutes. That time went back to the work that requires judgment — the conversations, the trade-off decisions, the coaching.

The less obvious impact is harder to put a number on, but it matters more: the level of rigor went up without a corresponding increase in human cost. Prep work that used to wait for a meeting now happens the night before, async. Research that used to block a decision runs in the background while the conversation is already happening. You go into the room more prepared, not just faster.

That changes the quality of the work, not just the speed of it. An escalation that used to get sent with rough edges because there wasn't time to sharpen it now gets sent with the three components that make it land. A kickoff that used to front-load assumptions now surfaces them as questions before the first slide. The gap between what good looks like and what actually ships narrowed — without adding headcount.

The impact on newer team members was meaningful too. A junior TPM running a kickoff with the kickoff skill is more likely to ask the right questions in the right order than one working from memory. The skill is a form of embedded coaching that scales without requiring more senior time.

---

## What this is not

These tools don't make good programs. They make the operational overhead of good programs smaller.

The judgment work — understanding what the team is actually optimizing for, knowing which risks are real versus hypothetical, reading the room in an exec review and deciding what to say versus what to hold — that still requires experience, context, and relationship. No skill automates that.

What these skills do is reduce the tax on judgment. Less time formatting, more time thinking. Less time reformatting the same update, more time getting the update right. Less time building the RAID log, more time making decisions on what's in it.

The TPM role is being rewritten by AI — not eliminated, rewritten. The execution layer is getting compressed. The judgment layer is becoming more valuable. These tools are a bet on that direction.

---

## Building in public

All of these skills are part of an ongoing project to build AI-native program management tooling and share it publicly. The goal is not to have a portfolio — it's to have proof. Anyone can say they work with AI. Fewer people can open a terminal and show you twenty-five tools doing the work.

If you're a senior leader hiring for a TPM role, or an early-stage company trying to figure out how to scale program management without scaling headcount in lockstep, I'm happy to walk through how these work in practice.

The tools run. The time savings are real. The philosophy is above.

---

*More on the projects and the reasoning behind them at [adrianhills.github.io](https://adrianhills.github.io).*
