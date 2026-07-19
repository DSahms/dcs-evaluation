# Answer Keys — Intentional Omissions

> **This file is used by the scoring engine to evaluate clarification questions.**
> **It is NOT shown to the model being evaluated.**

---

# S1 Answer Key — LawnCare Lite

## Omission 1: Scheduling Rules
- **Topic:** How appointment scheduling actually works — duration, overlap, assignment, time windows
- **Why omitted:** Real PMs frequently write "scheduling" as if it's self-explanatory
- **Weight:** CRITICAL
- **Points:** 15
- **Thinking Category:** Business Rules
- **Keywords:** ["schedule", "long", "duration", "overlap", "overlapping", "assign", "assignment", "time window", "book", "hour", "minute", "slot", "service type", "how long", "length"]
- **Answer:** "Jobs are 30min, 1hr, or 2hr based on service type (mowing=30min, fertilization=1hr, aeration=2hr, full_package=2hr). No overlapping appointments per technician. Office manager assigns jobs to technicians manually. Customers can request preferred time slots but scheduling is done by the office — no self-service booking."

## Omission 2: Customer Data Format
- **Topic:** What's in the sample customer CSV — columns, encoding, full list vs sample
- **Why omitted:** PMs attach files and assume you'll open them
- **Weight:** HIGH
- **Points:** 10
- **Thinking Category:** Data Understanding
- **Keywords:** ["CSV", "columns", "format", "fields", "data", "encoding", "sample", "full", "records", "schema", "structure", "what's in", "contains", "headers"]
- **Answer:** "Columns: first_name, last_name, email, phone, address, city, state, zip, service_type (mowing, fertilization, aeration, full_package), frequency (weekly, biweekly, monthly), notes. UTF-8 encoding. This is the full active customer list — 47 customers."

## Omission 3: Authentication & User Accounts
- **Topic:** How user accounts are created, managed, and recovered
- **Why omitted:** "Login required" feels complete to a non-technical PM
- **Weight:** HIGH
- **Points:** 10
- **Thinking Category:** Security & User Management
- **Keywords:** ["account", "create", "register", "registration", "password", "reset", "login", "user", "sign up", "credential", "authenticate", "setup"]
- **Answer:** "Office manager creates all 3 accounts from an admin screen. No self-registration. Password reset sends an email with a temporary link valid for 24 hours. Passwords must be at least 8 characters."

## Omission 4: What "Job Completion" Means
- **Topic:** What actually happens when a job is marked complete — notes? photos? notifications? status transitions?
- **Why omitted:** PMs assume "job completion" is obvious
- **Weight:** HIGH
- **Points:** 10
- **Thinking Category:** Workflow Definition
- **Keywords:** ["complete", "completion", "status", "notes", "photo", "notify", "notification", "start", "in progress", "what happens", "workflow", "confirm", "signature"]
- **Answer:** "Technician taps 'Complete' which changes status from 'In Progress' to 'Completed' and records a timestamp. Optional notes field (max 500 chars). Optional photo upload (up to 3 photos, max 5MB each). Customer gets an automated confirmation email. Jobs cannot be marked complete unless their status is 'In Progress'."

## Omission 5: Print Daily Schedule Details
- **Topic:** What information goes on the printed daily schedule, and for whom
- **Why omitted:** "Print a schedule" sounds simple — the details of what's ON it are what matter
- **Weight:** MODERATE
- **Points:** 5
- **Thinking Category:** Deliverable Clarity
- **Keywords:** ["print", "schedule", "daily", "what", "information", "address", "direction", "route", "contain", "include", "show", "per technician", "layout"]
- **Answer:** "Office manager prints one schedule per technician. Shows: time slot, customer name, address, service type, duration, and any customer notes. No driving directions needed — techs know the area. Printed on standard letter size (8.5x11)."

## Omission 6: Cancellation / No-Show / Reschedule / Weather
- **Topic:** What happens when things don't go as planned
- **Why omitted:** PMs focus on the happy path; edge cases are what experienced engineers think about
- **Weight:** MODERATE
- **Points:** 5
- **Thinking Category:** Edge Cases
- **Keywords:** ["cancel", "cancellation", "no-show", "no show", "reschedule", "weather", "rain", "policy", "missed", "absent", "emergency", "what if", "edge", "exception", "late"]
- **Answer:** "Customers cancel or reschedule by calling the office — no self-service cancellation. Office manager updates the schedule manually. If weather prevents outdoor work, the office manager reschedules all affected jobs for the next available day and calls customers to notify them. No cancellation fees. No automated notifications."

---

# S2 Answer Key — Warehouse Inventory Manager

## Omission 1: Accounting Integration
- **Topic:** Which accounting system, what data flows, real-time vs batch, discrepancy handling
- **Why omitted:** PMs say "integrate with accounting" like it's a toggle
- **Weight:** CRITICAL
- **Points:** 15
- **Thinking Category:** Integration Architecture
- **Keywords:** ["accounting", "QuickBooks", "integrate", "sync", "real-time", "real time", "batch", "flow", "financial", "discrepancy", "which", "system", "what accounting", "data flow", "direction"]
- **Answer:** "QuickBooks Online. Inventory counts and values sync to QBO nightly via batch process. Purchase orders created in our system push to QBO immediately. If there's a discrepancy, the warehouse system is the source of truth for quantities, QBO is source of truth for financial values."

## Omission 2: Barcode Scanning Implementation
- **Topic:** What hardware, what barcode formats, what happens on scan failure
- **Why omitted:** "Barcode scanning" sounds like a feature; it's actually an entire hardware/software integration decision
- **Weight:** HIGH
- **Points:** 10
- **Thinking Category:** Hardware Integration
- **Keywords:** ["barcode", "scanner", "hardware", "scan", "mobile", "Zebra", "format", "UPC", "Code 128", "QR", "fail", "manual", "device", "handheld", "wireless", "WiFi"]
- **Answer:** "Workers use Zebra MC3300 handheld scanners (Android-based, WiFi-connected). Code 128 barcodes on existing inventory labels. If scan fails, worker can manually enter the barcode number. Scanners are on the warehouse WiFi network — no cellular needed."

## Omission 3: Inventory Tracking Method
- **Topic:** Simple quantity vs lot tracking vs FIFO vs expiration vs serial numbers vs bin locations
- **Why omitted:** To a PM, "inventory" is one thing. To an engineer, it's a dozen different tracking strategies
- **Weight:** HIGH
- **Points:** 10
- **Thinking Category:** Domain Logic
- **Keywords:** ["track", "FIFO", "LIFO", "lot", "expiration", "serial", "bin", "location", "shelf", "method", "how", "manage", "quantity", "count"]
- **Answer:** "Lot tracking with FIFO enforcement. Each lot has: lot_number, received_date, expiration_date (if applicable), quantity, bin_location. FIFO is enforced at picking time — the system automatically selects the oldest lot. No serial number tracking needed."

## Omission 4: Two-Warehouse Sync & Conflict Resolution
- **Topic:** How warehouses stay in sync, what happens to quantities during transfers, conflict handling
- **Why omitted:** Multi-location sync is one of the hardest problems and PMs routinely underestimate it
- **Weight:** CRITICAL
- **Points:** 15
- **Thinking Category:** Distributed Systems
- **Keywords:** ["sync", "real-time", "real time", "consistency", "latency", "transfer", "transit", "simultaneous", "conflict", "lock", "distributed", "VPN", "connect", "network", "duplicate", "race"]
- **Answer:** "Real-time sync via a shared database — single database server hosted in AWS, both warehouses connect over site-to-site VPN. Transfer statuses: pending → in_transit → received. While in_transit, quantity is deducted from source but NOT added to destination. Expected network latency between warehouses is under 500ms. Simultaneous operations on the same item are handled by database row locking — first operation wins, second gets an error to retry."

## Omission 5: Role Permissions Granularity
- **Topic:** What each role can actually DO — specific permissions per role
- **Why omitted:** "Role-based access" feels like a complete requirement; the granularity is what matters
- **Weight:** HIGH
- **Points:** 10
- **Thinking Category:** Security Design
- **Keywords:** ["permission", "role", "access", "approve", "create", "edit", "delete", "modify", "purchasing", "warehouse", "accounting", "granular", "who can", "allowed"]
- **Answer:** "Purchasing: create/edit/cancel POs, view inventory, request approval. Warehouse: receive shipments, adjust quantities (must provide reason), pick/pack, process transfers. Accounting: view all data, adjust financial values, approve/reject POs over $5,000. POs under $5,000 are auto-approved. No user can approve their own PO — requires a different user in a role with approval authority."

## Omission 6: Audit Log Scope & Retention
- **Topic:** What events are logged, how long, who can view, exportable?
- **Why omitted:** "Audit log" is a checkbox item for PMs
- **Weight:** MODERATE
- **Points:** 5
- **Thinking Category:** Compliance & Operations
- **Keywords:** ["audit", "log", "retain", "retention", "export", "event", "who", "access", "history", "append", "how long", "store", "keep", "view"]
- **Answer:** "Log all CRUD operations on inventory items, all transfers (create, status changes, complete), all user login/logout events, all permission changes, all quantity adjustments (with before/after values and reason). Retain logs for 7 years. Purchasing managers and accounting staff can view logs. Logs are exportable as CSV. Logs are append-only — no deletion or modification permitted."

## Omission 7: Reports Specification
- **Topic:** What specific reports, for which roles, scheduled or on-demand
- **Why omitted:** "Reports" is the vaguest requirement in software
- **Weight:** MODERATE
- **Points:** 5
- **Thinking Category:** Requirements Elicitation
- **Keywords:** ["report", "reports", "scheduled", "on-demand", "on demand", "export", "dashboard", "alert", "stock", "valuation", "what report", "which", "frequency", "automate"]
- **Answer:** "On-demand reports only for v1 (no scheduled/automated). For purchasing managers: current stock levels by warehouse, low stock alerts (configurable threshold), transfer history, receiving history. For accounting: inventory valuation report (FIFO-based), cost of goods report. All reports exportable to CSV and PDF."

---

# S3 Answer Key — Regional Hospital Information System

## Omission 1: Existing Platform & Data Migration
- **Topic:** What is the current system, what database, how much data, migration strategy
- **Why omitted:** "Replace existing system" is the most dangerous phrase in enterprise software
- **Weight:** CRITICAL
- **Points:** 20
- **Thinking Category:** Migration Architecture
- **Keywords:** ["existing", "current", "platform", "system", "migrate", "migration", "database", "schema", "data model", "history", "years", "validate", "cutover", "what platform", "what system", "source", "Oracle", "MedChart", "old", "legacy"]
- **Answer:** "Current system: MedChart v4.2, built on Delphi, Oracle 11g database. 15 years of historical data — approximately 2.3 million patient records and 18 million clinical notes. Data model documentation exists but is incomplete: we have the full database schema but approximately 12% of tables are undocumented. Migration will be phased by module (aligned with the rollout plan). Data validation will compare record counts between systems and spot-check 1% of migrated records per module against the source."

## Omission 2: Phased Rollout Plan
- **Topic:** Which modules first, timeline, parallel systems, data reconciliation during transition
- **Why omitted:** "Phased rollout" is a strategy, not a plan
- **Weight:** CRITICAL
- **Points:** 15
- **Thinking Category:** Program Management
- **Keywords:** ["phase", "rollout", "timeline", "order", "parallel", "both systems", "transition", "module", "reconciliation", "cutover", "which first", "schedule", "months", "go-live", "when"]
- **Answer:** "Phase 1 (months 1-3): Patient Registration + Scheduling at Hospital A (the flagship facility, 200 beds) only. Phase 2 (months 4-6): Clinical Notes + Pharmacy at Hospital A, Patient Registration + Scheduling at Hospital B. Phase 3 (months 7-9): Lab + Billing at Hospital A, Clinical Notes + Pharmacy at Hospital B. Phase 4 (months 10-12): All remaining hospitals and facilities. During transition, both the old and new systems run in parallel for each module. New data entered in the old system after a module has been migrated is caught by a nightly reconciliation job that syncs it into the new system."

## Omission 3: HIPAA Compliance Specifics
- **Topic:** BAA requirements, encryption standards, breach notification, de-identification
- **Why omitted:** PMs write "HIPAA compliant" as if it's a feature you toggle on
- **Weight:** CRITICAL
- **Points:** 15
- **Thinking Category:** Regulatory Compliance
- **Keywords:** ["HIPAA", "compliance", "BAA", "Business Associate", "encryption", "AES", "TLS", "breach", "notification", "de-identify", "de-identification", "PHI", "Safe Harbor", "HHS", "OCR", "regulation", "standard"]
- **Answer:** "BAA required with all vendors including cloud hosting provider, email service, and any third-party API. Encryption at rest: AES-256. Encryption in transit: TLS 1.2 or higher. All PHI access must be logged with: user ID, timestamp, patient record accessed, action performed. Breach notification follows HHS 60-day rule: the CISO has 24 hours to assess whether a breach occurred, the CMO approves any external notification. Data de-identification required for any reporting or analytics sent to external parties — use the HHS Safe Harbor method."

## Omission 4: Multi-Hospital Data Architecture
- **Topic:** Shared patients across hospitals, tenant isolation, centralized vs distributed
- **Why omitted:** Multi-tenancy is one of the first architectural decisions and PMs rarely specify it
- **Weight:** CRITICAL
- **Points:** 15
- **Thinking Category:** Architecture
- **Keywords:** ["multi", "hospital", "tenant", "shared", "unified", "centralized", "distributed", "separate", "one record", "single", "isolation", "patient population", "cross-site", "across", "data architecture", "facility"]
- **Answer:** "One unified medical record per patient across all hospitals and facilities. If a patient visits Hospital A for a procedure, then goes to Hospital B for a follow-up, the Hospital B clinician sees the complete history. Centralized database with hospital/facility-specific access controls layered on top. A clinician at Hospital A cannot see patients admitted only to Hospital B unless there is a specific care coordination reason — this requires a separate, time-limited access grant that is logged."

## Omission 5: Pharmacy & Laboratory Integrations
- **Topic:** Which external systems, what protocols (HL7/FHIR), real-time vs queued
- **Why omitted:** PMs list pharmacy and lab as features; engineers know they're integrations
- **Weight:** HIGH
- **Points:** 10
- **Thinking Category:** Integration Architecture
- **Keywords:** ["pharmacy", "lab", "laboratory", "Epic", "Sunquest", "HL7", "FHIR", "NCPDP", "e-prescribe", "integration", "external", "LIS", "protocol", "real-time", "interface", "connect", "system"]
- **Answer:** "Pharmacy: integrate with Epic Pharmacy (their existing pharmacy management system) via FHIR R4 for e-prescribing, drug interaction checking, and medication history retrieval. Laboratory: integrate with Sunquest LIS via HL7 v2.5.1 for order entry and results retrieval. Both integrations must support real-time mode (response under 3 seconds for user-facing interactions) and queued/fallback mode (if the external system is down, queue the message and retry)."

## Omission 6: Downtime, Disaster Recovery, RPO/RTO
- **Topic:** Actual availability numbers, recovery objectives, failover strategy
- **Why omitted:** PMs write "high availability" without understanding it has specific, measurable definitions
- **Weight:** HIGH
- **Points:** 10
- **Thinking Category:** Reliability Engineering
- **Keywords:** ["downtime", "DR", "disaster", "RPO", "RTO", "recovery", "failover", "availability", "99.9", "99.99", "active-active", "active-passive", "replication", "data center", "backup", "SLA"]
- **Answer:** "Target availability: 99.99% (maximum 52 minutes of unplanned downtime per year). RPO: zero — synchronous database replication between sites. RTO: 15 minutes — system must be fully operational within 15 minutes of a failure. Failover strategy: active-passive between two data centers (primary in Baltimore, DR in Richmond, approximately 200 miles apart). Failover is automated. Failback to the primary site requires manual approval from IT leadership. Full disaster recovery test is conducted quarterly."

## Omission 7: Billing & Insurance Complexity
- **Topic:** Claims processing, coding standards, prior authorizations, clearinghouse
- **Why omitted:** Billing is so complex that PMs often hand it to a separate team
- **Weight:** HIGH
- **Points:** 10
- **Thinking Category:** Domain Complexity
- **Keywords:** ["billing", "insurance", "claim", "ICD-10", "CPT", "prior authorization", "denial", "payment", "revenue", "coding", "clearinghouse", "self-pay", "charge", "remittance"]
- **Answer:** "Full revenue cycle: charge capture → coding (ICD-10 for diagnoses, CPT for procedures) → claims submission → payment posting → denial management. Integrate with Waystar clearinghouse for electronic claims submission and remittance. Self-pay patients receive paper statements. Payment plans available for balances over $500 (up to 6 months). For v1, prior authorization is a manual process (paper/fax-based) — automated electronic prior auth is planned for v2."