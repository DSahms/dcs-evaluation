# Metric Suite — 100 Points

Three judges + one automated gate. Same packet version for every model.

---

## Gates (pass/fail before scoring)

| Gate | Rule |
|------|------|
| **Build** | Project installs and starts per dev README or documented command |
| **Smoke** | Automated smoke tests in packet pass (when `07_smoke_tests/` exists) |

Fail build gate → record score but mark **NOT HIREABLE** regardless of total.

---

## Score breakdown

| Metric | Pts | Judge / source |
|--------|-----|----------------|
| Requirements met | 18 | Compliance — cite FR-* |
| Acceptance criteria | 12 | Compliance — binary AC-* |
| Correctness | 10 | Compliance + smoke |
| Build success | 8 | Automated gate |
| Security appropriate | 7 | Compliance — vs tier |
| Engineering judgment | 10 | Judgment — proportional design |
| Simplicity | 4 | Judgment — sub-score |
| Maintainability | 4 | Judgment — could another dev take over |
| **Clarification round** | 10 | Judge D — see `10_Clarification_Round.md` |
| **End-user documentation** | **15** | **Doc judge — mandatory** |
| Performance | 0–2 | **Only if NFR in packet**; else N/A (exclude from total) |

**Total: 100** (98 + up to 2 perf when NFR defined → cap at 100)

---

## Hire bands (suggested)

| Total | Verdict |
|-------|---------|
| 85–100 | Strong hire — first draft |
| 70–84 | Hire with fixes — still one-shot benchmark |
| 55–69 | No hire — gaps or bloat |
| &lt;55 | Fail |

End-user doc **&lt;8/15** → cap verdict at **No hire** (beta unusable).

Engineering judgment **Catastrophic Bloat** → cap at **No hire** even if spec met.

---

## What we do NOT score (unless in packet)

- Same framework as reference app  
- Same folder layout as author  
- Maximum security  
- Maximum performance  
- Code elegance / design patterns for their own sake  
- Token cost (log separately for Dave — optional `cost_log.json`)  

---

## Optional log (not quality score)

```json
{
  "model": "",
  "packet_version": "",
  "input_tokens": 0,
  "output_tokens": 0,
  "estimated_cost_usd": 0,
  "one_shot": true
}
```

Cost matters to operators; it is not "better AI" unless packet adds budget NFR.

---

## Suite execution order

1. Stage 0 packet (frozen + oracle + assets)  
2. Stage 2A clarification round (scored)  
3. Stage 2B one-shot build (oracle answers appended)  
4. **Gate:** build + smoke  
5. **Judge A:** compliance (`04`)  
6. **Judge B:** engineering judgment (`05`)  
7. **Judge C:** end-user docs (`06`)  
8. **Judge D:** clarification (`10`)  
9. Aggregate → `08` weights → verdict  

---

## Model-vs-model fairness

Compare models only on:

- Same packet version + oracle answers  
- Same clarification rules (one round)  
- Same build rules (one shot after answers)  
- Same judges / prompts  
- Same smoke tests  

Like GPT-5 vs GPT-5.6 on the **same hidden task** — but the task is a **real product spec**, not a leaderboard puzzle.
