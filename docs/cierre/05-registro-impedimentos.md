# Registro de Impedimentos (Impediment Log)
## HorarioSmart — Fase de Control y Cierre

> Este registro documenta los obstáculos que frenaron el progreso del equipo durante la ejecución del proyecto (distintos de los defectos técnicos del producto), su impacto en el avance del trabajo y las acciones de mitigación aplicadas por el Scrum Master.

---

## 1. Registro de Impedimentos

| ID | Impedimento | Tipo | Impacto en el Avance | Detectado por | Acción de Mitigación | Estado |
|---|---|---|---|---|---|---|
| IMP-01 | **Falta de datos reales** de matrícula, docentes, cursos y aulas de una institución educativa para realizar pruebas representativas. | Disponibilidad de información | Medio — obligó al equipo a construir conjuntos de datos sintéticos para validar el algoritmo CSP. | Equipo completo (planificación) | Generación de datos de prueba sintéticos pero realistas, definidos en el Acta de Constitución como riesgo aceptado del PMV. | **Cerrado — Mitigado** |
| IMP-02 | **Alta complejidad algorítmica** del problema de generación de horarios (CSP con múltiples restricciones interdependientes), que ralentizó el avance de la implementación del backend. | Técnico | Alto — implicó tiempo adicional de investigación y modelado matemático antes de poder codificar el solver. | Escobar Bendezú, Aldrin (Backend) | Elaboración de una especificación formal (`Spec.md`) previa a la implementación, reduciendo iteraciones de prueba y error en el código. | **Cerrado — Mitigado** |
| IMP-03 | **Curva de aprendizaje en Google OR-Tools** (librería de optimización combinatoria), no utilizada previamente por el equipo. | Técnico / Conocimiento | Medio — retrasó la primera versión funcional del solver respecto a la estimación inicial. | Escobar Bendezú, Aldrin (Backend) | Estudio dirigido de la documentación oficial de `ortools.sat.python.cp_model` y prototipado incremental de restricciones (duras antes que blandas). | **Cerrado — Mitigado** |
| IMP-04 | **Configuración local de SonarQube** (instalación, gestión de espacio en disco mediante *junction* a unidad secundaria) consumió tiempo de equipo no estimado en el backlog. | Herramientas / Infraestructura | Medio — desplazó tiempo planificado para otras tareas del sprint de integración. | Equipo completo | Instalación de SonarQube Community Build en entorno local con redirección de almacenamiento (`D:\sonarqube-data`); configuración de *scanner* y reportes de cobertura (LCOV/Cobertura XML). | **Cerrado — Mitigado** |
| IMP-05 | **Disponibilidad horaria limitada del equipo** (3 integrantes compatibilizando el proyecto con otras cargas académicas), dificultando la coordinación de sesiones de trabajo conjunto y revisiones de código. | Organizacional | Bajo-Medio — algunas revisiones de código e integraciones se realizaron de forma asíncrona. | Meza Calderón, Ana Cristina (PM) | Adopción de comunicación constante (mensajería) y comités breves de sincronización al cierre de cada sprint, conforme a las normas de trabajo definidas en `docs/inicio/inicio.md`. | **Cerrado — Mitigado** |

---

## 2. Resumen de Impedimentos

| Indicador | Valor |
|---|---|
| Impedimentos identificados | 5 |
| Impedimentos cerrados/mitigados al cierre | 5 |
| Impedimentos abiertos al cierre | 0 |
| Impedimentos con impacto Alto | 1 (IMP-02) |
| Impedimentos con impacto Medio | 3 (IMP-01, IMP-03, IMP-04) |
| Impedimentos con impacto Bajo-Medio | 1 (IMP-05) |

---

## 3. Evidencia de Gestión Activa del Equipo

Todos los impedimentos registrados fueron identificados de manera proactiva por el equipo durante las retrospectivas de sprint y gestionados antes de convertirse en bloqueos críticos para el cronograma. En particular, el impedimento de mayor impacto (**IMP-02**, complejidad algorítmica) se resolvió mediante una decisión metodológica clave: invertir tiempo adicional en especificación formal antes de codificar, lo cual evitó retrabajos posteriores en la lógica central del sistema (`horario_repository.py`).

Ningún impedimento permaneció abierto al cierre del proyecto ni impactó negativamente la fecha de entrega comprometida en el Acta de Constitución.

---
*Documento elaborado conforme al enfoque PMBOK como parte de la fase de control y cierre del proyecto. Última actualización: 21 de junio de 2026.*
