# Registro de Incidentes o Problemas (Issue Log)
## HorarioSmart — Fase de Control y Cierre

> Este registro documenta problemas reales surgidos durante la ejecución del proyecto (distintos de los riesgos anticipados), su responsable, prioridad, estado y acciones correctivas aplicadas, conforme al enfoque PMBOK.

---

## 1. Registro de Incidentes

| ID | Descripción del Incidente | Componente Afectado | Responsable | Prioridad | Fecha de Detección | Estado | Acción Correctiva |
|---|---|---|---|---|---|---|---|
| ISS-01 | El endpoint de autenticación (`auth_api`) no estaba siendo servido por la aplicación, generando fallos en pruebas de integración. | Backend — `apis/__init__.py` | Escobar Bendezú, Aldrin | **Alta** | Fase de integración | **Resuelto** | Se agregó el registro explícito del router `auth_api` en `apis/__init__.py`. Validado con pruebas de integración. |
| ISS-02 | Análisis inicial de SonarQube reveló 129 issues abiertos (mantenibilidad), con 1 día 2 horas de esfuerzo estimado de corrección, y calificación de fiabilidad **D**. | Backend y Frontend (transversal) | Equipo completo | **Alta** | Análisis de calidad pre-cierre | **Resuelto** | Corrección iterativa por archivo: documentación de `HTTPException`, refactorización de ternarios anidados, eliminación de imports no usados, etc. Resultado: 0 issues. |
| ISS-03 | Cobertura de pruebas (*branches*) del frontend por debajo del umbral requerido (70%). | Frontend — `dashboard.ts`, `academic.service.ts` | López Rodríguez, Axel | **Media** | Fase de testing | **Resuelto** | Se agregaron pruebas adicionales para `getClases`, `getHoras` y rutas de éxito/error no cubiertas. |
| ISS-04 | Mocks de pruebas de horarios retornaban valores planos en lugar de *signals* de Angular, provocando fallos en pruebas de componente. | Frontend — pruebas de `dashboard.component.spec.ts` | López Rodríguez, Axel | **Media** | Fase de testing | **Resuelto** | Mocks corregidos para retornar `vi.fn()` compatibles con signals. |
| ISS-05 | Falla de contraste de color (criterios WCAG 1.4.3 / 1.4.11) detectada en `dashboard.css` y `login.css` (uso de gradientes/`rgba` translúcidos). | Frontend — hojas de estilo | López Rodríguez, Axel | **Media** | Auditoría de accesibilidad | **Resuelto** | Reemplazo de colores translúcidos por colores sólidos opacos verificados contra el estándar de contraste WCAG. |
| ISS-06 | Configuración insegura del servidor backend: *binding* a `host="0.0.0.0"` detectado como *Security Hotspot* por SonarQube. | Backend — `app.py` | Escobar Bendezú, Aldrin | **Media** | Análisis de seguridad | **Resuelto** | Cambio de `host="0.0.0.0"` a `host="127.0.0.1"` para entorno de desarrollo/pruebas. |

---

## 2. Resumen de Incidentes por Estado

| Estado | Cantidad |
|---|---|
| Resuelto | 6 |
| En seguimiento | 0 |
| Abierto | 0 |
| **Total** | **6** |

## 3. Resumen de Incidentes por Prioridad

| Prioridad | Cantidad | % Resueltos |
|---|---|---|
| Alta | 2 | 100% |
| Media | 4 | 100% |
| Baja | 0 | — |

---

## 4. Análisis de Causa Raíz (Resumen)

La mayoría de los incidentes registrados (ISS-02, ISS-03, ISS-05, ISS-06) se originaron por la **ausencia de un análisis de calidad continuo** durante los primeros sprints, concentrando la detección de problemas en una etapa avanzada del proyecto. El incidente ISS-01 evidenció la necesidad de una checklist de verificación de registro de endpoints al incorporar nuevos módulos de API. Esta causa raíz común se documenta con mayor detalle en el [Informe Final de Lecciones Aprendidas](./02-informe-final-lecciones-aprendidas.md), sección 4.

---
*Documento elaborado conforme al enfoque PMBOK como parte de la fase de control y cierre del proyecto. Última actualización: 21 de junio de 2026.*
