import { http, HttpResponse } from 'msw';

const API = 'http://127.0.0.1:8000/api';

export const handlers = [
  http.get(`${API}/estudiantes`, () =>
    HttpResponse.json({
      success: true,
      data: [
        { estudianteid: 1, codigo: 'EST-001', nombre: 'Juan', apellido: 'Perez', correo: 'jp@uni.edu', creditosacum: 30 },
        { estudianteid: 2, codigo: 'EST-002', nombre: 'Ana', apellido: 'Garcia', correo: 'ag@uni.edu', creditosacum: 60 },
      ],
    })
  ),

  http.post(`${API}/estudiantes`, () =>
    HttpResponse.json({ success: true, data: { id: 3, message: 'Estudiante creado exitosamente' } })
  ),

  http.delete(`${API}/estudiantes/:id`, () =>
    HttpResponse.json({ success: true, message: 'Estudiante eliminado.' })
  ),

  http.get(`${API}/docentes`, () =>
    HttpResponse.json({
      success: true,
      data: [
        { docenteid: 1, codigo: 'DOC-001', nombre: 'Carlos', apellido: 'Lopez', especialidad: 'Matematicas', correo: 'cl@uni.edu' },
      ],
    })
  ),

  http.post(`${API}/docentes`, () =>
    HttpResponse.json({ success: true, data: { id: 2, message: 'Docente creado' } })
  ),

  http.delete(`${API}/docentes/:id`, () =>
    HttpResponse.json({ success: true, message: 'Docente eliminado.' })
  ),

  http.get(`${API}/cursos`, () =>
    HttpResponse.json({
      success: true,
      data: [
        { cursoid: 1, codigo: 'MAT-101', nombre: 'Matematicas I', creditosreq: 0, docenteid: 1, cupos: 30, carreraid: 1, nombredocente: 'Carlos Lopez', nombrecarrera: 'Ingenieria' },
      ],
    })
  ),

  http.post(`${API}/cursos`, () =>
    HttpResponse.json({ success: true, data: { id: 2, message: 'Curso creado' } })
  ),

  http.delete(`${API}/cursos/:id`, () =>
    HttpResponse.json({ success: true, message: 'Curso eliminado.' })
  ),

  http.get(`${API}/aulas`, () =>
    HttpResponse.json({
      success: true,
      data: [
        { aulaid: 1, nombre: 'A101', capacidad: 30, edificio: 'Central', equipamiento: 'Proyector' },
        { aulaid: 2, nombre: 'A102', capacidad: 40, edificio: 'Central', equipamiento: 'Pizarra' },
      ],
    })
  ),

  http.post(`${API}/aulas`, () =>
    HttpResponse.json({ success: true, data: { id: 3, message: 'Aula creada' } })
  ),

  http.delete(`${API}/aulas/:id`, () =>
    HttpResponse.json({ success: true, message: 'Aula eliminada.' })
  ),

  http.get(`${API}/matriculas`, () =>
    HttpResponse.json({
      success: true,
      data: [
        { matriculaid: 1, estudianteid: 1, cursoid: 2, estado: 'Pendiente', nombreestudiante: 'Juan Perez', nombrecurso: 'Matematicas I' },
      ],
    })
  ),

  http.post(`${API}/matriculas`, () =>
    HttpResponse.json({ success: true, data: { id: 2, message: 'Matricula registrada' } })
  ),

  http.put(`${API}/matriculas/:id/estado`, ({ params }) =>
    HttpResponse.json({ success: true, message: 'Estado actualizado' })
  ),

  http.get(`${API}/horarios`, () =>
    HttpResponse.json({
      success: true,
      data: [
        { horarioid: 1, cursoid: 1, aulaid: 1, diasemana: 1, horainicio: '08:00', horafin: '10:00', nombrecurso: 'Matematicas I', nombreaula: 'A101', carreraid: 1 },
      ],
    })
  ),

  http.post(`${API}/horarios`, () =>
    HttpResponse.json({ success: true, data: { id: 2, message: 'Horario registrado exitosamente sin cruces' } })
  ),

  http.post(`${API}/horarios/generar`, () =>
    HttpResponse.json({ success: true, message: 'Se generaron 10 horario(s) exitosamente', data: { horarios_creados: 10, detalles: [] } })
  ),

  http.get(`${API}/carreras`, () =>
    HttpResponse.json({
      success: true,
      data: [
        { carreraid: 1, nombre: 'Ingenieria de Sistemas', facultad: 'Ingenieria' },
        { carreraid: 2, nombre: 'Ingenieria Civil', facultad: 'Ingenieria' },
      ],
    })
  ),

  http.post(`${API}/carreras`, () =>
    HttpResponse.json({ success: true, data: { id: 3, message: 'Carrera registrada' } })
  ),

  http.delete(`${API}/carreras/:id`, () =>
    HttpResponse.json({ success: true, message: 'Carrera eliminada logicamente' })
  ),

  http.get(`${API}/dashboard`, () =>
    HttpResponse.json({
      success: true,
      data: {
        total_estudiantes: 10,
        total_docentes: 5,
        total_cursos: 8,
        total_aulas: 6,
        matriculas_aprobadas: 4,
        matriculas_rechazadas: 1,
      },
    })
  ),

  http.get('http://127.0.0.1:8000/health', () =>
    HttpResponse.json({ status: 'healthy' })
  ),
];
