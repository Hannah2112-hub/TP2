# Selección del Enfoque del Proyecto

---

## 1. Introducción

El desarrollo de un sistema para la generación automática de horarios académicos en universidades con currículo flexible representa un problema complejo, debido a la presencia de múltiples variables, restricciones interdependientes y la necesidad de optimización.

En este contexto, resulta fundamental seleccionar un enfoque metodológico y tecnológico adecuado que permita abordar dicha complejidad de manera estructurada, escalable y eficiente.

---

## 2. Enfoque Metodológico

### 2.1 Selección de Scrum

Se ha seleccionado la metodología ágil **Scrum** para la gestión del proyecto, debido a su capacidad para manejar entornos dinámicos y problemas complejos mediante iteraciones cortas y entregas incrementales.

Scrum permite descomponer el sistema en funcionalidades pequeñas (historias de usuario), facilitando el desarrollo progresivo del sistema y la validación continua de resultados.

---

### 2.2 Justificación Técnica

El uso de Scrum se justifica por las siguientes características del proyecto:

- El problema presenta **alta complejidad** debido a múltiples restricciones (docentes, aulas, horarios, estudiantes).
- Existen **requerimientos que pueden evolucionar**, especialmente en la lógica de generación de horarios.
- Se requiere una **validación continua del sistema**, particularmente del algoritmo de optimización.
- Permite organizar el trabajo en **sprints**, facilitando la planificación y control del avance.

---

### 2.3 Comparación de metodologías

Se realizó un análisis comparativo de distintas metodologías de desarrollo con el fin de seleccionar la más adecuada para el proyecto.

| Criterio | Scrum | Cascada | Kanban |
| :--- | :--- | :--- | :--- |
| Enfoque | Iterativo e incremental | Secuencial | Flujo continuo |
| Adaptabilidad a cambios | Alta | Baja | Media |
| Manejo de incertidumbre | Alto | Bajo | Medio |
| Estructura del proceso | Basado en sprints definidos | Fases rígidas | Sin iteraciones definidas |
| Entregas | Incrementales y frecuentes | Una entrega final | Continuas |
| Adecuación al problema | Alta (problemas complejos) | Baja (problemas estables) | Media |
| Control del avance | Alto (revisiones por sprint) | Medio | Variable |
| Complejidad de implementación | Media | Baja | Baja |

---

### 2.4 Análisis

- **Scrum** permite gestionar la complejidad del problema mediante iteraciones, facilitando la validación progresiva del sistema.
- **Cascada** no resulta adecuado debido a su rigidez frente a cambios en los requerimientos.
- **Kanban** ofrece flexibilidad, pero carece de una estructura clara basada en iteraciones, lo cual limita la planificación del proyecto.

---

### 2.5 Decisión metodológica

En base al análisis realizado, se selecciona **Scrum** como metodología de desarrollo, ya que se adapta mejor a la naturaleza del problema y permite una gestión eficiente de la complejidad.

---

## 3. Enfoque Tecnológico

Se ha definido una arquitectura basada en **SPA (Single Page Application) + API REST**, la cual permite una clara separación entre la capa de presentación y la lógica de negocio del sistema.

Este enfoque facilita el desarrollo modular, la escalabilidad y la mantenibilidad del sistema.

---

### 3.1 Frontend: Angular

Se selecciona **Angular** como framework para el desarrollo del frontend.

#### Justificación técnica:

- Arquitectura estructurada basada en componentes
- Uso de **TypeScript**, que mejora la calidad del código
- Desarrollo de aplicaciones SPA
- Separación clara entre componentes, servicios y módulos

---

### 3.2 Backend: FastAPI

Se selecciona **FastAPI** como framework para el backend.

#### Justificación técnica:

- Alto rendimiento
- Uso de **Python**, ideal para algoritmos de optimización
- Validación de datos con tipado fuerte (Pydantic)
- Documentación automática (Swagger)

---

### 3.3 Comparación de alternativas tecnológicas

| Alternativa | Ventajas | Desventajas |
|------------|--------|------------|
| MERN Stack | Amplio uso, ecosistema JS | Limitado para algoritmos complejos |
| Django | Robusto y completo | Más pesado y menos flexible para APIs |
| Angular + FastAPI | Alto rendimiento, estructurado | Mayor curva de aprendizaje |

---

### 3.4 Criterios de selección

Para la elección del stack tecnológico se consideraron los siguientes factores:

- Complejidad del problema
- Necesidad de optimización
- Escalabilidad
- Mantenibilidad
- Rendimiento
- Separación de responsabilidades

---

### 3.5 Decisión tecnológica

Se selecciona la combinación **Angular + FastAPI**, debido a su capacidad para soportar el desarrollo de un sistema estructurado, escalable y orientado a la resolución de problemas complejos.

---

## 4. Coherencia con el Problema

El problema de generación de horarios académicos implica:

- Múltiples variables (cursos, docentes, aulas, estudiantes)
- Restricciones (disponibilidad, prerrequisitos, créditos)
- Interdependencias
- Necesidad de optimización

El enfoque seleccionado responde de la siguiente manera:

- **Scrum** permite gestionar la complejidad mediante iteraciones
- **Angular** facilita la construcción de una interfaz estructurada
- **FastAPI** permite implementar la lógica de negocio y algoritmos complejos

---

## 5. Conclusión

El enfoque metodológico y tecnológico seleccionado permite abordar de manera efectiva un problema complejo de ingeniería de software.

La combinación de Scrum, Angular y FastAPI proporciona una base sólida para el desarrollo incremental del sistema, garantizando escalabilidad, mantenibilidad y eficiencia en la generación de horarios académicos.
