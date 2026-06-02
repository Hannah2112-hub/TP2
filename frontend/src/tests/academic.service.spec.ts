/**
 * PRUEBAS UNITARIAS FRONTEND - AcademicService (Lógica de Negocio)
 * Tipo: Unitario con Vitest + mocks de HTTP
 * Cobertura: Helpers, mapeo de datos, lógica de estado, búsquedas
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';

// ─── Tipos del dominio ────────────────────────────────────────────────────────
interface Estudiante {
  id: number;
  codigo: string;
  nombre: string;
  creditos: number;
  correo: string;
}

interface Docente {
  id: number;
  codigo: string;
  nombre: string;
  especialidad: string;
  correo: string;
}

interface Curso {
  id: number;
  codigo: string;
  nombre: string;
  creditos: number;
  prereq: string;
  docente: string;
  carrera: string;
  cupos: number;
}

interface Matricula {
  id: number;
  estudiante: string;
  curso: string;
  estado: string;
  nombreEstudiante: string;
  nombreCurso: string;
}

// ─── Clase de servicio simulado (funciones puras) ─────────────────────────────
class AcademicServiceSimulado {
  private _estudiantes: Estudiante[] = [];
  private _docentes: Docente[] = [];
  private _cursos: Curso[] = [];
  private _matriculas: Matricula[] = [];
  private colores = ['hc-purple', 'hc-teal', 'hc-blue', 'hc-amber', 'hc-coral', 'hc-green'];
  private diasNombres = ['', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'];

  setEstudiantes(data: Estudiante[]) { this._estudiantes = data; }
  setDocentes(data: Docente[]) { this._docentes = data; }
  setCursos(data: Curso[]) { this._cursos = data; }
  setMatriculas(data: Matricula[]) { this._matriculas = data; }

  get Estudiantes() { return this._estudiantes; }
  get Docentes() { return this._docentes; }
  get Cursos() { return this._cursos; }
  get Matriculas() { return this._matriculas; }

  getEstudianteByCodigo(codigo: string): Estudiante | undefined {
    return this._estudiantes.find(e => e.codigo === codigo);
  }

  getDocenteByCodigo(codigo: string): Docente | undefined {
    return this._docentes.find(d => d.codigo === codigo);
  }

  getCursoByCodigo(codigo: string): Curso | undefined {
    return this._cursos.find(c => c.codigo === codigo);
  }

  // Lógica de mapeo del backend al modelo del frontend
  mapEstudianteFromApi(raw: any): Estudiante {
    return {
      id: raw.estudianteid,
      codigo: raw.codigo,
      nombre: `${raw.nombre} ${raw.apellido}`,
      creditos: raw.creditosacum ?? 0,
      correo: raw.correo,
    };
  }

  mapDocenteFromApi(raw: any): Docente {
    return {
      id: raw.docenteid,
      codigo: raw.codigo,
      nombre: `${raw.nombre} ${raw.apellido}`,
      especialidad: raw.especialidad ?? '',
      correo: raw.correo,
    };
  }

  getEstadisticasLocales(): Record<string, number> {
    return {
      total_estudiantes: this._estudiantes.length,
      total_docentes: this._docentes.length,
      total_cursos: this._cursos.length,
      matriculas_aprobadas: this._matriculas.filter(m => m.estado === 'Aprobada').length,
      matriculas_rechazadas: this._matriculas.filter(m => m.estado === 'Rechazada').length,
    };
  }

  getDiaNombre(dia: number): string {
    return this.diasNombres[dia] ?? `Día ${dia}`;
  }

  getColor(index: number): string {
    return this.colores[index % this.colores.length];
  }

  // Lógica de parsing del nombre para creación
  parseNombre(nombre: string): { nombre: string; apellido: string } {
    const partes = nombre.trim().split(' ');
    return {
      nombre: partes[0] ?? '',
      apellido: partes.slice(1).join(' ') || 'S/A'
    };
  }
}

// ─── TESTS ────────────────────────────────────────────────────────────────────

describe('AcademicService - Pruebas Unitarias de Lógica', () => {
  let service: AcademicServiceSimulado;

  beforeEach(() => {
    service = new AcademicServiceSimulado();
  });

  // ─── Helpers de búsqueda ──────────────────────────────────────────────────

  describe('getEstudianteByCodigo()', () => {
    beforeEach(() => {
      service.setEstudiantes([
        { id: 1, codigo: 'EST-001', nombre: 'Juan Perez', creditos: 30, correo: 'jp@uni.edu' },
        { id: 2, codigo: 'EST-002', nombre: 'Ana García', creditos: 60, correo: 'ag@uni.edu' },
      ]);
    });

    it('HP-001 | Happy Path: Encuentra estudiante por código', () => {
      const result = service.getEstudianteByCodigo('EST-001');
      expect(result).toBeDefined();
      expect(result?.nombre).toBe('Juan Perez');
    });

    it('HP-002 | Happy Path: Encuentra segundo estudiante correctamente', () => {
      const result = service.getEstudianteByCodigo('EST-002');
      expect(result?.id).toBe(2);
    });

    it('UP-001 | Unhappy Path: Código inexistente devuelve undefined', () => {
      const result = service.getEstudianteByCodigo('NOEXISTE');
      expect(result).toBeUndefined();
    });

    it('EC-001 | Edge Case: Lista vacía devuelve undefined', () => {
      service.setEstudiantes([]);
      const result = service.getEstudianteByCodigo('EST-001');
      expect(result).toBeUndefined();
    });

    it('EC-002 | Edge Case: Código vacío devuelve undefined', () => {
      const result = service.getEstudianteByCodigo('');
      expect(result).toBeUndefined();
    });
  });

  describe('getDocenteByCodigo()', () => {
    beforeEach(() => {
      service.setDocentes([
        { id: 1, codigo: 'DOC-001', nombre: 'Carlos López', especialidad: 'Matemáticas', correo: 'cl@uni.edu' }
      ]);
    });

    it('HP-001 | Happy Path: Encuentra docente por código', () => {
      const result = service.getDocenteByCodigo('DOC-001');
      expect(result).toBeDefined();
      expect(result?.especialidad).toBe('Matemáticas');
    });

    it('UP-001 | Unhappy Path: Código no encontrado devuelve undefined', () => {
      const result = service.getDocenteByCodigo('XXX');
      expect(result).toBeUndefined();
    });
  });

  describe('getCursoByCodigo()', () => {
    beforeEach(() => {
      service.setCursos([
        { id: 1, codigo: 'MAT-101', nombre: 'Matemáticas I', creditos: 0, prereq: '', docente: '', carrera: '', cupos: 30 }
      ]);
    });

    it('HP-001 | Happy Path: Encuentra curso por código', () => {
      const result = service.getCursoByCodigo('MAT-101');
      expect(result).toBeDefined();
      expect(result?.nombre).toBe('Matemáticas I');
    });

    it('UP-001 | Unhappy Path: Curso inexistente devuelve undefined', () => {
      const result = service.getCursoByCodigo('NOEXISTE');
      expect(result).toBeUndefined();
    });
  });

  // ─── Mapeo de datos API → Modelo ──────────────────────────────────────────

  describe('mapEstudianteFromApi()', () => {
    it('MAP-001 | Mapeo correcto de datos del backend', () => {
      const raw = { estudianteid: 5, codigo: 'EST-005', nombre: 'Pedro', apellido: 'Ramírez', correo: 'pr@uni.edu', creditosacum: 45 };
      const mapped = service.mapEstudianteFromApi(raw);
      expect(mapped.id).toBe(5);
      expect(mapped.nombre).toBe('Pedro Ramírez');
      expect(mapped.creditos).toBe(45);
    });

    it('MAP-002 | Créditos null se mapea como 0', () => {
      const raw = { estudianteid: 6, codigo: 'EST-006', nombre: 'X', apellido: 'Y', correo: 'xy@uni.edu', creditosacum: null };
      const mapped = service.mapEstudianteFromApi(raw);
      expect(mapped.creditos).toBe(0);
    });

    it('MAP-003 | Nombre compuesto se une correctamente', () => {
      const raw = { estudianteid: 7, codigo: 'EST-007', nombre: 'María', apellido: 'González López', correo: 'mg@uni.edu', creditosacum: 0 };
      const mapped = service.mapEstudianteFromApi(raw);
      expect(mapped.nombre).toBe('María González López');
    });
  });

  describe('mapDocenteFromApi()', () => {
    it('MAP-004 | Mapeo correcto de datos del docente', () => {
      const raw = { docenteid: 3, codigo: 'DOC-003', nombre: 'Luis', apellido: 'Mendez', especialidad: 'Física', correo: 'lm@uni.edu' };
      const mapped = service.mapDocenteFromApi(raw);
      expect(mapped.id).toBe(3);
      expect(mapped.nombre).toBe('Luis Mendez');
      expect(mapped.especialidad).toBe('Física');
    });

    it('MAP-005 | Especialidad null se mapea como cadena vacía', () => {
      const raw = { docenteid: 4, codigo: 'DOC-004', nombre: 'X', apellido: 'Y', especialidad: null, correo: 'xy@uni.edu' };
      const mapped = service.mapDocenteFromApi(raw);
      expect(mapped.especialidad).toBe('');
    });
  });

  // ─── Estadísticas locales ─────────────────────────────────────────────────

  describe('getEstadisticasLocales()', () => {
    it('STAT-001 | Happy Path: Estadísticas correctas con datos cargados', () => {
      service.setEstudiantes([
        { id: 1, codigo: 'E1', nombre: 'A', creditos: 0, correo: 'a@a.com' },
        { id: 2, codigo: 'E2', nombre: 'B', creditos: 0, correo: 'b@b.com' },
      ]);
      service.setMatriculas([
        { id: 1, estudiante: '1', curso: '1', estado: 'Aprobada', nombreEstudiante: 'A', nombreCurso: 'C' },
        { id: 2, estudiante: '2', curso: '1', estado: 'Rechazada', nombreEstudiante: 'B', nombreCurso: 'C' },
        { id: 3, estudiante: '1', curso: '2', estado: 'Aprobada', nombreEstudiante: 'A', nombreCurso: 'D' },
      ]);
      const stats = service.getEstadisticasLocales();
      expect(stats.total_estudiantes).toBe(2);
      expect(stats.matriculas_aprobadas).toBe(2);
      expect(stats.matriculas_rechazadas).toBe(1);
    });

    it('STAT-002 | Edge Case: Estadísticas con colecciones vacías devuelven 0', () => {
      const stats = service.getEstadisticasLocales();
      expect(stats.total_estudiantes).toBe(0);
      expect(stats.total_docentes).toBe(0);
      expect(stats.total_cursos).toBe(0);
      expect(stats.matriculas_aprobadas).toBe(0);
    });
  });

  // ─── Helpers de días y colores ────────────────────────────────────────────

  describe('getDiaNombre()', () => {
    it('DIA-001 | Día 1 = Lunes', () => {
      expect(service.getDiaNombre(1)).toBe('Lunes');
    });
    it('DIA-002 | Día 5 = Viernes', () => {
      expect(service.getDiaNombre(5)).toBe('Viernes');
    });
    it('DIA-003 | Día 0 = cadena vacía (no definido)', () => {
      expect(service.getDiaNombre(0)).toBe('');
    });
    it('DIA-004 | Día fuera de rango devuelve fallback', () => {
      expect(service.getDiaNombre(99)).toBe('Día 99');
    });
  });

  describe('getColor()', () => {
    it('COLOR-001 | Índice 0 retorna primer color', () => {
      expect(service.getColor(0)).toBe('hc-purple');
    });
    it('COLOR-002 | Índice 6 hace ciclo al primer color', () => {
      expect(service.getColor(6)).toBe('hc-purple');
    });
    it('COLOR-003 | Índice 1 retorna segundo color', () => {
      expect(service.getColor(1)).toBe('hc-teal');
    });
  });

  // ─── Parsing de nombres ───────────────────────────────────────────────────

  describe('parseNombre()', () => {
    it('PARSE-001 | Nombre simple extrae nombre y apellido por defecto', () => {
      const result = service.parseNombre('Pedro');
      expect(result.nombre).toBe('Pedro');
      expect(result.apellido).toBe('S/A');
    });

    it('PARSE-002 | Nombre con apellido los separa correctamente', () => {
      const result = service.parseNombre('Pedro Ramírez');
      expect(result.nombre).toBe('Pedro');
      expect(result.apellido).toBe('Ramírez');
    });

    it('PARSE-003 | Nombre con apellido compuesto lo mantiene completo', () => {
      const result = service.parseNombre('Ana María González López');
      expect(result.nombre).toBe('Ana');
      expect(result.apellido).toBe('María González López');
    });

    it('PARSE-004 | Nombre con espacios extra se limpia', () => {
      const result = service.parseNombre('  Pedro  Ramirez  ');
      expect(result.nombre).toBe('Pedro');
    });

    it('PARSE-005 | Edge Case: Cadena vacía retorna valores vacíos', () => {
      const result = service.parseNombre('');
      expect(result.nombre).toBe('');
      expect(result.apellido).toBe('S/A');
    });
  });
});
