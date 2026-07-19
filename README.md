# DCS Evaluation Suite (v2.1)

LLM **engineering evaluation** — not a leaderboard, not a benchmark game.

**North Star:** *Would I want this model at the other desk next week — for this kind of work?*

Every model gets the same incomplete job packet, one clarification round, then must deliver. We score the **baking** (objective outcomes), not the **cooking** (framework taste).

## Version

**Current: v2.1** (expanded from `LLM_Eval_Suite_v2.1.zip`)

Prior releases sit in `_archive/releases/` (v1, v2, v2.1 zips + Phase 1 report).

## Layout

```
packets/           Job packets, answer keys, Phase 1 prompt
scoring_engine/    Scorer + configs + test fixtures
runs/              Your model runs (questions, scores, builds)
_archive/releases/ Historical zip packages
```

## Quick start

See `RUN_TESTS.md`.

| Mode | What you learn |
|------|----------------|
| **ASK only** | Clarification quality (omission hunting) |
| **Full run** | ASK + BUILD + deliverables |

```powershell
# ASK score example
python scoring_engine\scoring_engine.py `
  --tier S1 `
  --questions runs\<model>_s1_questions.txt `
  --deliverables runs\_empty `
  --packet packets\S1_Job_Packet.md `
  --output runs\<model>_s1_inquiry_score.json
```

Or: `.\score_run.ps1 -Model <name> -Tier S1`

## Docs

- `LLM_Engineering_Eval_Suite_Planning.md` — design & philosophy  
- `LLM_Engineering_Eval_Suite_Scoring_Rubric.md` — how scoring works  

## Repo

https://github.com/DSahms/dcs-evaluation
