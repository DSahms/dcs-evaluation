# Phase 1 ASK Evaluation — Model Comparison Report

**Source Word doc:** `LLM_Eval_Suite_Phase1_Report.docx`  
**Report date on cover:** July 2026 · labeled **v1.0** · file dated **2026-07-12**  
**What it covers:** Phase 1 **ASK only** (clarification questions) — not BUILD  
**Suite generation:** written against the evaluation suite as it existed mid-July (before / around the v2 → v2.1 packet upgrades now in the repo)

> Plain-text copy of the Word report so you don’t need Microsoft Word. Charts in the original are described in prose only.

---

## Executive summary (what this doc is)

Five models were given **three incomplete job packets** (S1 lawn care, S2 warehouse, S3 hospital/HIPAA) and **one round** to ask clarification questions. Scoring measures whether they think like a senior engineer: find intentional gaps, especially **operational traps** and **training-data traps**.

**Central finding:** no model showed reliable operational awareness. Across ~15 model×packet runs, combined hit rate on operational + training-data traps was about **1 / 17**. Strong at surface requirements; weak at reading between the lines of business context.

Surprise: **Gemma 4B (base)** beat **Gemma 12B agentic** wherever they differed — agentic fine-tuning seemed to hurt the ASK phase (biased toward building, not discovering).

---

## Models tested

| Model | Notes from report |
|-------|-------------------|
| Gemma 4B (base) | Smallest; clean PEP; only Gemma trap hit |
| Gemma 12B Agentic | Worse ASK than 4B; Medium PEP ×2 |
| Venice AI | Most consistent; highest total among fully tested |
| ChatGPT | Strong S2; shotgun S3 (low CE) |
| Claude Sonnet 5 | Best single packet (S3); highest CE; incomplete S1 |

---

## Master scorecard (from the report)

Points are omission-detection scores. Empty S1 for ChatGPT/Claude = credits used on bigger packets first.

| Model | S1 (85) | S2 (90) | S3 (110) | Total | Avg CE | Traps | PEP |
|-------|---------|---------|----------|-------|--------|-------|-----|
| Gemma 4B | ~10 | ~40 | ~57 | **~107** | 0.61 | 1/7 | Clean |
| Gemma 12B Agentic | ~5 | ~35 | ~57 | **~97** | 0.70 | 0/7 | Med ×2 |
| Venice AI | 34 | 45 | 60 | **139** | 0.89 | 0/7 | Med ×3 |
| ChatGPT | — | ~75 | 62 | **~137** | 0.60 | 0/4 | Clean |
| Claude Sonnet 5 | — | 35 | **75** | **~110** | **0.97** | 0/4* | Clean |

\*Claude had *partial* training-data trap avoidance on S3 (not full).

**CE** = Clarification Efficiency (questions that hit real omissions ÷ questions asked)  
**PEP** = Premature Execution Penalty (committed to a solution during ASK)

---

## Key findings (short)

1. **Agentic fine-tuning can regress ASK** — use smaller/base models for discovery, reserve agentic for BUILD.  
2. **Training-data traps work** — every model still defaulted to FHIR/SSO patterns even when the packet said otherwise.  
3. **Operational traps are the hard gap** — ~6% hit rate; reading *business behavior* vs specs.  
4. **Venice** — underrated: consistent, private routing, best cumulative among fully tested; zero trap awareness.

## Hardest shared blind spots

- Multi-hospital data architecture (S3) — **0/5**  
- Two-warehouse sync (S2) — **1/4**  
- Pharmacy/lab & identity TD traps — no full avoids  

## Report’s own next steps (as of July)

1. Fix scoring-engine keyword false positives / CE counting  
2. Design Phase 2 **BUILD** and check whether ASK quality correlates with build quality  
3. Expand trap subtypes  

---

## How current is this vs today’s repo?

| Item | Status |
|------|--------|
| This Word report | **July 12, 2026** snapshot of **Phase 1 ASK results** |
| Live GitHub suite | **v2.1** packets + scoring engine (pushed later) |
| Phase 2 BUILD results | **Not in this Word doc** |
| Newer model runs after July 12 | Not in this report (local `runs/` may have extras) |

So: the document is still the best **written narrative of Phase 1 ASK outcomes**. It is **not** a live dashboard and may not match every number if packets/scorer moved in v2.1. Treat it as the Phase 1 findings memo, not “latest scoreboard forever.”

Original Word file: `_archive/releases/LLM_Eval_Suite_Phase1_Report.docx` (also in `D:\Miscellaneous\`).
