# Gestión de Riesgos y Oportunidades

## 1. Registros Obligatorios

### 1.1 Registro de Riesgos

| ID | Descripción del Riesgo | Probabilidad | Impacto | Estrategia de Mitigación |
| :--- | :--- | :--- | :--- | :--- |
| R-01 | **Falta de Solución Posible:** El sistema no logra encontrar un horario válido porque faltan aulas o porque hay demasiados cursos registrados. | Media | Alto debido a que bloquea la generación del horario | Mostrar un mensaje claro al usuario indicando que no hay solución. Sugerir agregar más aulas o reducir la cantidad de cursos. Filtrar las aulas por tamaño ayuda a detectar este problema a tiempo. |
| R-02 | **Demora en la Generación del Horario:** El proceso matemático para crear el horario toma demasiado tiempo y hace que el sistema se quede congelado. | Baja | Medio | Poner un límite de diez segundos al tiempo máximo de cálculo. Si el tiempo pasa, el proceso se detiene para evitar que el servidor colapse. |
| R-03 | **Datos Incompletos o Incorrectos:** La información de los docentes, cursos o aulas tiene errores, espacios vacíos o referencias cruzadas que fallan en la base de datos. | Media | Alto | Revisar estrictamente toda la información antes de guardarla. Usar reglas en la base de datos para asegurar que no falten datos importantes. |
| R-04 | **Fallo en Servicios Externos:** La base de datos pierde conexión o la herramienta matemática principal deja de funcionar repentinamente. | Baja | Alto | Usar bloques de código especiales para capturar estos errores. Mostrar un mensaje amigable al usuario en lugar de mostrar una pantalla de error del sistema. |

### 1.2 Registro de Oportunidades

| ID | Impacto Positivo Esperado | Estrategia de Aprovechamiento |
| :--- | :--- | :--- |
| O-01 | **Horarios Más Cómodos:** Mejorar la experiencia de los estudiantes y docentes al evitar horas muertas prolongadas o clases muy tarde en la noche. | Una vez que el sistema funcione de forma estable, agregar nuevas reglas matemáticas para agrupar las clases y evitar tiempos vacíos durante el día. |
| O-02 | **Uso en Otras Universidades:** Convertir el proyecto en un producto que se pueda vender a otras instituciones educativas. | Hacer que las reglas del sistema sean fáciles de activar o desactivar, para que cada nueva universidad pueda configurar el algoritmo según sus propias necesidades. |
| O-03 | **Permitir Horarios Fijos:** Dar la opción a los administradores de asignar algunos cursos a mano de forma obligatoria, y hacer que el resto del horario se arme respetando esa decisión. | Agregar la posibilidad de guardar horarios fijos en el algoritmo antes de calcular el resto de las clases disponibles. |

---

## 2. Análisis Esperado

### 2.1 Relación de Riesgos con Restricciones del Problema
El riesgo de Falta de Solución Posible ocurre cuando somos muy exigentes con las reglas matemáticas. El algoritmo obliga a que cada clase tenga un salón, un docente único y un bloque de horas fijo. Si no tenemos suficientes salones grandes o si faltan docentes disponibles, la matemática falla. Mientras más reglas estrictas tengamos y menos recursos haya, será más probable que este riesgo ocurra.

### 2.2 Relación de Riesgos con Limitaciones Técnicas
El riesgo de Demora en la Generación del Horario existe porque organizar clases es un problema matemático muy pesado para cualquier computadora. Si agregamos muchas carreras o facultades, el sistema se volverá más lento sin importar cuán rápido sea el equipo. Por eso, limitar el tiempo a diez segundos es la mejor solución técnica para evitar que la página web se quede cargando sin respuesta.

### 2.3 Relación de Riesgos con Dependencias Externas
El riesgo de Fallo en Servicios Externos demuestra que nuestro sistema depende mucho de otras herramientas. El código puede ser perfecto, pero si la base de datos se apaga o si el servidor tiene un error interno, no se podrá generar el horario. La mejor forma de evitar problemas graves es preparar la aplicación web para que muestre advertencias claras y amigables cuando falle algún servicio por detrás.
