# DCS Evaluation Suite

LLM engineering evaluation — job packets, answer keys, scoring engine, and run artifacts.

**North Star:** *Would I want this model at the other desk next week — for this kind of work?*

This is **evaluation software**, not a gamed leaderboard. Sample jobs are synthetic packets (S1/S2/S3).

## Quick start

See `RUN_TESTS.md` and `Phase1_Evaluation_Prompt.md`.

| Mode | What you learn |
|------|----------------|
| **ASK only** | Clarification quality (omission hunting) |
| **Full run** | ASK + BUILD + deliverables |

Score with `score_run.ps1` / `scoring_engine/`.

## Contents

- Job packets: `S1_Job_Packet.md` … `S3_Job_Packet.md`
- Answer keys: `S*_Answer_Key.md`, `Answer_Keys.md`
- Rubric & planning docs
- `runs/` — model inquiry scores and question dumps
- `scoring_engine/` — scoring scripts and result JSON

## Origin

Extracted from the **DCS benchmark** program (`D:\DCS benchmark\evaluation\`).
