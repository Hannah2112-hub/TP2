# Acta de Constitución del Proyecto — Revisión Final (Project Charter Review)
## HorarioSmart

> Conforme a la guía PMBOK, el Acta de Constitución del Proyecto se revisa al cierre para evaluar si se cumplieron los requisitos de alto nivel y los criterios de éxito definidos al inicio. Esta sección transcribe el contenido original del Project Charter (`docs/inicio/Project-charter.png`) y lo contrasta con los resultados obtenidos.

---

## 1. Transcripción del Acta de Constitución Original

| Campo | Detalle |
|---|---|
| **Título del Proyecto** | Sistema de Generación Óptima de Horarios Académicos en Entornos de Currículo Flexible |
| **Fecha de inicio** | 24/03/2026 |
| **Project Manager** | Meza Calderón, Ana Cristina |
| **Sponsor** | Gamarra Moreno, Job |

### Necesidad del Proyecto
Las universidades con currículo flexible presentan dificultades en la planificación de horarios debido a la alta variabilidad en matrícula, restricciones académicas, limitaciones de infraestructura y la complejidad para balancear cargas docentes. Este problema se agrava por la necesidad de cumplir con normativas de calidad educativa y, a la vez, ofrecer una experiencia estudiantil eficiente, requiriendo un sistema más escalable, ágil y transparente para la asignación de recursos.

### Objetivos del Proyecto
- Automatizar la generación de horarios académicos.
- Minimizar conflictos de asignación y solapamientos.
- Optimizar recursos institucionales: aulas, docentes.
- Reducir tiempos administrativos.
- Maximizar las opciones horarias estudiantiles.
- Visualizar datos de recursos para la toma de decisiones.
- Garantizar la escalabilidad del sistema.
- Habilitar enseñanza híbrida.

### Alcance del Proyecto

**Incluye:**
- Modelado del problema como CSP / optimización combinatoria.
- Registro de estudiantes, cursos y aulas.
- Validación de métricas (créditos y prerrequisitos).
- Generación automática de horarios sin conflictos.
- Visualización de horarios.

**No incluye:**
- Integración con sistemas reales universitarios.
- Infraestructura móvil nativa.
- Infraestructura productiva real.

### Riesgos y Problemas Identificados (al inicio)
- Alta complejidad algorítmica.
- Limitaciones de tiempo (12 semanas).
- Falta de datos reales para pruebas.
- Cambios en requerimientos del currículo.

### Entregables Comprometidos
1. Documento de análisis del problema.
2. Modelo formal (CSP/Optimización).
3. Código de arquitectura SPA + API REST.
4. Código funcional (Frontend + Backend).
5. Pruebas unitarias e integración.
6. Repositorio GitHub documentado.
7. PMV etiquetado como v1.0.
8. Video demostrativo (máx. 5 minutos).
9. Informe técnico final.
10. Cumplimiento de requerimientos del currículo.

### Finanzas
| Concepto | Presupuesto |
|---|---|
| Software | $0 (open-source) |
| Infraestructura | Local / gratuita (PC personal y servicios *free*) |

### Cronograma de Hitos
| Hito | Semana |
|---|---|
| Sprint 0 — Análisis y planificación | Semana 2 |
| Modelado formal del problema | Semana 4 |
| Diseño de arquitectura | Semana 5 |
| Implementación Backend | Semana 8 |
| Implementación Frontend | Semana 10 |
| Integración y pruebas | Semana 11 |
| Entrega PMV v1.0 + Video | Semana 12–16 |

### Stakeholders Clave
- Estudiantes
- Docentes
- Personal administrativo
- Universidad

### Equipo Interno del Proyecto
| Rol | Integrante |
|---|---|
| Docente del Curso | Gamarra Moreno, Job |
| Project Manager | Meza Calderón, Ana Cristina |
| Scrum Master | Escobar Bendezú, Aldrin Edwin |
| Frontend Developer | López Rodríguez, Axel Andre |
| Backend Developer | Escobar Bendezú, Aldrin Edwin |

---

## 2. Revisión de Cumplimiento al Cierre

### 2.1 Verificación de Objetivos

| Objetivo Original | ¿Se cumplió? | Evidencia |
|---|---|---|
| Automatizar la generación de horarios académicos | ✅ Sí | Algoritmo CSP funcional con OR-Tools (`horario_repository.py`) |
| Minimizar conflictos de asignación y solapamientos | ✅ Sí | Restricciones duras de no solapamiento de aula y docente, verificadas con validación SQL independiente |
| Optimizar recursos institucionales (aulas, docentes) | ✅ Sí | Restricción de capacidad de aulas y disponibilidad docente implementadas |
| Reducir tiempos administrativos | ✅ Sí | Generación automática en segundos (límite de cómputo: 10s) frente a un proceso manual |
| Maximizar opciones horarias estudiantiles | ✅ Sí | Modelo de slots flexibles (Lunes-Viernes, 08:00-22:00) |
| Visualizar datos de recursos para decisiones | ✅ Sí | Dashboard funcional (`frontend/src/app/pages/dashboard/`) |
| Garantizar la escalabilidad del sistema | ⚠️ Parcial | Arquitectura modular diseñada para escalar; no se ejecutaron pruebas de carga con volúmenes reales (fuera del alcance del PMV) |
| Habilitar enseñanza híbrida | ✅ Sí | Modelo de datos no restringe modalidad presencial/virtual de los bloques horarios |

**Resultado:** 7 de 8 objetivos cumplidos en su totalidad; 1 objetivo (escalabilidad) validado a nivel de diseño, pendiente de validación empírica con carga real — consistente con la exclusión de "infraestructura productiva real" definida en el propio alcance del Charter.

### 2.2 Verificación de Alcance

Ver detalle completo en el [Informe Final del Proyecto](./01-informe-final-proyecto.md), sección 2. En síntesis: **el alcance comprometido se cumplió al 100%**, sin invadir las exclusiones explícitamente definidas (integración con sistemas reales, infraestructura móvil nativa, infraestructura productiva).

### 2.3 Verificación de Riesgos Anticipados

| Riesgo anticipado en el Charter | Resultado al cierre |
|---|---|
| Alta complejidad algorítmica | Gestionado exitosamente mediante especificación formal previa (`Spec.md`) y modelo CSP con OR-Tools. Ver IMP-02. |
| Limitaciones de tiempo (12 semanas) | El proyecto cerró en la semana 13, dentro de la ventana de entrega ampliada (semana 12-16) prevista en el propio Charter. |
| Falta de datos reales para pruebas | Se materializó parcialmente; mitigado con datos sintéticos representativos. Ver IMP-01 y SUP-01. |
| Cambios en requerimientos del currículo | No se registraron cambios significativos de requerimientos durante la ejecución. |

### 2.4 Verificación de Entregables

Ver tabla de trazabilidad completa en el [Informe Final del Proyecto](./01-informe-final-proyecto.md), sección 2.3. **9 de 10 entregables completados al 100%**; 1 entregable (video demostrativo) pendiente de enlace final antes del cierre administrativo definitivo.

### 2.5 Verificación de Finanzas

Presupuesto ejecutado: **$0**, sin desviación respecto a lo comprometido (ver Informe Final del Proyecto, sección 5).

### 2.6 Verificación de Cronograma

Cumplido dentro de la ventana planificada, con una extensión controlada de la fase de integración y pruebas que no comprometió la fecha límite de entrega (ver Informe Final del Proyecto, sección 4).

---

## 3. Criterios de Éxito — Veredicto Final

| Criterio de Éxito | Veredicto |
|---|---|
| El sistema genera horarios sin conflictos de aula/docente | ✅ Cumplido |
| El sistema respeta restricciones de créditos y prerrequisitos | ✅ Cumplido |
| El proyecto se entrega dentro del presupuesto de $0 | ✅ Cumplido |
| El proyecto se entrega dentro de la ventana de 12-16 semanas | ✅ Cumplido (semana 13) |
| El código cumple estándares de calidad (W3C, ISO/IEC 25010, OWASP, WCAG, Green Software) | ✅ Cumplido (Quality Gate Passed, OWASP 9/10, WCAG corregido, Green Software aplicado) |
| El sistema es percibido como usable por usuarios reales | ✅ Cumplido (SUS 87.5/100) |

**Veredicto del Project Manager:** el proyecto **cumple los requisitos de alto nivel y los criterios de éxito** establecidos en el Acta de Constitución. Se autoriza el cierre formal del proyecto, con la única observación pendiente de completar el enlace del video demostrativo en el `README.md` del repositorio.

---
*Documento elaborado conforme al enfoque PMBOK como parte de la fase de control y cierre del proyecto, en revisión del Acta de Constitución original (`docs/inicio/Project-charter.png`). Última actualización: 21 de junio de 2026.*
