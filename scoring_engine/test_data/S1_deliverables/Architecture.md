# Architecture — LawnCare Lite

## Technology Choices

I chose the following technology stack for this project:

- **Frontend:** React with TypeScript — provides a responsive, component-based UI that works well on both desktop and mobile browsers, which is a key requirement for the field technicians using phones.
- **Backend:** Node.js with Express — lightweight, well-suited for a small-scale application with 3 users. JavaScript across the full stack reduces complexity for a small team.
- **Database:** PostgreSQL — reliable relational database that handles the structured data (customers, appointments, jobs) well. Could use SQLite given the small scale, but PostgreSQL is more robust if the business grows.
- **Authentication:** JWT-based session management with bcrypt password hashing — standard, well-tested approach.

I chose a monolithic architecture because this is a 3-user application serving a small business. Microservices, message queues, or event-driven architectures would be inappropriate over-engineering for this scale. A single Express server serving a React frontend is the right level of complexity.

## Non-Functional Requirements

- **Ease of use:** The React frontend uses a clean, simple UI with large touch targets for mobile use by technicians.
- **Responsive UI:** React components are designed mobile-first using CSS flexbox.
- **Reliability:** PostgreSQL provides ACID-compliant data storage. The server runs on a standard hosting provider with automatic restarts.

## Security

- JWT authentication with bcrypt-hashed passwords
- HTTPS required for all connections
- Input validation on all API endpoints
- CORS configured for the application's domain only

## Architecture Diagram

```
React Frontend (Desktop + Mobile Browser)
        |
        | HTTPS
        |
Express.js API Server
        |
        | SQL
        |
  PostgreSQL Database
```

## Limitations and Tradeoffs

- JWT tokens do not have an expiration mechanism in this version — this should be added before production.
- No offline support for field technicians — if they lose cell signal, they cannot update job status. This could be addressed with a service worker in a future version.
- The print daily schedule feature generates a simple HTML print view rather than a PDF — this is sufficient for the use case but could be upgraded.