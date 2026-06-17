---
layout: post
title: "Inside My Plaid Final Panel: A Program Management Loop, Three Angles, One Role"
date: 2026-06-16
description: "Three sessions in a single afternoon — engineering, operations, product — all circling the same question: can you bring order to integration work without becoming the bottleneck. The questions, the answers, and what the loop was really testing."
tags: [tpm, career, interviews]
---

A final panel is a triangulation exercise.

Three interviewers, three functions, one afternoon — and if you listen closely, they're all measuring the same thing from different seats. At Plaid the role was Integration Operations Program Manager: own the operational governance for new bank integrations, upgrades, and the long migration off screen-scraping onto API-based connections. The kind of program work where the artifacts — master timelines, status trackers, risk and decision logs, launch-readiness checklists — are the job, not the paperwork around it.

I sat with a senior engineer, a business-operations lead, and a product manager. Same role, three lenses. Here's the loop: the real questions, the answers I gave, and what I think each seat was actually probing.

---

## TL;DR

- **Don't describe your operating artifacts — claim them.** "I've run exactly this stack" lands harder than a tour of what a RAID log is. The panel already knows what good looks like; they want to know you've done it.
- **Give a client a date as a set of tradeoffs, not a number.** "We can go live sooner but can't validate data quality for a week" hands the decision to the person who owns the consequence.
- **A recurring gap between the ask and the estimate is a tooling signal, not a heroics signal.** Compress once. If you're compressing every time, the fix is investment in the pipeline, not another weekend.
- **Build the coalition at the team level before you escalate.** Walk into the VP room with alignment, not a fight to be refereed.
- **Escalate with an options summary and an explicit ask — never a problem.** Model the choices, name the tradeoffs, request the decision.
- **AI leverage is measured, not performed.** "Execution dropped from 70% of my week to 20%" beats a demo every time. The opposite of token-maxing.
- **For migrations with invisible downstream consumers, validation is feedback loops, not traceability.** When you can't see inside the black box, you sample, you build external feedback, you instrument what you can.

---

## Session 1 — Engineering Partnership & Technical Fluency

A senior backend engineer ran this one. The whole session was a credibility test: can you earn trust with engineers without pretending to be one, and can you tell a genuinely hard problem apart from a sandbagged estimate.

He opened with portfolio management — how do you hold a set of concurrent, complex workstreams together. I walked through a credit-bureau data migration: new data models and reporting formats rippling across 17-plus consumer teams, three parallel streams (the team building the new format, the team handling integrations, the consumer teams themselves), a critical path mapped across all of it.

The part that earned the most engagement wasn't the tracking — it was capacity planning:

> I flagged that peak-traffic windows would strain the bureau infrastructure mid-migration, while they were moving monolith to microservices. We built predictive analytics to pre-fetch the data two to three hours ahead of peak.

That's the move that separates a coordinator from a technical partner. Reading the system well enough to see the strain *before* it shows up in an incident.

Then the hypothetical: migrate a bank from screen-scraping to OAuth — how do you scope it? I refused to give a timeline first. What I'd gather: how mature the partner's stack is (greenfield or legacy), the volume and criticality of the data, whether it's a clean cutover or a live migration, and how novel this is for us — a standard pattern or a bespoke Chase-scale partner.

On the classic squeeze — the client wants four weeks, engineering says three months:

> Start at MVP scope. Justify the resourcing against real benefit — revenue, strategic value. Look hard at parallelization or added staffing to compress. And if that gap keeps showing up, stop treating it as a one-off and invest in the tooling that makes the next migration faster.

The last clause is the one that matters. Compressing a timeline once is execution. Compressing it every single time means the real problem is upstream of the schedule.

He closed on engineers pushing back. My answer wasn't "push harder" — it was coalition. On a backend-versus-frontend calculation dispute across three teams, I collated the options with neutral pros and cons, built agreement at the team level, and only then took a ratified recommendation up to the VPs. You don't hand executives an unframed fight and ask them to pick a side.

---

## Session 2 — Collaboration & Stakeholder Management

A business-operations lead ran this round, and it was the most about *how you work* — collaboration style, how you bring people along, how you build something where no process exists yet. This was a role that would be the first dedicated program owner for the area, so "can you operate without a playbook handed to you" was the whole question.

On bridging technical and non-technical stakeholders, I gave the frame I actually use:

> I align people around three audiences — what's good for the business, good for the employee, and good for the customer. Almost every cross-functional disagreement resolves faster when you name which of those three you're optimizing.

On building program artifacts from a blank page: the non-negotiables are clear goals, documented requirements, a real work breakdown, and a stakeholder/RACI matrix — then schedule adherence and top risks as the standing signals.

The part that drew the most interest was AI tooling, and I kept it concrete:

> I've built around twenty agents and skills that took execution work from roughly 70% of my week down to 20%. They draft post-meeting notes, update the RAID log, write the exec comms, build work-back schedules from PRDs and designs, populate the stakeholder matrix. I stay the human in the loop. It's about measurable leverage, not token-maxing.

That number — 70 to 20 — does more work than any description of the tooling. It reframes the whole conversation from "do you use AI" to "you've already operationalized it."

On getting people to actually adopt a tracker, my honest answer was "honey and salt": motivate with the *why*, build buy-in one-on-one during onboarding, agree on lightweight mechanics with each partner — but stay consistent about commitments and escalate when non-compliance persists. Adoption is a relationship before it's a rule.

When I asked what an amazing version of this person looks like, the answer was clarifying: step in as the full owner, read the current state fast, then change it — and use AI to get visibility across *all* ten-thousand-plus integrations, not just the hundred anyone watches today. That's a real problem worth solving, and it mapped almost exactly onto what I'd just described building.

---

## Session 3 — Product Collaboration & Prioritization

A product manager ran the longest session. The probe here was partnership and judgment: do you collaborate before you escalate, and do you know what launch-ready actually means.

The most-complex-project question pulled the Uber app rebuild — a monolith-to-microservices migration and a full redesign at once, ~1,000 engineers across time zones, a backlog of ~100 prioritized items. The hard part wasn't the dependency graph:

> The hardest part was the weekly Saturday review with the CEO — managing live executive feedback while protecting technical constraints he had no interest in hearing about. I handled it with proactive demos and incremental-progress framing instead of pushing back in the room.

The technical-depth question went to the bureau format migration, and the interesting wrinkle was the consumers I *couldn't* see: features we controlled, internal ML models we partly understood, and financial-institution eligibility criteria that were a total black box. You can't get traceability into someone else's eligibility model. So validation became sampling and external feedback loops with the bureaus — instrumenting what you can, inferring the rest.

On a project that went off the rails — a redesign rollout where engagement and revenue tanked mid-rollout — the recovery answer turned on discipline:

> We kept an untouched control group so we could isolate variables, ran root-cause on whether it was the design principles or missing engagement levers from the old platform, built a quick-win backlog, and re-merged the proven drivers into the new system. Recovered in about six weeks.

The escalation story was Uber Rewards: CFO and Chief Product Officer at odds over spend and tiers, a directive from the CEO. I modeled the tier options with FP&A and data science, brought in product marketing for competitive benchmarking, and when VP-level alignment wasn't reachable, escalated to the CEO with a clean options summary and an explicit ask for a decision. He chose to spend more and reassess after seven months once we had real longitudinal data. Escalation done right is a one-page decision, not a complaint.

Asked what makes a great PM partner, I gave a one-word answer and meant it: **decisiveness.** Knowing exactly what information you need to make the call, then making it and driving. Everything else a PM does is downstream of that.

---

## What I'd Tell Someone Going Into a Panel Like This

The thing a multi-session loop is really testing is consistency under rotation. Three people, three functions, comparing notes afterward. If your operating philosophy shifts depending on who's in the room, that shows up in the debrief. Mine didn't have to be performed to stay consistent, because it's the same system underneath: name the audiences, build the artifacts, measure the leverage, build coalition before you escalate, and give people decisions framed as tradeoffs.

The other thing: for a role that's the *first* of its kind on a team, every interviewer is quietly asking whether you can operate without a playbook handed to you. The strongest signal you can give is to describe the operating system you'd bring — specifically, by name — and then show it already running. Not "here's how I'd set up governance," but "here's the stack I've run, here's the number it moved, here's where I'd point it first."

And claim your artifacts. The master timeline, the risk log, the launch-readiness checklist, the AI agent that drafts the comms — when those are genuinely your wheelhouse, the worst thing you can do is describe them in the abstract like a textbook. Say you've run exactly this. Because you have.

---

*Find me on [LinkedIn](https://www.linkedin.com/in/hillsadrian/).*
