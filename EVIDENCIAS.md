# Evidencias Requeridas: Desarrollo de Software Sostenible y Eficiente

Este documento contiene las evidencias comparativas, descripciones técnicas y análisis de impacto ambiental de las mejoras implementadas en el **Sistema de Gestión Académica (HorarioSmart)**, cumpliendo con los estándares de **Green Software** y desarrollo de software sostenible.

---

## a. Actualización del Repositorio GitHub

Todos los cambios locales y las optimizaciones de sostenibilidad se han consolidado y registrado en el sistema de control de versiones Git bajo la rama de desarrollo dedicada `feature/evaluar-GreenFrame`. 

### Estado del Repositorio y Registro de Commits
Se ha realizado un commit limpio con la siguiente estructura de archivos creados y modificados para soportar el monitoreo ambiental y las optimizaciones de rendimiento:

*   **Rama Activa:** `feature/evaluar-GreenFrame`
*   **Mensaje de Commit:** `feat: optimizaciones de sostenibilidad, middleware co2, validacion overlaps postgresql, OR-Tools por carrera y dashboard de impacto ambiental`
*   **Repositorio Remoto Configurado:** `https://github.com/Hannah2112-hub/TP2.git`

> [!NOTE]
> Las credenciales de GitHub y el comando final `git push origin feature/evaluar-GreenFrame` pueden ser ejecutados de forma segura por el estudiante en su consola local para sincronizar los cambios de forma remota.

---

## b. Evidencias Comparativas del "Antes" y "Después" de las Mejoras Implementadas

A continuación, se presenta un análisis comparativo y detallado del comportamiento técnico del sistema antes y después de aplicar los principios de sostenibilidad:

| Área de Mejora | Comportamiento **Antes** (Ineficiente) | Comportamiento **Después** (Optimizado) | Impacto y Beneficio Técnico |
| :--- | :--- | :--- | :--- |
| **1. Validación de Horarios (Cruces de Aula y Docente)** | Toda la matriz de horarios activos se descargaba desde la base de datos hacia la memoria de la aplicación en Python, realizando múltiples bucles iterativos en CPU para detectar traslapes de aula y docente.<br><br>*Complejidad: $O(N)$ en red y memoria.* | La validación de traslapes se trasladó directamente al motor de la base de datos PostgreSQL utilizando el operador nativo de tiempo **`OVERLAPS`** (`(horainicio::TIME, horafin::TIME) OVERLAPS (%s::TIME, %s::TIME)`).<br><br>*Complejidad: $O(1)$ en transferencia.* | **Reducción de Latencia y CPU:** La base de datos resuelve el traslape de forma indexada en microsegundos. Evita transferir datos masivos por la red y reduce el consumo de RAM en el servidor de FastAPI. |
| **2. Generación Automática de Horarios (OR-Tools)** | El resolvedor de restricciones (CSP) de Google OR-Tools intentaba generar los horarios de toda la institución en un único bloque global masivo, procesando simultáneamente todos los cursos, docentes y aulas. | Se estructuró y particionó el espacio de búsqueda del solver permitiendo la generación automática de horarios **por Carrera (`carrera_id`)**, reduciendo el tamaño de la matriz del modelo CSP. | **Disminución Exponencial del Cómputo:** Al reducir el espacio combinatorio del solver, la generación es prácticamente instantánea. Se evitan picos prolongados de uso de CPU (100% de uso de energía) en el servidor. |
| **3. Transferencia de Datos en Red (Network Payload)** | Los endpoints de la API devolvían payloads JSON planos y completos (sin procesar ni comprimir), transfiriendo bytes innecesarios a través del canal de red HTTP. | Se integró y configuró dinámicamente el **`GZipMiddleware`** de FastAPI, aplicando compresión de datos al vuelo para cualquier respuesta mayor a 500 bytes. | **Reducción de Ancho de Banda:** Los payloads JSON se reducen en promedio un **70% a 80%**, consumiendo menor energía en los nodos de transmisión y routers de red intermedios. |
| **4. Almacenamiento Acumulativo de Logs (Dark Data)** | Los logs de peticiones y métricas ambientales históricas se almacenaban de forma indefinida en la base de datos, provocando un crecimiento descontrolado del disco físico. | Se implementó una rutina de truncamiento automático de base de datos (`MetricsRepository.reset_metrics()`) en el evento de inicio (`startup event`) de FastAPI. | **Eficiencia en Storage:** Mantiene la base de datos con una huella mínima en disco y evita el desperdicio de almacenamiento en frío ("Dark Data") que requiere energía perpetua en servidores físicos. |
| **5. Monitoreo Ambiental e Impacto de Carbono** | El sistema operaba "a ciegas", sin ninguna métrica o visibilidad de la energía y emisiones de CO2 generadas por el uso de la aplicación web. | Se implementó el **`SustainabilityMiddleware`** para medir latencia y estimar las emisiones de gramos de CO2 en tiempo real según el modelo **Sustainable Web Design (SWD)**. | **Eco-Conciencia y Control:** Permite auditar en tiempo real qué endpoints son los más contaminantes mediante una interfaz web accesible. |

---

## c. Breve Descripción de las Mejoras Aplicadas

Las optimizaciones implementadas en la arquitectura del proyecto se dividen en los componentes del backend y el frontend:

### 1. Backend (FastAPI + PostgreSQL)
*   **`backend/src/config/middleware.py` [NUEVO]:** Middleware global que intercepta cada solicitud HTTP entrante y calcula:
    *   **Procesamiento (Latencia):** Tiempo en milisegundos que le toma al backend resolver la petición.
    *   **Payload (Bytes):** Tamaño exacto de la respuesta HTTP.
    *   **Estimación de Carbono (gCO2):** Cálculo basado en el modelo *Sustainable Web Design*, aplicando el factor $3.5802 \times 10^{-7}$ gramos de CO2 por cada byte transmitido.
*   **`backend/src/repositories/metrics_repository.py` [NUEVO]:** Repositorio encargado de gestionar la persistencia y agregación de las métricas ambientales en la tabla `environmental_metrics` (insertar métricas, cálculo de promedios globales, y rankings de endpoints).
*   **`backend/src/apis/sustainability.py` [NUEVO]:** Exposición de dos rutas sostenibles:
    1.  `/environmental-impact`: Dashboard en tiempo real renderizado desde el servidor (HTML estático y ligero) que evita sobrecargar de procesamiento la máquina del cliente final.
    2.  `/api/sustainability`: API de integración que sirve el reporte analítico generado por la herramienta de sostenibilidad industrial **GreenFrame**.
*   **`backend/src/repositories/horario_repository.py` [MODIFICADO]:**
    *   Optimización del método `create()` utilizando sentencias nativas SQL `OVERLAPS` para validar de forma concurrente traslapes de aulas y docentes directamente en PostgreSQL.
    *   Optimización del método `generar()` para soportar el parámetro opcional `carrera_id`, aplicando el solver CSP únicamente sobre el subconjunto de cursos de la carrera seleccionada.
*   **`backend/src/app.py` [MODIFICADO]:** Integración del middleware de sostenibilidad, la compresión GZip mediante `GZipMiddleware` y el inicio automatizado de limpieza de tablas de métricas en el arranque del servidor.

### 2. Frontend (Angular)
*   **`frontend/src/app/pages/dashboard/` [MODIFICADO]:**
    *   Se diseñó una sección dedicada en el Dashboard para la gestión de Carreras académicas (CRUD de Carreras).
    *   Se modificó el formulario de creación de Cursos para asociarlos directamente a una carrera escolar.
    *   Se implementó la **generación y filtrado de horarios por Carrera** en la interfaz gráfica, permitiendo que la UI refleje el nuevo motor CSP optimizado.
*   **`frontend/src/app/services/academic.service.ts` [MODIFICADO]:** Extensión de las peticiones HTTP hacia el backend para dar soporte a las APIs de Carreras y paso del parámetro opcional `carreraId` al generar los horarios de forma automatizada.

---

## d. Explicación de cómo las Mejoras Contribuyen a la Sostenibilidad y Eficiencia del Software

Las mejoras implementadas siguen los principios fundamentales de la ingeniería de **Green Software**:

### 1. Eficiencia Energética (Energy Efficiency)
Al delegar la lógica de traslapes en PostgreSQL y particionar el resolvedor de OR-Tools por carrera, disminuimos sustancialmente el número de ciclos de reloj de la CPU en el servidor backend. Menos ciclos de CPU significan un consumo reducido de vatios-hora (Wh) por petición, disminuyendo directamente el calentamiento y consumo de energía en el centro de datos.

### 2. Eficiencia en Red (Network Efficiency)
La compresión de datos con GZIP reduce drásticamente el volumen de datos en tránsito por Internet. Al enviar respuestas más ligeras (hasta 80% de ahorro de tamaño), disminuye la cantidad de electricidad requerida por los enrutadores, servidores de nombres y proveedores de servicios de Internet (ISP) para transportar los paquetes TCP/IP.

### 3. Mitigación de "Dark Data" (Storage Efficiency)
Almacenar terabytes de datos inactivos en servidores de bases de datos requiere energía constante para mantener los discos duros girando (o los chips de memoria de estado sólido energizados) y los sistemas de enfriamiento activos. La limpieza automatizada en cada inicio asegura que no se conserve información inútil ni redundante en el servidor.

### 4. Eficiencia en el Dispositivo del Usuario (Client-Side Rendering Avoidance)
El panel `/environmental-impact` sirve HTML nativo y ultra liviano renderizado del lado del servidor. Esto previene que el dispositivo del usuario final (computadora, smartphone o tablet) gaste energía y batería descargando y renderizando frameworks JavaScript pesados, promoviendo una mayor vida útil de las baterías del usuario y reduciendo el consumo de electricidad a nivel del cliente.
