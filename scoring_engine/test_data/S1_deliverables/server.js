const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const { Pool } = require('pg');

const app = express();
app.use(express.json());

// Database connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// Authentication middleware
function requireAuth(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Authentication required' });
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    res.status(401).json({ error: 'Invalid or expired token' });
  }
}

// POST /api/auth/login
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ error: 'Email and password required' });

  const result = await pool.query('SELECT * FROM users WHERE email = $1', [email]);
  const user = result.rows[0];
  if (!user) return res.status(401).json({ error: 'Invalid credentials' });

  const valid = await bcrypt.compare(password, user.password_hash);
  if (!valid) return res.status(401).json({ error: 'Invalid credentials' });

  const token = jwt.sign({ userId: user.id, role: user.role }, process.env.JWT_SECRET);
  res.json({ token, user: { id: user.id, name: user.name, role: user.role } });
});

// Customer CRUD
app.get('/api/customers', requireAuth, async (req, res) => {
  const { search } = req.query;
  let query = 'SELECT * FROM customers';
  if (search) {
    query += ' WHERE name ILIKE $1 OR email ILIKE $1 OR phone ILIKE $1';
    return res.json((await pool.query(query, [`%${search}%`])).rows);
  }
  res.json((await pool.query(query)).rows);
});

app.post('/api/customers', requireAuth, async (req, res) => {
  const { first_name, last_name, email, phone, address, city, state, zip } = req.body;
  if (!first_name || !last_name || !email) {
    return res.status(400).json({ error: 'First name, last name, and email are required' });
  }
  const result = await pool.query(
    'INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip) VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING *',
    [first_name, last_name, email, phone, address, city, state, zip]
  );
  res.status(201).json(result.rows[0]);
});

// Appointment scheduling
app.get('/api/appointments', requireAuth, async (req, res) => {
  const { date, technician_id } = req.query;
  let query = 'SELECT a.*, c.first_name, c.last_name, c.address FROM appointments a JOIN customers c ON a.customer_id = c.id WHERE 1=1';
  const params = [];
  if (date) { params.push(date); query += ` AND a.date = $${params.length}`; }
  if (technician_id) { params.push(technician_id); query += ` AND a.technician_id = $${params.length}`; }
  res.json((await pool.query(query, params)).rows);
});

app.post('/api/appointments', requireAuth, async (req, res) => {
  const { customer_id, technician_id, date, start_time, duration, service_type } = req.body;
  if (!customer_id || !technician_id || !date || !start_time || !duration) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  // Check for overlapping appointments for this technician
  const overlap = await pool.query(
    `SELECT id FROM appointments WHERE technician_id = $1 AND date = $2 AND start_time < $3 AND start_time + ($4 || ' minutes')::interval > $5`,
    [technician_id, date, start_time, duration, start_time]
  );
  if (overlap.rows.length > 0) {
    return res.status(409).json({ error: 'Technician already has an overlapping appointment' });
  }
  const result = await pool.query(
    'INSERT INTO appointments (customer_id, technician_id, date, start_time, duration, service_type) VALUES ($1,$2,$3,$4,$5,$6) RETURNING *',
    [customer_id, technician_id, date, start_time, duration, service_type]
  );
  res.status(201).json(result.rows[0]);
});

// Job completion
app.patch('/api/jobs/:id/complete', requireAuth, async (req, res) => {
  const { notes, photos } = req.body;
  const job = (await pool.query('SELECT * FROM appointments WHERE id = $1', [req.params.id])).rows[0];
  if (!job) return res.status(404).json({ error: 'Job not found' });
  if (job.status !== 'in_progress') {
    return res.status(400).json({ error: 'Jobs can only be completed from In Progress status' });
  }
  const result = await pool.query(
    'UPDATE appointments SET status = $1, completed_at = NOW(), completion_notes = $2, photos = $3 WHERE id = $4 RETURNING *',
    ['completed', notes || null, photos || null, req.params.id]
  );
  // Send confirmation email
  const customer = (await pool.query('SELECT * FROM customers WHERE id = $1', [job.customer_id])).rows[0];
  // emailService.sendCompletionNotification(customer.email, job);
  res.json(result.rows[0]);
});

// Print daily schedule
app.get('/api/schedule/daily/:date', requireAuth, async (req, res) => {
  const result = await pool.query(
    `SELECT a.*, t.name as technician_name, c.first_name, c.last_name, c.address, c.service_type
     FROM appointments a
     JOIN users t ON a.technician_id = t.id
     JOIN customers c ON a.customer_id = c.id
     WHERE a.date = $1
     ORDER BY t.name, a.start_time`,
    [req.params.date]
  );
  res.json(result.rows);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));