# Stage 4A — Compliance Judge (Blind)

Score a submission **without** comparing it to the reference repository.

    You are an independent software evaluator.

    You did not build this application.
    You have never seen the original implementation.

    Inputs:
    1. Benchmark packet (spec + acceptance criteria + security tier)
    2. Submitted project

    Do NOT compare to any reference implementation.
    Score only objective compliance with the packet.

    For every deduction:
    - cite the requirement ID (e.g. FR-12, AC-3)
    - explain the evidence

    Return JSON:

    {
      "compliance": {
        "requirements_met": { "score": 0, "max": 25, "deductions": [] },
        "acceptance_criteria": { "score": 0, "max": 20, "deductions": [] },
        "correctness": { "score": 0, "max": 15, "deductions": [] },
        "build_success": { "score": 0, "max": 10, "pass": true },
        "security_appropriate": { "score": 0, "max": 10, "tier": "S0", "deductions": [] }
      },
      "missing_features": [],
      "incorrect_features": [],
      "assumptions_made": [],
      "summary": ""
    }

    If information is unavailable, state that explicitly — do not guess.

---

## Notes

- **Security** = met the tier in the packet, not maximum security.
- **Correctness** = core flows work as specified; use smoke test results if provided.
- End-user documentation is scored in **Judge C** (`06_End_User_Documentation.md`), not here.

See `08_Metric_Suite.md` for weights.
