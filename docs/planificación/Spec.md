# Especificación Formal del Sistema HorarioSmart

## 1. Definición de Elementos del Sistema

### 1.1 Entradas
El algoritmo de programación de horarios recibe los siguientes conjuntos de datos desde la base de datos PostgreSQL/SQL Server:
- **Cursos Activos ($C$):** Conjunto de cursos con atributos $c_{id}$, $c_{cupos}$ y $c_{docente}$.
- **Aulas Activas ($A$):** Conjunto de espacios físicos con atributos $a_{id}$ y $a_{capacidad}$.
- **Configuración de Tiempo ($T$):** Matriz tridimensional definida por $d \in \{1,2,3,4,5\}$ (Lunes a Viernes) y $h \in \{08:00, 10:00, ..., 20:00\}$ (bloques de 2 horas). Esto produce un conjunto de slots discretos $S$.

### 1.2 Salidas
- **Asignaciones Válidas ($H$):** Conjunto de registros de horario generados, donde cada entrada $h_i \in H$ se define como una tupla $(c_{id}, a_{id}, d, h_{inicio}, h_{fin})$.
- **Reporte de Estado:** Objeto JSON con el resultado de la operación, conteo de horarios creados (`HorariosCreados`) y un log de errores/advertencias (`Detalles` - ej. cursos sin aulas con capacidad suficiente).

### 1.3 Reglas de Negocio
- Toda sesión de clase estándar tiene una duración ininterrumpida de 2 horas.
- La generación de un nuevo horario sobrescribe (marca como inactivos o elimina) los horarios previamente generados (`DELETE FROM horarios WHERE activo = TRUE`), garantizando que la fuente de la verdad siempre sea la última ejecución exitosa del CSP.
- El sistema no puede programar un curso en un aula si la capacidad de la misma es menor a los cupos inscritos/esperados del curso. Estas variables se eliminan del dominio antes de enviar al solver.

### 1.4 Casos Límite (Edge Cases)
- **Falta de Recursos Activos:** No hay docentes, cursos o aulas registrados. El sistema aborta tempranamente sin llamar a OR-Tools.
- **Sobre-restricción Matemática (Infeasibility):** Existen más cursos que los slots/aulas combinados pueden soportar, o la disponibilidad del docente colisiona insalvablemente. El solver retorna estado `INFEASIBLE`. El sistema informa al usuario para que libere recursos (ej. añada aulas o distribuya carga docente).
- **Docente No Asignado:** Un curso puede no tener un docente asignado en etapa temprana (`docenteid IS NULL`). El sistema permite programar el aula y el horario ignorando la colisión docente para ese curso particular.

---

## 2. Análisis de Coherencia

### 2.1 Especificación vs Modelado del Problema
La especificación de "evitar conflictos" se traduce de forma coherente en el modelado del Constraint Satisfaction Problem (CSP) mediante la definición de variables booleanas $x_{c, a, s}$ que representan si un curso $c$ está en el aula $a$ en el slot $s$.
Las restricciones operativas se modelan como ecuaciones matemáticas lineales:
- **Capacidad:** Pre-filtrado estricto `if capacidad < cupos: continue`. Reduce el espacio de búsqueda.
- **Sesiones:** $\sum_{a,s} x_{c,a,s} = 2 \quad \forall c$.
- **Colisiones Aula:** $\sum_{c} x_{c,a,s} \leq 1 \quad \forall a, s$.
- **Colisiones Docente:** $\sum_{c \in C_{docente}} \sum_{a} x_{c,a,s} \leq 1 \quad \forall docente, s$.

### 2.2 Especificación vs Implementación
La implementación en `horario_repository.py` refleja fielmente este modelo utilizando la librería `ortools.sat.python.cp_model`. Además, se implementa una función `validar()` completamente independiente en SQL puro para proveer una doble comprobación (double-check), verificando que la salida del motor OR-Tools efectivamente cumpla la especificación en la base de datos (con cláusulas `OVERLAPS`).

### 2.3 Reducción de Ambigüedad en Requerimientos
El requerimiento inicial "Generación automática de horarios sin conflictos" era altamente ambiguo. En esta especificación, se reduce la ambigüedad al definir exactamente:
1. Qué es un conflicto: (a) Traslape espacio-temporal de aula, (b) Traslape temporal de docente, (c) Deficiencia de capacidad.
2. Qué es un bloque temporal: Slots rígidos de 2 horas generados matricialmente, no horarios continuos arbitrarios (que volverían el problema NP-Hard de empaquetamiento).

### 2.4 Anticipación de Conflictos
El modelo anticipa los conflictos al nivel del árbol de decisiones lógicas (CSP). Al limitar las sumatorias booleanas a $\leq 1$, el solver descarta automáticamente cualquier rama del árbol de posibilidades que implicaría un solapamiento (ej. el mismo docente a la misma hora en distinto lugar). A diferencia de un algoritmo "Greedy", que podría llegar a un callejón sin salida (dead end) y fallar, el motor CSP hace "backtracking" inteligente para asegurar una asignación globalmente válida.
