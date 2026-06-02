import { describe, it, expect, vi, beforeEach } from 'vitest';
import { of } from 'rxjs';
import { DashboardComponent } from '../app/pages/dashboard/dashboard';
import { AuthService } from '../app/services/auth.service';
import { AcademicService } from '../app/services/academic.service';

function createDashboard() {
  const mockRouter = { navigate: vi.fn() };
  const auth = new AuthService(mockRouter as any);
  const http = { get: vi.fn().mockReturnValue(of({ success: true, data: [] })), post: vi.fn().mockReturnValue(of({ success: true })), delete: vi.fn().mockReturnValue(of({})) };
  const academic = new AcademicService(http as any);
  const component = new DashboardComponent(auth, academic);
  return { component, auth, academic, http };
}

describe('DashboardComponent - Pruebas de Clase', () => {
  let ctx: ReturnType<typeof createDashboard>;
  let component: DashboardComponent;
  let academic: AcademicService;

  beforeEach(() => {
    vi.restoreAllMocks();
    ctx = createDashboard();
    component = ctx.component;
    academic = ctx.academic;
  });

  it('RENDER-001 | Componente se inicializa', () => expect(component).toBeTruthy());
  it('RENDER-002 | currentPage inicia como dashboard', () => expect(component.currentPage()).toBe('dashboard'));
  it('RENDER-003 | cargando inicia como false', () => expect(component.cargando()).toBe(false));
  it('RENDER-004 | mensaje inicia vacio', () => expect(component.mensaje()).toBe(''));
  it('RENDER-005 | stats inicia vacio', () => expect(component.stats()).toEqual({}));

  describe('Navegación', () => {
    it('NAV-001 | navigate cambia pagina', () => { component.navigate('estudiantes'); expect(component.currentPage()).toBe('estudiantes'); });
    it('NAV-002 | navigate a dashboard', () => { component.navigate('cursos'); component.navigate('dashboard'); expect(component.currentPage()).toBe('dashboard'); });
  });

  describe('Logout', () => {
    it('LOGOUT-001 | logout llama auth.logout', () => { const spy = vi.spyOn(ctx.auth, 'logout'); component.logout(); expect(spy).toHaveBeenCalledOnce(); });
  });

  describe('Mensajes', () => {
    it('MSG-001 | showMsg success', () => { component.showMsg('OK', 'success'); expect(component.mensaje()).toBe('OK'); expect(component.mensajeTipo()).toBe('success'); });
    it('MSG-002 | showMsg error', () => { component.showMsg('Fail', 'error'); expect(component.mensajeTipo()).toBe('error'); });
    it('MSG-003 | Mensaje se borra tras 4s', () => { vi.useFakeTimers(); component.showMsg('tmp', 'info'); vi.advanceTimersByTime(4000); expect(component.mensaje()).toBe(''); vi.useRealTimers(); });
  });

  describe('Helpers', () => {
    it('PAD-001 | pad(5) = "05"', () => expect(component.pad(5)).toBe('05'));
    it('PAD-002 | pad(10) = "10"', () => expect(component.pad(10)).toBe('10'));
    it('PAD-003 | pad(0) = "00"', () => expect(component.pad(0)).toBe('00'));
  });

  describe('Carreras', () => {
    it('CRUD-CAR-001 | registrarCarrera sin datos muestra error', async () => { await component.registrarCarrera(); expect(component.mensajeTipo()).toBe('error'); });
    it('CRUD-CAR-002 | registrarCarrera exitoso', async () => { component.carNombre.set('Ing'); component.carFacultad.set('Fac'); await component.registrarCarrera(); expect(component.mensaje()).toBe('Carrera registrada correctamente'); });
    it('CRUD-CAR-003 | registrarCarrera con fallo de API', async () => { vi.spyOn(academic, 'agregarCarrera').mockResolvedValue(false); component.carNombre.set('X'); component.carFacultad.set('Y'); await component.registrarCarrera(); expect(component.mensajeTipo()).toBe('error'); });
    it('CRUD-CAR-004 | eliminarCarrera con objeto', async () => { const spy = vi.spyOn(academic, 'eliminarCarrera').mockResolvedValue(undefined); await component.eliminarCarrera({ id: 1 }); expect(spy).toHaveBeenCalledWith(1); });
    it('CRUD-CAR-005 | eliminarCarrera con ID directo', async () => { const spy = vi.spyOn(academic, 'eliminarCarrera').mockResolvedValue(undefined); await component.eliminarCarrera(2); expect(spy).toHaveBeenCalledWith(2); });
  });

  describe('Estudiantes', () => {
    it('CRUD-EST-001 | registrarEstudiante validacion falla', async () => { await component.registrarEstudiante(); expect(component.mensajeTipo()).toBe('error'); });
    it('CRUD-EST-002 | registrarEstudiante exitoso', async () => { component.estNombre.set('Ana'); component.estCodigo.set('E001'); await component.registrarEstudiante(); expect(component.mensaje()).toBe('Estudiante registrado correctamente'); });
    it('CRUD-EST-003 | registrarEstudiante fallo API', async () => { vi.spyOn(academic, 'agregarEstudiante').mockResolvedValue(false); component.estNombre.set('Luis'); component.estCodigo.set('E002'); await component.registrarEstudiante(); expect(component.mensajeTipo()).toBe('error'); });
    it('CRUD-EST-004 | eliminarEstudiante', async () => { const spy = vi.spyOn(academic, 'eliminarEstudiante').mockResolvedValue(undefined); await component.eliminarEstudiante({ id: 5 }); expect(spy).toHaveBeenCalledWith(5); });
  });

  describe('Docentes', () => {
    it('CRUD-DOC-001 | registrarDocente validacion falla', async () => { await component.registrarDocente(); expect(component.mensajeTipo()).toBe('error'); });
    it('CRUD-DOC-002 | registrarDocente exitoso', async () => { component.docNombre.set('Carlos'); component.docCodigo.set('D001'); await component.registrarDocente(); expect(component.mensaje()).toBe('Docente registrado correctamente'); });
    it('CRUD-DOC-003 | registrarDocente fallo API', async () => { vi.spyOn(academic, 'agregarDocente').mockResolvedValue(false); component.docNombre.set('X'); component.docCodigo.set('D002'); await component.registrarDocente(); expect(component.mensajeTipo()).toBe('error'); });
    it('CRUD-DOC-004 | eliminarDocente', async () => { const spy = vi.spyOn(academic, 'eliminarDocente').mockResolvedValue(undefined); await component.eliminarDocente(3); expect(spy).toHaveBeenCalledWith(3); });
  });

  describe('Cursos', () => {
    it('CRUD-CUR-001 | registrarCurso validacion falla', async () => { await component.registrarCurso(); expect(component.mensajeTipo()).toBe('error'); });
    it('CRUD-CUR-002 | registrarCurso exitoso', async () => { component.curNombre.set('Algebra'); component.curCodigo.set('C001'); await component.registrarCurso(); expect(component.mensaje()).toBe('Curso registrado correctamente'); });
    it('CRUD-CUR-003 | registrarCurso fallo API', async () => { vi.spyOn(academic, 'agregarCurso').mockResolvedValue(false); component.curNombre.set('X'); component.curCodigo.set('C002'); await component.registrarCurso(); expect(component.mensajeTipo()).toBe('error'); });
    it('CRUD-CUR-004 | eliminarCurso', async () => { const spy = vi.spyOn(academic, 'eliminarCurso').mockResolvedValue(undefined); await component.eliminarCurso(1); expect(spy).toHaveBeenCalledWith(1); });
  });

  describe('Aulas', () => {
    it('CRUD-AUL-001 | registrarAula validacion falla', async () => { await component.registrarAula(); expect(component.mensajeTipo()).toBe('error'); });
    it('CRUD-AUL-002 | registrarAula exitoso', async () => { component.aulaNombre.set('A-101'); await component.registrarAula(); expect(component.mensaje()).toBe('Aula registrada correctamente'); });
    it('CRUD-AUL-003 | registrarAula fallo API', async () => { vi.spyOn(academic, 'agregarAula').mockResolvedValue(false); component.aulaNombre.set('X'); await component.registrarAula(); expect(component.mensajeTipo()).toBe('error'); });
    it('CRUD-AUL-004 | eliminarAula', async () => { const spy = vi.spyOn(academic, 'eliminarAula').mockResolvedValue(undefined); await component.eliminarAula(3); expect(spy).toHaveBeenCalledWith(3); });
  });

  describe('Matricula', () => {
    it('MAT-001 | validarMatricula sin IDs muestra error', async () => { await component.validarMatricula(); expect(component.mensajeTipo()).toBe('error'); });
    it('MAT-002 | validarMatricula exitoso', async () => { component.matEstudiante.set('1'); component.matCurso.set('2'); await component.validarMatricula(); expect(component.mensaje()).toBeTruthy(); });
  });

  describe('Horarios', () => {
    it('HOR-001 | generarHorarios sin cursos muestra error', async () => { await component.generarHorarios(); expect(component.mensajeTipo()).toBe('error'); });
    it('HOR-002 | registrarOfertaHoraria sin datos muestra error', async () => { await component.registrarOfertaHoraria(); expect(component.mensajeTipo()).toBe('error'); });
  });

  describe('Async', () => {
    it('ASYNC-001 | refreshStats llama getEstadisticas', async () => { const spy = vi.spyOn(academic, 'getEstadisticas').mockResolvedValue({}); await component.refreshStats(); expect(spy).toHaveBeenCalledOnce(); });
    it('ASYNC-002 | ngOnInit llama refreshStats', async () => { const spy = vi.spyOn(component, 'refreshStats').mockResolvedValue(undefined); await component.ngOnInit(); expect(spy).toHaveBeenCalledOnce(); });
  });

  describe('getHoras', () => {
    it('HORAS-001 | getHoras sin horarios retorna []', () => { expect(component.getHoras()).toEqual([]); });
    it('HORAS-002 | getHoras con horarios retorna horas', () => {
      vi.spyOn(academic, 'HorarioGenerado', 'get').mockReturnValue(vi.fn(() => [
        { horaInicio: 8, horaFin: 12, dia: 'Lunes', curso: 'Algebra', aula: 'A101', docente: 'Dr. Perez', color: 'hc-blue', id: 1, carreraId: 1 }
      ]));
      component.horInicio.set(8);
      component.horBloque.set(2);
      const horas = component.getHoras();
      expect(horas.length).toBeGreaterThan(0);
      expect(horas).toContain(8);
      expect(horas).toContain(10);
    });
  });

  describe('getClases', () => {
    it('CLASES-001 | getClases sin carrera filtrada', () => {
      vi.spyOn(academic, 'HorarioGenerado', 'get').mockReturnValue(vi.fn(() => [
        { horaInicio: 8, horaFin: 10, dia: 'Lunes', curso: 'Algebra', aula: 'A101', docente: 'Dr. Perez', color: 'hc-blue', id: 1, carreraId: 1 }
      ]));
      component.horCarrera.set('');
      const clases = component.getClases('Lunes', 8);
      expect(clases.length).toBe(1);
      expect(clases[0].curso).toBe('Algebra');
    });
    it('CLASES-002 | getClases con filtro de carrera', () => {
      vi.spyOn(academic, 'HorarioGenerado', 'get').mockReturnValue(vi.fn(() => [
        { horaInicio: 8, horaFin: 10, dia: 'Lunes', curso: 'Algebra', aula: 'A101', docente: 'Dr. Perez', color: 'hc-blue', id: 1, carreraId: 1 },
        { horaInicio: 8, horaFin: 10, dia: 'Lunes', curso: 'Calculo', aula: 'A102', docente: 'Dr. Gomez', color: 'hc-teal', id: 2, carreraId: 2 }
      ]));
      component.horCarrera.set('1');
      const clases = component.getClases('Lunes', 8);
      expect(clases.length).toBe(1);
      expect(clases[0].curso).toBe('Algebra');
    });
    it('CLASES-003 | getClases sin coincidencias retorna []', () => {
      vi.spyOn(academic, 'HorarioGenerado', 'get').mockReturnValue(vi.fn(() => []));
      const clases = component.getClases('Lunes', 10);
      expect(clases).toEqual([]);
    });
    it('CLASES-004 | getClases con carrera string vacio muestra todas', () => {
      vi.spyOn(academic, 'HorarioGenerado', 'get').mockReturnValue(vi.fn(() => [
        { horaInicio: 8, horaFin: 10, dia: 'Martes', curso: 'Fisica', aula: 'A103', docente: 'Dr. Ruiz', color: 'hc-amber', id: 3, carreraId: 2 }
      ]));
      component.horCarrera.set('');
      const clases = component.getClases('Martes', 8);
      expect(clases.length).toBe(1);
    });
  });

  describe('Horarios success', () => {
    it('HOR-SUCCESS-001 | generarHorarios exitoso', async () => {
      vi.spyOn(academic, 'Cursos', 'get').mockReturnValue(vi.fn(() => [{ id: 1 }] as any));
      vi.spyOn(academic, 'generarHorarios').mockResolvedValue({ ok: true, mensaje: 'Horarios generados' });
      component.horInicio.set(8);
      component.horBloque.set(2);
      component.horCarrera.set('1');
      await component.generarHorarios();
      expect(component.mensaje()).toBe('Horarios generados');
      expect(component.mensajeTipo()).toBe('success');
    });
    it('HOR-SUCCESS-002 | registrarOfertaHoraria exitoso', async () => {
      vi.spyOn(academic, 'agregarHorario').mockResolvedValue({ ok: true, mensaje: 'Horario registrado' });
      component.oferCurso.set('1');
      component.oferAula.set('2');
      component.oferDia.set('1');
      component.oferHoraI.set('08:00');
      component.oferHoraF.set('10:00');
      await component.registrarOfertaHoraria();
      expect(component.mensaje()).toBe('Horario registrado');
      expect(component.mensajeTipo()).toBe('success');
    });
  });

  describe('cargando signal', () => {
    it('CARG-001 | cargando se activa durante generarHorarios', async () => {
      vi.spyOn(academic, 'Cursos', 'get').mockReturnValue(vi.fn(() => [{ id: 1 }] as any));
      vi.spyOn(academic, 'generarHorarios').mockImplementation(async () => {
        expect(component.cargando()).toBe(true);
        return { ok: true, mensaje: 'OK' };
      });
      await component.generarHorarios();
      expect(component.cargando()).toBe(false);
    });
  });

  describe('Form reset', () => {
    it('RESET-001 | registrarCurso exitoso resetea campos', async () => {
      vi.spyOn(academic, 'agregarCurso').mockResolvedValue(true);
      component.curNombre.set('Test');
      component.curCodigo.set('T001');
      await component.registrarCurso();
      expect(component.curNombre()).toBe('');
      expect(component.curCodigo()).toBe('');
    });
  });
});
