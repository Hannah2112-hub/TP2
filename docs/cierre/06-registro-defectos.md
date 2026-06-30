# Registro de Defectos (Defect Log)
## HorarioSmart — Fase de Control y Cierre

> Este registro documenta los defectos técnicos detectados en el producto de software (a nivel de código, configuración o comportamiento), permitiendo su identificación temprana, clasificación por severidad, corrección y validación, conforme a las buenas prácticas de calidad del proyecto.

---

## 1. Registro de Defectos

| ID | Defecto | Componente | Severidad | Origen de Detección | Estado | Corrección Aplicada | Validación |
|---|---|---|---|---|---|---|---|
| DEF-01 | Endpoint `auth_api` no registrado en el router principal, devolviendo error 404 en rutas de autenticación. | Backend — `apis/__init__.py` | **Alta** | Pruebas de integración | **Corregido** | Registro explícito del router `auth_api`. | Validado con suite de pruebas de integración (`test_apis_bulk.py`). |
| DEF-02 | 90 *code smells* de mantenibilidad y 41 problemas de fiabilidad detectados en el análisis estático inicial. | Backend y Frontend (transversal) | **Alta** | SonarQube (análisis estático) | **Corregido** | Refactorización de `HTTPException` con `Annotated` types (8 archivos API); refactorización de ternarios anidados en `sustainability.py`; reducción de complejidad ciclomática en `horario_repository.py` (≤15); eliminación de imports no usados y *readonly params* en TypeScript. | Re-análisis SonarQube: 0 *code smells*, Maintainability Rating A. |
| DEF-03 | Contraste de color insuficiente (no conforme a WCAG 1.4.3/1.4.11) en `dashboard.css` y `login.css` por uso de colores translúcidos. | Frontend — hojas de estilo | **Media** | Auditoría de accesibilidad | **Corregido** | Sustitución de colores `rgba`/gradientes por colores sólidos opacos verificados. | Validación visual manual contra estándar de contraste WCAG AA. |
| DEF-04 | Elementos interactivos sin navegación por teclado adecuada (`tabindex` mal utilizado, ausencia de manejadores de teclado) en `dashboard.html`. | Frontend — `dashboard.html` | **Media** | Auditoría de accesibilidad | **Corregido** | Eliminación de `tabindex` problemático; incorporación de manejadores `keydown.enter`. | Verificación manual de navegación por teclado. |
| DEF-05 | 26 campos de formulario sin asociación `label`/`for`-`id`, afectando lectores de pantalla (WCAG 2.4.6 / 4.1.2). | Frontend — `dashboard.html`, `login.html` | **Media** | Auditoría de accesibilidad | **Corregido** | Incorporación de 26 etiquetas `<label>` con atributos `for`/`id` correctamente emparejados. | Revisión manual de pares `label`/`input`. |
| DEF-06 | Configuración de servidor insegura: *binding* del backend a `host="0.0.0.0"`, expuesto innecesariamente a todas las interfaces de red. | Backend — `app.py` | **Media** | SonarQube (Security Hotspot) | **Corregido** | Cambio a `host="127.0.0.1"` para entorno de desarrollo/pruebas. | Re-análisis SonarQube: 0 *Security Hotspots* pendientes. |
| DEF-07 | *Security Hotspot* por uso de `random.randint()` en `horario_repository.py`, marcado inicialmente como posible debilidad criptográfica. | Backend — `horario_repository.py` (línea 211) | **Baja** (falso positivo confirmado) | SonarQube (Security Hotspot) | **Corregido / Revisado** | Análisis técnico que confirma que el uso es para sembrar el solver CSP de OR-Tools, no con fines criptográficos. Marcado como *Safe* en SonarQube con justificación documentada. | Hotspot revisado al 100%, sin impacto en Security Rating (A). |
| DEF-08 | Prueba E2E `test_navigation_to_redoc` falla de forma intermitente por cambio en el selector HTML de la documentación Redoc generada por FastAPI. | Backend — pruebas E2E | **Baja** | Ejecución de suite E2E (pytest + SeleniumBase) | **Pendiente** | No corregido al cierre; no afecta funcionalidad del sistema (solo la documentación interactiva de la API). | No aplica — defecto no funcional, sin impacto en el producto entregado. |

---

## 2. Resumen de Defectos por Severidad

| Severidad | Identificados | Corregidos | Pendientes |
|---|---|---|---|
| Alta | 2 | 2 | 0 |
| Media | 4 | 4 | 0 |
| Baja | 2 | 1 | 1 |
| **Total** | **8** | **7** | **1** |

## 3. Resumen de Defectos por Componente

| Componente | Cantidad de defectos | % Corregidos |
|---|---|---|
| Backend | 4 | 75% (3/4 corregidos; 1 pendiente de baja severidad) |
| Frontend | 3 | 100% |
| Transversal (Backend + Frontend) | 1 | 100% |

## 4. Defecto Pendiente al Cierre

El único defecto que permanece abierto al cierre del proyecto es **DEF-08**, de severidad **Baja**, relacionado con la inestabilidad del selector HTML de la documentación Redoc autogenerada por FastAPI en pruebas E2E. Este defecto:

- **No afecta** la funcionalidad central del sistema (generación de horarios, autenticación, gestión de entidades académicas).
- **No representa** un riesgo de seguridad ni de calidad de datos.
- Se documenta como **deuda técnica conocida** para una futura iteración, donde se recomienda reemplazar el selector frágil por un atributo `data-testid` estable.

---
*Documento elaborado conforme al enfoque PMBOK e ISO/IEC 25010 como parte de la fase de control y cierre del proyecto. Última actualización: 21 de junio de 2026.*
