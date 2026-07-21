# Future — Live Customer Intake (v2)

**Today (v1):** Pre-written clarification oracle — stand-in because we cannot run a live customer in the lab yet.

**Tomorrow (v2):** Customer at the kiosk. You are busy. They sit in the other chair. AI runs intake — conversation, uploads, read-back — **then** build.

This document is the north star. v1 benchmarks remain valid; v2 extends them when the workstation exists.

---

## The vision (Dave's desk)

```
You (busy)          Customer              AI workstation
    │                   │                        │
    │── "Talk to that ──►│                        │
    │    chair"         │── kiosk conversation ───►│
    │                   │   uploads, describes     │
    │                   │                        │ read-back loop
    │                   │◄── "Here's what I heard" │
    │                   │── "No, not that…" ──────►│ refine
    │                   │                        │
    │                   │                        ▼
    │                   │                   frozen work order
    │                   │                        │
    │                   │                        ▼ build
```

Two engineers at two desks was always the **competition**.  
The customer at the kiosk is the **intake** — and in v2, **both humans and AI can be part of it.**

---

## What v1 cannot judge (and should not pretend to)

| v1 (oracle) | v2 (live) |
|-------------|-----------|
| Pre-written answers | Real customer nuance |
| No "you know what I mean" | Tone, hesitation, correction |
| Fair AI vs AI on fixed bytes | Fair AI vs AI on intake + build skill |

**Rule:** Do not score a model on live-customer empathy in v1. Score **clarification against oracle** only.

When v2 exists, add a separate **Intake Quality** dimension — did the AI run the conversation well?

---

## The read-back loop (core human skill — and AI skill)

Your workflow:

1. You describe what you're trying to build  
2. AI gives you a paragraph back  
3. You read it: *"My God, that's off"*  
4. You don't ask "where did AI go wrong" first — you ask **"what did I say wrong?"**

That loop is **requirements engineering**. Most people skip it and blame shit-out.

### v2 intake must include

| Step | Purpose |
|------|---------|
| **Listen** | Customer talks, uploads sketches/screenshots |
| **Paraphrase** | AI returns structured summary: "Here's what I heard" |
| **Confirm** | Customer corrects: "Not that — I meant…" |
| **Revise** | AI updates spec draft |
| **Sign-off** | Customer agrees: "Yes, build that" |
| **Build** | One shot (or v2 build rules) |

**Score in v2:** quality of paraphrase, number of correction rounds to alignment, whether AI blamed customer vs refined language.

---

## v1 stand-in (what we do now)

Until the kiosk exists:

1. Packet includes **intentional nuance gaps** (documented in oracle, not public to models)  
2. **One clarification round** — models ask; oracle answers  
3. Optional **read-back simulation:** model must output `SUMMARY_OF_REQUIREMENTS` before build; judge compares to spec (did they hear correctly?)

This trains the muscle without a live customer.

---

## v2 scoring additions (when ready)

| Dimension | Measures |
|-----------|----------|
| Paraphrase accuracy | Read-back matched customer intent after corrections |
| Correction handling | Improved after "you're off" without defensiveness |
| Intake completeness | Captured uploads, platform, user type |
| Time to sign-off | Professional efficiency |
| Build (existing suite) | Unchanged — still judgment, docs, compliance |

---

## Fairness across versions

| Compare | Fair? |
|---------|-------|
| Model A vs B on same v1 packet + oracle | Yes |
| Model A vs B on same v2 customer session (recorded, replayed) | Yes — same recording for all |
| v1 scores vs v2 scores | No — different benchmarks, label separately |

Record **benchmark_version: v1-oracle | v2-live** on every run.

---

## Principle (do not forget)

> Don't judge an engineer on requirements they never had a chance to shape.  
> Give them the intake — or an honest stand-in — then judge the build.

v1 is the honest stand-in.  
v2 is the goal you're building the workstation to reach.
