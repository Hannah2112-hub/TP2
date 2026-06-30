# Informe Final de Lecciones Aprendidas (Final Lessons Learned Report)
## HorarioSmart — Sistema de Generación Óptima de Horarios Académicos

| Campo | Detalle |
|---|---|
| **Proyecto** | HorarioSmart |
| **Equipo** | Escobar Bendezú, Aldrin Edwin (Backend / Scrum Master) · López Rodríguez, Axel Andre (Frontend) · Meza Calderón, Ana Cristina (Project Manager / Analista) |
| **Periodo cubierto** | 24/03/2026 – 21/06/2026 |
| **Fecha del informe** | 21/06/2026 |

---

## 1. Propósito

Este documento consolida las lecciones aprendidas y retrospectivas realizadas a lo largo del proyecto HorarioSmart, con el propósito de identificar **qué prácticas funcionaron bien** —para que el equipo y otros equipos las adopten en proyectos futuros— y **qué no funcionó**, con el fin de evitarlo en próximas iteraciones. La información proviene de las retrospectivas de sprint, el análisis de calidad (SonarQube), el proceso de testing y la gestión de riesgos e incidentes registrados durante el ciclo de vida del proyecto.

---

## 2. Metodología de Recolección

Las lecciones aprendidas se recopilaron mediante:
- Retrospectivas al cierre de cada sprint (metodología Scrum).
- Análisis comparativo de métricas de calidad antes/después de las correcciones (SonarQube).
- Revisión del Registro de Riesgos, Registro de Incidentes y Registro de Defectos.
- Discusión final de cierre de proyecto entre los tres integrantes del equipo.

---

## 3. Qué Salió Bien (Buenas Prácticas a Replicar)

### 3.1 Decisiones técnicas y de arquitectura

| Lección aprendida | Evidencia / Resultado |
|---|---|
| Modelar el problema de horarios como un **CSP** (Constraint Satisfaction Problem) en lugar de un algoritmo *greedy* evitó callejones sin salida (*dead ends*) y garantizó matemáticamente la ausencia de conflictos. | Cero conflictos de aula/docente detectados en validación SQL independiente (`validar()` en `horario_repository.py`). |
| Definir desde el inicio una **especificación formal** (`Spec.md`) con entradas, salidas, reglas de negocio y casos límite redujo la ambigüedad del requerimiento original ("generación de horarios sin conflictos"). | El requerimiento ambiguo se tradujo en restricciones duras y blandas verificables. |
| Separar claramente **frontend (Angular) y backend (FastAPI)** mediante una arquitectura SPA + API REST facilitó el trabajo paralelo del equipo sin bloqueos entre disciplinas. | Desarrollo simultáneo de frontend y backend desde la semana 5. |
| Implementar una **doble validación** (solver OR-Tools + consulta SQL con `OVERLAPS`) añadió una capa de confianza adicional sobre la corrección del resultado. | Reducción a 0 *bugs* de fiabilidad reportados por SonarQube. |

### 3.2 Proceso y gestión

| Lección aprendida | Evidencia / Resultado |
|---|---|
| Adoptar **Scrum** con sprints cortos permitió validar de forma incremental un problema de alta incertidumbre algorítmica. | Cumplimiento de hitos planificados (Sprint 0 a integración) sin retrasos que comprometieran la fecha de entrega. |
| Definir roles claros desde el Project Charter (PM, Scrum Master, Backend, Frontend) evitó ambigüedad de responsabilidades en un equipo pequeño de 3 personas. | Sin conflictos de asignación de tareas reportados durante el proyecto. |
| Usar Git/GitHub con commits frecuentes y descriptivos facilitó la trazabilidad de cambios y la integración continua del trabajo de los tres integrantes. | Historial de versiones consistente en el repositorio. |

### 3.3 Calidad y testing

| Lección aprendida | Evidencia / Resultado |
|---|---|
| Invertir tiempo en **pruebas automatizadas** desde etapas tempranas (no solo al final) elevó la cobertura global a 97.1%, muy por encima del umbral mínimo (70-80%). | 430 pruebas automatizadas (224 backend + 206 frontend). |
| Ejecutar **SonarQube de forma iterativa** (no solo una vez al final) permitió corregir progresivamente 129 issues hasta llegar a 0, evitando una acumulación de deuda técnica inmanejable al cierre. | Deuda técnica final: 0 horas (desde 1 día 2 horas). |
| Justificar explícitamente las **exclusiones de cobertura** (archivos de configuración, bootstrap, tipos TypeScript) evitó perseguir métricas de cobertura poco significativas. | Tabla de justificación de exclusiones documentada en `EVIDENCIAS_TESTING.md`. |
| Revisar manualmente los *Security Hotspots* en lugar de ignorarlos o suprimirlos automáticamente permitió distinguir falsos positivos (uso de `random.randint` como semilla del solver, no criptográfico) de riesgos reales. | 100% de hotspots revisados, 0 vulnerabilidades reales. |

### 3.4 Accesibilidad y experiencia de usuario

| Lección aprendida | Evidencia / Resultado |
|---|---|
| Auditar el sistema contra criterios **WCAG** (contraste, navegación por teclado, etiquetas) antes del cierre evitó dejar la accesibilidad como una mejora post-entrega. | Corrección de 5 criterios WCAG documentada en `METRICAS_CALIDAD14.md`. |
| Aplicar el instrumento **SUS** con usuarios reales (aunque fuera un grupo reducido de 5 participantes) brindó una validación objetiva de usabilidad más allá de la opinión interna del equipo. | SUS promedio de 87.5/100 (clasificación Excelente). |

---

## 4. Qué No Funcionó (Para Evitar en el Futuro)

| Problema identificado | Causa raíz | Recomendación para futuros proyectos |
|---|---|---|
| Acumulación de **129 issues de SonarQube** detectados recién en una revisión tardía. | El análisis de calidad estático se ejecutó por primera vez después de tener una porción significativa del código implementado, en lugar de integrarlo desde el primer sprint. | Integrar el análisis SonarQube (o equivalente) **desde el Sprint 0** como parte del pipeline de cada entrega, no como una actividad de cierre. |
| El endpoint `auth_api` no estaba registrado correctamente en `apis/__init__.py`, generando fallos en pruebas de integración (Issue de severidad Alta). | Falta de una lista de verificación (checklist) de registro de rutas al añadir nuevos módulos de API. | Establecer una checklist de "Definition of Done" por historia de usuario que incluya verificación de registro/exposición de endpoints. |
| Un test E2E (`test_navigation_to_redoc`) permanece fallando al cierre por un selector HTML no encontrado. | Dependencia de un selector específico del documento Redoc que cambió entre versiones de FastAPI/Swagger. | Usar selectores más resilientes (data-testid) en vez de depender de estructuras HTML generadas por librerías de terceros. |
| Configuración inicial de **SonarQube local** consumió tiempo de equipo no planificado (instalación, gestión de espacio en disco mediante *junction*). | Subestimación del esfuerzo de configuración de herramientas de calidad en el entorno local del equipo. | Reservar explícitamente tiempo de "Sprint 0" para *tooling* y considerar alternativas en la nube (SonarCloud) para evitar configuración local compleja. |
| La cobertura de *branches* del frontend estuvo inicialmente por debajo del umbral del 70%. | Las pruebas iniciales cubrían el camino feliz (*happy path*) pero no los casos de error ni ramas condicionales. | Diseñar casos de prueba explícitamente para ramas de error desde la redacción de la historia de usuario, no solo para el resultado exitoso. |
| El supuesto de **disponibilidad de datos reales** para pruebas no se cumplió plenamente (riesgo R-03 / impedimento registrado). | El proyecto no tuvo acceso a datos institucionales reales de matrícula, docentes y aulas. | En proyectos académicos, solicitar formalmente (desde la fase de inicio) datasets anonimizados representativos a la institución, o definir un generador de datos sintéticos validado desde el principio. |

---

## 5. Acciones Correctivas Aplicadas Durante el Proyecto

1. **Refactorización de complejidad ciclomática** en `horario_repository.py` hasta reducirla a ≤ 15, mejorando la mantenibilidad del módulo más crítico del sistema.
2. **Corrección de seguridad de configuración**: cambio de `host="0.0.0.0"` a `host="127.0.0.1"` en `app.py` para evitar exposición innecesaria del servidor.
3. **Estandarización de manejo de errores** en los endpoints (`HTTPException` documentadas con `Annotated` types) en 8 archivos de API.
4. **Reescritura de validaciones espacio-temporales** usando `OVERLAPS` en SQL en lugar de iteración en memoria, mejorando tanto el rendimiento como la sostenibilidad (huella de cómputo).
5. **Compresión GZIP** añadida como mejora no solicitada, alineada al objetivo de sostenibilidad del proyecto.

---

## 6. Recomendaciones para Futuros Equipos / Proyectos

1. **Adoptar control de calidad estático desde el primer sprint**, no como actividad de cierre, para distribuir el esfuerzo de corrección a lo largo del proyecto.
2. **Definir criterios de aceptación (Definition of Done)** que incluyan explícitamente registro de rutas/endpoints, pruebas de rama de error y revisión de accesibilidad básica.
3. **Planificar tiempo de *tooling*** (configuración de SonarQube, entornos de testing, CI) como una tarea visible del backlog, no como tiempo implícito.
4. **Gestionar el riesgo de datos reales** solicitando datasets representativos desde la fase de inicio del proyecto, en lugar de asumir su disponibilidad futura.
5. **Mantener la práctica de doble validación** (algoritmo + verificación independiente) en sistemas donde la corrección del resultado es crítica para el usuario final.
6. **Conservar la práctica de retrospectivas por sprint**, ya que permitió identificar y corregir desviaciones de forma incremental en lugar de acumularlas hasta el cierre.

---

## 7. Aprendizaje Organizacional

El proyecto demuestra que, incluso con un equipo reducido (3 integrantes) y presupuesto cero, es posible alcanzar un producto con **calificaciones de calidad A** en seguridad, fiabilidad y mantenibilidad, siempre que el control de calidad se trate como una actividad continua y no como un paso final. La principal transferencia de conocimiento hacia futuros proyectos del equipo es la **integración temprana de herramientas de calidad y testing en el flujo de trabajo Scrum**, evitando la concentración de esfuerzo correctivo al final del ciclo de vida del proyecto.

---
*Documento elaborado conforme al enfoque PMBOK como parte de la fase de control y cierre del proyecto. Última actualización: 21 de junio de 2026.*
