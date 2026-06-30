# Documentación de Capacitación
## HorarioSmart — Manual de Usuario y Manual Técnico de Operación

> Este documento reúne la documentación necesaria para que el **cliente** (Universidad / personal administrativo) y el **equipo de operaciones** que herede el producto puedan utilizar, mantener y desplegar el sistema HorarioSmart, conforme a la fase de cierre del proyecto.

---

## PARTE A — Manual de Usuario

### A.1 Descripción General

**HorarioSmart** es un sistema web de gestión académica que permite registrar estudiantes, docentes, cursos y aulas, validar matrículas, y generar automáticamente horarios académicos libres de conflictos.

### A.2 Roles de Usuario

El sistema reconoce tres tipos de usuario (`TipoUsuario`):

| Rol | Descripción |
|---|---|
| **admin** | Personal administrativo. Acceso completo a la gestión de carreras, estudiantes, docentes, cursos, aulas, matrícula y generación de horarios. |
| **docente** | Usuario docente. Puede visualizar su información académica y los horarios generados. |
| **estudiante** | Usuario estudiante. Puede visualizar su matrícula y horario asignado. |

### A.3 Acceso al Sistema (Inicio de Sesión)

1. Ingresar a la URL del sistema (ver sección B.3 para el entorno de despliegue).
2. En la pantalla **"Iniciar Sesión"**, completar los campos:
   - **Correo electrónico** (campo `email`).
   - **Contraseña** (campo `password`).
3. Hacer clic en **"Ingresar al Sistema"**.
4. En caso de credenciales inválidas, el sistema mostrará un mensaje de error en pantalla.

### A.4 Navegación Principal

Una vez autenticado, el usuario accede al **Panel Principal**, con un menú lateral que contiene las siguientes secciones:

| Sección del menú | Función |
|---|---|
| **Panel principal** | Muestra métricas generales: total de estudiantes, docentes, cursos y aulas registradas, además de las últimas matrículas realizadas. |
| **Carreras** | Registro y administración de carreras/programas académicos. |
| **Estudiantes** | Registro y administración de estudiantes. |
| **Docentes** | Registro y administración de docentes, incluyendo su disponibilidad horaria. |
| **Cursos** | Registro de cursos, créditos, prerrequisitos y cupos. |
| **Aulas** | Registro de aulas, con su capacidad y características. |
| **Matrícula** | Registro de matrícula de estudiantes en cursos, con validación automática de créditos y prerrequisitos. |
| **Horarios** | Generación, visualización y validación de horarios académicos. |

El usuario puede cerrar sesión en cualquier momento mediante el botón de salida ubicado en la parte inferior del menú lateral.

### A.5 Flujo de Trabajo Recomendado (Rol Administrador)

Para generar un horario académico completo desde cero, se recomienda seguir el siguiente orden:

1. **Registrar Carreras** (si aplica al plan curricular).
2. **Registrar Aulas**, especificando su capacidad.
3. **Registrar Docentes**, especificando su disponibilidad horaria.
4. **Registrar Cursos**, especificando cupos, créditos y, de corresponder, el docente asignado.
5. **Registrar Estudiantes**.
6. **Matricular estudiantes en cursos** desde la sección "Matrícula" — el sistema validará automáticamente el límite de créditos (20-22) y los prerrequisitos.
7. Ingresar a la sección **"Horarios"** y ejecutar la **generación automática de horarios**.
8. Revisar el resultado: el sistema reporta el número de horarios creados y, de existir advertencias (por ejemplo, cursos sin aulas con capacidad suficiente), las muestra en el detalle de la operación.
9. Opcionalmente, ejecutar la **validación de horarios**, que realiza una verificación independiente (vía SQL) de que no existan solapamientos de aula o docente.

### A.6 Mensajes y Validaciones Comunes

| Situación | Mensaje / Comportamiento esperado |
|---|---|
| Se intenta matricular a un estudiante excediendo el límite de créditos | El sistema rechaza la operación e informa el motivo. |
| Se intenta matricular un curso sin cumplir un prerrequisito | El sistema rechaza la operación e informa el motivo. |
| No existen suficientes aulas/docentes disponibles para generar un horario válido | El sistema informa que no fue posible generar una solución completa y sugiere agregar más aulas o reducir la cantidad de cursos. |
| La generación de horarios excede el tiempo máximo de cómputo (10 segundos) | El proceso se detiene automáticamente para evitar la sobrecarga del servidor; se recomienda reducir el volumen de datos o reintentar. |

### A.7 Preguntas Frecuentes (FAQ)

**¿Qué pasa si genero un nuevo horario cuando ya existe uno previo?**
El sistema reemplaza (desactiva) los horarios generados previamente y crea un nuevo conjunto de asignaciones, garantizando que la información vigente sea siempre la del último cálculo exitoso.

**¿Puedo asignar manualmente un curso a un horario fijo?**
En la versión actual (PMV v1.0) esta funcionalidad no está disponible; se encuentra documentada como mejora futura (ver oportunidad O-03 en el Registro de Riesgos).

**¿El sistema funciona en dispositivos móviles?**
La interfaz es una aplicación web (SPA); no se desarrolló una aplicación móvil nativa, conforme al alcance definido en el Acta de Constitución.

---

## PARTE B — Manual Técnico de Operación y Mantenimiento

> Dirigido al equipo de operaciones/desarrollo que herede el mantenimiento del sistema.

### B.1 Arquitectura del Sistema

| Capa | Tecnología |
|---|---|
| Frontend | Angular (SPA) |
| Backend | FastAPI (Python ≥ 3.14) |
| Base de datos | PostgreSQL / SQL Server |
| Motor de optimización | Google OR-Tools (`cp_model`, CSP) |
| Control de versiones | Git / GitHub |

La comunicación entre frontend y backend se realiza mediante peticiones HTTP/JSON sobre una API REST documentada automáticamente con Swagger/OpenAPI.

### B.2 Estructura del Repositorio

```
TP2/
├── backend/
│   ├── src/
│   │   ├── apis/            # Endpoints REST (aula, auth, carrera, curso, docente, estudiante, horario, matricula, sustainability)
│   │   ├── repositories/    # Acceso a datos y lógica del solver CSP
│   │   ├── services/        # Lógica de negocio
│   │   ├── schemas/         # Esquemas Pydantic
│   │   └── config/          # Configuración de base de datos y middleware
│   └── tests/                # Pruebas unitarias, integración y E2E (pytest)
├── frontend/
│   └── src/app/
│       ├── pages/            # dashboard, login
│       ├── services/         # academic.service.ts, auth.service.ts
│       ├── guards/           # auth.guard.ts
│       └── models/           # modelos.ts
├── docs/
│   ├── inicio/                # Visión, backlog, equipo, requerimientos
│   ├── planificación/         # Especificación formal, constitución técnica, riesgos
│   └── cierre/                # Documentación de control y cierre (este conjunto)
└── evidencias/                 # Capturas de evidencia técnica (SonarQube, etc.)
```

### B.3 Instalación y Puesta en Marcha

**1. Clonar el repositorio:**
```bash
git clone https://github.com/Hannah2112-hub/TP2
cd TP2
```

**2. Backend (FastAPI):**
```bash
cd backend
pip install -r requirements.txt   # o: uv sync, según gestor de paquetes configurado
uvicorn src.app:app --reload
```

**3. Frontend (Angular):**
```bash
cd frontend
npm install
npm run build
```

**4. Configuración de base de datos:**
- Configurar las credenciales de conexión a PostgreSQL/SQL Server mediante variables de entorno (archivo `.env`, ver `backend/src/config/database.py`).
- Ejecutar las migraciones/scripts de creación de esquema si corresponde.

### B.4 Ejecución de Pruebas (para mantenimiento continuo)

**Backend:**
```bash
cd backend
python -m pytest tests/ --cov=src --cov-report=html
```
Reporte de cobertura disponible en `backend/htmlcov/index.html`.

**Frontend:**
```bash
cd frontend
npx vitest run --coverage
```
Reporte de cobertura disponible en `frontend/coverage/index.html`.

**Pruebas E2E (Cypress):**
```bash
cd frontend
npx cypress run
```

### B.5 Análisis de Calidad (SonarQube)

El proyecto fue auditado con **SonarQube Community Build**. Para reproducir el análisis:

1. Levantar una instancia local o usar SonarCloud.
2. Configurar el archivo `sonar-project.properties` (ya incluido en el repositorio) con la clave del proyecto y las rutas de los reportes de cobertura (LCOV para frontend, Cobertura XML para backend).
3. Ejecutar el *scanner* con un token de análisis válido.
4. Revisar el dashboard resultante: se espera **Quality Gate: Passed**, calificaciones **A** en seguridad, fiabilidad y mantenibilidad.

### B.6 Endpoints Principales de la API

| Método | Ruta | Función |
|---|---|---|
| `POST` | `/login` | Autenticación de usuario |
| `GET` | `/horarios` | Consultar horarios generados |
| `POST` | `/horarios` | Crear un registro de horario |
| `POST` | `/horarios/generar` | Ejecutar el algoritmo de generación automática de horarios (CSP) |
| `GET` | `/horarios/validar` | Validación independiente (SQL) de ausencia de conflictos |
| `GET` | `/dashboard` | Obtener métricas para el panel principal |

La documentación interactiva completa de la API está disponible automáticamente en la ruta `/docs` (Swagger UI) al ejecutar el backend.

### B.7 Consideraciones de Sostenibilidad (Green Software)

El sistema implementa prácticas de eficiencia energética documentadas en `INFORME_SOSTENIBILIDAD.md`:
- Compresión GZIP de respuestas HTTP mayores a 500 bytes.
- Validaciones de solapamiento resueltas a nivel de base de datos (`OVERLAPS`) en lugar de en memoria.
- Truncamiento automático de métricas históricas al reiniciar el backend.
- Panel de monitoreo de impacto ambiental disponible en la ruta `/environmental-impact`.

Se recomienda al equipo de operaciones mantener estas prácticas y monitorear periódicamente el panel de sostenibilidad.

### B.8 Mantenimiento y Soporte

| Aspecto | Recomendación |
|---|---|
| Deuda técnica conocida | Ver [Registro de Defectos](./06-registro-defectos.md), DEF-08 (selector E2E de Redoc inestable). |
| Mejoras backlog pendientes | Exportación a PDF/Excel, integración con sistemas académicos reales, asignación manual de horarios fijos, optimización avanzada con IA (ver `docs/inicio/inicio.md`, sección Backlog). |
| Monitoreo de calidad | Re-ejecutar SonarQube ante cada cambio significativo de código para evitar acumulación de deuda técnica (lección aprendida documentada en el Informe Final de Lecciones Aprendidas). |
| Contacto del equipo original | Ver integrantes del equipo en la sección de Stakeholders del Acta de Constitución revisada. |

---
*Documento elaborado conforme a la fase de control y cierre del proyecto, para uso del cliente y del equipo de operaciones que heredará el producto. Última actualización: 21 de junio de 2026.*
