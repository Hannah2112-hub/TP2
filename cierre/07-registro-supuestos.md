# Registro de Supuestos (Assumption Log)
## HorarioSmart — Fase de Control y Cierre

> Este registro consolida y valida, al cierre del proyecto, los supuestos definidos originalmente en la fase de inicio (`docs/inicio/inicio.md`), documentando su impacto potencial y su estado de validación durante la ejecución. Sirve como documentación útil para futuros proyectos que deseen aprender del proceso actual.

---

## 1. Registro de Supuestos

| ID | Supuesto | Categoría | Impacto si resultaba falso | Estado de Validación al Cierre |
|---|---|---|---|---|
| SUP-01 | La información ingresada al sistema (estudiantes, docentes, cursos, aulas) es correcta, completa y actualizada. | Datos | Alto — el sistema depende directamente de la calidad de los datos para generar horarios válidos; datos incorrectos producirían horarios inconsistentes sin que el sistema pudiera detectarlo. | **Parcialmente validado.** Se implementaron validaciones de integridad a nivel de base de datos y backend, mitigando el riesgo, pero el supuesto de calidad del dato de origen permanece bajo responsabilidad del usuario que registra la información (no se contó con una fuente institucional real para verificación completa — ver IMP-01). |
| SUP-02 | Los prerrequisitos de los cursos están correctamente definidos en el sistema. | Académico | Medio — de no cumplirse, se podrían generar matrículas académicamente incoherentes sin que el PMV las detecte. | **Validado dentro del alcance del PMV.** La validación de prerrequisitos se implementó (RF-02) y fue probada con datos sintéticos coherentes; no se validó contra una malla curricular institucional real, lo cual queda fuera del alcance comprometido. |
| SUP-03 | Los docentes cuentan con una disponibilidad previamente registrada en el sistema. | Operativo | Medio — sin esta información, el algoritmo no podría respetar restricciones de tiempo docente al generar el horario. | **Validado.** El modelo de datos y el algoritmo CSP consideran la disponibilidad docente como entrada obligatoria; validado mediante pruebas unitarias del backend. |
| SUP-04 | Los estudiantes seleccionan cursos dentro del rango permitido de créditos (20–22 créditos). | Académico | Bajo-Medio — de no cumplirse, se simplificaría incorrectamente la lógica de validación de matrícula del PMV. | **Validado.** La restricción de créditos se implementó y probó como parte de RF-02 (Validación de matrícula). |
| SUP-05 | Las aulas poseen características definidas (capacidad, tipo, equipamiento) suficientes para asignar espacios adecuados. | Infraestructura de datos | Medio — sin esta información, el algoritmo no podría aplicar la restricción dura de capacidad de aulas. | **Validado.** La restricción de capacidad de aulas (`c.cupos ≤ a.capacidad`) se implementó como restricción dura del modelo CSP y fue verificada en pruebas. |
| SUP-06 | El sistema operará inicialmente en un entorno controlado (no productivo). | Alcance / Infraestructura | Bajo — de requerirse entorno productivo desde el inicio, se habría necesitado presupuesto e infraestructura adicional no contemplados ($0). | **Validado.** El alcance excluyó explícitamente la infraestructura productiva real (definido en el Project Charter); el sistema se ejecutó en entorno local/gratuito durante todo el ciclo de vida del proyecto. |
| SUP-07 | No se considerarán cambios en tiempo real durante la generación del horario (el proceso es de tipo *batch*, no interactivo). | Funcional / Algorítmico | Medio — de requerirse regeneración en tiempo real ante cada cambio, el diseño del solver CSP habría requerido un enfoque incremental más complejo. | **Validado.** El sistema implementa regeneración completa (`DELETE ... WHERE activo = TRUE` seguido de nueva generación), conforme a la regla de negocio documentada en `Spec.md`, sin necesidad de un modelo incremental. |

---

## 2. Supuestos Adicionales Identificados Durante la Ejecución

| ID | Supuesto | Categoría | Impacto si resultaba falso | Estado de Validación al Cierre |
|---|---|---|---|---|
| SUP-08 | Las herramientas open-source utilizadas (FastAPI, Angular, OR-Tools, SonarQube Community, PostgreSQL/SQL Server) serían suficientes para cumplir los objetivos del proyecto sin incurrir en costos. | Técnico / Financiero | Alto — de no cumplirse, se habría comprometido el presupuesto de $0 definido en el Charter. | **Validado.** El proyecto se ejecutó íntegramente con herramientas gratuitas/open-source, sin desviación presupuestaria (ver Informe Final del Proyecto, sección 5). |
| SUP-09 | Un equipo de 3 integrantes sería suficiente para cubrir los roles de Project Manager, Scrum Master, Backend Developer y Frontend Developer simultáneamente (con superposición de roles). | Organizacional | Medio — de no cumplirse, se habría requerido redistribuir el alcance o extender el cronograma. | **Validado.** El equipo cubrió exitosamente los cuatro roles mediante superposición (Aldrin Escobar como Backend Developer y Scrum Master), sin impacto negativo documentado en el cronograma final. |

---

## 3. Resumen de Validación

| Indicador | Valor |
|---|---|
| Supuestos totales registrados | 9 |
| Supuestos validados completamente | 7 |
| Supuestos validados parcialmente (dentro del alcance del PMV) | 2 (SUP-01, SUP-02) |
| Supuestos invalidados | 0 |

**Conclusión:** ningún supuesto crítico del proyecto fue invalidado durante la ejecución. Los supuestos **SUP-01** y **SUP-02** se consideran validados *dentro del alcance del PMV* (datos sintéticos controlados), pero requieren re-validación explícita con datos institucionales reales en una eventual fase de despliegue productivo, conforme a la exclusión de alcance documentada en el Acta de Constitución.

---
*Documento elaborado conforme al enfoque PMBOK como parte de la fase de control y cierre del proyecto. Última actualización: 21 de junio de 2026.*
