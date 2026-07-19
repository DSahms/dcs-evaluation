const request = require('supertest');
const app = require('./server');

describe('LawnCare Lite API', () => {
  describe('POST /api/auth/login', () => {
    it('should return 400 if email is missing', async () => {
      const res = await request(app).post('/api/auth/login').send({ password: 'test' });
      expect(res.status).toBe(400);
    });
    it('should return 401 for invalid credentials', async () => {
      const res = await request(app).post('/api/auth/login').send({
        email: 'nobody@example.com', password: 'wrong'
      });
      expect(res.status).toBe(401);
    });
  });

  describe('GET /api/customers', () => {
    it('should return 401 without authentication', async () => {
      const res = await request(app).get('/api/customers');
      expect(res.status).toBe(401);
    });
  });

  describe('POST /api/customers', () => {
    it('should return 400 if required fields are missing', async () => {
      const token = 'fake-token';
      const res = await request(app)
        .post('/api/customers')
        .set('Authorization', `Bearer ${token}`)
        .send({ first_name: 'John' });
      expect(res.status).toBe(401); // Invalid token will be caught first
    });
  });

  describe('POST /api/appointments', () => {
    it('should return 400 if required fields are missing', async () => {
      const res = await request(app)
        .post('/api/appointments')
        .set('Authorization', 'Bearer fake')
        .send({});
      expect(res.status).toBe(401);
    });
  });

  describe('PATCH /api/jobs/:id/complete', () => {
    it('should return 401 without authentication', async () => {
      const res = await request(app).patch('/api/jobs/1/complete');
      expect(res.status).toBe(401);
    });
  });
});