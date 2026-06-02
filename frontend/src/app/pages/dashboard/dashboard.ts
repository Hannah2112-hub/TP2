import { Component, signal, computed, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { AcademicService } from '../../services/academic.service';
import {
  Estudiante,
  Docente,
  Curso,
  Aula,
  Matricula,
  AsignacionHorario,
} from '../../models/modelos';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class DashboardComponent implements OnInit {
  currentPage = signal('dashboard');

  // Formulario: Carrera
  carNombre   = signal('');
  carFacultad = signal('');

  // Formulario: Estudiante
  estNombre   = signal('');
  estCodigo   = signal('');
  estCreditos = signal(0);
  estCorreo   = signal('');

  // Formulario: Docente
  docNombre  = signal('');
  docCodigo  = signal('');
  docEsp     = signal('');
  docCorreo  = signal('');

  // Formulario: Curso
  curNombre    = signal('');
  curCodigo    = signal('');
  curCreditos  = signal(0);
  curPrereq    = signal('');
  curDocente   = signal('');
  curCarrera   = signal('');
  curCupos     = signal(30);

  // Formulario: Aula
  aulaNombre   = signal('');
  aulaCap      = signal(40);
  aulaEdificio = signal('');
  aulaEquip    = signal('');

  // Formulario: Matrícula
  matEstudiante = signal('');
  matCurso      = signal('');

  // Formulario: Horarios Automáticos
  horCarrera = signal('');
  horInicio = signal(9);
  horBloque = signal(2);
  oferCurso  = signal('');
  oferAula   = signal('');
  oferDia    = signal(1);
  oferHoraI  = signal('08:00');
  oferHoraF  = signal('10:00');

  // Mensajes de feedback
  mensaje     = signal('');
  mensajeTipo = signal<'success' | 'error' | 'info'>('info');
  cargando    = signal(false);

  // Stats del dashboard
  stats = signal<Record<string, number>>({});

  // Datos reactivos desde el service
  carreras    = computed(() => this.academicService.Carreras());
  docentes    = computed(() => this.academicService.Docentes());
  cursos      = computed(() => this.academicService.Cursos());
  estudiantes = computed(() => this.academicService.Estudiantes());
  aulas       = computed(() => this.academicService.Aulas());
  matriculas  = computed(() => this.academicService.Matriculas());
  horario     = computed(() => this.academicService.HorarioGenerado());

  diasSemana  = [
    { id: 1, nombre: 'Lunes' },
    { id: 2, nombre: 'Martes' },
    { id: 3, nombre: 'Miércoles' },
    { id: 4, nombre: 'Jueves' },
    { id: 5, nombre: 'Viernes' },
    { id: 6, nombre: 'Sábado' }
  ];

  dias    = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'];
  colores = ['hc-purple', 'hc-teal', 'hc-blue', 'hc-amber', 'hc-coral', 'hc-green'];

  constructor(
    public auth: AuthService,
    public academicService: AcademicService,
  ) {}

  async ngOnInit() {
    await this.refreshStats();
  }

  navigate(page: string) {
    this.currentPage.set(page);
  }

  logout() {
    this.auth.logout();
  }

  showMsg(txt: string, type: 'success' | 'error' | 'info') {
    this.mensaje.set(txt);
    this.mensajeTipo.set(type);
    setTimeout(() => this.mensaje.set(''), 4000);
  }

  pad(n: number): string {
    return n < 10 ? '0' + n : n.toString();
  }

  async refreshStats() {
    const s = await this.academicService.getEstadisticas();
    this.stats.set(s);
  }

  // ── CARRERAS ──────────────────────────────────────────────────────────────
  async registrarCarrera() {
    if (!this.carNombre() || !this.carFacultad()) {
      this.showMsg('Nombre y facultad son requeridos', 'error');
      return;
    }
    this.cargando.set(true);
    const ok = await this.academicService.agregarCarrera({
      nombre:   this.carNombre(),
      facultad: this.carFacultad(),
    });
    this.cargando.set(false);
    if (ok) {
      this.showMsg('Carrera registrada correctamente', 'success');
      this.carNombre.set(''); this.carFacultad.set('');
      await this.refreshStats();
    } else {
      this.showMsg('Error al registrar la carrera', 'error');
    }
  }

  async eliminarCarrera(item: any) {
    const id = item.id ?? item;
    await this.academicService.eliminarCarrera(id);
    await this.refreshStats();
  }

  // ── ESTUDIANTES ────────────────────────────────────────────────────────────
  async registrarEstudiante() {
    if (!this.estNombre() || !this.estCodigo()) {
      this.showMsg('Nombre y código son requeridos', 'error');
      return;
    }
    this.cargando.set(true);
    const ok = await this.academicService.agregarEstudiante({
      codigo:   this.estCodigo(),
      nombre:   this.estNombre(),
      creditos: this.estCreditos(),
      correo:   this.estCorreo(),
    });
    this.cargando.set(false);
    if (ok) {
      this.showMsg('Estudiante registrado correctamente', 'success');
      this.estNombre.set(''); this.estCodigo.set(''); this.estCorreo.set(''); this.estCreditos.set(0);
      await this.refreshStats();
    } else {
      this.showMsg('Error al registrar el estudiante', 'error');
    }
  }

  async eliminarEstudiante(item: any) {
    const id = item.id ?? item;
    await this.academicService.eliminarEstudiante(id);
    await this.refreshStats();
  }

  // ── DOCENTES ───────────────────────────────────────────────────────────────
  async registrarDocente() {
    if (!this.docNombre() || !this.docCodigo()) {
      this.showMsg('Nombre y código son requeridos', 'error');
      return;
    }
    this.cargando.set(true);
    const ok = await this.academicService.agregarDocente({
      codigo:       this.docCodigo(),
      nombre:       this.docNombre(),
      especialidad: this.docEsp(),
      correo:       this.docCorreo(),
    });
    this.cargando.set(false);
    if (ok) {
      this.showMsg('Docente registrado correctamente', 'success');
      this.docNombre.set(''); this.docCodigo.set(''); this.docEsp.set(''); this.docCorreo.set('');
      await this.refreshStats();
    } else {
      this.showMsg('Error al registrar el docente', 'error');
    }
  }

  async eliminarDocente(item: any) {
    const id = item.id ?? item;
    await this.academicService.eliminarDocente(id);
    await this.refreshStats();
  }

  // ── CURSOS ─────────────────────────────────────────────────────────────────
  async registrarCurso() {
    if (!this.curNombre() || !this.curCodigo()) {
      this.showMsg('Nombre y código son requeridos', 'error');
      return;
    }
    this.cargando.set(true);
    const ok = await this.academicService.agregarCurso({
      codigo:   this.curCodigo(),
      nombre:   this.curNombre(),
      creditos: this.curCreditos(),
      prereq:   this.curPrereq(),
      docente:  this.curDocente(),
      carrera:  this.curCarrera(),
      cupos:    this.curCupos(),
    });
    this.cargando.set(false);
    if (ok) {
      this.showMsg('Curso registrado correctamente', 'success');
      this.curNombre.set(''); this.curCodigo.set(''); this.curPrereq.set(''); this.curDocente.set(''); this.curCarrera.set('');
      await this.refreshStats();
    } else {
      this.showMsg('Error al registrar el curso', 'error');
    }
  }

  async eliminarCurso(item: any) {
    const id = item.id ?? item;
    await this.academicService.eliminarCurso(id);
    await this.refreshStats();
  }

  // ── AULAS ──────────────────────────────────────────────────────────────────
  async registrarAula() {
    if (!this.aulaNombre()) {
      this.showMsg('El nombre es requerido', 'error');
      return;
    }
    this.cargando.set(true);
    const ok = await this.academicService.agregarAula({
      nombre:       this.aulaNombre(),
      capacidad:    this.aulaCap(),
      edificio:     this.aulaEdificio(),
      equipamiento: this.aulaEquip(),
    });
    this.cargando.set(false);
    if (ok) {
      this.showMsg('Aula registrada correctamente', 'success');
      this.aulaNombre.set(''); this.aulaEdificio.set(''); this.aulaEquip.set(''); this.aulaCap.set(40);
      await this.refreshStats();
    } else {
      this.showMsg('Error al registrar el aula', 'error');
    }
  }

  async eliminarAula(item: any) {
    const id = item.id ?? item;
    await this.academicService.eliminarAula(id);
    await this.refreshStats();
  }

  // ── MATRÍCULA ──────────────────────────────────────────────────────────────
  async validarMatricula() {
    const estudianteId = Number(this.matEstudiante());
    const cursoId      = Number(this.matCurso());

    if (!estudianteId || !cursoId) {
      this.showMsg('Seleccione estudiante y curso', 'error');
      return;
    }
    this.cargando.set(true);
    const { ok, mensaje } = await this.academicService.agregarMatricula(estudianteId, cursoId);
    this.cargando.set(false);
    this.showMsg(mensaje, ok ? 'success' : 'error');
    if (ok) { this.matEstudiante.set(''); this.matCurso.set(''); }
  }

  // ── HORARIOS ───────────────────────────────────────────────────────────────
  async generarHorarios() {
    if (this.academicService.Cursos().length === 0) {
      this.showMsg('No hay cursos registrados', 'error');
      return;
    }
    this.cargando.set(true);
    const carreraId = this.horCarrera() ? Number(this.horCarrera()) : undefined;
    const { ok, mensaje } = await this.academicService.generarHorarios(
      Number(this.horInicio()),
      Number(this.horBloque()),
      carreraId
    );
    this.cargando.set(false);
    this.showMsg(mensaje, ok ? 'success' : 'error');
  }

  async registrarOfertaHoraria() {
    const cId = Number(this.oferCurso());
    const aId = Number(this.oferAula());
    const d   = Number(this.oferDia());
    const hI  = this.oferHoraI();
    const hF  = this.oferHoraF();

    if (!cId || !aId || !d || !hI || !hF) {
      this.showMsg('Complete todos los campos del horario', 'error');
      return;
    }
    
    this.cargando.set(true);
    const { ok, mensaje } = await this.academicService.agregarHorario(cId, aId, d, hI, hF);
    this.cargando.set(false);
    this.showMsg(mensaje, ok ? 'success' : 'error');
    if (ok) {
      this.oferCurso.set(''); this.oferAula.set('');
    }
  }

  getHoras(): number[] {
    const h = this.academicService.HorarioGenerado();
    if (h.length === 0) return [];
    const maxHora = Math.max(...h.map((a) => a.horaFin));
    const inicio  = Number(this.horInicio());
    const bloque  = Number(this.horBloque());
    const horas: number[] = [];
    for (let i = inicio; i < maxHora; i += bloque) horas.push(i);
    return horas;
  }

  getClases(dia: string, hora: number): AsignacionHorario[] {
    const selectedCarrera = this.horCarrera() ? Number(this.horCarrera()) : null;
    return this.academicService
      .HorarioGenerado()
      .filter((a) => {
        if (selectedCarrera && a.carreraId !== selectedCarrera) return false;
        return a.dia === dia && a.horaInicio <= hora && a.horaFin > hora;
      });
  }
}
