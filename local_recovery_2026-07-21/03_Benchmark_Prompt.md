# Stage 2 — Build Prompt (After Clarification)

**Run order:** `10_Clarification_Round.md` first → oracle answers appended → **then** this prompt.

Give **only** this prompt plus the packet **including clarification answers** to every model.

    You are participating in a software engineering benchmark.

    You already had ONE round of clarifying questions. Answers are below.
    You may NOT ask further questions.

    Produce a complete production-quality implementation of the application described below.

    Rules:
    - One build shot. No clarifying questions.
    - Document assumptions in ASSUMPTIONS.md (especially anything you did not ask about).
    - Do not omit requested features.
    - Follow the security tier in the packet — appropriate, not excessive.
    - Produce all required source files.
    - Include USER_GUIDE.md for non-developers (see packet).
    - Developer README does not substitute for the user guide.

    Output the full project.

    BEGIN CLARIFICATION ANSWERS
    <PASTE oracle responses>
    END CLARIFICATION ANSWERS

    BEGIN BENCHMARK PACKET
    <PASTE: product spec, acceptance criteria, security tier, end-user doc requirements, assets list>
    END BENCHMARK PACKET

---

## Consequence rule

Poor or missing clarification → wrong assumptions → **compliance and correctness suffer**.  
The benchmark does not rescue the model. That was their decision at step 2 (ASK).

---

## One-shot rule

Multiple coaching rounds after build = **failed interview**. Score what the first build delivered.

Track: model ID, packet version, clarification transcript, token cost (log only).
