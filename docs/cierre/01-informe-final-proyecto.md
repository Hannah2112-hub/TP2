# Informe Final del Proyecto (Final Project Report)
## HorarioSmart — Sistema de Generación Óptima de Horarios Académicos en Entornos de Currículo Flexible

| Campo | Detalle |
|---|---|
| **Proyecto** | HorarioSmart — Sistema de Generación Óptima de Horarios Académicos |
| **Project Manager** | Meza Calderón, Ana Cristina |
| **Sponsor / Docente del curso** | Gamarra Moreno, Job |
| **Fecha de inicio** | 24/03/2026 |
| **Fecha de cierre** | 21/06/2026 |
| **Repositorio** | https://github.com/Hannah2112-hub/TP2 |
| **Versión entregada** | PMV v1.0.0 |

---

## 1. Resumen Ejecutivo

El proyecto **HorarioSmart** desarrolló un Producto Mínimo Viable (PMV) orientado a resolver, mediante automatización algorítmica, la planificación de horarios académicos en instituciones de educación superior con currículo flexible. El problema fue abordado como un **Problema de Satisfacción de Restricciones (CSP)**, resuelto con la librería **Google OR-Tools**, sobre una arquitectura **SPA + API REST** construida con **Angular** (frontend) y **FastAPI** (backend), utilizando **PostgreSQL/SQL Server** como motor de persistencia.

El equipo de proyecto, conformado por tres integrantes, trabajó bajo la metodología ágil **Scrum**, organizando el desarrollo en sprints desde Sprint 0 (análisis y planificación) hasta la entrega final del PMV etiquetado como **v1.0**.

Al cierre del proyecto se verifica el cumplimiento del **100% de los entregables obligatorios** definidos en el Acta de Constitución, con un sistema funcional, probado (**430 pruebas automatizadas**, **97.1% de cobertura global**), libre de vulnerabilidades y bugs críticos (**Quality Gate: Passed** en SonarQube), accesible (correcciones **WCAG**), evaluado positivamente en usabilidad (**SUS = 87.5/100, clasificación Excelente**) y documentado conforme a buenas prácticas de sostenibilidad (**Green Software**).

El proyecto se considera **cerrado exitosamente**, cumpliendo los criterios de éxito definidos en el Project Charter, sin desviaciones de costo (presupuesto $0, infraestructura local/gratuita) y con una variación de cronograma mínima, contenida dentro de la ventana de entrega planificada (semana 12–16).

---

## 2. Desempeño del Alcance (Scope Performance)

### 2.1 Alcance planificado (según Project Charter)

**Incluido en el alcance:**
- Modelado del problema como CSP / optimización combinatoria.
- Registro de estudiantes, cursos y aulas.
- Validación de métricas (créditos y prerrequisitos).
- Generación automática de horarios sin conflictos.
- Visualización de horarios.

**Excluido explícitamente del alcance:**
- Integración con sistemas reales universitarios.
- Infraestructura móvil nativa.
- Infraestructura productiva real (despliegue en producción institucional).

### 2.2 Verificación del alcance entregado

| Elemento del alcance | Estado | Evidencia |
|---|---|---|
| Modelado CSP / optimización combinatoria | ✅ Cumplido | `backend/src/repositories/horario_repository.py` (OR-Tools `cp_model`), `docs/planificación/Spec.md` |
| Registro de estudiantes, docentes, cursos y aulas | ✅ Cumplido | `backend/src/apis/{estudiante,docente,curso,aula}_api.py` |
| Validación de créditos y prerrequisitos en matrícula | ✅ Cumplido | `backend/src/services/matricula_service.py`, RF-02 |
| Generación automática de horarios sin conflictos | ✅ Cumplido | `horario_repository.py`, restricciones duras (Hard Constraints) verificadas por validación SQL independiente |
| Visualización de horarios | ✅ Cumplido | `frontend/src/app/pages/dashboard/` |
| Autenticación y control de acceso por roles | ✅ Cumplido (no comprometido formalmente, valor agregado) | `auth_api.py`, `auth.guard.ts` |
| Panel de impacto ambiental / sostenibilidad | ✅ Cumplido (valor agregado, Green Software) | `sustainability.py`, `INFORME_SOSTENIBILIDAD.md` |
| Integración con sistemas reales universitarios | 🚫 Fuera de alcance (según lo planificado) | No aplica — exclusión documentada en Charter |
| Infraestructura móvil nativa | 🚫 Fuera de alcance (según lo planificado) | No aplica — exclusión documentada en Charter |
| Despliegue en infraestructura productiva real | 🚫 Fuera de alcance (según lo planificado) | Entorno local/gratuito, conforme a presupuesto $0 |

**Conclusión de alcance:** el sistema entregado cumple el **100%** del alcance comprometido, sin recortes de funcionalidades críticas, y suma dos capacidades adicionales (panel de sostenibilidad y control de acceso por roles) no exigidas explícitamente pero alineadas a los objetivos del proyecto.

### 2.3 Trazabilidad de entregables comprometidos en el Charter

| # | Entregable comprometido | Estado | Ubicación en el repositorio |
|---|---|---|---|
| 1 | Documento de análisis del problema | ✅ | `docs/inicio/inicio.md` (sección Problema, Requerimientos) |
| 2 | Modelo formal (CSP/Optimización) | ✅ | `docs/planificación/Spec.md`, `docs/planificación/constitution.md` |
| 3 | Código de arquitectura SPA + API REST | ✅ | `frontend/`, `backend/` |
| 4 | Código funcional (Frontend + Backend) | ✅ | `frontend/src/app/`, `backend/src/` |
| 5 | Pruebas unitarias e integración | ✅ | `backend/tests/`, `frontend/src/tests/`, `frontend/cypress/` |
| 6 | Repositorio GitHub documentado | ✅ | https://github.com/Hannah2112-hub/TP2 |
| 7 | PMV etiquetado como v1.0 | ✅ | Release `v1.0` |
| 8 | Video demostrativo | ⏳ Pendiente de enlace final | `README.md` (sección Video explicativo) |
| 9 | Informe técnico final | ✅ | Este documento + `METRICAS_CALIDAD14.md`, `EVIDENCIAS14.md` |
| 10 | Cumplimiento de requerimientos del currículo | ✅ | RF-01 a RF-05 y requerimientos no funcionales en `docs/inicio/inicio.md` |

> **Acción de cierre pendiente:** completar el enlace al video demostrativo (máx. 5 minutos) en `README.md` antes de la entrega final del repositorio.

---

## 3. Desempeño de Calidad (Quality Performance)

| Indicador | Resultado | Umbral / Meta | Estado |
|---|---|---|---|
| Quality Gate (SonarQube) | **Passed** | Passed | ✅ |
| Security Rating | **A** (0 vulnerabilidades) | A | ✅ |
| Reliability Rating | **A** (0 bugs) — mejorado desde **D** (41 problemas) | A | ✅ |
| Maintainability Rating | **A** (0 code smells) — mejorado desde 90 code smells | A | ✅ |
| Cobertura de código global | **97.1%** (Backend 96.8% / Frontend 97.6%) | ≥ 70–80% | ✅ |
| Duplicación de código | **0.5%** | < 3% | ✅ |
| Security Hotspots revisados | **100%** (1 hotspot, marcado *Safe*) | 100% | ✅ |
| Pruebas automatizadas totales | **430** (224 backend + 206 frontend) | — | ✅ |
| Issues SonarQube abiertos | **0** (reducidos desde 129) | 0 | ✅ |
| Deuda técnica | **0 horas** (reducida desde 1 día 2 horas) | Mínima | ✅ |
| Cumplimiento OWASP Top 10 (2025) | **9/10 mitigadas**, 1 no aplica (SSRF) | Mitigación total de categorías aplicables | ✅ |
| Accesibilidad WCAG | Contraste, navegación por teclado, etiquetas `label` corregidas | Criterios 1.4.3, 1.4.11, 2.1.1, 2.4.6, 4.1.2 | ✅ |
| Usabilidad (SUS) | **87.5 / 100** — Excelente (A) | > 68 (Bueno) | ✅ |

**Análisis:** la calidad del producto evolucionó de un estado inicial con riesgos significativos (calificación de fiabilidad D, 129 issues abiertos, 0% de cobertura de pruebas) a un estado final con **calificaciones A en seguridad, fiabilidad y mantenibilidad**, cobertura de pruebas superior al 97% y cero deuda técnica. El detalle completo de la evidencia y metodología se encuentra en `METRICAS_CALIDAD14.md` y `EVIDENCIAS14.md`.

---

## 4. Desempeño del Cronograma (Schedule Performance)

### 4.1 Hitos planificados vs. ejecutados

| Hito | Semana planificada (Charter) | Estado de cumplimiento |
|---|---|---|
| Sprint 0 — Análisis y planificación | Semana 2 | ✅ Cumplido en fecha |
| Modelado formal del problema (CSP/Spec) | Semana 4 | ✅ Cumplido en fecha |
| Diseño de arquitectura (SPA + API REST) | Semana 5 | ✅ Cumplido en fecha |
| Implementación Backend | Semana 8 | ✅ Cumplido, con extensión menor para refactorización de complejidad ciclomática |
| Implementación Frontend | Semana 10 | ✅ Cumplido en fecha |
| Integración y pruebas | Semana 11 | ⚠️ Extendido — la consolidación de cobertura (70% → 97.1%) y la corrección de 129 issues de SonarQube se prolongaron hasta el cierre |
| Entrega PMV v1.0 + Video demostrativo | Semana 12–16 | ✅ Entregado dentro de la ventana planificada (cierre en semana 13) |

### 4.2 Análisis de variación

La fase de **integración, pruebas y aseguramiento de calidad** (originalmente acotada a la semana 11) se extendió de forma controlada hasta el cierre del proyecto, debido a:

1. El esfuerzo adicional requerido para elevar la cobertura de pruebas automatizadas desde un piso aceptable (≥70%) hasta el resultado final (97.1%).
2. La corrección iterativa de **129 issues** detectados por SonarQube en el primer análisis.
3. Las correcciones de accesibilidad (WCAG) y la revisión formal del *Security Hotspot* detectado.

Esta variación **no comprometió la fecha límite de entrega**, ya que el Charter contemplaba una ventana de cuatro semanas (semana 12 a 16) para la entrega del PMV, dentro de la cual el cierre se realiza en la **semana 13**. Se considera el cronograma **cumplido sin impacto en la fecha de entrega comprometida**.

---

## 5. Desempeño de Costos (Cost Performance)

| Concepto | Presupuestado (Charter) | Ejecutado | Variación |
|---|---|---|---|
| Software | $0 (uso de herramientas open-source) | $0 (FastAPI, Angular, SQLServer/PostgreSQL, GitHub, SonarQube Community, OR-Tools) | $0 |
| Infraestructura | Local / gratuita (PC personal y servicios *free tier*) | Local / gratuita | $0 |
| **Total** | **$0** | **$0** | **Sin desviación** |

El proyecto se ejecutó íntegramente bajo el modelo de **costo cero**, utilizando exclusivamente herramientas de código abierto y recursos propios del equipo, conforme a lo establecido en el Acta de Constitución. No se registran desviaciones presupuestarias.

---

## 6. Resumen de Riesgos e Incidentes

### 6.1 Riesgos

Se identificaron y gestionaron **4 riesgos formales** durante la ejecución (ver detalle en [`03-registro-riesgos.md`](./03-registro-riesgos.md)). Ninguno de los riesgos de alto impacto se materializó de forma crítica; los riesgos relacionados con la complejidad algorítmica y los tiempos de generación fueron mitigados mediante límites de tiempo de cómputo (10 segundos) y validación SQL independiente del resultado del solver.

| Resumen | Cantidad |
|---|---|
| Riesgos identificados | 4 |
| Riesgos mitigados / cerrados sin impacto | 4 |
| Riesgos materializados con impacto en el proyecto | 0 |
| Oportunidades identificadas | 3 |

### 6.2 Incidentes y defectos

| Resumen | Cantidad |
|---|---|
| Incidentes/problemas registrados (Issue Log) | 6 |
| Defectos técnicos registrados (Defect Log) | 8 |
| Defectos corregidos y validados | 7 |
| Defectos pendientes al cierre (severidad baja, sin impacto funcional) | 1 |
| Impedimentos registrados | 5 |

Detalle completo en [`04-registro-incidentes.md`](./04-registro-incidentes.md), [`06-registro-defectos.md`](./06-registro-defectos.md) y [`05-registro-impedimentos.md`](./05-registro-impedimentos.md).

---

## 7. Análisis Comparativo: Plan vs. Ejecución

| Dimensión | Planificado | Ejecutado | Resultado |
|---|---|---|---|
| Alcance | 5 capacidades funcionales núcleo + exclusiones definidas | 5 capacidades núcleo + 2 capacidades adicionales (roles, sostenibilidad) | Superado |
| Calidad | Sin meta cuantitativa explícita en el Charter | Quality Gate Passed, A/A/A, 97.1% cobertura | Superado |
| Cronograma | Entrega en semana 12–16 | Cierre en semana 13 | Cumplido |
| Costo | $0 | $0 | Cumplido |
| Equipo | 3 integrantes con roles definidos (PM, Scrum Master, Backend, Frontend) | Roles mantenidos sin cambios de personal | Cumplido |
| Metodología | Scrum, sprints iterativos | Scrum aplicado con retrospectivas por sprint | Cumplido |

---

## 8. Conclusiones Estratégicas

1. **Viabilidad técnica confirmada:** el uso de un solver CSP (OR-Tools) para la generación de horarios resultó adecuado para garantizar matemáticamente la ausencia de conflictos, validando la decisión arquitectónica tomada en la fase de planificación.
2. **La inversión en calidad fue determinante:** el mayor esfuerzo del proyecto se concentró en la fase de control de calidad (testing, SonarQube, accesibilidad), lo cual elevó significativamente la confiabilidad del producto final sin incurrir en sobrecostos.
3. **Escalabilidad pendiente de validación real:** dado que el alcance excluyó explícitamente la infraestructura productiva real, se recomienda como trabajo futuro una prueba de carga con datos institucionales reales antes de un eventual despliegue productivo.
4. **El producto cumple su propósito de PMV:** valida la hipótesis central del proyecto (generación automática de horarios sin conflictos) y deja una base sólida y documentada para iteraciones futuras (backlog de mejoras: exportación PDF/Excel, integración con sistemas académicos reales, optimización avanzada con IA).

---

## 9. Cierre Formal del Proyecto

| Criterio de éxito (Acta de Constitución) | Verificación al cierre |
|---|---|
| Automatizar la generación de horarios académicos | ✅ Verificado |
| Minimizar conflictos de asignación y solapamientos | ✅ Verificado (restricciones duras 100% cumplidas) |
| Optimizar recursos institucionales (aulas, docentes) | ✅ Verificado |
| Reducir tiempos administrativos | ✅ Verificado (generación en segundos vs. proceso manual) |
| Maximizar opciones horarias estudiantiles | ✅ Verificado |
| Visualizar datos de recursos para decisiones | ✅ Verificado (dashboard) |
| Garantizar escalabilidad del sistema | ⚠️ Validado a nivel de diseño; pendiente de prueba con carga real |
| Habilitar enseñanza híbrida | ✅ Soportado por el modelo de datos y la arquitectura |

**Declaración de cierre:** en virtud del cumplimiento verificado de los criterios de éxito y entregables establecidos en el Acta de Constitución del Proyecto, el equipo de dirección del proyecto declara **formalmente cerrado** el proyecto HorarioSmart en su fase de PMV v1.0, con las observaciones y acciones pendientes documentadas en la sección 2.3 de este informe.

| Rol | Nombre | Aprobación |
|---|---|---|
| Project Manager | Meza Calderón, Ana Cristina | Aprobado |
| Sponsor / Docente del curso | Gamarra Moreno, Job | Pendiente de validación formal |

---
*Documento elaborado conforme al enfoque PMBOK como parte de la fase de control y cierre del proyecto. Última actualización: 21 de junio de 2026.*
