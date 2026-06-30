# Declaración de Trabajo (Statement of Work — SOW)
## HorarioSmart

> **Nota de adaptación académica:** el proyecto HorarioSmart no contempló la contratación de proveedores externos. Sin embargo, conforme a la consigna del curso, se documenta la presente Declaración de Trabajo (SOW) como mecanismo formal de **validación del alcance comprometido y los entregables acordados** entre el equipo de desarrollo (en su rol de "proveedor interno" del producto) y el Sponsor / Docente del curso (en su rol de "cliente interno"), antes del cierre del proyecto.

---

## 1. Partes Involucradas

| Rol | Parte |
|---|---|
| **Proveedor interno (equipo ejecutor)** | Equipo de proyecto HorarioSmart: Meza Calderón, Ana Cristina (Project Manager); Escobar Bendezú, Aldrin Edwin (Scrum Master / Backend Developer); López Rodríguez, Axel Andre (Frontend Developer) |
| **Cliente / Patrocinador** | Gamarra Moreno, Job (Sponsor y Docente del curso *Taller de Proyectos 2*) |
| **Beneficiarios finales (stakeholders)** | Estudiantes, docentes, personal administrativo y la Universidad Continental |

---

## 2. Objeto del Documento

Esta Declaración de Trabajo tiene por objeto **verificar formalmente** que el trabajo comprometido en el Acta de Constitución del Proyecto fue completado en su totalidad, sirviendo como respaldo documental para el cierre administrativo y académico del proyecto, conforme al enfoque PMBOK.

---

## 3. Alcance del Trabajo Comprometido

El equipo se comprometió a diseñar, desarrollar y entregar un **Producto Mínimo Viable (PMV)** denominado HorarioSmart, consistente en una aplicación web (arquitectura SPA + API REST) capaz de:

1. Registrar entidades académicas: estudiantes, docentes, cursos y aulas.
2. Validar restricciones de matrícula (créditos máximos, prerrequisitos).
3. Generar automáticamente horarios académicos libres de conflictos mediante un modelo de optimización (CSP).
4. Visualizar los horarios generados para estudiantes y docentes.
5. Documentar el proceso de desarrollo, calidad, sostenibilidad y cierre conforme a buenas prácticas de ingeniería de software y PMBOK.

El trabajo se ejecutó bajo metodología **Scrum**, en sprints iterativos, dentro de un periodo de **12 a 16 semanas** a partir del 24/03/2026, con un presupuesto de **$0** (uso exclusivo de herramientas open-source y recursos propios del equipo).

---

## 4. Entregables Comprometidos vs. Entregados (Checklist de Verificación)

| # | Entregable Comprometido | ¿Completado? | Observaciones |
|---|---|---|---|
| 1 | Documento de análisis del problema | ✅ | `docs/inicio/inicio.md` |
| 2 | Modelo formal (CSP/Optimización) | ✅ | `docs/planificación/Spec.md`, `docs/planificación/constitution.md` |
| 3 | Código de arquitectura SPA + API REST | ✅ | `frontend/`, `backend/` |
| 4 | Código funcional (Frontend + Backend) | ✅ | Repositorio completo |
| 5 | Pruebas unitarias e integración | ✅ | 430 pruebas automatizadas, cobertura 97.1% |
| 6 | Repositorio GitHub documentado | ✅ | https://github.com/Hannah2112-hub/TP2 |
| 7 | PMV etiquetado como v1.0 | ✅ | Release `v1.0` |
| 8 | Video demostrativo (máx. 5 minutos) | ⏳ | Pendiente de enlace final en `README.md` |
| 9 | Informe técnico final | ✅ | `docs/cierre/01-informe-final-proyecto.md` + documentación de métricas y evidencias |
| 10 | Cumplimiento de requerimientos del currículo (RF/RNF) | ✅ | RF-01 a RF-05 y requerimientos no funcionales verificados |
| 11 | Documentación de control y cierre del proyecto (PMBOK) | ✅ | `docs/cierre/` (presente conjunto documental) |

**Nivel de cumplimiento del alcance comprometido: 10 de 11 entregables completados al 100% (91%); 1 entregable en estado pendiente de formalización menor (enlace de video), sin impacto en la funcionalidad ni calidad del producto.**

---

## 5. Criterios de Aceptación

El trabajo se considera **aceptado** si cumple las siguientes condiciones, verificadas en este documento y en el Informe Final del Proyecto:

| Criterio de Aceptación | Cumplimiento |
|---|---|
| El sistema genera horarios sin conflictos verificables | ✅ Cumplido |
| El repositorio se encuentra documentado y organizado en Markdown | ✅ Cumplido |
| El producto aprueba el Quality Gate de SonarQube | ✅ Cumplido (Passed) |
| El producto cuenta con pruebas automatizadas con cobertura ≥ 70-80% | ✅ Cumplido (97.1%) |
| El producto no presenta vulnerabilidades ni bugs críticos | ✅ Cumplido (0 bugs, 0 vulnerabilidades) |
| El producto cumple criterios básicos de accesibilidad (WCAG) | ✅ Cumplido |
| El producto fue evaluado en usabilidad con usuarios reales | ✅ Cumplido (SUS 87.5/100) |
| Se entrega documentación de cierre conforme a PMBOK | ✅ Cumplido (este conjunto documental) |

---

## 6. Cronograma de Ejecución del Trabajo

| Fase | Periodo | Estado |
|---|---|---|
| Sprint 0 — Análisis y planificación | Semana 1-2 | Completado |
| Modelado formal y diseño de arquitectura | Semana 3-5 | Completado |
| Implementación Backend | Semana 6-8 | Completado |
| Implementación Frontend | Semana 9-10 | Completado |
| Integración, pruebas y aseguramiento de calidad | Semana 11-12 | Completado (con extensión controlada) |
| Control y cierre del proyecto | Semana 13 | Completado |

---

## 7. Validación Formal de Cumplimiento

En virtud de la verificación de entregables (sección 4) y criterios de aceptación (sección 5) documentados en esta Declaración de Trabajo, se concluye que:

> **El trabajo comprometido por el equipo de proyecto HorarioSmart ha sido completado conforme al alcance, calidad y cronograma establecidos en el Acta de Constitución del Proyecto**, quedando como única acción pendiente la incorporación del enlace al video demostrativo final, de carácter administrativo y sin impacto en el producto de software entregado.

| Rol | Nombre | Validación |
|---|---|---|
| Project Manager (proveedor interno) | Meza Calderón, Ana Cristina | Confirma cumplimiento del alcance |
| Sponsor / Docente del curso (cliente) | Gamarra Moreno, Job | Pendiente de validación formal en sesión de cierre |

---
*Documento elaborado conforme al enfoque PMBOK, adaptado a un contexto académico sin proveedores externos, como parte de la fase de control y cierre del proyecto. Última actualización: 21 de junio de 2026.*
