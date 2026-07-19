# LLM Engineering Evaluation Suite — Scoring Rubric

---

## How This Rubric Works

Every criterion is designed for **automation**. Each item is one of:

- **CHECKLIST** — Present or absent. Binary. Script can verify.
- **KEYWORD MATCH** — Does the output contain required terms? Regex/string match.
- **STRUCTURE CHECK** — Does the document follow the required format? Pattern matching.
- **HEURISTIC** — Simple rules an LLM-as-judge can evaluate with a tightly constrained prompt (not open-ended judgment).

**Human involvement:** Appeals court only — steps in for disputes.

---

## Point Distribution

### S1 — LawnCare Lite (200 points)

| Category | Max Points | Automation Method |
|----------|-----------|-------------------|
| Inquiry — Omission Detection | 55 | Keyword match |
| Inquiry — Question Quality | 20 | Heuristic |
| Deliverable Completeness | 50 | Checklist |
| Engineering Judgment | 45 | Checklist + Heuristic |
| Documentation | 30 | Checklist + Heuristic |

### S2 — Warehouse Inventory (250 points)

| Category | Max Points | Automation Method |
|----------|-----------|-------------------|
| Inquiry — Omission Detection | 70 | Keyword match |
| Inquiry — Question Quality | 25 | Heuristic |
| Deliverable Completeness | 55 | Checklist |
| Engineering Judgment | 65 | Checklist + Heuristic |
| Documentation | 35 | Checklist + Heuristic |

### S3 — Hospital Information System (300 points)

| Category | Max Points | Automation Method |
|----------|-----------|-------------------|
| Inquiry — Omission Detection | 95 | Keyword match |
| Inquiry — Question Quality | 30 | Heuristic |
| Deliverable Completeness | 55 | Checklist |
| Engineering Judgment | 90 | Checklist + Heuristic |
| Documentation | 30 | Checklist + Heuristic |

---

## CATEGORY 1: Inquiry — Omission Detection

**Already defined in planning document.** Keyword matching against the answer key.

### Matching Rules (Automated)

```
For each omission in the tier's answer key:
  1. Check if model's clarification questions contain ANY of the omission's keywords
  2. If YES → award the omission's point value
  3. If NO → award 0 points
  4. No partial credit
```

### Additional Inquiry Rules

| Situation | Points | Rule |
|-----------|--------|------|
| Asked about something already in the packet | -2 per occurrence | "This is answered in your packet, section X" — if they ask it, they didn't read carefully |
| Asked a technology preference question (framework, language, etc.) | 0 (neutral) | Not scored either way. Answer: "Your choice — document your decision." |
| Asked a reasonable question not in the key | 0 (neutral) | No penalty. The model was being thorough. |
| Submitted zero questions | -10 (all tiers) | Even a junior developer asks questions. Submitting nothing is a signal. |

---

## CATEGORY 2: Inquiry — Question Quality

This scores HOW the model asks, not just WHETHER they ask the right things.

### Criteria (All Tiers)

| # | Criterion | Points | Check Method |
|---|-----------|--------|-------------|
| Q1 | Questions are submitted as a single batch (not one at a time) | 3 | Structure check — did they submit all questions in one message? |
| Q2 | Each question is clearly separated and numbered | 3 | Structure check — numbered list or clear separators present? |
| Q3 | No questions that are answered by reading the packet carefully | 0 to -6 | Keyword match against packet content — each "already answered" question = -2 pts |
| Q4 | Questions demonstrate reading comprehension of the packet | 5 | Heuristic — do questions reference specific details from the packet? (e.g., "You mentioned 150 users — are they...") |
| Q5 | Questions show awareness of the project's complexity level | S1: 3 / S2: 5 / S3: 8 | Heuristic — are the questions appropriate for the tier's complexity? (S1: business basics. S2: system design. S3: enterprise architecture.) |
| Q6 | Questions prioritize what matters most (critical gaps first) | S1: 3 / S2: 5 / S3: 9 | Heuristic — are the most important omissions asked about? Weighted by omission criticality. |

### Question Quality Scoring Logic

```
Q1 (Batch submission): 
  IF questions appear to be a single coherent submission → +3
  ELSE → 0

Q2 (Clear formatting):
  IF questions are numbered or clearly separated → +3
  IF questions are a wall of text with no structure → 0

Q3 (No packet re-questions): [Negative scoring]
  FOR each question that is answered in the packet → -2
  Minimum: -6 (capped)

Q4 (Reading comprehension):
  IF at least 2 questions reference specific details from the packet → +5
  ELSE IF at least 1 question references a specific detail → +3
  ELSE → 0

Q5 (Complexity awareness):
  S1: Questions about basic business rules and workflow → +3
      Questions about microservices architecture → 0 (over-thinking)
  S2: Questions about system design, integrations, concurrency → +5
      Questions that only a junior would ask (basic CRUD) → +2
  S3: Questions about compliance, migration, distributed systems → +8
      Questions that only address mid-level concerns → +3

Q6 (Prioritization):
  Score = (critical omissions asked / total critical omissions) × max_points
  Example S3: 3 of 4 critical omissions asked → (3/4) × 9 = 6.75 → round to 7
```

---

## CATEGORY 3: Deliverable Completeness

### Required Files (All Tiers)

| File | Points | Check Method |
|------|--------|-------------|
| Architecture.md | 5 | File exists? |
| ASSUMPTIONS.md | 5 | File exists? |
| README.md | 5 | File exists? |
| Source code (functional application) | S1: 10 / S2: 10 / S3: 10 | Code files exist and form a runnable application? |
| Tests | S1: 5 / S2: 5 / S3: 5 | Test files exist with at least basic test cases? |
| Build instructions (in README or separate file) | S1: 5 / S2: 5 / S3: 5 | Step-by-step instructions to build and run? |

**Subtotal: 35 points (all tiers)**

### Functional Requirements Coverage

Each tier has a list of functional requirements. Each requirement must be addressed in either the code OR Architecture.md (explaining how it would be implemented).

**Scoring: Points per requirement addressed**

#### S1 Functional Requirements (15 points — 3pts each)

| # | Requirement | How to Verify |
|---|------------|---------------|
| 1 | Customer management | Code has customer CRUD? Architecture mentions it? |
| 2 | Appointment scheduling | Code has scheduling? Architecture addresses it? |
| 3 | Job completion | Code has completion workflow? |
| 4 | Search customers | Search functionality exists? |
| 5 | Print daily schedule | Print/view schedule feature exists? |

#### S2 Functional Requirements (20 points — ~3.3pts each, rounded)

| # | Requirement | How to Verify |
|---|------------|---------------|
| 1 | Inventory management | Inventory CRUD operations exist? |
| 2 | Transfers between warehouses | Transfer workflow with status tracking? |
| 3 | Barcode scanning | Scanning interface/integration mentioned? |
| 4 | Audit log | Audit logging implemented or architected? |
| 5 | Reports | At least one report capability? |
| 6 | Permissions/role-based access | Role definitions and access control? |

#### S3 Functional Requirements (20 points — ~2.9pts each, rounded)

| # | Requirement | How to Verify |
|---|------------|---------------|
| 1 | Patient registration | Patient record creation? |
| 2 | Scheduling | Appointment/scheduling system? |
| 3 | Clinical notes | Clinical documentation capability? |
| 4 | Pharmacy | Pharmacy module or integration architected? |
| 5 | Laboratory | Lab module or integration architected? |
| 6 | Billing | Billing/revenue cycle addressed? |
| 7 | Auditing | Comprehensive audit system? |

**Verification method:** Checklist + keyword search across code and Architecture.md. The requirement is "addressed" if it appears as implemented code OR as a deliberate architectural decision explaining how/when it will be implemented.

---

## CATEGORY 4: Engineering Judgment

### 4A: ASSUMPTIONS.md Quality (All Tiers)

**Required structure per assumption (from Phase 1 Prompt):**

| Field | Points | Check Method |
|-------|--------|-------------|
| Unknown | 2 per assumption | Keyword: does entry contain "Unknown" or equivalent label? |
| Decision | 3 per assumption | Keyword: does entry state what was decided? |
| Reasoning | 3 per assumption | Heuristic: is there a justification (more than one sentence)? |
| Risk | 2 per assumption | Keyword: does entry mention risk, impact, or consequence? |

**Scoring logic:**

```
MAX_ASSUMPTIONS_TO_SCORE = 10 (score first 10 if more exist)

FOR each assumption in ASSUMPTIONS.md (up to 10):
  has_unknown = check for "Unknown" label/section → +2
  has_decision = check for stated decision → +3
  has_reasoning = check for justification (length > 30 chars after "Reasoning" label) → +3
  has_risk = check for risk/impact mention → +2
  assumption_score = sum of above (max 10 per assumption)

assumptions_total = sum of all assumption scores
assumptions_max = 10 × 10 = 100

# Normalize to category points:
# S1: 15 pts, S2: 20 pts, S3: 30 pts
normalized_score = (assumptions_total / assumptions_max) × tier_points
```

**Bonus — Assumption Relevance:**

| Check | Points |
|-------|--------|
| At least 3 assumptions relate to the intentional omissions (things they should have asked about but didn't, or asked about and got answers for) | +3 |
| At least 1 assumption addresses an edge case not in the packet | +2 |

### 4B: Architecture.md Quality

| # | Criterion | Points | Check Method |
|---|-----------|--------|-------------|
| A1 | Architecture is documented (not just code comments) | 3 | File exists and has > 200 words? |
| A2 | Technology choices are stated | 3 | Keywords: framework, language, database, etc. mentioned? |
| A3 | Technology choices include REASONING (why, not just what) | S1: 5 / S2: 7 / S3: 10 | Heuristic: does it explain WHY each choice was made, with reference to requirements? |
| A4 | Architecture addresses non-functional requirements from the packet | S1: 3 / S2: 5 / S3: 8 | Checklist: for each NFR in the packet, is there a corresponding architectural decision? |
| A5 | Architecture is APPROPRIATE to the tier's complexity | S1: 4 / S2: 6 / S3: 10 | Heuristic (see below) |
| A6 | Tradeoffs and limitations are acknowledged | S1: 2 / S2: 4 / S3: 7 | Heuristic: does it mention what was sacrificed or what won't scale? |

#### A5 — Architecture Appropriateness (Heuristic Rules)

**This is the over/under-engineering check. It is NOT about which tech they chose.**

**S1 (Junior — simple web app, 3 users):**
```
OVER-ENGINEERING signals (any = 0 points for A5):
  - Microservices architecture mentioned
  - Event-driven / message queue mentioned
  - Kubernetes or container orchestration
  - More than 3 separate services/backend components
  - Event sourcing or CQRS
  - Load balancer mentioned
  - "Scalable to millions" type language

UNDER-ENGINEERING signals (any = 0 points for A5):
  - No authentication mentioned in architecture
  - No database mentioned
  - No error handling strategy
  - Flat file storage for customer data

APPROPRIATE (full points):
  - Monolithic or simple client-server architecture
  - Single database (SQLite, PostgreSQL, etc.)
  - Basic authentication
  - Reasonable tech choices with reasoning tied to "3 users, small business"
```

**S2 (Mid-level — 150 users, integrations, multi-location):**
```
OVER-ENGINEERING signals:
  - Microservices for what is fundamentally a CRUD + integration app
  - Event sourcing
  - Custom RPC protocol
  - More than 5 separate services

UNDER-ENGINEERING signals:
  - No mention of how to handle concurrent access
  - No integration architecture for accounting system
  - No role-based access design
  - Single server with no consideration for 150 users
  - SQLite mentioned (not appropriate for multi-user concurrent access)

APPROPRIATE:
  - Monolith or limited services (2-3)
  - Proper database (PostgreSQL, MySQL)
  - Integration strategy for accounting (API, webhook, batch)
  - RBAC design
  - Some consideration of concurrency and performance
```

**S3 (Enterprise — 8,000 users, HIPAA, migration):**
```
OVER-ENGINEERING signals:
  - Blockchain (unless for audit — even then, questionable)
  - Custom encryption algorithms
  - Reinventing protocols
  - Overly complex microservices (20+ services) for the stated modules

UNDER-ENGINEERING signals:
  - Single server deployment
  - No mention of high availability / failover
  - No encryption strategy for PHI
  - No migration strategy for existing data
  - No compliance framework
  - SQLite or other inappropriate database for enterprise scale
  - No mention of how integrations (pharmacy, lab) work

APPROPRIATE:
  - Scalable architecture (microservices or well-structured monolith)
  - Multi-tier (load balancer, app servers, database cluster)
  - Encryption at rest and in transit specified
  - Migration strategy documented
  - Integration architecture for external systems
  - HIPAA compliance measures addressed
  - High availability / DR strategy
```

### 4C: Security (Per Packet's Security Section)

Each tier's packet has a "Security" section. The architecture MUST address every item in it.

#### S1 Security Requirements (5 points)

| Requirement | Points | Verify |
|------------|--------|--------|
| Login required | 2 | Is authentication implemented/architected? |
| No payment or medical data (implies: no need for PCI/HIPAA, but basic security still needed) | 3 | Does architecture mention basic security (passwords hashed, HTTPS, input validation)? |

#### S2 Security Requirements (10 points)

| Requirement | Points | Verify |
|------------|--------|--------|
| Role-based access | 4 | Are roles defined? Are permissions specified? |
| Encrypted transport | 3 | Is HTTPS/TLS mentioned? |
| Audit logs | 3 | Is audit logging architected? |

#### S3 Security Requirements (15 points)

| Requirement | Points | Verify |
|------------|--------|--------|
| Enterprise identity (SSO, LDAP, Active Directory) | 4 | Is enterprise authentication mentioned? |
| Encryption (at rest and in transit) | 4 | Are both specified with standards? |
| Auditing | 4 | Comprehensive audit architecture? |
| Healthcare compliance (HIPAA) | 3 | Compliance measures beyond basic security? |

**Verification:** Keyword search in Architecture.md and code for security-related terms matching the packet's requirements.

---

## CATEGORY 5: Documentation (README Quality)

### Required Sections (Each scored: Present + Accessible)

| # | Section | S1 Pts | S2 Pts | S3 Pts | Presence Check | Accessibility Check |
|---|---------|--------|--------|--------|----------------|-------------------|
| D1 | Prerequisites (with versions) | 3 | 3 | 3 | Section heading + items listed | Each item has version number? |
| D2 | What Each Prerequisite IS (plain English explanation) | 3 | 3 | 3 | Sub-check of D1 | Each prerequisite has a 1-sentence explanation? |
| D3 | Step-by-step Installation | 5 | 5 | 3 | Section exists | Every command explained (what it does)? |
| D4 | Configuration | 4 | 5 | 4 | Section exists | Every config var explained with example? |
| D5 | Database Setup | 4 | 4 | 3 | Section exists (if applicable) | Steps to create DB, run migrations, seed? |
| D6 | Running the App | 4 | 5 | 5 | Section exists | Exact command + what you'll see when it works? |
| D7 | Troubleshooting | 4 | 5 | 5 | Section exists | At least 3 problems + solutions? |
| D8 | Project Structure | 3 | 5 | 4 | Section exists | Major folders/files explained in plain English? |

### Scoring Per Section

```
FOR each section (D1-D8):
  presence = section_heading_exists ? 1 : 0
  accessibility = meets_accessibility_criteria ? 1 : 0
  
  IF presence == 0:
    section_score = 0
  ELSE IF accessibility == 0:
    section_score = section_points × 0.4  (has section, but not accessible)
  ELSE:
    section_score = section_points  (has section AND it's accessible)

documentation_total = sum of all section_scores
```

### Accessibility Heuristic (for automated checking)

```
FOR each section:
  # Check if technical terms are explained
  technical_terms_found = count of known tech terms in section
  terms_explained = count of those terms that have an adjacent explanation
    (within 50 chars: "is a", "is used to", "allows you to", "—", ":", 
     parentheses with explanation, etc.)
  
  accessibility_ratio = terms_explained / technical_terms_found
  
  IF accessibility_ratio >= 0.7 → ACCESSIBLE
  IF accessibility_ratio >= 0.4 → PARTIAL → 40% of section points
  IF accessibility_ratio < 0.4 → NOT ACCESSIBLE → 40% of section points
```

### README Anti-Patterns (Deductions)

| Anti-Pattern | Deduction | Why |
|-------------|-----------|-----|
| "Just run npm install and npm start" with no explanation | -3 | Assumes the reader knows what npm is |
| "See documentation" / "Refer to docs" without linking or summarizing | -2 | Circular reference |
| Uses jargon without explanation (e.g., "set up your ORM", "configure your CI/CD") | -1 per occurrence (max -5) | Not accessible to non-technical users |
| Missing from README (present only in other files) | 0 (no penalty, but that section doesn't get points) | Sections must be IN the README |

---

## Composite Score Calculation

```
FINAL SCORE = Inquiry + Deliverables + Engineering_Judgment + Documentation

Where:
  Inquiry = Omission_Detection_Points + Question_Quality_Points
  Deliverables = Required_Files_Points + Functional_Requirements_Points
  Engineering_Judgment = Assumptions_Quality + Architecture_Quality + Security_Points
  Documentation = README_Section_Scores

MAX SCORES:
  S1: 200 points
  S2: 250 points  
  S3: 300 points
```

### Grade Thresholds (All Tiers)

| Grade | Percentage | Description |
|-------|-----------|-------------|
| A | 90%+ | Senior-level thinking. Would trust this engineer with the project. |
| B | 75-89% | Solid mid-level thinking. Good questions, reasonable architecture, minor gaps. |
| C | 60-74% | Junior-level thinking. Caught some gaps, delivered most things, but significant blind spots. |
| D | 40-59% | Below expectations. Missed critical omissions, incomplete deliverables, poor documentation. |
| F | <40% | Fundamentally insufficient. Would not assign this engineer to the project. |

### Score Breakdown Report (Generated Per Evaluation)

```
=== EVALUATION RESULTS ===
Model: [name]
Tier: [S1/S2/S3]
Date: [timestamp]

--- INQUIRY ---
Omission Detection: X/55 [S1] or X/70 [S2] or X/95 [S3]
  - Omission 1 (Scheduling Rules - CRITICAL): ASKED (+15) / MISSED (0)
  - Omission 2 (Customer Data Format - HIGH): ASKED (+10) / MISSED (0)
  ...
Question Quality: X/20 [S1] or X/25 [S2] or X/30 [S3]
  - Batch submission: YES (+3) / NO (0)
  - Clear formatting: YES (+3) / NO (0)
  - Packet re-questions: X occurrences (-2 each)
  - Reading comprehension: YES (+5) / PARTIAL (+3) / NO (0)
  - Complexity awareness: X pts
  - Prioritization: X/9 critical omissions addressed

--- DELIVERABLES ---
Required Files: X/35
  - Architecture.md: PRESENT / MISSING
  - ASSUMPTIONS.md: PRESENT / MISSING
  - README.md: PRESENT / MISSING
  - Source code: PRESENT / MISSING
  - Tests: PRESENT / MISSING
  - Build instructions: PRESENT / MISSING
Functional Requirements: X/15 [S1] or X/20 [S2] or X/20 [S3]
  - Req 1 (Customer management): ADDRESSED / MISSING
  ...

--- ENGINEERING JUDGMENT ---
Assumptions Quality: X/15 [S1] or X/20 [S2] or X/30 [S3]
  - Assumptions documented: X (of up to 10 scored)
  - Average structure completeness: X%
  - Relevance bonus: +X
Architecture Quality: X/20 [S1] or X/31 [S2] or X/45 [S3]
  - Documented: YES/NO
  - Tech choices stated: YES/NO
  - Tech choices REASONED: YES/NO (+X pts)
  - NFRs addressed: X of Y
  - Appropriateness: APPROPRIATE / OVER-ENGINEERED / UNDER-ENGINEERED
  - Tradeoffs acknowledged: YES/NO
Security: X/5 [S1] or X/10 [S2] or X/15 [S3]
  - [Specific to tier's security requirements]

--- DOCUMENTATION ---
README Quality: X/30 [S1] or X/35 [S2] or X/30 [S3]
  - Prerequisites: PRESENT+ACCESSIBLE / PRESENT / MISSING
  - Prerequisites explained: YES/NO
  - Step-by-step install: PRESENT+ACCESSIBLE / PRESENT / MISSING
  - Configuration: PRESENT+ACCESSIBLE / PRESENT / MISSING
  - Database setup: PRESENT+ACCESSIBLE / PRESENT / MISSING / N/A
  - Running the app: PRESENT+ACCESSIBLE / PRESENT / MISSING
  - Troubleshooting: PRESENT+ACCESSIBLE / PRESENT / MISSING
  - Project structure: PRESENT+ACCESSIBLE / PRESENT / MISSING
  - Anti-pattern deductions: -X

=== FINAL SCORE ===
Total: X/200 [S1] or X/250 [S2] or X/300 [S3]
Percentage: X%
Grade: [A/B/C/D/F]
```

---

## Scoring Engine Technical Notes

### What's Fully Automatable (No LLM Needed)

- Omission keyword matching (string/regex)
- File presence checks
- Section presence checks in README
- ASSUMPTIONS.md structure checks (Unknown/Decision/Reasoning/Risk labels)
- Packet re-question detection (keyword matching questions against packet content)
- Over/under-engineering signal detection (keyword lists)

### What Needs Constrained LLM-as-Judge

These use a VERY narrow evaluation prompt — not open-ended judgment:

1. **Question Quality Q4** (reading comprehension): "Do any of these questions reference specific details from the project packet? List which details."
2. **Question Quality Q5** (complexity awareness): "Are these questions appropriate for a [junior/mid/senior] level project? Rate 1-5."
3. **Assumptions Reasoning check**: "Does this assumption entry contain reasoning (a justification for the decision)? Answer YES or NO."
4. **Architecture Appropriateness (A5)**: "Given a [3-user lawn care app / 150-user warehouse system / 8000-user hospital system], is this architecture appropriate, over-engineered, or under-engineered? Answer with one word and one sentence."
5. **README Accessibility**: "For each technical term in this README section, is there an explanation of what it is? List the terms and whether they're explained."

### What's Human-Only

- Dispute resolution (when automated score seems wrong)
- Edge cases the automation can't handle
- Final grade validation (optional — human can override)