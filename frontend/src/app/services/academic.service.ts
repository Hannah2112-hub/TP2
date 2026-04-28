import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import {
  Estudiante,
  Docente,
  Curso,
  Aula,
  Matricula,
  AsignacionHorario,
} from '../models/modelos';

const API = 'http://127.0.0.1:8000/api';

interface ApiResponse<T = any> {
  success: boolean;
  message?: string;
  data?: T;
}

@Injectable({
  providedIn: 'root',
})
export class AcademicService {
  // ── Signals reactivos (fuente de verdad para la UI) ──────────────────────
  private estudiantes = signal<Estudiante[]>([]);
  private docentes    = signal<Docente[]>([]);
  private cursos      = signal<Curso[]>([]);
  private aulas       = signal<Aula[]>([]);
  private matriculas  = signal<Matricula[]>([]);
  private horarioGenerado = signal<AsignacionHorario[]>([]);
  private dashboardMetrics = signal<Record<string, number>>({});

  private colores = ['hc-purple', 'hc-teal', 'hc-blue', 'hc-amber', 'hc-coral', 'hc-green'];
  private diasNombres = ['', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'];

  constructor(private http: HttpClient) {
    this.cargarTodo();
  }

  // ── Getters readonly ──────────────────────────────────────────────────────
  get Estudiantes()     { return this.estudiantes.asReadonly(); }
  get Docentes()        { return this.docentes.asReadonly(); }
  get Cursos()          { return this.cursos.asReadonly(); }
  get Aulas()           { return this.aulas.asReadonly(); }
  get Matriculas()      { return this.matriculas.asReadonly(); }
  get HorarioGenerado() { return this.horarioGenerado.asReadonly(); }

  // ── Carga inicial ─────────────────────────────────────────────────────────
  async cargarTodo() {
    await Promise.all([
      this.cargarEstudiantes(),
      this.cargarDocentes(),
      this.cargarCursos(),
      this.cargarAulas(),
      this.cargarMatriculas(),
      this.cargarHorarios(),
    ]);
  }

  // ── ESTUDIANTES ───────────────────────────────────────────────────────────
  async cargarEstudiantes() {
    try {
      const res = await firstValueFrom(
        this.http.get<ApiResponse<any[]>>(`${API}/estudiantes`)
      );
      if (res.success && res.data) {
        this.estudiantes.set(res.data.map((e: any) => ({
          id:       e.estudianteid,
          codigo:   e.codigo,
          nombre:   `${e.nombre} ${e.apellido}`,
          creditos: e.creditosacum ?? 0,
          correo:   e.correo,
        })));
      }
    } catch (e) { console.error('Error cargando estudiantes:', e); }
  }

  async agregarEstudiante(est: Estudiante): Promise<boolean> {
    const partes = est.nombre.trim().split(' ');
    const nombre   = partes[0] ?? '';
    const apellido = partes.slice(1).join(' ') || 'S/A';
    try {
      const res = await firstValueFrom(
        this.http.post<ApiResponse>(`${API}/estudiantes`, {
          codigo:       est.codigo,
          nombre,
          apellido,
          correo:       est.correo,
          creditosAcum: est.creditos,
        })
      );
      if (res.success) { await this.cargarEstudiantes(); return true; }
      return false;
    } catch (e) { console.error('Error registrando estudiante:', e); return false; }
  }

  async eliminarEstudiante(id: number) {
    try {
      await firstValueFrom(this.http.delete(`${API}/estudiantes/${id}`));
      await this.cargarEstudiantes();
    } catch (e) { console.error('Error eliminando estudiante:', e); }
  }

  // ── DOCENTES ──────────────────────────────────────────────────────────────
  async cargarDocentes() {
    try {
      const res = await firstValueFrom(
        this.http.get<ApiResponse<any[]>>(`${API}/docentes`)
      );
      if (res.success && res.data) {
        this.docentes.set(res.data.map((d: any) => ({
          id:           d.docenteid,
          codigo:       d.codigo,
          nombre:       `${d.nombre} ${d.apellido}`,
          especialidad: d.especialidad ?? '',
          correo:       d.correo,
        })));
      }
    } catch (e) { console.error('Error cargando docentes:', e); }
  }

  async agregarDocente(doc: Docente): Promise<boolean> {
    const partes   = doc.nombre.trim().split(' ');
    const nombre   = partes[0] ?? '';
    const apellido = partes.slice(1).join(' ') || 'S/A';
    try {
      const res = await firstValueFrom(
        this.http.post<ApiResponse>(`${API}/docentes`, {
          codigo:       doc.codigo,
          nombre,
          apellido,
          especialidad: doc.especialidad,
          correo:       doc.correo,
        })
      );
      if (res.success) { await this.cargarDocentes(); return true; }
      return false;
    } catch (e) { console.error('Error registrando docente:', e); return false; }
  }

  async eliminarDocente(id: number) {
    try {
      await firstValueFrom(this.http.delete(`${API}/docentes/${id}`));
      await this.cargarDocentes();
    } catch (e) { console.error('Error eliminando docente:', e); }
  }

  // ── CURSOS ────────────────────────────────────────────────────────────────
  async cargarCursos() {
    try {
      const res = await firstValueFrom(
        this.http.get<ApiResponse<any[]>>(`${API}/cursos`)
      );
      if (res.success && res.data) {
        this.cursos.set(res.data.map((c: any) => ({
          id:       c.cursoid,
          codigo:   c.codigo,
          nombre:   c.nombre,
          creditos: c.creditosreq ?? 0,
          prereq:   c.prerequisitoid ? String(c.prerequisitoid) : '',
          docente:  c.docenteid ? String(c.docenteid) : '',
          cupos:    c.cupos ?? 30,
          nombreDocente: c.nombredocente ?? '',
        })));
      }
    } catch (e) { console.error('Error cargando cursos:', e); }
  }

  async agregarCurso(curso: Curso): Promise<boolean> {
    try {
      const res = await firstValueFrom(
        this.http.post<ApiResponse>(`${API}/cursos`, {
          codigo:        curso.codigo,
          nombre:        curso.nombre,
          creditosReq:   curso.creditos,
          prerequisitoID: curso.prereq ? Number(curso.prereq) : null,
          docenteID:     curso.docente ? Number(curso.docente) : null,
          cupos:         curso.cupos,
        })
      );
      if (res.success) { await this.cargarCursos(); return true; }
      return false;
    } catch (e) { console.error('Error registrando curso:', e); return false; }
  }

  async eliminarCurso(id: number) {
    try {
      await firstValueFrom(this.http.delete(`${API}/cursos/${id}`));
      await this.cargarCursos();
    } catch (e) { console.error('Error eliminando curso:', e); }
  }

  // ── AULAS ─────────────────────────────────────────────────────────────────
  async cargarAulas() {
    try {
      const res = await firstValueFrom(
        this.http.get<ApiResponse<any[]>>(`${API}/aulas`)
      );
      if (res.success && res.data) {
        this.aulas.set(res.data.map((a: any) => ({
          id:           a.aulaid,
          nombre:       a.nombre,
          capacidad:    a.capacidad ?? 0,
          edificio:     a.edificio ?? '',
          equipamiento: a.equipamiento ?? '',
        })));
      }
    } catch (e) { console.error('Error cargando aulas:', e); }
  }

  async agregarAula(aula: Aula): Promise<boolean> {
    try {
      const res = await firstValueFrom(
        this.http.post<ApiResponse>(`${API}/aulas`, {
          nombre:       aula.nombre,
          capacidad:    aula.capacidad,
          edificio:     aula.edificio,
          equipamiento: aula.equipamiento,
        })
      );
      if (res.success) { await this.cargarAulas(); return true; }
      return false;
    } catch (e) { console.error('Error registrando aula:', e); return false; }
  }

  async eliminarAula(id: number) {
    try {
      await firstValueFrom(this.http.delete(`${API}/aulas/${id}`));
      await this.cargarAulas();
    } catch (e) { console.error('Error eliminando aula:', e); }
  }

  // ── MATRÍCULAS ────────────────────────────────────────────────────────────
  async cargarMatriculas() {
    try {
      const res = await firstValueFrom(
        this.http.get<ApiResponse<any[]>>(`${API}/matriculas`)
      );
      if (res.success && res.data) {
        this.matriculas.set(res.data.map((m: any) => ({
          id:         m.matriculaid,
          estudiante: String(m.estudianteid),
          curso:      String(m.cursoid),
          estado:     m.estado,
          detalle:    m.nombreestudiante
                        ? `${m.nombreestudiante} → ${m.nombrecurso}`
                        : m.estado,
          nombreEstudiante: m.nombreestudiante ?? '',
          nombreCurso:      m.nombrecurso ?? '',
        })));
      }
    } catch (e) { console.error('Error cargando matrículas:', e); }
  }

  async agregarMatricula(estudianteId: number, cursoId: number): Promise<{ ok: boolean; mensaje: string }> {
    try {
      const res = await firstValueFrom(
        this.http.post<ApiResponse>(`${API}/matriculas`, {
          estudianteID: estudianteId,
          cursoID:      cursoId,
        })
      );
      await this.cargarMatriculas();
      return { ok: res.success, mensaje: res.message ?? (res.success ? 'Matrícula registrada' : 'Error') };
    } catch (err: any) {
      const msg = err?.error?.detail ?? 'Error al conectar con el servidor';
      return { ok: false, mensaje: msg };
    }
  }

  // ── HORARIOS ──────────────────────────────────────────────────────────────
  async cargarHorarios() {
    try {
      const res = await firstValueFrom(
        this.http.get<ApiResponse<any[]>>(`${API}/horarios`)
      );
      if (res.success && res.data) {
        this.horarioGenerado.set(res.data.map((h: any, i: number) => ({
          id:         h.horarioid,
          curso:      h.nombrecurso ?? `Curso ${h.cursoid}`,
          codigo:     String(h.cursoid),
          docente:    '—',
          dia:        this.diasNombres[h.diasemana] ?? `Día ${h.diasemana}`,
          horaInicio: parseInt(h.horainicio?.split(':')[0] ?? '8', 10),
          horaFin:    parseInt(h.horafin?.split(':')[0] ?? '10', 10),
          aula:       h.nombreaula ?? `Aula ${h.aulaid}`,
          color:      this.colores[i % this.colores.length],
        })));
      }
    } catch (e) { console.error('Error cargando horarios:', e); }
  }

  async generarHorarios(inicio: number, bloque: number): Promise<{ ok: boolean; mensaje: string }> {
    const horaStr = `${String(inicio).padStart(2, '0')}:00`;
    try {
      const res = await firstValueFrom(
        this.http.post<ApiResponse>(
          `${API}/horarios/generar?hora_inicio=${horaStr}&bloques_horas=${bloque}`,
          {}
        )
      );
      await this.cargarHorarios();
      return { ok: res.success, mensaje: res.message ?? 'Horarios generados' };
    } catch (err: any) {
      const msg = err?.error?.detail ?? 'Error al generar horarios';
      return { ok: false, mensaje: msg };
    }
  }

  // ── DASHBOARD ─────────────────────────────────────────────────────────────
  async getEstadisticas(): Promise<Record<string, number>> {
    try {
      const res = await firstValueFrom(
        this.http.get<ApiResponse<Record<string, number>>>(`${API}/dashboard`)
      );
      if (res.success && res.data) {
        this.dashboardMetrics.set(res.data);
        return res.data;
      }
    } catch (e) { console.error('Error cargando dashboard:', e); }
    // Fallback con conteo local
    return {
      total_estudiantes:    this.estudiantes().length,
      total_docentes:       this.docentes().length,
      total_cursos:         this.cursos().length,
      total_aulas:          this.aulas().length,
      matriculas_aprobadas: this.matriculas().filter(m => m.estado === 'Aprobada').length,
      matriculas_rechazadas:this.matriculas().filter(m => m.estado === 'Rechazada').length,
    };
  }

  // ── Helpers para búsqueda ─────────────────────────────────────────────────
  getEstudianteByCodigo(codigo: string): Estudiante | undefined {
    return this.estudiantes().find((e) => e.codigo === codigo);
  }
  getDocenteByCodigo(codigo: string): Docente | undefined {
    return this.docentes().find((d) => d.codigo === codigo);
  }
  getCursoByCodigo(codigo: string): Curso | undefined {
    return this.cursos().find((c) => c.codigo === codigo);
  }
}
