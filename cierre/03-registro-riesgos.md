# Registro de Riesgos (Risk Register)
## HorarioSmart — Fase de Control y Cierre

> Este documento actualiza, al cierre del proyecto, el registro de riesgos identificado originalmente en la fase de planificación (`docs/planificación/Riesgos_Oportunidades.md`), incorporando el **estado final** y la **evidencia de cierre** de cada riesgo.

---

## 1. Registro de Riesgos

| ID | Descripción del Riesgo | Categoría | Probabilidad | Impacto | Estrategia de Respuesta Aplicada | Estado Final | Fecha de Identificación | Fecha de Cierre |
|---|---|---|---|---|---|---|---|---|
| R-01 | **Falta de solución posible:** el sistema no logra encontrar un horario válido por falta de aulas o exceso de cursos registrados. | Técnico / Algorítmico | Media | Alto (bloquea la generación del horario) | Mensaje claro al usuario cuando el solver retorna `INFEASIBLE`; sugerencia de agregar aulas o reducir cursos; filtrado de aulas por tamaño. | **Mitigado — No materializado** | Semana 4 (modelado formal) | 21/06/2026 |
| R-02 | **Demora en la generación del horario:** el proceso de optimización toma demasiado tiempo y congela el sistema. | Técnico / Rendimiento | Baja | Medio | Límite de cómputo de 10 segundos en el solver OR-Tools; el proceso se detiene automáticamente al superar el límite. | **Mitigado — No materializado** | Semana 4 | 21/06/2026 |
| R-03 | **Datos incompletos o incorrectos:** información de docentes, cursos o aulas con errores, vacíos o referencias cruzadas inválidas. | Datos / Calidad | Media | Alto | Validación estricta de datos antes de persistir; reglas de integridad a nivel de base de datos. | **Mitigado — Parcialmente materializado** (ver Impedimento IMP-01 por falta de datos reales para pruebas) | Semana 4 | 21/06/2026 |
| R-04 | **Fallo en servicios externos:** pérdida de conexión a la base de datos o falla del motor de optimización (OR-Tools). | Infraestructura / Dependencias | Baja | Alto | Manejo de excepciones (*try/except*) en capas críticas; mensajes amigables al usuario en lugar de errores de sistema sin tratar. | **Mitigado — No materializado** | Semana 4 | 21/06/2026 |

### 1.1 Riesgos adicionales identificados durante la ejecución (no previstos en planificación)

| ID | Descripción del Riesgo | Categoría | Probabilidad | Impacto | Estrategia de Respuesta Aplicada | Estado Final |
|---|---|---|---|---|---|---|
| R-05 | **Acumulación de deuda técnica** por falta de análisis de calidad continuo, detectada tardíamente vía SonarQube (129 issues). | Calidad de software | Alta (materializado) | Medio | Plan de corrección iterativo ejecutado en bloque previo al cierre; ver Registro de Defectos. | **Materializado — Cerrado y corregido al 100%** |
| R-06 | **Falsos positivos de seguridad** en el análisis estático (Security Hotspots) que podrían generar una calificación de seguridad incorrecta si no se revisan manualmente. | Seguridad | Media (materializado) | Bajo | Revisión manual del hotspot (`random.randint` en `horario_repository.py`) con justificación técnica; marcado como *Safe*. | **Materializado — Cerrado sin impacto real** |

---

## 2. Registro de Oportunidades

| ID | Impacto Positivo Esperado | Estrategia de Aprovechamiento | Estado al Cierre |
|---|---|---|---|
| O-01 | **Horarios más cómodos:** mejora de la experiencia de estudiantes y docentes evitando horas muertas prolongadas o clases tardías. | Agregar reglas matemáticas adicionales (restricciones blandas) para agrupar clases y reducir tiempos vacíos. | Restricciones blandas definidas en `constitution.md`; implementación completa queda como backlog de mejora futura. |
| O-02 | **Uso en otras universidades:** posibilidad de convertir el proyecto en un producto reutilizable por otras instituciones. | Hacer configurables las reglas del algoritmo para adaptarse a distintas instituciones. | No abordado en el PMV (fuera del alcance comprometido); queda documentado como oportunidad futura. |
| O-03 | **Horarios fijos asignados manualmente:** permitir a administradores fijar ciertos cursos manualmente antes de ejecutar el resto del algoritmo. | Guardar horarios fijos en el modelo antes de invocar al solver. | No implementado en el PMV; identificado como mejora futura en el backlog (`docs/inicio/inicio.md`). |

---

## 3. Análisis de Cierre

### 3.1 Relación de riesgos con restricciones del problema
El riesgo **R-01** se relaciona directamente con la rigurosidad de las restricciones duras del modelo CSP (capacidad de aulas, sesiones requeridas, no solapamiento). Durante la ejecución del proyecto, este riesgo **no se materializó** gracias a que los conjuntos de datos de prueba utilizados mantuvieron una proporción adecuada entre cursos, aulas y docentes disponibles.

### 3.2 Relación de riesgos con limitaciones técnicas
El riesgo **R-02** se gestionó exitosamente mediante el límite de cómputo de 10 segundos, validado en las pruebas de rendimiento del backend. No se registraron incidentes de bloqueo del sistema por tiempos de generación excesivos durante el proyecto.

### 3.3 Relación de riesgos con dependencias externas
El riesgo **R-04** no se materializó durante el desarrollo ni las pruebas; el manejo de excepciones implementado fue validado mediante pruebas de integración que simulan fallos de base de datos.

### 3.4 Riesgo emergente más relevante del proyecto
El riesgo **R-05** (acumulación de deuda técnica) fue, en retrospectiva, el de mayor impacto real sobre el cronograma del proyecto, al concentrar un esfuerzo correctivo significativo en la fase de integración y pruebas (ver Informe Final de Lecciones Aprendidas, sección 4). Se cerró exitosamente, pero motiva una recomendación explícita para proyectos futuros: integrar el análisis de calidad estático desde etapas tempranas.

---

## 4. Resumen de Cierre

| Indicador | Valor |
|---|---|
| Riesgos totales identificados (planificación + ejecución) | 6 |
| Riesgos materializados con impacto negativo neto al cierre | 0 |
| Riesgos materializados y corregidos sin impacto en alcance/costo | 2 (R-05, R-06) |
| Riesgos mitigados sin materializarse | 4 (R-01 a R-04) |
| Oportunidades aprovechadas en el PMV | 0 de 3 (documentadas como backlog futuro) |

---
*Documento elaborado conforme al enfoque PMBOK como parte de la fase de control y cierre del proyecto. Última actualización: 21 de junio de 2026.*
