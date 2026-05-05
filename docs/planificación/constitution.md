# Constitución del Sistema HorarioSmart (Spec-Driven Development)

## 1. Principios del Sistema
- **Automatización y Eficiencia:** El sistema busca eliminar la asignación manual de horarios, reduciendo errores humanos y tiempos de planificación mediante algoritmos de optimización.
- **Transparencia Arquitectónica:** Se mantiene una separación clara entre la interfaz de usuario (SPA con Angular) y la lógica de negocio/optimización (API REST con FastAPI).
- **Resolución Basada en Restricciones (CSP):** El problema de la calendarización no se aborda mediante heurísticas simples o enfoques greedy, sino a través de un modelo de Satisfacción de Restricciones (CSP) utilizando Google OR-Tools para garantizar matemáticamente la ausencia de conflictos.
- **Fiabilidad y Validación Continua:** Los horarios generados deben ser rigurosamente verificados contra cruces y límites de recursos tanto en el momento de su generación como a través de consultas analíticas (Validación SQL).

## 2. Reglas Globales
- **Integridad de Datos:** No se puede programar ningún curso que no cuente con un docente asignado (si se requiere) o una cantidad de cupos definida. Asimismo, las aulas deben tener una capacidad explícita.
- **Unidad de Tiempo Base:** La planificación se rige mediante "slots" o bloques horarios fijos (ej. bloques de 2 horas) dentro de un límite operativo institucional definido (Lunes a Viernes, 08:00 a 22:00).
- **Prioridad de Factibilidad:** La primera meta del sistema es encontrar una solución factible (horario libre de colisiones). La optimización de preferencias (soft constraints) entra en juego sólo si el espacio de soluciones lo permite en un tiempo razonable.

## 3. Restricciones Duras (Hard Constraints)
Son de cumplimiento obligatorio; su violación hace que el horario sea inválido.
1. **Capacidad de Aulas:** El número de cupos de un curso (`c.cupos`) debe ser estrictamente menor o igual a la capacidad del aula asignada (`a.capacidad`).
2. **Requisito de Sesiones:** Todo curso activo debe ser programado exactamente la cantidad de sesiones requeridas a la semana (ej. 2 sesiones de 2 horas).
3. **Distribución Semanal:** Un curso específico no puede ser programado más de una vez en un mismo día.
4. **No Solapamiento de Aulas:** Un aula específica solo puede albergar, como máximo, una sesión de un curso en un mismo slot temporal.
5. **No Solapamiento de Docentes:** Un docente no puede estar asignado a más de una sesión de curso simultáneamente en el mismo slot temporal.

## 4. Restricciones Blandas (Soft Constraints)
Son preferibles pero no bloqueantes; su violación no invalida la solución, pero reduce la "calidad" del horario.
1. **Minimización de Tiempos Muertos ("Huecos"):** Evitar espacios prolongados sin clases en el horario de un docente o estudiante.
2. **Balanceo de Carga Semanal:** Distribuir las horas de forma equitativa entre los días de la semana, evitando días sobrecargados y días vacíos.
3. **Horarios Extremos:** Minimizar las asignaciones en los últimos bloques de la noche (20:00 - 22:00) si hay disponibilidad en horas más tempranas.
4. **Uso Óptimo de Aulas:** Asignar cursos a aulas cuya capacidad sea lo más cercana posible a los cupos requeridos, evitando ocupar auditorios grandes para cursos de pocos alumnos si no es estrictamente necesario.
