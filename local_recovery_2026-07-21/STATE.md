# DCS Evaluation — STATE

**Last updated:** 2026-07-06  
**Path:** `D:\DCS benchmark\`

---

## What this is

**Evaluation software** — not a gamed benchmark. Feed a job packet at **S1, S2, or S3** scope → one clarification round → one build → judge **at that level's bar**.

---

## Active work

| Piece | Location | Status |
|-------|----------|--------|
| Direction doc | `DCS_EVALUATION.md` | ✅ rewritten |
| Phase 1 prompt | `evaluation/Phase1_Common_Evaluation_Prompt.md` | ✅ |
| S1 basic packet | `evaluation/S1_Job_Packet.md` (LawnCare Lite) | ✅ |
| S2 involved packet | `evaluation/S2_Job_Packet.md` (Warehouse) | ✅ |
| S3 enterprise packet | `evaluation/S3_Job_Packet.md` (Hospital) | ✅ |
| Clarification oracles (per packet) | — | ⬜ |
| Level-specific score sheets | — | ⬜ |
| First model comparison run | — | ⬜ |

---

## Older framework (reference only)

Root `00`–`11` + `_archive/` — intake, judges, kiosk notes from the earlier "benchmark" framing. **Not** the live direction. Mine for ideas; don't treat as fixed law.

---

## Boundary

No portfolio apps (NURA, Arden, Pink Skies, Story Keeper, Ledger, etc.). Sample jobs in `evaluation/` are synthetic.

---

## Core flow

```
FEED → ASK (once) → BUILD → EVALUATE (level-appropriate)
```

---

## File order

**Lost the thread?** `DCS_EVALUATION_GUIDE.md` ← **start here** (full process + scoring)

**Phone / quick direction:** `DCS_EVALUATION.md`

**Phase 1 samples:** `evaluation/`

**Legacy reference:** `00`–`11`, `_archive/`
