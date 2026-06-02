import { describe, it, expect, vi, beforeEach } from 'vitest';
import { of, throwError } from 'rxjs';
import { AcademicService } from '../app/services/academic.service';

function mockHttp(result: any) {
  return {
    get: vi.fn().mockReturnValue(of(result)),
    post: vi.fn().mockReturnValue(of(result)),
    delete: vi.fn().mockReturnValue(of({})),
  } as any;
}

function errorHttp(error: any) {
  return {
    get: vi.fn().mockReturnValue(throwError(() => error)),
    post: vi.fn().mockReturnValue(throwError(() => error)),
    delete: vi.fn().mockReturnValue(throwError(() => error)),
  } as any;
}

const mockEstudiante = {
  success: true,
  data: [{ estudianteid: 1, codigo: 'E001', nombre: 'Juan', apellido: 'Pérez', correo: 'juan@test.com', creditosacum: 120 }]
};

const mockDocente = {
  success: true,
  data: [{ docenteid: 1, codigo: 'D001', nombre: 'María', apellido: 'López', especialidad: 'Matemáticas', correo: 'maria@test.com' }]
};

const mockCurso = {
  success: true,
  data: [{ cursoid: 1, codigo: 'C001', nombre: 'Álgebra', creditosreq: 4, cupos: 30, prerequisitoid: null, docenteid: 1, carreraid: 1, nombredocente: 'Dr. Pérez', nombrecarrera: 'Ingeniería' }]
};

const mockAula = {
  success: true,
  data: [{ aulaid: 1, nombre: 'A-101', capacidad: 30, edificio: 'A', equipamiento: 'Proyector' }]
};

const mockMatricula = {
  success: true,
  data: [{ matriculaid: 1, estudianteid: 1, cursoid: 1, estado: 'Aprobada', nombreestudiante: 'Juan Pérez', nombrecurso: 'Álgebra' }]
};

const mockHorario = {
  success: true,
  data: [{ horarioid: 1, cursoid: 1, nombrecurso: 'Álgebra', diasemana: 1, horainicio: '08:00', horafin: '10:00', aulaid: 1, nombreaula: 'A-101', carreraid: 1 }]
};

const mockCarrera = {
  success: true,
  data: [{ carreraid: 1, nombre: 'Ingeniería de Sistemas', facultad: 'Ingeniería' }]
};

const mockDashboard = {
  success: true,
  data: { total_estudiantes: 10, total_docentes: 5, total_cursos: 8, total_aulas: 6, matriculas_aprobadas: 15, matriculas_rechazadas: 3 }
};

const mockDashboardFallback = {
  success: false,
  data: null
};

describe('AcademicService - Pruebas Unitarias con HttpClient mockeado', () => {
  let service: AcademicService;

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  describe('cargarEstudiantes', () => {
    it('ACAD-001 | Carga exitosa mapea estudiantes correctamente', async () => {
      service = new AcademicService(mockHttp(mockEstudiante));
      await service.cargarEstudiantes();
      expect(service.Estudiantes().length).toBe(1);
      expect(service.Estudiantes()[0].codigo).toBe('E001');
      expect(service.Estudiantes()[0].nombre).toBe('Juan Pérez');
      expect(service.Estudiantes()[0].creditos).toBe(120);
    });

    it('ACAD-002 | Error en carga no lanza excepción', async () => {
      service = new AcademicService(errorHttp(new Error('Network error')));
      await expect(service.cargarEstudiantes()).resolves.toBeUndefined();
      expect(service.Estudiantes().length).toBe(0);
    });
  });

  describe('cargarDocentes', () => {
    it('ACAD-003 | Carga exitosa mapea docentes correctamente', async () => {
      service = new AcademicService(mockHttp(mockDocente));
      await service.cargarDocentes();
      expect(service.Docentes().length).toBe(1);
      expect(service.Docentes()[0].codigo).toBe('D001');
      expect(service.Docentes()[0].especialidad).toBe('Matemáticas');
    });
  });

  describe('cargarCursos', () => {
    it('ACAD-004 | Carga exitosa mapea cursos correctamente', async () => {
      service = new AcademicService(mockHttp(mockCurso));
      await service.cargarCursos();
      expect(service.Cursos().length).toBe(1);
      expect(service.Cursos()[0].codigo).toBe('C001');
      expect(service.Cursos()[0].cupos).toBe(30);
    });
  });

  describe('cargarAulas', () => {
    it('ACAD-005 | Carga exitosa mapea aulas correctamente', async () => {
      service = new AcademicService(mockHttp(mockAula));
      await service.cargarAulas();
      expect(service.Aulas().length).toBe(1);
      expect(service.Aulas()[0].nombre).toBe('A-101');
    });
  });

  describe('cargarMatriculas', () => {
    it('ACAD-006 | Carga exitosa mapea matrículas correctamente', async () => {
      service = new AcademicService(mockHttp(mockMatricula));
      await service.cargarMatriculas();
      expect(service.Matriculas().length).toBe(1);
      expect(service.Matriculas()[0].estado).toBe('Aprobada');
    });
  });

  describe('cargarHorarios', () => {
    it('ACAD-007 | Carga exitosa mapea horarios correctamente', async () => {
      service = new AcademicService(mockHttp(mockHorario));
      await service.cargarHorarios();
      expect(service.HorarioGenerado().length).toBe(1);
      expect(service.HorarioGenerado()[0].curso).toBe('Álgebra');
      expect(service.HorarioGenerado()[0].dia).toBe('Lunes');
    });
  });

  describe('cargarCarreras', () => {
    it('ACAD-008 | Carga exitosa mapea carreras correctamente', async () => {
      service = new AcademicService(mockHttp(mockCarrera));
      await service.cargarCarreras();
      expect(service.Carreras().length).toBe(1);
      expect(service.Carreras()[0].nombre).toBe('Ingeniería de Sistemas');
    });
  });

  describe('cargarTodo', () => {
    it('ACAD-009 | cargarTodo constructor llama a 7 endpoints', async () => {
      const http = {
        get: vi.fn().mockReturnValue(of(mockEstudiante)),
        post: vi.fn().mockReturnValue(of({})),
        delete: vi.fn().mockReturnValue(of({})),
      };
      service = new AcademicService(http as any);
      // Constructor llama cargarTodo: 7 endpoints (carreras, estudiantes, docentes, cursos, aulas, matriculas, horarios)
      expect(http.get).toHaveBeenCalledTimes(7);
    });
  });

  describe('getEstadisticas', () => {
    it('ACAD-010 | getEstadisticas con datos del API', async () => {
      service = new AcademicService(mockHttp(mockDashboard));
      const stats = await service.getEstadisticas();
      expect(stats.total_estudiantes).toBe(10);
      expect(stats.total_docentes).toBe(5);
    });

    it('ACAD-011 | getEstadisticas fallback cuando API falla', async () => {
      service = new AcademicService(mockHttp(mockDashboardFallback));
      // Poblar datos locales para el fallback
      const http2 = mockHttp(mockEstudiante);
      service = new AcademicService(http2);
      await service.cargarEstudiantes();

      const svc2 = new AcademicService(mockHttp(mockDashboardFallback));
      await svc2.cargarEstudiantes();
      const stats = await svc2.getEstadisticas();
      expect(stats).toHaveProperty('total_estudiantes');
    });
  });

  describe('Métodos de búsqueda local', () => {
    it('ACAD-012 | getEstudianteByCodigo con datos cargados', async () => {
      service = new AcademicService(mockHttp(mockEstudiante));
      await service.cargarEstudiantes();
      expect(service.getEstudianteByCodigo('E001')).toBeDefined();
      expect(service.getEstudianteByCodigo('INEXISTENTE')).toBeUndefined();
    });
  });

  describe('Métodos de escritura', () => {
    it('ACAD-013 | agregarEstudiante retorna true en éxito', async () => {
      const http = mockHttp({ success: true, data: { id: 1 } });
      service = new AcademicService(http);
      const result = await service.agregarEstudiante({ codigo: 'E002', nombre: 'Ana García', creditos: 90, correo: 'ana@test.com' } as any);
      expect(result).toBe(true);
    });

    it('ACAD-014 | agregarEstudiante retorna false cuando API falla', async () => {
      const http = mockHttp({ success: false });
      service = new AcademicService(http);
      const result = await service.agregarEstudiante({ codigo: 'E002', nombre: 'Ana', creditos: 90, correo: 'ana@test.com' } as any);
      expect(result).toBe(false);
    });

    it('ACAD-015 | agregarDocente retorna true en éxito', async () => {
      const http = mockHttp({ success: true });
      service = new AcademicService(http);
      const result = await service.agregarDocente({ codigo: 'D002', nombre: 'Carlos Ruiz', especialidad: 'Física', correo: 'carlos@test.com' } as any);
      expect(result).toBe(true);
    });

    it('ACAD-016 | agregarCurso retorna true en éxito', async () => {
      const http = mockHttp({ success: true });
      service = new AcademicService(http);
      const result = await service.agregarCurso({ codigo: 'C002', nombre: 'Cálculo', creditos: 5, prereq: '', docente: '1', carrera: '1', cupos: 30 } as any);
      expect(result).toBe(true);
    });

    it('ACAD-017 | agregarAula retorna true en éxito', async () => {
      const http = mockHttp({ success: true });
      service = new AcademicService(http);
      const result = await service.agregarAula({ nombre: 'B-201', capacidad: 40, edificio: 'B', equipamiento: 'TV' } as any);
      expect(result).toBe(true);
    });

    it('ACAD-018 | agregarCarrera retorna true en éxito', async () => {
      const http = mockHttp({ success: true });
      service = new AcademicService(http);
      const result = await service.agregarCarrera({ nombre: 'Medicina', facultad: 'Ciencias de la Salud' } as any);
      expect(result).toBe(true);
    });

    it('ACAD-019 | agregarMatricula retorna ok en éxito', async () => {
      const http = mockHttp({ success: true, message: 'Matrícula registrada' });
      service = new AcademicService(http);
      const result = await service.agregarMatricula(1, 2);
      expect(result.ok).toBe(true);
      expect(result.mensaje).toBe('Matrícula registrada');
    });

    it('ACAD-020 | agregarMatricula retorna error cuando falla', async () => {
      const http = mockHttp({ success: false, message: 'Error' });
      service = new AcademicService(http);
      const result = await service.agregarMatricula(1, 2);
      expect(result.ok).toBe(false);
    });

    it('ACAD-021 | generarHorarios retorna ok en éxito', async () => {
      const http = mockHttp({ success: true, message: 'Horarios generados' });
      service = new AcademicService(http);
      const result = await service.generarHorarios(8, 2);
      expect(result.ok).toBe(true);
    });

    it('ACAD-022 | generarHorarios con carreraId retorna ok', async () => {
      const http = mockHttp({ success: true });
      service = new AcademicService(http);
      const result = await service.generarHorarios(8, 2, 1);
      expect(result.ok).toBe(true);
    });

    it('ACAD-023 | agregarHorario retorna ok en éxito', async () => {
      const http = mockHttp({ success: true, message: 'Horario registrado' });
      service = new AcademicService(http);
      const result = await service.agregarHorario(1, 1, 1, '08:00', '10:00');
      expect(result.ok).toBe(true);
    });

    it('ACAD-024 | eliminarEstudiante no lanza en éxito', async () => {
      const http = { get: vi.fn().mockReturnValue(of(mockEstudiante)), post: vi.fn(), delete: vi.fn().mockReturnValue(of({})) };
      service = new AcademicService(http as any);
      await expect(service.eliminarEstudiante(1)).resolves.toBeUndefined();
    });

    it('ACAD-025 | eliminarDocente no lanza en éxito', async () => {
      const http = { get: vi.fn().mockReturnValue(of(mockDocente)), post: vi.fn(), delete: vi.fn().mockReturnValue(of({})) };
      service = new AcademicService(http as any);
      await expect(service.eliminarDocente(1)).resolves.toBeUndefined();
    });

    it('ACAD-026 | eliminarCurso no lanza en éxito', async () => {
      const http = { get: vi.fn().mockReturnValue(of(mockCurso)), post: vi.fn(), delete: vi.fn().mockReturnValue(of({})) };
      service = new AcademicService(http as any);
      await expect(service.eliminarCurso(1)).resolves.toBeUndefined();
    });

    it('ACAD-027 | eliminarCarrera no lanza en éxito', async () => {
      const http = { get: vi.fn().mockReturnValue(of(mockCarrera)), post: vi.fn(), delete: vi.fn().mockReturnValue(of({})) };
      service = new AcademicService(http as any);
      await expect(service.eliminarCarrera(1)).resolves.toBeUndefined();
    });

    it('ACAD-028 | Error de red en agregarEstudiante retorna false', async () => {
      const http = errorHttp(new Error('Network error'));
      service = new AcademicService(http);
      const result = await service.agregarEstudiante({ codigo: 'E999', nombre: 'Error', creditos: 0, correo: '' } as any);
      expect(result).toBe(false);
    });

    it('ACAD-029 | Error de red en agregarMatricula retorna ok=false', async () => {
      const http = errorHttp({ error: { detail: 'Error de conexión' } });
      service = new AcademicService(http);
      const result = await service.agregarMatricula(1, 2);
      expect(result.ok).toBe(false);
      expect(result.mensaje).toBe('Error de conexión');
    });

    it('ACAD-030 | Error de red en generarHorarios retorna ok=false', async () => {
      const http = errorHttp({ error: { detail: 'Error de conexión' } });
      service = new AcademicService(http);
      const result = await service.generarHorarios(8, 2);
      expect(result.ok).toBe(false);
    });

    it('ACAD-031 | Error de red en agregarHorario retorna ok=false', async () => {
      const http = errorHttp({ error: { detail: 'Error de conexión' } });
      service = new AcademicService(http);
      const result = await service.agregarHorario(1, 1, 1, '08:00', '10:00');
      expect(result.ok).toBe(false);
    });
  });
});
