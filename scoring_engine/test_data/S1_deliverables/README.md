# LawnCare Lite — README

## Prerequisites

Before you begin, you need the following installed on your computer:

- **Node.js (version 18 or higher)** — a JavaScript runtime that allows you to run the server code. Download it from [nodejs.org](https://nodejs.org).
- **PostgreSQL (version 14 or higher)** — a database system that stores all the application's data (customers, appointments, etc.). Download from [postgresql.org](https://www.postgresql.org/download/).
- **npm** — a package manager that comes automatically with Node.js. It downloads the extra code libraries this project needs.

## What Each Tool Does

- **Node.js** — runs the backend server. Think of it as the engine that powers the application.
- **PostgreSQL** — stores your data permanently. Without it, all customer info and schedules would be lost when the server restarts.
- **npm** — downloads and manages code packages (libraries) that the project depends on. Similar to an app store but for code.

## Installation

1. **Clone the repository** — copy this project to your computer by opening your terminal (Command Prompt on Windows, Terminal on Mac) and running:
   ```
   git clone https://github.com/example/lawncare-lite.git
   cd lawncare-lite
   ```
   This downloads all the project files to your computer and enters the project folder.

2. **Install dependencies** — download all the required code libraries:
   ```
   npm install
   ```
   This command reads the `package.json` file and downloads everything the project needs. It may take a minute or two.

3. **Set up the database** — create the database and tables:
   ```
   createdb lawncare
   npm run migrate
   npm run seed
   ```
   - `createdb lawncare` creates an empty database called "lawncare" (this is a PostgreSQL command)
   - `npm run migrate` creates the required tables (customers, appointments, jobs, etc.)
   - `npm run seed` inserts the sample customer data from the CSV file

## Configuration

The application uses environment variables for configuration. Create a file called `.env` in the project root:

```
PORT=3000
DATABASE_URL=postgresql://localhost:5432/lawncare
JWT_SECRET=your-secret-key-here
EMAIL_API_KEY=your-sendgrid-key-here
```

- **PORT** — the port number the server listens on. 3000 is the default. You can change it if something else is already using port 3000.
- **DATABASE_URL** — tells the app how to connect to your PostgreSQL database. "localhost" means your own computer, 5432 is PostgreSQL's default port.
- **JWT_SECRET** — a secret string used to secure user login sessions. Make up any long random string.
- **EMAIL_API_KEY** — your SendGrid API key for sending emails. You can get a free one at sendgrid.com.

## Database Setup

If you don't already have PostgreSQL running:

1. Install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)
2. The installer will set up PostgreSQL as a service that runs automatically when your computer starts
3. It will also create a default "postgres" user — remember the password you set during installation
4. Then run the migration and seed commands from the Installation section above

## Running the Application

Start the development server:

```
npm start
```

This starts both the backend server and the frontend. Open your web browser and go to:

```
http://localhost:3000
```

You should see the LawnCare Lite login page. If you see this, the app is running correctly.

## Troubleshooting

- **"Port 3000 is already in use"** — another program is using port 3000. Either stop that program, or change the PORT number in your `.env` file to something else (like 3001).
- **"Connection refused" when starting** — PostgreSQL is probably not running. Restart the PostgreSQL service: on Mac, `brew services restart postgresql`. On Windows, open Services and restart PostgreSQL.
- **"npm: command not found"** — Node.js is not installed or not in your system PATH. Reinstall Node.js from nodejs.org and restart your terminal.
- **Migration errors** — make sure your DATABASE_URL in `.env` is correct and PostgreSQL is running. Try running `npm run migrate` again.
- **Login doesn't work after seeding** — the seed script creates a default admin account: email `admin@greenthumb.com`, password `changeme123`. Make sure you're using these credentials.

## Project Structure

```
lawncare-lite/
  src/
    server.js          — the main backend server (handles API requests)
    routes/            — defines what happens when someone visits each URL
      customers.js     — customer management (add, edit, search)
      appointments.js  — scheduling and appointment management
      jobs.js          — job completion and status updates
      auth.js          — login, logout, password reset
    models/            — defines how data is structured in the database
      Customer.js
      Appointment.js
      Job.js
    middleware/        — code that runs before requests are processed
      auth.js          — checks if a user is logged in
  client/
    App.js             — the main frontend application
    components/        — reusable UI pieces (buttons, forms, etc.)
      Schedule.js      — the daily schedule view
      CustomerForm.js  — the form for adding/editing customers
    pages/             — full pages of the application
      Login.js         — the login page
      Dashboard.js     — the main screen after logging in
  package.json         — lists all dependencies and scripts
  .env.example         — example configuration file
```