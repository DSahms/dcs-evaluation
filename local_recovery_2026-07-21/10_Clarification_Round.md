# Stage 2A — Clarification Round (Core Step: ASK)

**Part of the benchmark — not optional.** See `00_FRAMEWORK.md`: FEED → **ASK** → BUILD.

After the model receives the Benchmark Packet, it gets **one shot** to ask whether anything is missing before building.

---

## Why this is fair

| Real desk | Benchmark |
|-----------|-------------|
| Customer gives vague spec | Packet may include intentional ambiguities (documented in intake oracle) |
| Good engineer asks before building | Model gets **one** question round |
| Bad engineer assumes and ships wrong thing | Model that runs silent gets penalized |
| Customer answers | **Pre-written answers** — same for every model |

Human advantage (reading the room, emotional context) is **not** simulated.  
Technical + **professional** advantage (knowing what to ask) **is** measured.

---

## What the model receives (baseline packet)

Same as Stage 0 output, plus optional:

| Asset | Purpose |
|-------|---------|
| `01_product_spec.md` | Work order |
| `02_acceptance_criteria.md` | Definition of done |
| `03_security_tier.md` | Appropriate security |
| `04_end_user_doc_requirements.md` | Manual requirements |
| `06_assets/screenshots/` | UI intent (if visual app) |
| `06_assets/wireframes/` | Drawings / mockups |
| `06_assets/sample_data/` | Example inputs/outputs |

**Not included:** reference repo, author's implementation notes.

---

## Clarification prompt (Stage 2A)

    You are a senior engineer reviewing a work order before starting implementation.

    Read the entire Benchmark Packet including any screenshots and wireframes.

    You may ask UP TO 10 clarifying questions in ONE round.
    After this round, you will receive answers and must build with NO further questions.

    Rules:
    - Ask only questions that materially affect scope, security, UX, or acceptance criteria.
    - Do not ask for information already stated in the packet.
    - Do not ask which framework or library to use unless the spec requires a constraint.
    - Number your questions Q1, Q2, …

    If you believe the packet is complete, respond with:
    NO_CLARIFICATIONS_NEEDED
    and briefly state why you are ready to build.

    Output format:
    ```json
    {
      "clarifications_needed": true,
      "questions": [
        { "id": "Q1", "topic": "...", "question": "..." }
      ]
    }
    ```
    OR
    ```json
    {
      "clarifications_needed": false,
      "ready_rationale": "..."
    }
    ```

---

## Answer oracle (fairness critical)

During **packet intake** (`09_Packet_Intake_Quality.md`), authors pre-write:

`packet/clarification_oracle.md`

For each **known ambiguity** in the spec:

```markdown
### Q: [expected question theme]
**Answer:** [authoritative, frozen answer — same for all models]

### Q: Install target — Android sideload vs web?
**Answer:** Android APK sideload only for v1. USER_GUIDE must cover unknown-source prompt.
```

Optional: **trap ambiguities** — intentional gaps that a good engineer should ask about.  
Oracle documents which gaps exist so judges can score fairly.

**Models never get live human answers.** Only oracle lookup (automated or human facilitator pastes matching answers).

Unmatched questions get: *"Not specified; use minimal reasonable assumption and document in ASSUMPTIONS.md."*

---

## Stage 2B — Build (after answers)

After oracle responses are appended to the packet:

    You previously asked clarifying questions. Answers are below.
    Now build in ONE shot. No further questions.

    [ANSWERS]
    [ORIGINAL PACKET]

(See `03_Benchmark_Prompt.md` for full build rules.)

---

## Scoring clarification (Judge D)

**Max 10 points** — part of professional judgment, not optional fluff.

| Score | Behavior |
|-------|----------|
| **9–10** | Asked precise questions that matched oracle gaps; or correctly declared NO_CLARIFICATIONS when packet complete |
| **6–8** | Asked some useful questions; missed one important gap |
| **3–5** | Asked vague or redundant questions; missed major ambiguities |
| **0–2** | Silent run despite known gaps; or asked for info already in spec |
| **Penalty** | Asked for stack/framework choice when spec is behavior-only |

Judge inputs:

1. Packet + oracle (which gaps were known)  
2. Model's clarification JSON  
3. Whether build violated unstated assumptions answerable from oracle  

**Silent failure example:** Packet says "store locally" without platform; oracle expects platform question; model never asked → deduct clarification + may deduct compliance.

**Good NO_CLARIFICATIONS:** Packet explicitly states platform, tier, AC complete → declaring ready is correct (+points).

---

## Intake: screenshots & drawings audit (AI pass)

During packet freeze, run AI on assets:

    Compare screenshots/wireframes to 01_product_spec.md.
    List UI elements visible in images but missing from spec.
    List spec claims not supported by images.
    List questions a engineer would ask after seeing visuals.

Merge into spec or oracle before freeze.

This improves **input quality** so clarification round tests judgment, not author laziness.

---

## Human vs AI desk (your metaphor)

| You at the desk | AI competitor |
|-----------------|---------------|
| Read customer's tone, hesitation | Reads spec + screenshots |
| Know when "simple" isn't simple | Must ask or assume |
| One round to clarify before build | Same one round |
| Judged on build + judgment + docs | Same suite |

Emotional read isn't in scope. **Professional curiosity is.**

---

## Pipeline update

```
Packet frozen (with oracle + assets)
        │
        ▼
Stage 2A  Clarification round (one round, scored)
        │
        ▼
Oracle answers appended (identical for all models)
        │
        ▼
Stage 2B  One-shot build
        │
        ▼
Gates + Judges A/B/C/D
```

---

## Clarification in v1 vs live customer in v2

**Today:** Models do not get a live customer. They get a frozen packet and **one clarification round** against a **pre-written oracle** — a fair stand-in, not the final form.

**Tomorrow:** Customer at the kiosk; AI runs intake (conversation, uploads, **read-back loop**), then build. See `11_Future_Live_Intake.md`.

Do not score v1 models on empathy or live nuance. Score whether they **asked what a professional would ask** given the packet — and whether a v2 read-back summary would have been accurate (optional exercise).
