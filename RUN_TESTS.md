# Model Testing — Quick Run Guide

**Repo:** [DSahms/dcs-evaluation](https://github.com/DSahms/dcs-evaluation) · **Suite:** v2.1  
**Folder:** `D:\DCS benchmark\evaluation\`

This is an **evaluation suite**, not a benchmark leaderboard.

---

## Two test modes

| Mode | Time | Cost | What you learn |
|------|------|------|----------------|
| **ASK only** | ~10 min/model | Free–low | Clarification quality (omission hunting) |
| **Full run** | 1–3 hr/model | Cursor subscription | ASK + BUILD + deliverables |

**Start with ASK on S1.** Gemini already ran: `runs/gemini_s1_*`.

---

## ASK-only test (do this first)

### 1. Give the model (fresh chat, no agent coaching)

Paste **both** files in order:

1. `packets/Phase1_Evaluation_Prompt.md`
2. `packets/S1_Job_Packet.md` (or S2/S3)

Say: *"Submit your one round of clarification questions only. Do not build yet."*

### 2. Save the questions

Save to `runs/<model>_s1_questions.txt`

Examples:
- `claude_sonnet_s1_questions.txt`
- `codex_s1_questions.txt`
- `composer_s1_questions.txt`
- `glm_s1_questions.txt`

### 3. Score it

```powershell
cd "D:\DCS benchmark\evaluation"
.\score_run.ps1 -Model claude_sonnet -Tier S1
```

Or manually:

```powershell
python scoring_engine\scoring_engine.py `
  --tier S1 `
  --questions runs\claude_sonnet_s1_questions.txt `
  --deliverables runs\_empty `
  --packet packets\S1_Job_Packet.md `
  --output runs\claude_sonnet_s1_inquiry_score.json
```

### 4. Compare

| Model | Omissions (/55) | Inquiry (/75) | Notes |
|-------|-----------------|---------------|-------|
| gemini | 50 | 64 | Done 2026-07-07 |
| | | | |
| | | | |

---

## Full run (Cursor agent)

1. **Fresh chat** — pick model from dropdown **first**
2. Paste `packets/Phase1_Evaluation_Prompt.md` + packet
3. Model asks → you answer from `packets/S1_Answer_Key.md` (do NOT show them the key file)
4. Model builds one shot into folder: `runs/<model>_s1_build/`
5. Score:

```powershell
.\score_run.ps1 -Model claude_sonnet -Tier S1 -Deliverables runs\claude_sonnet_s1_build
```

---

## Fair fight rules

- Fresh chat per model
- Same packet + same prompt every time
- Don't coach one model more than another
- ASK: use plain chat for cloud models (no Cursor agent) when comparing raw question skill
- BUILD: Cursor is fine — same harness for all

---

## Oracle answers (S1)

When they ask, respond from `packets/S1_Answer_Key.md` only. Same answers for every model.

---

## Suggested order

1. **Claude Sonnet** — ASK only → score → compare to Gemini
2. **Codex or Composer** — ASK only
3. Winner on ASK → one full S1 BUILD in Cursor

---

*Update `MODEL_PREDICTIONS.md` after each run.*
