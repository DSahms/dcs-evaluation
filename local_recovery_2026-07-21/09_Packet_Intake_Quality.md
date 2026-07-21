# Stage 0B — Packet Intake & Quality Gate

**Before any AI vs AI test:** the Benchmark Packet must pass intake.  
Crap in, crap out. A shitty work order makes every model look bad — unfairly.

---

## Two phases (do not confuse them)

| Phase | Human interaction? | Purpose |
|-------|-------------------|---------|
| **Intake** (this doc) | **Yes** — deliberate, multi-pass | Produce a **fair, complete** frozen packet |
| **Benchmark** (Stage 2) | **No** — one shot | Measure model on a **fixed** work order |

Real life: you talk to the customer for two weeks, *then* the engineer builds once on a signed SOW.  
Benchmark life: intake finishes the SOW, *then* models get the SOW only.

---

## Who does intake (avoid gray-elephant bias)

| Role | Who | Must NOT be |
|------|-----|-------------|
| **Reference owner** | Knows the app exists | Sole spec author |
| **Neutral analyst** | Stage 1 prompt / AI pass on repo | App author |
| **Packet reviewer** | Second pair of eyes | Same person as analyst only |
| **Intake approver** | Dave or designated — signs freeze | Model under test |

**Rule:** whoever built the reference app **cannot** be the only human who wrote the packet.

---

## AI-assisted intake (fair input, not cheating the benchmark)

Use AI **on the packet**, not on the submission.

### Pass 1 — Extract (AI + repo)

Prompt: neutral requirements analyst (`02_Specification_Generator.md`).

Output: draft `01_product_spec.md` with numbered FR-* and AC-*.

### Pass 2 — Completeness audit (AI, different session)

Give AI **only the draft spec** — not the repo. Ask:

    You are a customer receiving this work order before signing.
    List every ambiguity, missing acceptance criterion, and assumption
    that would cause two engineers to build different products.
    List missing end-user documentation requirements.
    List security tier gaps.

Fix the spec until this pass returns "no blocking ambiguities."

### Pass 3 — Adversarial shrink (AI)

Ask:

    Which requirements smuggle implementation choices (frameworks, libraries)?
    Which lines describe the author's solution instead of user outcomes?
    Rewrite violations as behavior-only requirements.

### Pass 4 — Human sign-off

Human reads:

- Can a non-author explain what "done" means?
- Does `03_security_tier.md` match app class?
- Does `04_end_user_doc_requirements.md` cover install for a non-dev?
- Is `05_out_of_scope.md` explicit?

**Freeze only after sign-off.**

---

## Intake checklist (packet quality gate)

### A. Work order completeness

- [ ] Executive summary — one paragraph a customer understands  
- [ ] User goals include **non-technical users**  
- [ ] Every screen / flow described  
- [ ] FR-* IDs stable and referenced in acceptance criteria  
- [ ] AC-* are binary (pass/fail, no "should feel good")  
- [ ] Unknowns listed — not hidden assumptions  

### B. Fairness (no smuggled elephant)

- [ ] No required framework unless justified in spec  
- [ ] Behavior stated, not "match existing codebase"  
- [ ] Security tier assigned (S0/S1/S2) with excessive/insufficient examples  
- [ ] NFRs measurable or marked N/A  

### C. End-user reality

- [ ] Install path defined for target platform  
- [ ] Permission / "unknown source" class prompts anticipated  
- [ ] USER_GUIDE requirements in packet (`06` template)  

### D. Testability

- [ ] Smoke tests or AC cover core path  
- [ ] Another model could fail for missing FR-7, not vague "quality"  

### E. Freeze metadata

- [ ] `packet_version` (e.g. `guestbook-v1`)  
- [ ] Date frozen  
- [ ] Intake approver name  
- [ ] Reference repo path **not** in model bundle  

**Fail any blocking item → do not run AI vs AI.**

---

## Customer simulation (optional but strong)

Before freeze, run **one** cheap model with a fake intake prompt:

    You are the customer. Read this spec.
    What would you ask before signing the contract?
    What would confuse your beta tester?

Merge answers into spec. This simulates Monday-morning back-and-forth **before** the build — not during the benchmark.

---

## Project size (small vs large)

Size matters less than **intake quality**.

| Small app + great packet | Large app + vague packet |
|--------------------------|---------------------------|
| Fair AI vs AI | Unfair — models guess differently |

Start smaller if intake pipeline is new. **Do not** start large until one packet has passed full intake once.

First reference app criteria:

- Clear user-facing flows  
- S0 or S1 tier  
- Real end-user install story (web or mobile)  
- **Not** a product from your own portfolio — use standalone open-source or synthetic apps  
- Motivation to write good acceptance criteria (someone cares about the outcome)

Start with S0/S1 and clear flows. Reserve S2 (facility, air-gapped) until intake pipeline is proven.

---

## What models never see during intake

- Intake conversation transcripts (optional archive for humans only)  
- Reference repo  
- "How I built it" notes  

What models **do** see at benchmark time:

- Frozen packet only — same bytes for every competitor.

---

## Intake failure modes (watch for these)

| Symptom | Cause | Fix |
|---------|-------|-----|
| All models "fail" differently on same FR | Ambiguous FR | Pass 2 completeness audit |
| All models over-engineer | Spec implies enterprise | Pass 3 adversarial shrink |
| Doc judge scores random | Packet didn't define USER_GUIDE sections | `04_end_user_doc_requirements.md` |
| Author's model wins always | Spec encodes their stack | Remove implementation requirements |
| Human beta still can't install | Packet ignored platform reality | End-user doc checklist in intake |

---

## Summary

**Fair AI vs AI = fair work order first.**

Intake is the customer meeting. Benchmark is Monday build — one shot, no bounce-back.

Use AI to **stress-test the spec**, not to let the benchmarked model negotiate requirements.

When intake checklist passes → freeze → **then** run the suite (`08_Metric_Suite.md`).
