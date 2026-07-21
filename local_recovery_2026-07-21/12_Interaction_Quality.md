# Interaction Quality & Personality (Log + Light Score)

**Not everything is ones and zeros.** Models differ in tone, sycophancy, over-explaining, and long-context behavior. Industry benchmarks mostly ignore this. We capture it **honestly** — score a little, log a lot.

---

## What we can score today (Judge D + optional flags)

| Signal | How | Points |
|--------|-----|--------|
| Asked when oracle had gaps | Judge D vs oracle | Up to 10 (in `08`) |
| Silent when gaps existed | Judge D deduction | Same |
| Questions already in spec | Judge D deduction | Same |
| **Middle-context trap** | Key FR buried mid-packet; build violates it | Compliance deduction + flag |
| **Wrong assumption logged** | ASSUMPTIONS.md contradicts oracle | Compliance + flag |

### Middle-context trap (objective proxy for "Gemini middle hell")

During packet intake, authors place one **critical requirement only in the middle** of a long spec (e.g. FR-22: "Android sideload only").

If the model never asks about platform and builds for web → failed to absorb middle context.  
Measurable without judging "personality" directly.

---

## What we log but don't fully automate (yet)

Human or reviewer fills `run_log/interaction_notes.md` per model run:

| Flag | Example (your experience) |
|------|----------------------------|
| `sycophantic` | Agreed 8+8≠16 after you said math was wrong |
| `over_explains` | Explains gravity when you said you know pen drops |
| `condescending` | Talks down; repeats what you already stated |
| `conflict_avoidant` | Won't push back on bad premise; pleases instead of clarifies |
| `context_drift` | Strong start/end in transcript; contradicted middle of spec |
| `hallucinated_agreement` | Invents justification for user's incorrect correction |

**These do not auto-fail a run** in v1 unless they caused a spec violation.  
They **do** go in the comparison report when Dave picks a model for the other chair.

---

## Why personality isn't a big numeric score (yet)

| Problem | Reality |
|---------|---------|
| "Arrogant" is subjective | Log it; compare runs side-by-side |
| Pleasing vs professional | Hard to JSON without false precision |
| Vendor training changes monthly | Log persists; scores are versioned |

**Approach:** Judge D scores **professional curiosity** (objective-ish). Interaction log captures **how it felt to work with** — same way you'd debrief after interviewing a human.

---

## Clarification round captures personality indirectly

Model that **asks precise questions** → professional.  
Model that **asks nothing** on a competitor-replacement spec missing platform → reckless.  
Model that **asks ten obvious questions** → not listening.

All of that is **behavior**, not vibe — scoreable in Judge D.

The Gemini math story is **sycophantic hallucination under pressure** — flag in log; if it led to wrong ASSUMPTIONS.md, compliance judge cites it.

---

## v1 run artifact

```
benchmark-runs/<model>-<packet>-<date>/
  clarification.json      # What they asked
  assumptions.md          # What they assumed
  interaction_notes.md    # Human flags (optional)
  scores.json             # Full suite
```

Compare models for Dave's workstation decision — not just total score.

---

## Do not pollute the benchmark

Vendor grudges ("Gemini bad") don't belong in judge prompts.  
**Observable behaviors** do: didn't ask, wrong ask, middle FR missed, agreed to false premise in writing.

Let the run prove it.
