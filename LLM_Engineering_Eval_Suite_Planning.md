# LLM Engineering Evaluation Suite — Planning Session

**Status:** Build Phase v2
**Date:** 2026-07-09

---

## What This Is

A **3-tier evaluation suite** that tests LLMs as if they were software engineers receiving a real work ticket from a PM. Not a benchmark — a **suite of tests**.

Every model gets the same packet, the same rules, one round of clarification questions, then must deliver. The packets are **intentionally incomplete** — smart engineers (and smart models) should spot the gaps and ask about them.

---

## Core Philosophy

### Baking vs. Cooking

Software has objective truths (baking/chemistry) and subjective preferences (cooking/art). **We only score the baking.**

**"Baking" — Objective, Scorable:**
- Security requirements met (SQL injection prevention, encryption, audit logging)
- Data integrity (input validation, error handling)
- Completeness (all functional requirements addressed, all deliverables present)
- Appropriate complexity (no over-engineering a 3-user app, no under-engineering an 8000-user hospital system)
- Assumptions documented with Unknown/Decision/Reasoning/Risk

**"Cooking" — NOT Scored:**
- Framework choice (React vs. Vue vs. Svelte)
- Language choice (TypeScript, Python, Go)
- Naming conventions
- File/folder organization
- Specific architectural pattern (MVC, Clean Architecture, etc.) — UNLESS it objectively fails requirements

### The Neutrality Principle

1. **Score outcomes, not implementations** — "does the system handle concurrency?" not "did they use proper dependency injection?"
2. **Intentional omissions are about DOMAIN needs, not technology choices** — "What data format are we migrating from?" not "Should I use REST or GraphQL?"
3. **The answer key is written by the human evaluator, not by any LLM** — eliminates model bias
4. **Pre-define what "good questions" look like BEFORE any LLM runs**

### The Efficiency Problem (South Jersey Driving Analogy)

Two routes both work. Both get you there. One is less efficient.

**Solution:** Don't score which route they took. Score whether they CONSIDERED the route.

- NOT scored: "They used 200 lines when 100 would suffice"
- SCORED: "Did they justify their approach in Architecture.md?"
- NOT scored: "They chose Redux when state was simple"
- SCORED: "Did they consider alternatives and explain their choice?"

**Architecture.md is the thinking differentiator.** A strong model writes: "I considered X, Y, and Z. I chose X because [requirements-specific reason]. The tradeoff is [acknowledged risk]."

### One-Shot Enforcement

1. One clarification round only — can't iteratively refine understanding
2. Requirements freeze after answers — no going back
3. Single deliverable submission — no revisions
4. Architecture.md requirement forces thinking BEFORE coding

---

## The Three Tiers

| Tier | Project | Users | Complexity | Maps To |
|------|---------|-------|-----------|---------|
| **S1** | LawnCare Lite | 3 users (1 office manager, 2 field techs) | Simple CRUD web app | Junior Developer |
| **S2** | Warehouse Inventory Manager | 150 users (purchasing, warehouse, accounting) | RBAC, integrations, multi-location | Mid-Level Developer |
| **S3** | Regional Hospital Information System | ~8,000 users, multiple hospitals | HIPAA, migration, enterprise integrations | Enterprise Architect |

---

## Scoring Framework

### Three Scoring Categories

**1. Inquiry Score (Process — "Did they think before they built?")**
- Identified intentional omissions? (Keyword match against answer key — automated)
- Questions were well-formed and relevant? (Human judgment — narrow scope)
- Didn't ask questions already answered in the packet? (Checklist — automated)

**2. Deliverable Completeness (Outcome — "Did they ship everything?")**
- All required files present? (Checklist)
- All functional requirements addressed? (Checklist)
- Non-functional requirements addressed? (Checklist)

**3. Engineering Judgment (Outcome — "Was the thinking sound?")**
- Assumptions documented with Unknown/Decision/Reasoning/Risk? (Structure check)
- Architecture appropriate to complexity level? (Objective fit assessment)
- Security requirements met per stated security section? (Checklist)
- Architecture.md explains WHY decisions were made? (Presence check)

**Explicitly NOT Scored:**
- Code style, framework choice, language choice, naming conventions, specific patterns (unless they objectively fail requirements)

### Documentation Scoring — "Explain It To My Mom" Standard

A non-technical person should get from "I have a computer" to "the app is running" using only the README. Every gap is a measurable failure.

**Required README Sections (each scored as present/absent):**

| Section | Must Contain |
|---------|-------------|
| **Prerequisites** | Every single thing needed BEFORE starting, with version numbers and download links |
| **What Each Prerequisite IS** | One sentence explaining what the tool is in plain English |
| **Step-by-step Installation** | Every command, in order, with explanation of what each command does |
| **Configuration** | Every config file, every environment variable, what it does, what to set it to, example values |
| **Database Setup** | How to create it, run migrations, seed data |
| **Running the App** | Exact command, what you should see when it works, what port |
| **Troubleshooting** | At minimum 3-5 common problems and how to fix them |
| **Project Structure** | What each major folder/file does in plain English |

**Accessibility check:** For every technical term or command, is there a brief explanation of what it is or what it does? (Automatable)

---

## Intentional Omissions — The DNA of the System

### How Omission Scoring Works

Each omission in the answer key has:
- **Topic** — what's missing
- **Why omitted** — realistic PM behavior
- **Expected question keywords** — for automated matching
- **Answer** — what to tell the model if they ask
- **Points** — how much it's worth
- **Weight** — CRITICAL / HIGH / MODERATE
- **Thinking category** — what pattern it tests

**Matching rules:**
- Question matches an omission's keywords → **points awarded**
- Reasonable question not in key → **neutral (no penalty, no bonus)**
- Question reveals they didn't read the packet → **small deduction**
- Question about technology preference → **neutral, answer is "your choice"**

### S1 Omissions — LawnCare Lite (Junior Level)

**Total omission points: 85** (v1: 55, +30 from v2 operational traps)

Tests: basic requirements gathering, common-sense business thinking, attention to detail, AND whether the model thinks like a business person not just a coder.

| # | Topic | Points | Weight | Thinking Category | Type |
|---|-------|--------|--------|-------------------|------|
| 1 | Scheduling Rules — job duration, overlap, assignment, time windows | 15 | CRITICAL | Business Rules | Original |
| 2 | Customer Data Format — CSV columns, encoding, full vs sample | 10 | HIGH | Data Understanding | Original |
| 3 | Authentication & User Accounts — account creation, password reset | 10 | HIGH | Security & User Management | Original |
| 4 | What "Job Completion" Means — status only? Notes? Photos? Notifications? | 10 | HIGH | Workflow Definition | Original |
| 5 | Print Daily Schedule — what's on it? For whom? | 5 | MODERATE | Deliverable Clarity | Original |
| 6 | Cancellation / No-Show / Reschedule / Weather | 5 | MODERATE | Edge Cases | Original |
| 7 | Customer Data Ownership & Portability — who owns the list if sold? | 10 | HIGH | Business Continuity | **Operational Trap** |
| 8 | Technician Schedule Visibility — can they see each other's work? | 10 | HIGH | Operational Privacy | **Operational Trap** |
| 9 | Daily Capacity Limits — max jobs per tech per day? | 10 | HIGH | Operational Reality | **Operational Trap** |

**S1 Answer Key:**

**Omission 1 — Scheduling Rules:**
- Keywords: ["schedule", "long", "duration", "overlap", "assign", "time window", "book", "hour", "minute", "slot"]
- Answer: "Jobs are 30min, 1hr, or 2hr based on service type. No overlapping per technician. Office manager assigns manually. Customers can request preferred time slots but scheduling is done by the office."

**Omission 2 — Customer Data Format:**
- Keywords: ["CSV", "columns", "format", "fields", "data", "encoding", "sample", "full", "records"]
- Answer: "Columns: first_name, last_name, email, phone, address, city, state, zip, service_type (mowing, fertilization, aeration, full_package), frequency (weekly, biweekly, monthly), notes. UTF-8. This is the full active customer list — 47 customers."

**Omission 3 — Authentication & User Accounts:**
- Keywords: ["account", "create", "register", "password", "reset", "login", "user", "sign up"]
- Answer: "Office manager creates all accounts. No self-registration. Password reset sends an email with a temporary link valid for 24 hours."

**Omission 4 — Job Completion:**
- Keywords: ["complete", "completion", "status", "notes", "photo", "notify", "notification", "start", "in progress"]
- Answer: "Technician taps 'Complete' which changes status and records timestamp. Optional notes field (max 500 chars). Optional photo upload (up to 3). Customer gets a confirmation email. Jobs cannot be completed unless status is 'In Progress'."

**Omission 5 — Print Daily Schedule:**
- Keywords: ["print", "schedule", "daily", "what", "information", "address", "direction", "route"]
- Answer: "Office manager prints one schedule per technician. Shows: time, customer name, address, service type, duration, and any notes. No driving directions needed — techs know the area."

**Omission 6 — Cancellation/No-Show/Reschedule:**
- Keywords: ["cancel", "no-show", "reschedule", "weather", "rain", "policy", "missed", "absent"]
- Answer: "Customer can cancel or reschedule by calling the office. No automated cancellation. If weather prevents work, office manager reschedules all affected jobs and notifies customers. No cancellation fees."

---

### S2 Omissions — Warehouse Inventory Manager (Mid Level)

**Total omission points: 90** (v1: 70, +20 from v2 operational traps)

Tests: system design thinking, integration awareness, concurrency, multi-stakeholder consideration, AND whether the model understands that software exists in a messy real-world operational context.

| # | Topic | Points | Weight | Thinking Category | Type |
|---|-------|--------|--------|-------------------|------|
| 1 | Accounting Integration — which system? Data flow? Real-time or batch? | 15 | CRITICAL | Integration Architecture | Original |
| 2 | Barcode Scanning — hardware? Formats? Fallback? | 10 | HIGH | Hardware Integration | Original |
| 3 | Inventory Tracking Method — FIFO? Lot tracking? Expiration? Bin locations? | 10 | HIGH | Domain Logic | Original |
| 4 | Two-Warehouse Sync & Conflict Resolution — consistency model, in-transit, locking | 15 | CRITICAL | Distributed Systems | Original |
| 5 | Role Permissions Granularity — what can each role DO? | 10 | HIGH | Security Design | Original |
| 6 | Audit Log Scope & Retention — what events? How long? Who sees it? | 5 | MODERATE | Compliance & Operations | Original |
| 7 | Reports — what reports? For whom? Scheduled or on-demand? | 5 | MODERATE | Requirements Elicitation | Original |
| 8 | Shared Credentials & Account Security — stop the "log in as them" problem | 10 | HIGH | Operational Realities | **Operational Trap** |
| 9 | Approval Workflow Reality — Tom's text approvals vs. system workflow | 10 | HIGH | Change Management | **Operational Trap** |

**S2 Answer Key:**

**Omission 1 — Accounting Integration:**
- Keywords: ["accounting", "QuickBooks", "integrate", "sync", "real-time", "batch", "flow", "financial", "discrepancy"]
- Answer: "QuickBooks Online. Inventory counts and values sync to QBO nightly (batch). Purchase orders created in our system push to QBO. If there's a discrepancy, the warehouse system is the source of truth for quantities, QBO is source of truth for financial values."

**Omission 2 — Barcode Scanning:**
- Keywords: ["barcode", "scanner", "hardware", "scan", "mobile", "Zebra", "format", "UPC", "Code 128", "QR", "fail", "manual"]
- Answer: "Workers will use Zebra MC3300 handheld scanners (Android-based, WiFi). Code 128 barcodes on existing inventory labels. If scan fails, worker can manually enter the barcode number. All scanners are on the warehouse WiFi network."

**Omission 3 — Inventory Tracking Method:**
- Keywords: ["track", "FIFO", "LIFO", "lot", "expiration", "serial", "bin", "location", "shelf", "method"]
- Answer: "Lot tracking with FIFO. Each lot has: lot_number, received_date, expiration_date (if applicable), quantity, bin_location. FIFO is enforced at picking time — oldest lot picked first. No serial number tracking needed."

**Omission 4 — Two-Warehouse Sync:**
- Keywords: ["sync", "real-time", "consistency", "latency", "transfer", "transit", "simultaneous", "conflict", "lock", "distributed", "VPN"]
- Answer: "Real-time sync via a shared database (single database server, both warehouses connect over VPN). Transfer status: pending → in_transit → received. While in_transit, quantity is deducted from source but not added to destination. Expected latency between warehouses is under 500ms. Simultaneous transfers are handled by database row locking — first one wins, second gets an error to retry."

**Omission 5 — Role Permissions:**
- Keywords: ["permission", "role", "access", "approve", "create", "edit", "delete", "modify", "purchasing", "warehouse", "accounting", "granular"]
- Answer: "Purchasing: create/edit/cancel POs, view inventory, request approval. Warehouse: receive shipments, adjust quantities (with reason), pick/pack, transfer. Accounting: view all, adjust financial values, approve/reject POs over $5,000. POs under $5,000 are auto-approved. No one can approve their own PO."

**Omission 6 — Audit Log:**
- Keywords: ["audit", "log", "retain", "export", "event", "who", "access", "history", "append"]
- Answer: "Log: all CRUD operations on inventory, all transfers, all user login/logout, all permission changes, all quantity adjustments (with before/after values). Retain for 7 years. Purchasing managers and accounting can view. Exportable as CSV. Append-only — no deletion or modification."

**Omission 7 — Reports:**
- Keywords: ["report", "reports", "scheduled", "on-demand", "export", "dashboard", "alert", "stock", "valuation"]
- Answer: "On-demand reports for purchasing managers: current stock levels, low stock alerts, transfer history, receiving history. For accounting: inventory valuation report, cost of goods report. All exportable to CSV and PDF. No scheduled/automated reports for v1."

---

### S3 Omissions — Regional Hospital Information System (Enterprise Level)

**Total omission points: 110** (v1: 95, +15 from v2 training data traps)

Tests: architectural thinking, compliance awareness, migration strategy, enterprise-scale consideration, AND whether the model can resist its training data bias when the packet says otherwise.

| # | Topic | Points | Weight | Thinking Category | Type |
|---|-------|--------|--------|-------------------|------|
| 1 | Existing Platform & Data Migration — what system? Schema? 15 years of data? | 20 | CRITICAL | Migration Architecture | Original |
| 2 | Phased Rollout Plan — which modules first? Parallel systems? Data reconciliation? | 15 | CRITICAL | Program Management | Original |
| 3 | HIPAA Compliance Specifics — BAA? Encryption standards? Breach protocol? | 15 | CRITICAL | Regulatory Compliance | Original |
| 4 | Multi-Hospital Data Architecture — shared patients? Tenant isolation? One record or many? | 15 | CRITICAL | Architecture | Original |
| 5 | Pharmacy & Lab Integrations — HL7 vs FHIR? Follow existing or standardize? | 10 | HIGH | Integration Architecture | **Training Data Trap** |
| 6 | Downtime, DR, RPO/RTO — actual numbers? Failover strategy? | 10 | HIGH | Reliability Engineering | Original |
| 7 | Billing & Insurance — claims? ICD-10? Prior auth? Clearinghouse? | 10 | HIGH | Domain Complexity | Original |
| 8 | Identity Provider Fragmentation — unified SSO or pluggable auth? | 15 | CRITICAL | Scope Discipline | **Training Data Trap** |

**S3 Answer Key:**

**Omission 1 — Existing Platform & Migration:**
- Keywords: ["existing", "current", "platform", "system", "migrate", "migration", "database", "schema", "data model", "history", "years", "validate", "cutover"]
- Answer: "Current system: MedChart v4.2, built on Delphi, Oracle 11g database. 15 years of historical data, approximately 2.3 million patient records, 18 million clinical notes. Data model documentation exists but is incomplete — we have the schema but some tables are undocumented. Migration will be phased by module (see rollout plan). Data validation will compare record counts and spot-check 1% of migrated records per module."

**Omission 2 — Phased Rollout:**
- Keywords: ["phase", "rollout", "timeline", "order", "parallel", "both systems", "transition", "module", "reconciliation", "cutover"]
- Answer: "Phase 1 (months 1-3): Patient Registration + Scheduling at Hospital A only. Phase 2 (months 4-6): Clinical Notes + Pharmacy at Hospital A, Patient Registration + Scheduling at Hospital B. Phase 3 (months 7-9): Lab + Billing at Hospital A, Clinical Notes + Pharmacy at Hospital B. Phase 4 (months 10-12): All remaining hospitals. During transition, both systems run in parallel. New data entered in old system after module migration is caught by a nightly reconciliation job."

**Omission 3 — HIPAA Compliance:**
- Keywords: ["HIPAA", "compliance", "BAA", "Business Associate", "encryption", "AES", "TLS", "breach", "notification", "de-identify", "de-identification", "PHI", "Safe Harbor"]
- Answer: "BAA required with all vendors (cloud hosting, email service, any third-party API). Encryption: AES-256 at rest, TLS 1.2+ in transit. All PHI access logged with user, timestamp, patient, and action. Breach notification: follow HHS 60-day rule — CISO has 24 hours to assess, CMO approves notification. De-identification needed for any reporting sent to external parties (use Safe Harbor method)."

**Omission 4 — Multi-Hospital Architecture:**
- Keywords: ["multi", "hospital", "tenant", "shared", "unified", "centralized", "distributed", "separate", "one record", "single", "isolation", "patient population"]
- Answer: "One unified medical record per patient across all hospitals. Patient visits Hospital A for a procedure, then goes to Hospital B for follow-up — Hospital B clinician sees the full history. Centralized database with hospital-specific access controls. A clinician at Hospital A cannot see patients admitted only to Hospital B unless there's a specific care coordination reason (requires separate access grant)."

**Omission 5 — Pharmacy & Lab Integrations:**
- Keywords: ["pharmacy", "lab", "laboratory", "Epic", "Sunquest", "HL7", "FHIR", "NCPDP", "e-prescribe", "integration", "external", "LIS", "protocol", "real-time"]
- Answer: "Pharmacy: integrate with Epic Pharmacy (their existing system) via FHIR R4 for e-prescribing, drug interaction checking, and medication history. Lab: integrate with Sunquest LIS via HL7 v2.5.1 for order entry and results retrieval. Both integrations must support real-time (under 3 seconds) and queued/fallback modes."

**Omission 6 — Downtime/DR/RPO/RTO:**
- Keywords: ["downtime", "DR", "disaster", "RPO", "RTO", "recovery", "failover", "availability", "99.9", "99.99", "active-active", "active-passive", "replication", "data center"]
- Answer: "Target: 99.99% uptime. RPO: zero (synchronous replication). RTO: 15 minutes. Active-passive failover between two data centers (primary in City A, DR in City B, 200 miles apart). Automated failover with manual approval for failback. Full DR test quarterly."

**Omission 7 — Billing & Insurance:**
- Keywords: ["billing", "insurance", "claim", "ICD-10", "CPT", "prior authorization", "denial", "payment", "revenue", "coding", "clearinghouse", "self-pay"]
- Answer: "Full revenue cycle: charge capture → coding (ICD-10, CPT) → claims submission → payment posting → denial management. Integrate with Waystar clearinghouse for claims. Self-pay patients get paper statements. Payment plans: up to 6 months for balances over $500. For v1, prior authorization is manual (paper/fax) — automated prior auth is v2."

---

## Point Distribution Summary

| Tier | Critical (15-20pts) | High (10pts) | Moderate (5pts) | Total Omission Points | Max Score |
|------|---------------------|--------------|-----------------|----------------------|-----------|
| **S1** | 1 (15pts) | 6 (60pts) | 2 (10pts) | **85** | **230** |
| **S2** | 2 (30pts) | 5 (50pts) | 2 (10pts) | **90** | **270** |
| **S3** | 5 (80pts) | 3 (30pts) | 0 | **110** | **315** |

Point scaling reflects difficulty: S1 omissions are easier to spot (lower total), S3 omissions require deep architectural thinking (higher total).

v2 changes added operational traps (S1/S2) and training data traps (S3) to address the training data bias finding — see "Key Finding: Training Data Bias" section below.

---

## Automation Architecture

### How The Full Evaluation Runs

```
STEP 1: Model receives Job Packet + Phase 1 Evaluation Prompt
STEP 2: Model submits clarification questions
STEP 3: Auto-scoring engine compares questions against Answer Key
        - Keyword match on intentional omissions → points awarded
        - Missed critical omission → points deducted
        - Reasonable question not in key → neutral
        - Question already answered in packet → small deduction
STEP 4: Answers from key are returned to model
STEP 5: Model submits deliverables (single submission, no revisions)
STEP 6: Auto-scoring engine checks deliverables:
        - All required files present? (checklist)
        - All functional requirements addressed? (checklist)
        - ASSUMPTIONS.md format correct? (structure check)
        - README documentation completeness? (checklist + accessibility)
        - Architecture.md explains reasoning? (presence check)
        - Over/under-engineering signals? (heuristic checks)
        - Security requirements met? (checklist per tier)
STEP 7: Composite score generated
        - Human ONLY steps in for disputes or edge cases
```

**Human is the appeals court, not the judge.**

---

## Phase 1 Evaluation Prompt (Common to All Tiers)

```
You are acting as a professional software engineer responding to a
real-world project assignment.

You have received a Project Packet. Treat it as if it came from a
project manager.

## Rules

1. Read the entire packet before responding.
2. You may ask **one round** of clarification questions.
3. Submit all clarification questions together.
4. After receiving answers, requirements are frozen.
5. If information remains unknown, document assumptions in ASSUMPTIONS.md.
6. Every assumption must include:
   - Unknown
   - Decision
   - Reasoning
   - Risk
7. Choose architectures, frameworks and technologies using sound
   engineering judgment unless constrained.
8. Deliver:
   - Architecture.md
   - ASSUMPTIONS.md
   - README.md
   - Source code
   - Tests
   - Build instructions
   - Any required configuration
```

---

## Randomization Strategy (v2 Plan)

For v1: Build 3 solid tiers. The omissions themselves provide randomization because no model has seen YOUR specific packet.

For v2: Create domain variants per tier — same complexity, same omission TYPES, different domain skins:
- S1 variants: lawn care, bakery ordering, pet grooming, tutoring scheduler, personal trainer bookings
- S2 variants: warehouse inventory, retail POS, fleet management, event venue management
- S3 variants: hospital system, banking platform, government services portal, university student system

The thinking patterns being tested remain identical across variants. Only the domain context changes.

---

## Key Finding: Training Data Bias (2026-07-09)

**Discovery:** During initial testing with Gemini, we observed that it performed BETTER on S3 (enterprise hospital, 8,000 users, HIPAA, migration) than on S1 (simple lawn care app, 3 users). This was counterintuitive — S1 should be the easy one.

**Root Cause:** LLMs are trained on vastly more enterprise software content than small-business operational content. GitHub, Stack Overflow, and tech blogs have thousands of articles about HIPAA compliance, FHIR integrations, and enterprise architecture. They have almost nothing about whether a lawn care technician should be able to see their coworker's schedule, or how many lawns you can mow in a day.

**Implication:** Our v1 omissions were inadvertently biased toward the kind of technical questions that appear in LLM training data. S1's omissions (scheduling rules, CSV format, auth, job completion) are all standard software engineering questions. An LLM can pattern-match them from training data without actually "thinking like a business person."

**The Fix (v2 — Implemented):**

Two new omission types designed to test what training data CAN'T teach:

### 1. Operational Traps (S1 and S2)

Questions that require small-business common sense, not technical knowledge. These test whether the model thinks like a business person, not just a coder.

**Design principles:**
- The packet includes a "Business Operations" section with realistic human details (names, relationships, existing bad habits)
- The hints are EMBEDDED in the narrative, not stated as requirements
- A coder reads the section and moves on. A business thinker spots the implications.
- The correct question is about PEOPLE and PROCESS, not technology

**S1 Operational Traps (3 new, +30 pts):**
- Data ownership — "Who owns the customer list if Maria sells?" (business continuity thinking)
- Technician visibility — "Can Jake see Sam's schedule?" (operational privacy, human dynamics)
- Daily capacity — "Is there a max number of jobs per tech?" (real-world service business experience)

**S2 Operational Traps (2 new, +20 pts):**
- Shared credentials — "The packet says workers share logins, HR wants it stopped — how?" (change management, not just auth)
- Approval reality — "Tom approves POs by text — force everything through the system or accommodate reality?" (the #1 reason business software fails: building perfect workflows nobody follows)

### 2. Training Data Traps (S3)

Questions where a well-read LLM will confidently answer from training data patterns but get it WRONG because this specific project is different. The packet explicitly contains contradictory information, and the model must notice.

**Design principles:**
- The packet includes a "Business Operations" section that EXPLICITLY states a non-standard approach
- LLM training data says "do X" — the packet says "we're doing Y instead"
- A model that asks about it demonstrates reading comprehension + resistance to bias
- A model that doesn't ask will confidently build the wrong thing in Architecture.md

**S3 Training Data Traps (2, one modifies existing + one new, +15 pts net):**
- FHIR trap — "Every healthcare article says use FHIR. The packet says don't replace existing integration methods. Pharmacy at Hospital A uses HL7 v2.5.1, not FHIR. The model that assumes FHIR failed to read the business context." (modified existing Omission 5)
- SSO trap — "Every enterprise article says use unified SSO. The packet lists three different identity providers and says unification is a separate project. The model that designs a single IdP scored well on training data but failed on scope discipline." (new Omission 8, 15 pts)

**Why This Matters:**

These traps directly address the bias we discovered. If an LLM scores high on S1/S2 in v2, it's not because it pattern-matched technical omissions from training data — it's because it demonstrated actual business thinking. And if an LLM scores high on S3 in v2, it's not because it regurgitated healthcare IT best practices — it's because it actually read the packet and noticed where this project DEVIATES from best practices.

This is the difference between testing knowledge and testing judgment.

---

## Next Steps — Build Phase

- [x] Finalize omissions
- [x] Build complete scoring rubric (inquiry + deliverables + engineering judgment + documentation)
  - Saved to: `LLM_Engineering_Eval_Suite_Scoring_Rubric.md`
- [x] Write full S1 job packet (with omissions baked in — they look like normal incomplete PM packets)
- [x] Write full S2 job packet
- [x] Write full S3 job packet
  - Packets saved to: `packets/S1_Job_Packet.md`, `packets/S2_Job_Packet.md`, `packets/S3_Job_Packet.md`
  - Phase 1 prompt: `packets/Phase1_Evaluation_Prompt.md`
  - Answer keys: `packets/S1_Answer_Key.md`, `packets/S2_Answer_Key.md`, `packets/S3_Answer_Key.md`
- [x] Build the automated scoring engine
  - Engine: `scoring_engine/scoring_engine.py`
  - Tier configs: `scoring_engine/configs/S1.json`, `S2.json`, `S3.json`
  - Tested with both good and bad question sets — scoring differentiates correctly
  - Features: negation detection (rejecting over-engineering ≠ using it), keyword matching, accessibility scoring, anti-pattern deductions
  - CLI: `python scoring_engine.py --tier S1 --questions questions.txt --deliverables dir/ --packet packet.md`
- [x] v2: Add operational traps to S1 (+3 omissions) and S2 (+2 omissions)
- [x] v2: Add training data traps to S3 (modify Omission 5 + new Omission 8)
- [x] v2: Add "Business Operations" sections to all three packets
- [x] v2: Update scoring configs and point distributions
- [x] v2: Document training data bias finding and v2 design rationale
- [x] v2: Fix keyword matching false positives — 3-layer matching system
  - Problem: bare substring matching gave S2 Omission 5 (Role Permissions) full credit when "warehouse" and "accounting" appeared in unrelated sentences about barcodes and sync. Worth 10/90 points (~10%) for a topic the model never engaged with.
  - Fix: 3-layer matching for HIGH/CRITICAL omissions:
    1. **Strong signals** — topic-specific phrases (FIFO, BAA, RPO, "who can") where a single match anywhere = ASKED
    2. **Proximity clustering** — 2+ keywords within 250 chars of each other = ASKED (prevents scattered incidental matches)
    3. **Noise filter** — clusters where ALL keywords are generic domain words (warehouse, accounting, patient, schedule) are rejected. At least one specific keyword required.
  - MODERATE omissions (5 pts): keep single-keyword matching (acceptable false-positive cost)
  - Added `strong_signals` to every HIGH/CRITICAL omission and `generic_domain_words` to every tier config
  - Also caught and fixed: "customer list" strong signal on S1 O7 was triggering from a CSV format question; "shared" in S2 O4 keywords conflicted with S2 O8 strong signal; "approve" in S2 O9 keywords conflicted with S2 O5 strong signal
- [ ] Test v2 against multiple LLMs (inquiry round comparison)