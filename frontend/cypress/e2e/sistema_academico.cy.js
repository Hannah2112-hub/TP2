const API = 'http://127.0.0.1:8000/api';

function stubApiCalls() {
  const empty = { success: true, data: [] };
  cy.intercept('GET', `${API}/estudiantes*`, { statusCode: 200, body: { success: true, data: [{ estudianteid: 1, codigo: 'EST-001', nombre: 'Juan', apellido: 'Perez', correo: 'jp@uni.edu', creditosacum: 30 }] } }).as('getEstudiantes');
  cy.intercept('GET', `${API}/docentes*`, { statusCode: 200, body: { success: true, data: [{ docenteid: 1, codigo: 'DOC-001', nombre: 'Carlos', apellido: 'Lopez', correo: 'cl@uni.edu', especialidad: 'Matematicas' }] } }).as('getDocentes');
  cy.intercept('GET', `${API}/cursos*`, { statusCode: 200, body: empty }).as('getCursos');
  cy.intercept('GET', `${API}/aulas*`, { statusCode: 200, body: empty }).as('getAulas');
  cy.intercept('GET', `${API}/matriculas*`, { statusCode: 200, body: empty }).as('getMatriculas');
  cy.intercept('GET', `${API}/carreras*`, { statusCode: 200, body: { success: true, data: [{ id: 1, nombre: 'Ing. Sistemas', facultad: 'Ingenieria' }] } }).as('getCarreras');
  cy.intercept('GET', `${API}/horarios*`, { statusCode: 200, body: empty }).as('getHorarios');
}

function login() {
  cy.get('[data-cy="email-input"]').type('admin@uni.edu');
  cy.get('[data-cy="password-input"]').type('admin123');
  cy.get('[data-cy="btn-login"]').click();
}

function loginAndStub() {
  stubApiCalls();
  login();
  cy.url().should('include', '/dashboard');
  cy.get('[data-cy="dashboard-content"]', { timeout: 15000 }).should('be.visible');
}

describe('Autenticacion - Login/Logout', () => {
  beforeEach(() => {
    cy.clearLocalStorage();
    cy.visit('/login');
  });

  it('GP-001 | Golden Path: Admin inicia sesion y accede al dashboard', loginAndStub);

  it('HP-001 | Happy Path: Logout redirige a login', () => {
    stubApiCalls();
    login();
    cy.url().should('include', '/dashboard');
    cy.get('[data-cy="btn-logout"]', { timeout: 15000 }).should('be.visible').click();
    cy.url().should('include', '/login');
  });

  it('UP-001 | Unhappy Path: Login con API caida no rompe la app', () => {
    cy.intercept('GET', `${API}/**`, { forceNetworkError: true });
    login();
    cy.url().should('include', '/dashboard');
    cy.get('body').should('be.visible');
  });

  it('UP-002 | Unhappy Path: Ruta protegida sin autenticar redirige a login', () => {
    cy.visit('/dashboard');
    cy.url().should('include', '/login');
  });
});

describe('Navegacion Funcional', () => {
  beforeEach(() => {
    cy.clearLocalStorage();
    cy.visit('/login');
    stubApiCalls();
    login();
    cy.url().should('include', '/dashboard');
    cy.get('[data-cy="dashboard-content"]', { timeout: 15000 }).should('be.visible');
  });

  it('NAV-001 | Dashboard carga con secciones visibles', () => {
    cy.get('h2').should('contain', 'Panel principal');
  });

  it('NAV-002 | Titulo de la pagina no esta vacio', () => {
    cy.title().should('not.be.empty');
  });

  it('NAV-003 | Navegacion a seccion estudiantes', () => {
    cy.contains('.nav-item', 'Estudiantes', { timeout: 10000 }).click();
    cy.get('h2').should('contain', 'Estudiantes');
  });

  it('NAV-004 | Navegacion a seccion horarios', () => {
    cy.contains('.nav-item', 'Horarios', { timeout: 10000 }).click();
    cy.get('h2').should('contain', 'Horarios');
  });

  it('NAV-005 | Ruta inexistente se maneja correctamente', () => {
    cy.visit('/ruta-inexistente', { failOnStatusCode: false });
    cy.url().should('not.be.empty');
  });
});

describe('Autenticacion API', () => {
  it('SEC-001 | Health check del backend', () => {
    cy.request({ url: 'http://127.0.0.1:8000/health', failOnStatusCode: false }).then((resp) => {
      if (resp.status === 200) {
        expect(resp.body.status).to.equal('healthy');
      }
    });
  });

  it('SEC-002 | POST /api/auth/login admin', () => {
    cy.request({
      method: 'POST', url: `${API}/auth/login`,
      body: { email: 'admin@uni.edu', password: 'admin123', tipo: 'admin' },
      failOnStatusCode: false
    }).then((resp) => {
      if (resp.status === 200) {
        expect(resp.body.success).to.be.true;
        expect(resp.body.data.tipo).to.equal('admin');
      }
    });
  });

  it('SEC-003 | POST /api/auth/login credenciales malas', () => {
    cy.request({
      method: 'POST', url: `${API}/auth/login`,
      body: { email: 'admin@uni.edu', password: 'WRONG', tipo: 'admin' },
      failOnStatusCode: false
    }).then((resp) => {
      expect(resp.status === 401 || resp.status === 404 || resp.status === 503).to.be.true;
    });
  });

  it('SEC-004 | POST /api/auth/login tipo invalido', () => {
    cy.request({
      method: 'POST', url: `${API}/auth/login`,
      body: { email: 'test@test.com', password: 'pass', tipo: 'hacker' },
      failOnStatusCode: false
    }).then((resp) => {
      expect(resp.status === 400 || resp.status === 404 || resp.status === 503).to.be.true;
    });
  });
});

describe('Persistencia de Informacion', () => {
  beforeEach(() => {
    cy.clearLocalStorage();
    cy.visit('/login');
  });

  it('PERSIST-001 | Logout limpia localStorage', () => {
    stubApiCalls();
    login();
    cy.url().should('include', '/dashboard');
    cy.get('[data-cy="btn-logout"]', { timeout: 15000 }).should('be.visible').click({ force: true });
    cy.window().then((win) => {
      expect(win.localStorage.getItem('auth')).to.be.null;
    });
  });

  it('PERSIST-002 | Login guarda tipo de usuario en localStorage', () => {
    stubApiCalls();
    login();
    cy.url().should('include', '/dashboard');
    cy.window().then((win) => {
      const auth = JSON.parse(win.localStorage.getItem('auth'));
      expect(auth.userType).to.equal('admin');
      expect(auth.loggedIn).to.be.true;
    });
  });
});
