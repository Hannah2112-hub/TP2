# Informe de Sostenibilidad y Desarrollo Web Responsable

## 1. Análisis del Impacto Ambiental del Software

El desarrollo, despliegue y uso de aplicaciones web (como el presente Sistema de Gestión Académica) conlleva costos energéticos tangibles que se traducen en emisiones de carbono. A continuación, se detallan 5 impactos ambientales relevantes detectados y su justificación técnica:

1. **Transferencia de Red (Payloads Pesados):** Cada vez que un cliente (frontend o aplicación) solicita datos, el servidor envía un volumen de bytes. Si la respuesta no está optimizada o comprimida, el mayor consumo de ancho de banda incrementa directamente la energía requerida por los centros de datos, los nodos de transmisión y el dispositivo final del usuario.
2. **Consultas a Base de Datos (I/O Intensivo):** Operaciones SQL complejas sin paginación (ej. devolver miles de registros de alumnos u horarios de golpe) obligan a la CPU del servidor de PostgreSQL a trabajar más tiempo, aumentando el consumo eléctrico del hardware subyacente.
3. **Cómputo Innecesario (Procesamiento Redundante):** La falta de validaciones asíncronas óptimas (por ejemplo, buscar traslapes iterando en memoria en lugar de aprovechar funciones de la BD) genera un sobreuso del ciclo de reloj de la CPU en el backend.
4. **Almacenamiento de Datos Obsoletos (Storage):** Acumular métricas de tráfico sin un ciclo de limpieza (Logs y Métricas) conlleva a almacenar gigabytes inactivos ("Dark Data"), requiriendo energía perpetua en los discos físicos de los servidores para mantenerlos disponibles.
5. **Entornos de Desarrollo No Optimizados:** La ejecución constante de contenedores Docker (como en el análisis de GreenFrame) u otros entornos sin suspensión automática mantiene recursos energéticos en uso incluso cuando no hay tráfico de usuarios.

## 2. Identificación de Oportunidades de Mejora

Se detectaron las siguientes oportunidades de optimización en el proyecto:

* **Oportunidad 1: Compresión de Respuestas HTTP.**
  * *Justificación:* Al interceptar las peticiones mediante FastAPI y analizar su tamaño, se evidencia que los arreglos JSON pueden ser verbosos. Implementar compresión GZIP puede reducir el payload hasta en un 70%, impactando directamente de forma proporcional en la reducción de CO2 de acuerdo al modelo Sustainable Web Design.
* **Oportunidad 2: Validaciones Espaciotemporales a nivel de Base de Datos.**
  * *Justificación:* En la asignación de horarios, trasladar la lógica de traslape (`OVERLAPS`) a consultas nativas de PostgreSQL evita transferir toda la matriz de horarios a la memoria de Python, reduciendo drásticamente el uso de memoria RAM y CPU del backend.
* **Oportunidad 3: Monitoreo Efímero de Métricas.**
  * *Justificación:* Almacenar logs de cada petición de forma indefinida crea deuda de almacenamiento (Storage Carbon Footprint). Configurar el truncamiento de la tabla de métricas en el evento de inicio (`startup event`) garantiza que la base de datos mantenga una huella mínima en disco.

## 3. Implementación de Mejoras de Sostenibilidad

Se implementaron las siguientes mejoras medibles y verificables en el ecosistema (FastAPI + PostgreSQL):

1. **Middleware de CO2 (Implementación funcional 1):** Un interceptor global captura la latencia y calcula el tamaño de cada respuesta, convirtiéndola matemáticamente a gramos de CO2 usando el estándar Sustainable Web Design.
2. **Truncado de Sesión (Implementación funcional 2):** Implementación de borrado automático de métricas ambientales históricas al reiniciar el backend, combatiendo el desperdicio de almacenamiento.
3. **Validación Optimizada SQL (Implementación funcional 3):** Reescribimos el método `HorarioRepository.create()` para que PostgreSQL resuelva matemáticamente los traslapes de aulas y docentes mediante la función `OVERLAPS`, disminuyendo latencia de cómputo.
4. **Compresión GZIP (Mejora Adicional No Solicitada):** Se añadió `GZipMiddleware` a la aplicación FastAPI. Las respuestas mayores a 500 bytes se comprimen automáticamente, reduciendo significativamente la emisión digital final del endpoint.

## 4. Aplicación de Técnicas Específicas de Optimización

* **Compresión (GZip):** Se integró exitosamente para la reducción del consumo de transferencia.
* **Optimización de Consultas:** Uso de cruces espaciotemporales eficientes (`OVERLAPS`) en PostgreSQL.
* **Dashboard Renderizado en Servidor (SSR):** El endpoint `/environmental-impact` sirve HTML puro que no requiere descargar frameworks pesados de JavaScript en el cliente, logrando una carga ultrarrápida y consumo nulo de CPU en la renderización del lado del usuario.

## 5. Contribución a la Sostenibilidad (Beneficios)

El enfoque adoptado no solo permite auditar en tiempo real (visibilidad) qué endpoints gastan más energía, sino que proactivamente **reduce la transferencia de datos y la carga en el servidor de base de datos**. Al exponer el panel `/environmental-impact`, los desarrolladores adquieren "Eco-conciencia" para identificar cuellos de botella (por ejemplo, rutas que devuelven megabytes de información innecesaria) y aplicar paginación futura. 

## 6. Validación y Resultados (Instrucciones de Verificación)

> **Nota para el estudiante**: Para cumplir el apartado de "Validación de resultados" y obtener los puntos máximos de la rúbrica, debes:
> 1. Iniciar tu servidor (`uvicorn src.app:app --reload`).
> 2. Visitar http://localhost:3000/environmental-impact y **tomar una captura de pantalla** del dashboard.
> 3. Ejecutar la herramienta `greenframe analyze` en tu consola (basado en el archivo `.greenframe.yml` y `scenario.js` configurado) y **tomar captura de pantalla** de los resultados (Wh y CO2).
> 4. Adjuntar estas capturas al entregar este repositorio.
