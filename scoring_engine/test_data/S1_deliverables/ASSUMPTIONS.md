# ASSUMPTIONS.md

## Assumption 1: Database Technology

- **Unknown:** Which database technology to use
- **Decision:** PostgreSQL 15
- **Reasoning:** The packet does not specify a database. PostgreSQL is a reliable, free, relational database that fits the structured data needs (customers, appointments, jobs) and is well-supported. SQLite was considered but PostgreSQL is more robust for concurrent access even with only 3 users.
- **Risk:** PostgreSQL may be overkill for a 3-person company. It requires a running server whereas SQLite would be file-based and simpler to set up.

## Assumption 2: Service Types

- **Unknown:** What specific lawn care services are offered
- **Decision:** The service types from the CSV will be used: mowing, fertilization, aeration, full_package
- **Reasoning:** The sample CSV contains a service_type column with these values. This is the most authoritative source available.
- **Risk:** The company may offer additional services not in the current customer list.

## Assumption 3: Email Service for Notifications

- **Unknown:** How to send emails (confirmation emails, password resets)
- **Decision:** Use a transactional email service (SendGrid or similar)
- **Reasoning:** The application needs to send emails for job completion confirmations and password resets. A transactional email API is the standard approach for this.
- **Risk:** Adds a third-party dependency. If the email service is down, notifications will fail.

## Assumption 4: Photo Storage

- **Unknown:** Where to store uploaded job completion photos
- **Decision:** Local filesystem storage with a configurable upload directory
- **Reasoning:** For 3 users and a small volume of photos (up to 3 per job), local storage is simple and sufficient. Cloud storage (S3) would add complexity and cost.
- **Risk:** Local storage does not scale well if the business grows significantly or needs to serve photos to external users.

## Assumption 5: Cancellation Workflow

- **Unknown:** Whether customers can cancel through the application or only by phone
- **Decision:** Cancellations are handled by phone call to the office only
- **Reasoning:** The application is for the office manager and technicians. There is no customer-facing portal mentioned in the requirements.
- **Risk:** If the company later wants customer self-service, this will need to be redesigned.

## Assumption 6: Error Handling Strategy

- **Unknown:** How the application should handle errors (network failures, concurrent edits, invalid data)
- **Decision:** Graceful error messages displayed to the user, with server-side logging for debugging. Optimistic concurrency control for simultaneous edits.
- **Reasoning:** Users are not highly technical per the requirements. Errors should be understandable. Server-side logging helps the developer diagnose issues.
- **Risk:** Optimistic concurrency could lead to data conflicts if two users edit the same record.