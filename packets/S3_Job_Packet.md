# Project Packet — Regional Hospital Information System

**Assigned:** July 2026
**Project Type:** Replacement / Migration
**Status:** Ready for Development
**Classification:** Healthcare IT — Compliance Required

---

## 1. Project Overview

Build a new patient management platform to replace the existing system used by Regional Health Partners (RHP). RHP operates multiple hospital facilities and needs a modern, compliant platform that supports clinical workflows, patient management, and regulatory requirements.

## 2. Business Context

Regional Health Partners is a healthcare network that has grown through acquisition. They currently operate multiple hospital facilities across the region, with a combined patient base spanning several million records accumulated over 15+ years of operation.

The existing patient management platform is end-of-life. The vendor has announced it will no longer receive security updates after next year. RHP leadership has approved a replacement project with a phased rollout plan to minimize disruption to clinical operations.

This is a high-stakes project. System downtime directly impacts patient care. Data integrity errors could result in regulatory violations, fines, or patient harm. The new system must meet or exceed all current compliance requirements.

## 3. Users

Approximately 8,000 users across multiple hospital facilities, including:

- **Clinical staff** — physicians, nurses, medical assistants
- **Administrative staff** — registration, scheduling, billing
- **Pharmacy staff** — pharmacists, pharmacy technicians
- **Laboratory staff** — lab technicians, pathologists
- **IT staff** — system administration, support
- **Management** — department heads, compliance officers, executives

## 4. Functional Requirements

### 4.1 Patient Registration
- Register new patients
- Maintain patient demographic and contact information
- Search for existing patients

### 4.2 Scheduling
- Schedule patient appointments
- Manage provider schedules
- Handle appointment conflicts and waitlists

### 4.3 Clinical Notes
- Create and manage clinical documentation
- Support clinical workflows

### 4.4 Pharmacy
- Manage pharmacy operations
- Support medication-related workflows

### 4.5 Laboratory
- Manage laboratory orders and results
- Support laboratory workflows

### 4.6 Billing
- Manage patient billing
- Support insurance and claims processing

### 4.7 Auditing
- Comprehensive audit trail of system activity

## 5. Non-Functional Requirements

- **Availability:** 24x7 availability required. System downtime impacts patient care.
- **Reliability:** High reliability. Data loss or corruption is unacceptable in a healthcare setting.
- **Scalability:** Must support 8,000+ concurrent users across multiple facilities with acceptable performance.

## 6. Technical Constraints

- Migration from existing platform with phased rollout
- Must integrate with existing pharmacy and laboratory systems

## 7. Security

- Enterprise identity management
- Encryption of sensitive data
- Comprehensive auditing
- Healthcare regulatory compliance (HIPAA)

## 8. Deliverables

- Architecture documentation
- Source code
- Tests
- Deployment guide
- Operations guide
- ASSUMPTIONS.md documenting any assumptions made
- Build instructions

## 9. Business Operations

Regional Health Partners has grown through acquisition. Each hospital that joined the network had its own existing IT infrastructure, identity systems, and vendor contracts. While RHP leadership wants a unified platform long-term, they have been explicit with the IT team: minimize disruption to existing operational patterns during this migration. If a hospital's pharmacy system works fine with its current integration method, don't replace the integration method just to standardize on a newer protocol.

The identity management situation is particularly fragmented. Hospital A uses Microsoft Active Directory. Hospital B uses Okta. Hospital C still uses a local LDAP server that their previous IT director set up. The CIO has mentioned wanting to move everyone to a single identity provider eventually, but for this project, the priority is getting the new patient management system live — identity unification is a separate initiative.

## 10. Provided Assets

- Wireframes for core screens (files: wireframe-registration.png, wireframe-schedule.png, wireframe-clinical.png, wireframe-billing.png)
- Interface specifications for existing pharmacy system (file: pharmacy-interface-spec.pdf)
- Interface specifications for existing laboratory system (file: lab-interface-spec.pdf)
- Sample datasets (files: sample-patients.csv, sample-orders.csv)

## 11. Clarification

You have **one round** of clarification questions. Submit all questions together. After receiving answers, requirements are frozen.