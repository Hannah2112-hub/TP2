import { describe, it, expect, vi, beforeEach } from 'vitest';
import { LoginComponent } from '../app/pages/login/login';
import { AuthService } from '../app/services/auth.service';

function createComponent() {
  const mockRouter = { navigate: vi.fn() };
  const auth = new AuthService(mockRouter as any);
  const component = new LoginComponent(auth as any, mockRouter as any);
  return { component, auth, router: mockRouter };
}

describe('LoginComponent - Pruebas de Clase', () => {
  let component: LoginComponent;
  let auth: AuthService;
  let router: { navigate: ReturnType<typeof vi.fn> };

  beforeEach(() => {
    localStorage.clear();
    const ctx = createComponent();
    component = ctx.component;
    auth = ctx.auth;
    router = ctx.router;
  });

  // ─── Estado inicial ──────────────────────────────────────────────────

  describe('Estado Inicial', () => {
    it('RENDER-001 | Componente se inicializa correctamente', () => {
      expect(component).toBeTruthy();
    });

    it('RENDER-002 | tipoUsuario inicia como admin', () => {
      expect(component.tipoUsuario()).toBe('admin');
    });

    it('RENDER-003 | showError inicia como false', () => {
      expect(component.showError()).toBe(false);
    });

    it('RENDER-004 | errorMessage inicia vacio', () => {
      expect(component.errorMessage()).toBe('');
    });

    it('RENDER-005 | email y password inician vacios', () => {
      expect(component.email()).toBe('');
      expect(component.password()).toBe('');
    });
  });

  // ─── Signals y reactividad ────────────────────────────────────────────

  describe('Signals y Reactividad', () => {
    it('SIGNAL-001 | selectType cambia a docente', () => {
      component.selectType('docente');
      expect(component.tipoUsuario()).toBe('docente');
    });

    it('SIGNAL-002 | selectType cambia a estudiante', () => {
      component.selectType('estudiante');
      expect(component.tipoUsuario()).toBe('estudiante');
    });

    it('SIGNAL-003 | selectType alterna entre tipos', () => {
      component.selectType('docente');
      component.selectType('admin');
      expect(component.tipoUsuario()).toBe('admin');
      component.selectType('estudiante');
      expect(component.tipoUsuario()).toBe('estudiante');
    });

    it('SIGNAL-004 | email signal se actualiza con set', () => {
      component.email.set('test@uni.edu');
      expect(component.email()).toBe('test@uni.edu');
    });

    it('SIGNAL-005 | password signal se actualiza con set', () => {
      component.password.set('secret123');
      expect(component.password()).toBe('secret123');
    });
  });

  // ─── Flujo de autenticación ────────────────────────────────────────────

  describe('Flujo de Autenticación', () => {
    it('LOGIN-001 | Login exitoso establece isLoggedIn en AuthService', () => {
      component.email.set('admin@uni.edu');
      component.password.set('admin123');
      component.login();
      expect(auth.isLoggedIn()).toBe(true);
    });

    it('LOGIN-002 | Login exitoso navega a /dashboard', () => {
      component.login();
      expect(router.navigate).toHaveBeenCalledWith(['/dashboard']);
    });

    it('LOGIN-003 | Login establece currentUserType como admin', () => {
      component.login();
      expect(auth.currentUserType()).toBe('admin');
    });
  });

  // ─── Manejo de errores ────────────────────────────────────────────────

  describe('Manejo de Errores', () => {
    it('ERROR-001 | showError se activa cuando login falla', () => {
      vi.spyOn(auth, 'login').mockReturnValue(false);
      component.login();
      expect(component.showError()).toBe(true);
    });

    it('ERROR-002 | Mensaje de error correcto', () => {
      vi.spyOn(auth, 'login').mockReturnValue(false);
      component.login();
      expect(component.errorMessage()).toBe('Credenciales incorrectas. Intenta de nuevo.');
    });

    it('ERROR-003 | showError permanece false con login exitoso', () => {
      component.login();
      expect(component.showError()).toBe(false);
    });
  });

  // ─── Operaciones asincrónicas ──────────────────────────────────────────

  describe('Operaciones Asincrónicas', () => {
    it('ASYNC-001 | Error se oculta tras 4 segundos (fake timers)', () => {
      vi.useFakeTimers();
      vi.spyOn(auth, 'login').mockReturnValue(false);
      component.login();
      expect(component.showError()).toBe(true);
      vi.advanceTimersByTime(4000);
      expect(component.showError()).toBe(false);
      vi.useRealTimers();
    });

    it('ASYNC-002 | Timeout no se activa si nunca hubo error', () => {
      vi.useFakeTimers();
      component.login();
      expect(component.showError()).toBe(false);
      vi.advanceTimersByTime(4000);
      expect(component.showError()).toBe(false);
      vi.useRealTimers();
    });
  });

  // ─── Casos límite ──────────────────────────────────────────────────────

  describe('Casos Limite', () => {
    it('LIMIT-001 | Login con campos vacios funciona', () => {
      component.login();
      expect(auth.isLoggedIn()).toBe(true);
    });

    it('LIMIT-002 | selectType no lanza excepcion con cualquier valor', () => {
      expect(() => component.selectType('admin' as any)).not.toThrow();
    });

    it('LIMIT-003 | Login sin email funciona igual', () => {
      component.password.set('pass');
      component.login();
      expect(auth.isLoggedIn()).toBe(true);
    });
  });

  // ─── Integración con AuthService real ──────────────────────────────────

  describe('Integración con AuthService', () => {
    it('AUTH-001 | Login integrado: isLoggedIn se actualiza', () => {
      component.login();
      expect(auth.isLoggedIn()).toBe(true);
    });

    it('AUTH-002 | Login integrado: userType se actualiza', () => {
      component.login();
      expect(auth.currentUserType()).toBe('admin');
    });

    it('AUTH-003 | Login con selectType previo actualiza tipo', () => {
      component.selectType('docente');
      component.login();
      expect(auth.currentUserType()).toBe('docente');
    });
  });
});
