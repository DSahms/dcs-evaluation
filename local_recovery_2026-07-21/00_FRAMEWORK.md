# Core Flow (Simple — No Drift)

**This is the benchmark.** Everything else supports these three steps.

```
1. FEED    → Benchmark packet (spec, screenshots, acceptance, tier, assets)
2. ASK     → One shot: "Is anything missing?" (scored — their choice)
3. BUILD   → One shot after oracle answers (consequences of step 2)
```

If they don't ask when they should → they suffer on build. **That was their decision.**

If they ask wrong things or ignore answers → they suffer. **Their decision.**

No kiosk in v1. No twelve rounds. **Feed → ask once → build.**

---

## Real-world intake this simulates

> "My competitor has an app that does X and Y. I want X, Y, and Z."

Specs come from that conversation. At entry level we freeze the result as the packet.  
The model still gets **one professional chance** to say: *"With what you gave me, I need clarity on…"*

Same as a good engineer before committing — not live customer yet (`11` is future notes).

---

## Pipeline (full)

```
Stage 0   Packet + oracle (intake quality — before any model runs)
    ↓
Stage 2A  ASK — one round (Judge D)
    ↓
Stage 2B  BUILD — one shot (Judges A/B/C + gate)
    ↓
Hire / no hire
```

---

## Principles (updated)

| Principle | Meaning |
|-----------|---------|
| **Feed → ask → build** | Three steps; ask is mandatory phase, not optional |
| **One ask, one build** | Not a chat; not coaching loops |
| **Consequences** | Bad intake choices hurt build score — don't rescue |
| **Blind** | Judges never see reference repo |
| **Proportional** | Simplest solution for the tier |
| **End-user docs** | Non-dev can install without you |
| **Consequences** | Bad intake choices hurt build score — don't rescue |
| **Blind** | Judges never see reference repo |
| **Proportional** | Simplest solution for the tier |
| **End-user docs** | Non-dev can install without you |
| **Same oracle** | Every model gets identical answers (v1) |

**Out of v1 scope:** personality scoring, kiosk live intake (`11` is future notes only).

## North star

> **Which AI reads the packet, asks what matters once, builds once, and documents for real users?**

---

## Document map

| File | Purpose |
|------|---------|
| `STATE.md` | Re-entry |
| `01`–`09` | Packet, judges, tiers, metrics, intake |
| `10_Clarification_Round.md` | **Core ASK step** |
| `03_Benchmark_Prompt.md` | **Core BUILD step** (after answers) |
| `11_Future_Live_Intake.md` | Future notes (kiosk) — not v1 |
| ~~`12_Interaction_Quality.md`~~ | **Parked** — personality not in v1 |

**Path:** `D:\DCS benchmark\`
