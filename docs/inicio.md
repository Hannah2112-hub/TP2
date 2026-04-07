# Proyecto: HorarioSmart

## Tabla de Contenidos
- [Declaracion de la Visión del Proyecto](#vision-del-proyecto)
- [Enfoque del Proyecto](#enfoque-del-proyecto)
- [Problema](#problema)
- [Backlog](#backlog)
- [Equipo](#equipo)
- [Supuestos y Restricciones](#supuestos-y-restricciones)
- [Requerimientos](#requerimientos)
- [Repositorio](#repositorio)

---

## Declaracion De La Visión del Proyecto

Para coordinadores académicos y estudiantes<br>
Que necesitan optimizar la planificación de horarios<br>
El sistema HorarioSmart<br>
Es una aplicación web inteligente<br>
Que permite generar horarios académicos automáticamente sin conflictos<br>
A diferencia de los métodos manuales tradicionales<br>
Nuestro sistema utiliza algoritmos de optimización para mejorar la eficiencia y calidad de los horarios generados<br>

---

## Enfoque del Proyecto

El proyecto se basa en un enfoque orientado a la optimización, utilizando:

- Algoritmos de asignación automática  
- Restricciones académicas (disponibilidad, capacidad, horarios)  
- Minimización de conflictos (cruces de clases, docentes duplicados, etc.)  
- Interfaz amigable para la gestión de horarios  

Se busca una solución escalable que pueda adaptarse a diferentes instituciones educativas.

---

## Problema

La generación manual de horarios académicos presenta múltiples dificultades:

- Conflictos entre cursos y docentes  
- Uso ineficiente de aulas  
- Alto consumo de tiempo en planificación  
- Errores humanos frecuentes  

Este proyecto busca resolver estos problemas mediante automatización inteligente.

---

## Backlog

### Funcionalidades principales

- [ ] Registro de cursos  
- [ ] Registro de docentes  
- [ ] Registro de aulas  
- [ ] Definición de disponibilidad de docentes  
- [ ] Generación automática de horarios  
- [ ] Visualización de horarios  
- [ ] Edición manual de horarios  
- [ ] Validación de conflictos  

### Mejoras futuras

- [ ] Exportación a PDF/Excel  
- [ ] Integración con sistemas académicos  
- [ ] Uso de inteligencia artificial para optimización avanzada  

---

## Equipo

- Desarrollador(es):  
  - Escobar Bendezu Aldrin Edwin
  - Lopez Rodriguez Axel Andre
  - Meza Calderon Ana Cristina
    
- Roles:  
  - Backend  
  - Frontend  
  - Análisis  
  - Testing  

---

## Supuestos y Restricciones

### Supuestos

Para el desarrollo del Producto Mínimo Viable (PMV), se establecen los siguientes supuestos:

- La información ingresada al sistema es correcta, completa y actualizada.  
  Esto permite evitar errores en la generación de horarios, ya que el sistema depende directamente de la calidad de los datos.

- Los prerrequisitos de los cursos están correctamente definidos.  
  Se asume esta condición para garantizar la coherencia académica sin necesidad de validar estructuras complejas en el PMV.

- Los docentes cuentan con una disponibilidad previamente registrada.  
  Esto facilita la asignación automática de horarios respetando sus restricciones de tiempo.

- Los estudiantes seleccionan cursos dentro del rango permitido de créditos.  
  Permite simplificar la lógica inicial del sistema, evitando validaciones complejas adicionales.

- Las aulas poseen características definidas (capacidad, tipo, equipamiento).  
  Esto permite asignar espacios adecuados según las necesidades de cada curso.

- El sistema operará inicialmente en un entorno controlado.  
  Reduce la complejidad en las primeras etapas del desarrollo.

- No se considerarán cambios en tiempo real durante la generación del horario.  
  Esto simplifica el algoritmo en el PMV, permitiendo enfocarse en la generación inicial.

---

### Restricciones

#### a) Restricciones técnicas

- Limitación en la capacidad de procesamiento.  
  El sistema debe generar soluciones en tiempos razonables, lo cual limita la complejidad de los algoritmos utilizados.

- Implementación en arquitectura web (SPA + API REST).  
  Responde a los lineamientos del proyecto y garantiza separación de responsabilidades.

---

#### b) Restricciones académicas

- Cumplimiento obligatorio de prerrequisitos.  
  Garantiza la coherencia en la formación académica de los estudiantes.

- Límite de créditos por estudiante (20–22).  
  Evita sobrecarga académica y asegura cumplimiento de normativas institucionales.

- Asignación coherente según plan de estudios.  
  Permite mantener la estructura curricular definida.

---

#### c) Restricciones operativas

- Disponibilidad limitada de docentes.  
  Reduce las combinaciones posibles y afecta la generación de horarios.

- Disponibilidad limitada de aulas.  
  Obliga a optimizar el uso de espacios físicos.

- Restricciones de horarios institucionales.  
  Limita los bloques de tiempo disponibles para asignación.

---

#### d) Restricciones sociales

- Equidad en la asignación de horarios.  
  Busca evitar favoritismos o distribución desigual de horarios.

- Evitar sobrecarga en horarios pico.  
  Mejora la experiencia de estudiantes y docentes.

---

#### e) Restricciones de seguridad

- Protección de datos personales.  
  Necesaria para cumplir con normativas de privacidad.

- Control de acceso basado en roles.  
  Garantiza que cada usuario acceda solo a la información correspondiente.

---

#### f) Restricciones ambientales

- Uso eficiente de recursos computacionales.  
  Permite reducir costos operativos y mejorar rendimiento.

- Minimización del consumo energético.  
  Alineado con prácticas de desarrollo sostenible (Green Software).

---

## Requerimientos

### Requerimientos Funcionales

# 1. Visión General del Proyecto

El sistema consiste en el desarrollo de un **Producto Mínimo Viable (PMV)** de una aplicación web para la generación automática de horarios académicos en instituciones de educación superior con currículo flexible.

El sistema permitirá gestionar entidades académicas (estudiantes, docentes, cursos y aulas), validar restricciones académicas y generar horarios libres de conflictos mediante un modelo de optimización.

El alcance del sistema incluye la generación de horarios válidos en función de restricciones definidas, así como su visualización para usuarios finales.

---

# 2. Especificación de Requerimientos Funcionales (SMART)

| ID | Nombre del Requerimiento | Descripción Técnica (Trigger/Lógica/Resultado) | Criterio de Aceptación (Dado que... Cuando... Entonces...) |
| :--- | :--- | :--- | :--- |
| RF-01 | Registro de entidades académicas | El sistema recibe datos de entrada mediante formularios para estudiantes, docentes, cursos y aulas, valida su estructura y los almacena en la base de datos. | Dado que el usuario ingresa datos válidos, cuando envía el formulario, entonces el sistema registra la entidad y la persiste correctamente. |
| RF-02 | Validación de matrícula | El sistema recibe la selección de cursos de un estudiante, valida créditos máximos y prerrequisitos antes de confirmar la matrícula. | Dado que un estudiante selecciona cursos, cuando se valida la matrícula, entonces el sistema rechaza la operación si excede créditos o incumple prerrequisitos. |
| RF-03 | Generación automática de horarios | El sistema procesa las entidades registradas y ejecuta un algoritmo que asigna cursos a bloques horarios, docentes y aulas sin conflictos. | Dado que existen datos registrados, cuando se ejecuta la generación, entonces el sistema produce un horario sin solapamientos de aulas, docentes o cursos. |
| RF-04 | Validación de conflictos | El sistema analiza el horario generado y verifica que no existan conflictos de asignación en recursos o tiempos. | Dado un horario generado, cuando se ejecuta la validación, entonces el sistema confirma que no existen conflictos o reporta inconsistencias. |
| RF-05 | Visualización de horarios | El sistema presenta los horarios generados en una interfaz estructurada por estudiante o docente. | Dado que existe un horario generado, cuando el usuario accede a la vista, entonces el sistema muestra correctamente los bloques horarios asignados. |

---

# 3. Árbol de Calidad y Requerimientos No Funcionales (arc42)

| Categoría arc42 | Atributo de Calidad | Requerimiento Cuantificable (Métrica) | Justificación de Negocio |
| :--- | :--- | :--- | :--- |
| Rendimiento | Tiempo de generación | El sistema debe generar un horario completo para hasta 100 cursos en ≤ 10 segundos (percentil 95). | Si no se cumple, el sistema no será usable en contextos reales. |
| Rendimiento | Tiempo de respuesta | Las operaciones CRUD deben responder en ≤ 1 segundo (percentil 95). | Impacta directamente en la experiencia del usuario. |
| Escalabilidad | Volumen de datos | El sistema debe soportar al menos 500 estudiantes y 200 cursos sin degradación mayor al 20% del rendimiento. | Permite crecimiento del sistema sin rediseño inmediato. |
| Usabilidad | Facilidad de uso | Un usuario nuevo debe completar el registro de una entidad en ≤ 2 minutos sin asistencia. | Reduce curva de aprendizaje y errores operativos. |
| Seguridad | Control de acceso | El sistema debe restringir acceso a funcionalidades mediante autenticación y roles (admin/usuario). | Previene accesos no autorizados. |
| Seguridad | Protección de datos | Los datos sensibles deben almacenarse utilizando mecanismos de cifrado estándar (ej. hashing para credenciales). | Evita exposición de información crítica. |
| Disponibilidad | Tiempo operativo | El sistema debe estar disponible al menos el 95% del tiempo durante el periodo de uso. | Garantiza acceso continuo al sistema. |
| Mantenibilidad | Modularidad | El sistema debe estar organizado en módulos independientes (frontend/backend) con bajo acoplamiento. | Facilita mantenimiento y evolución del sistema. |
| Mantenibilidad | Testabilidad | Al menos el 70% de la lógica crítica debe ser cubierta por pruebas unitarias. | Reduce errores en cambios futuros. |

---

# 4. Notas de Refinamiento

Durante la especificación de requerimientos se identificaron términos ambiguos en la descripción inicial, los cuales fueron transformados en métricas verificables bajo el enfoque SMART:

- “Procesamiento rápido” → definido como ≤ 10 segundos para generación de horarios  
- “Sistema usable” → definido como registro en ≤ 2 minutos sin asistencia  
- “Alta seguridad” → definido mediante control de acceso y cifrado  
- “Escalable” → definido como soporte de volumen específico con tolerancia de degradación  

Estas transformaciones permiten que cada requerimiento sea medible, verificable y alineado con pruebas objetivas de cumplimiento (Pasa/No pasa), asegurando la viabilidad técnica del sistema.

---

## Repositorio

Repositorio del proyecto:  
👉 https://github.com/Hannah2112-hub/TP2
