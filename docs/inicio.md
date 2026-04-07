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

- RF01: Registrar cursos, docentes y aulas  
- RF02: Definir disponibilidad de docentes  
- RF03: Generar horarios automáticamente  
- RF04: Detectar conflictos  
- RF05: Permitir edición manual de horarios  

### Requerimientos No Funcionales

- RNF01: Interfaz amigable  
- RNF02: Tiempo de generación eficiente  
- RNF03: Escalabilidad del sistema  
- RNF04: Seguridad en el manejo de datos  

---

## Repositorio

Repositorio del proyecto:  
👉 https://github.com/Hannah2112-hub/TP2
