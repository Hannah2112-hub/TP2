import { describe, it, expect, beforeAll, afterAll, afterEach, beforeEach } from 'vitest';
import { HttpRequest, HttpResponse, http } from 'msw';
import { setupServer } from 'msw/node';
import { handlers } from '../mocks/handlers';

const API = 'http://127.0.0.1:8000/api';

const server = setupServer(...handlers);

beforeAll(() => server.listen({ onUnhandledRequest: 'bypass' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('MSW - Pruebas de integracion con MSW', () => {
  it('MSW-001 | MSW server intercepta GET /estudiantes', async () => {
    const res = await fetch(`${API}/estudiantes`);
    const body = await res.json();
    expect(res.status).toBe(200);
    expect(body.success).toBe(true);
    expect(Array.isArray(body.data)).toBe(true);
    expect(body.data.length).toBeGreaterThan(0);
  });

  it('MSW-002 | MSW server intercepta GET /docentes', async () => {
    const res = await fetch(`${API}/docentes`);
    const body = await res.json();
    expect(res.status).toBe(200);
    expect(body.success).toBe(true);
    expect(body.data.length).toBeGreaterThan(0);
  });

  it('MSW-003 | MSW server intercepta GET /cursos', async () => {
    const res = await fetch(`${API}/cursos`);
    const body = await res.json();
    expect(res.status).toBe(200);
    expect(body.success).toBe(true);
  });

  it('MSW-004 | MSW server intercepta GET /aulas', async () => {
    const res = await fetch(`${API}/aulas`);
    const body = await res.json();
    expect(res.status).toBe(200);
    expect(body.success).toBe(true);
    expect(body.data.length).toBe(2);
  });

  it('MSW-005 | MSW server intercepta GET /matriculas', async () => {
    const res = await fetch(`${API}/matriculas`);
    const body = await res.json();
    expect(res.status).toBe(200);
    expect(body.success).toBe(true);
  });

  it('MSW-006 | MSW server intercepta GET /horarios', async () => {
    const res = await fetch(`${API}/horarios`);
    const body = await res.json();
    expect(res.status).toBe(200);
    expect(body.success).toBe(true);
  });

  it('MSW-007 | MSW server intercepta GET /carreras', async () => {
    const res = await fetch(`${API}/carreras`);
    const body = await res.json();
    expect(res.status).toBe(200);
    expect(body.success).toBe(true);
    expect(body.data.length).toBe(2);
  });

  it('MSW-008 | MSW server intercepta GET /dashboard', async () => {
    const res = await fetch(`${API}/dashboard`);
    const body = await res.json();
    expect(res.status).toBe(200);
    expect(body.success).toBe(true);
    expect(body.data.total_estudiantes).toBe(10);
  });

  it('MSW-009 | MSW server intercepta POST /estudiantes', async () => {
    const res = await fetch(`${API}/estudiantes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ codigo: 'EST-003', nombre: 'Test', apellido: 'User' }),
    });
    const body = await res.json();
    expect(res.status).toBe(200);
    expect(body.success).toBe(true);
  });

  it('MSW-010 | MSW server intercepta POST /horarios/generar', async () => {
    const res = await fetch(`${API}/horarios/generar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hora_inicio: '08:00', bloques_horas: 2, carrera_id: 1 }),
    });
    const body = await res.json();
    expect(res.status).toBe(200);
    expect(body.success).toBe(true);
    expect(body.data.horarios_creados).toBe(10);
  });

  it('MSW-011 | MSW server intercepta DELETE /estudiantes/1', async () => {
    const res = await fetch(`${API}/estudiantes/1`, { method: 'DELETE' });
    const body = await res.json();
    expect(res.status).toBe(200);
    expect(body.success).toBe(true);
  });

  it('MSW-012 | MSW server intercepta health check', async () => {
    const res = await fetch('http://127.0.0.1:8000/health');
    const body = await res.json();
    expect(res.status).toBe(200);
    expect(body.status).toBe('healthy');
  });

  it('MSW-013 | Handler personalizado para 404', async () => {
    server.use(
      http.get(`${API}/inexistente`, () => {
        return new HttpResponse(null, { status: 404 });
      })
    );
    const res = await fetch(`${API}/inexistente`);
    expect(res.status).toBe(404);
  });

  it('MSW-014 | Handler personalizado para 500', async () => {
    server.use(
      http.get(`${API}/estudiantes`, () => {
        return new HttpResponse(null, { status: 500 });
      })
    );
    const res = await fetch(`${API}/estudiantes`);
    expect(res.status).toBe(500);
  });

  it('MSW-015 | Handler personalizado para 503', async () => {
    server.use(
      http.get(`${API}/estudiantes`, () => {
        return new HttpResponse(null, { status: 503 });
      })
    );
    const res = await fetch(`${API}/estudiantes`);
    expect(res.status).toBe(503);
  });
});
