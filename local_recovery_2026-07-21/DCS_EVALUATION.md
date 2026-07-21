# DCS Evaluation — Program Direction

**One file. Read on your phone.**

**Folder:** `D:\DCS benchmark\`  
**Updated:** 2026-07-06

---

## What this is (not a benchmark)

This is **evaluation software** — a way to see how an AI performs as a **real engineer on a real job**, at the **right scale for that job**.

We are **not** building a gamed leaderboard. We are **not** using one fixed scorecard for every assignment. A lawn-care scheduler and a hospital platform are different jobs; judgment flexes with scope.

**North Star:** *Would I want this model at the other desk next week — for **this kind** of work?*

---

## Boundary

**Separate from Dave's portfolio.** NURA, Arden, Pink Skies, Story Keeper, Ledger, etc. do not belong in this program. Sample jobs are synthetic packets (see `evaluation/`) or other standalone work orders — never portfolio products.

---

## Two tracks on disk

| Track | Location | Status |
|-------|----------|--------|
| **Active — Phase 1 samples** | `evaluation/` | Prompt + S1/S2/S3 job packets |
| **Earlier framework** | Root `00`–`11`, `_archive/` | Reference only — judges, intake ideas, kiosk notes; not the live direction |

When in doubt, **`evaluation/` + this file** are truth for where we're going.

---

## The process (same spine, flexible bar)

```
FEED  →  ASK (once)  →  BUILD / DELIVER  →  EVALUATE (level-appropriate)
```

1. **Feed** — Project packet (frozen work order + assets + oracle for fair AI-vs-AI).
2. **Ask** — One clarification round. Good questions matter; silence when the spec is ambiguous has consequences.
3. **Build** — One shot after answers freeze. Architecture, code, tests, README, ASSUMPTIONS.md (see Phase 1 prompt).
4. **Evaluate** — Score **against the level you assigned**, not against a universal enterprise checklist.

---

## Three scope levels (S1 / S2 / S3)

**S1 / S2 / S3 = job complexity**, not security tiers (old docs used S0–S2 for security — different thing).

| Level | Example packet | Users / scale | Evaluation emphasis |
|-------|----------------|---------------|---------------------|
| **S1 — Basic** | LawnCare Lite | ~3, small business | Simplicity, usability, ships fast, right-sized auth |
| **S2 — Involved** | Warehouse inventory | ~150, multi-role | RBAC, audit, integrations, deployment — no overbuild |
| **S3 — Enterprise vision** | Regional hospital | ~8,000, regulated | Architecture, ops, compliance, migration — still proportional |

### Engineer A vs B (every level)

Both meet the written requirements. **A** picks the stack and shape that fit **this level**. **B** brings Kubernetes, OAuth galaxies, and microservices to a three-person lawn crew.

At S3, B might also mean **under**-engineering — hand-waving compliance or migration. Level sets the floor **and** the ceiling.

### What is not fixed

- Point weights (old 100-pt sheet was one experiment)
- Mandatory end-user sideload guide on every job (S1 web app for office staff ≠ S3 ops runbook)
- Same deliverable depth — S1 README vs S3 operations guide
- Same security bar — login for lawn care ≠ HIPAA program for hospital packet

Judges and checklists **attach to the packet level**, not one global rubric.

---

## Phase 1 — what's ready now

**Folder:** `evaluation/`

| File | Purpose |
|------|---------|
| `Phase1_Common_Evaluation_Prompt.md` | Shared engineer prompt (ASK rules + deliverables) |
| `S1_Job_Packet.md` | Basic job |
| `S2_Job_Packet.md` | Involved job |
| `S3_Job_Packet.md` | Enterprise vision job |

**To run:** prompt + one packet → clarification (oracle) → submission → evaluate at that level.

---

## Clarification round (still core)

One round owed to the model — and to you — to see where the packet failed.

- Ask real gaps → good  
- Silent when confused → assumptions pile up → judge accordingly  
- Ask what's already in the packet → noise  

For AI-vs-AI fairness: pre-write **oracle answers** per packet version; every model gets the same follow-up.

---

## What we evaluate (flex by level)

| Dimension | S1 | S2 | S3 |
|-----------|----|----|-----|
| Requirements met | ✓ | ✓ | ✓ |
| Build runs / tests | ✓ | ✓ | ✓ |
| Engineering judgment (A vs B) | ✓ heavy | ✓ heavy | ✓ heavy |
| Clarification quality | ✓ | ✓ | ✓ |
| Architecture proportionate to scale | light | ✓ | ✓ heavy |
| Deployment / ops docs | README | deployment guide | ops + migration |
| Security / compliance | login tier | RBAC + audit | enterprise + healthcare |
| End-user install guide | if non-dev installs | role-based admin docs | ops / clinical workflows |

Not every row gets the same weight. **Pick the bar when you pick the packet.**

---

## Fairness rules

- Same packet bytes for every model at that level  
- Same oracle answers after ASK  
- Evaluators blind to any "reference implementation" if one exists privately  
- Packet author ≠ sole writer (intake quality still matters)  
- Bad packet → fix packet before evaluating models  

---

## Future (not Phase 1)

| Idea | Notes |
|------|-------|
| Live kiosk intake | Customer at other chair; AI runs intake (`11` in old framework) |
| Read-back loop | "Here's what I heard" before freeze |
| Personality / interaction scoring | Parked — `12_Interaction_Quality.md` |
| Automated build gate + smoke | Nice to have; not blocking Phase 1 |
| Token / cost log | Separate from quality |

---

## Pipeline (one picture)

```
Pick level: S1 | S2 | S3
        ↓
Load evaluation/Phase1 prompt + packet
        ↓
Model ASK (once) → oracle answers
        ↓
Model BUILD (once)
        ↓
Evaluate at THAT level's bar
        ↓
Compare models — who for this kind of work?
```

---

## Next steps

1. Add **clarification oracles** for S1, S2, S3 packets (when comparing models)  
2. Run **two models** on same packet + oracle  
3. Draft **level-specific evaluation sheets** (light for S1, heavier for S3)  
4. Optional: move root `00`–`11` into `_archive/framework-v0/` when you're done mining them  

---

## One sentence

> **Feed a real job at the right scope, one ask and one build, judge proportionately — not with one benchmark scoreboard.**

---

## File map

| Read this | When |
|-----------|------|
| **`DCS_EVALUATION_GUIDE.md`** | **Full process + scoring** (re-entry when lost) |
| **`DCS_EVALUATION.md`** | Direction (this file — phone-friendly) |
| `evaluation/README.md` | Phase 1 samples index |
| `STATE.md` | Quick status |
| `00`–`11` | Older framework — reference only |

---

*DCS Evaluation — working engineers, real work orders, level-appropriate judgment.*
