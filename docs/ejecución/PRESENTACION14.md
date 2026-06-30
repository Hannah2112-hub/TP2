# Matrícula - Universidad Continental

## Revisión de Calidad - Aplicación Web Full Stack

**Proyecto de Fin de Asignatura**
Taller de Proyectos 2 – Ingeniería de Sistemas e Informática

**Equipo de desarrollo**
Junio 2026

---

# Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Frontend | Angular 19 + TypeScript |
| Backend | FastAPI + Python 3.14 |
| Base de datos | SQLite |
| Testing Frontend | Vitest |
| Testing Backend | Pytest + Coverage |
| Análisis de calidad | SonarQube 26.6.0 |
| Seguridad | OWASP Top 10 2025 |
| Accesibilidad | WCAG 2.1 |
| Usabilidad | SUS (System Usability Scale) |

---

# SonarQube - Dashboard General

| Métrica | Valor | Estado |
|---|---|---|
| Quality Gate | **OK** | ✅ |
| Bugs | **0** | ✅ |
| Vulnerabilities | **0** | ✅ |
| Code Smells | **0** | ✅ |
| Coverage | **97.1%** | ✅ |
| Duplications | **0.5%** | ✅ |
| Security Hotspots | **0** | ✅ |
| Hotspots Reviewed | **100%** | ✅ |
| Deuda Técnica | **0 horas** | ✅ |
| Security Rating | **A** | ✅ |
| Reliability Rating | **A** | ✅ |
| Maintainability Rating | **A** | ✅ |

---

# Métricas por Componente

| Métrica | Backend (Python) | Frontend (TypeScript) |
|---|---|---|
| Líneas de código | 1,572 | 2,375 |
| Coverage | **96.8%** | **97.6%** |
| Líneas sin cubrir | 32 | 0 |
| Duplicaciones | 0.0% | 0.8% |
| Bugs | 0 | 0 |
| Vulnerabilities | 0 | 0 |
| Code Smells | 0 | 0 |

---

# OWASP Top 10 2025 - Evaluación

| # | Categoría | Estado | Mitigación |
|---|---|---|---|
| A01 | Broken Access Control | ✅ Mitigado | Auth guard Angular + JWT + validación roles backend |
| A02 | Cryptographic Failures | ✅ Mitigado | Contraseñas con hash, tokens JWT con expiración |
| A03 | Injection | ✅ Mitigado | Parámetros tipados con Annotated, validación FastAPI |
| A04 | Insecure Design | ✅ Mitigado | Arquitectura en capas, separación de responsabilidades |
| A05 | Security Misconfiguration | ✅ Mitigado | host=127.0.0.1, CORS configurado, HTTPS |
| A06 | Vulnerable Components | ✅ Mitigado | Dependencias actualizadas, sin CVEs conocidos |
| A07 | Identification and Auth Failures | ✅ Mitigado | JWT con expiración, login con roles, sin sesiones abiertas |
| A08 | Software and Data Integrity Failures | ✅ Mitigado | Validación de entrada en todos los endpoints |
| A09 | Security Logging and Monitoring Failures | ✅ Mitigado | console.error en catch blocks, logs estructurados |
| A10 | Server-Side Request Forgery (SSRF) | ⚠️ No aplica | Sin requests externos a URLs del usuario |

**Resultado: 9/10 categorías mitigadas, 1 no aplica**

---

# OWASP - Detalle de Mitigaciones

## Autenticación y Autorización
- JWT con tiempo de expiración
- Auth guard en Angular que redirige a login
- Roles: admin, docente, estudiante
- Backend valida token en cada endpoint

## Validación de Entradas
- FastAPI valida parámetros con Pydantic
- `Annotated[type, Query()]` para parámetros de consulta
- `HTTPException` con códigos de estado correctos

## Seguridad de Configuración
- Servidor escucha en `127.0.0.1` (no `0.0.0.0`)
- Sin exponer puertos innecesarios
- Variables de entorno para secretos

---

# WCAG - Accesibilidad

## Criterios Evaluados y Corregidos

| Criterio WCAG | Problema Detectado | Corrección Implementada |
|---|---|---|
| 1.4.3 Contrast (Minimum) | Colores con gradientes/rgba sin contraste verificable | Colores sólidos opacos: #4f46e5, #1e2a4a, #0f2a1e, #2d1518, #1a2240, #ffffff |
| 1.4.11 Non-text Contrast | Fondos transparentes | Fondos sólidos con contraste ≥ 4.5:1 |
| 2.1.1 Keyboard | tabindex en divs sin handlers | Eliminados tabindex, agregados (keydown.enter) |
| 2.4.6 Headings and Labels | Inputs sin label asociado | 26 etiquetas `<label>` con pares `for`/`id` |
| 4.1.2 Name, Role, Value | Inputs accesibles | Labels correctamente asociados a inputs |

---

# WCAG - Evidencias de Corrección

## Antes (CSS)
```css
/* ❌ Sin contraste verificable */
background: linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.6));
color: rgba(255, 255, 255, 0.9);
```

## Después (CSS)
```css
/* ✅ Colores sólidos opacos */
background: #4f46e5;
color: #ffffff;
```

## Antes (HTML)
```html
<!-- ❌ Sin label -->
<input type="email" placeholder="Correo">
```

## Después (HTML)
```html
<!-- ✅ Con label asociado -->
<label for="login-email">Correo electrónico</label>
<input id="login-email" type="email">
```

---

# SUS - System Usability Scale

## Instrumento Aplicado

Se aplicó el cuestionario SUS a **5 participantes** que utilizaron el sistema de matrícula.

### Preguntas del Instrumento

| # | Pregunta | Tipo |
|---|---|---|
| 1 | Creo que usaré este sistema frecuentemente | Positiva |
| 2 | Encontré el sistema innecesariamente complejo | Negativa |
| 3 | Creo que el sistema fue fácil de usar | Positiva |
| 4 | Creo que necesitaré asistencia técnica para usarlo | Negativa |
| 5 | Encontré que las diversas funciones estaban bien integradas | Positiva |
| 6 | Creo que hay demasiada inconsistencia en este sistema | Negativa |
| 7 | La mayoría de personas aprenderá a usar este sistema rápidamente | Positiva |
| 8 | Encontré el sistema muy incómodo de usar | Negativa |
| 9 | Me sentí muy confiado usando el sistema | Positiva |
| 10 | Necesité aprender muchas cosas antes de poder usar el sistema | Negativa |

---

# SUS - Respuestas Recopiladas

| # | Pregunta | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|---|
| 1 | Frecuencia de uso | 5 | 4 | 5 | 4 | 5 |
| 2 | Complejidad innecesaria | 2 | 1 | 2 | 3 | 1 |
| 3 | Fácil de usar | 5 | 4 | 5 | 4 | 5 |
| 4 | Necesidad de asistencia | 1 | 2 | 1 | 2 | 1 |
| 5 | Funciones integradas | 4 | 5 | 4 | 4 | 5 |
| 6 | Inconsistencia | 2 | 1 | 2 | 2 | 1 |
| 7 | Aprendizaje rápido | 5 | 4 | 5 | 4 | 5 |
| 8 | Incómodo de usar | 1 | 2 | 1 | 2 | 1 |
| 9 | Confianza en uso | 5 | 4 | 5 | 4 | 5 |
| 10 | Aprendizaje previo | 1 | 2 | 1 | 3 | 1 |

---

# SUS - Cálculo del Puntaje

## Fórmula
- Preguntas positivas (1, 3, 5, 7, 9): Puntuación = Respuesta - 1
- Preguntas negativas (2, 4, 6, 8, 10): Puntuación = 5 - Respuesta
- **SUS Score = Suma × 2.5**

## Resultados por Participante

| Participante | Suma Puntuaciones | SUS Score | Clasificación |
|---|---|---|---|
| Persona 1 | 37 | **92.5** | Excelente (A) |
| Persona 2 | 33 | **82.5** | Excelente (A) |
| Persona 3 | 37 | **92.5** | Excelente (A) |
| Persona 4 | 28 | **70.0** | Bueno (B) |
| Persona 5 | 40 | **100.0** | Excelente (A) |

---

# SUS - Resultado Final

## Puntaje Promedio

```
(92.5 + 82.5 + 92.5 + 70.0 + 100.0) / 5 = 87.5
```

## **SUS Score: 87.5 / 100**

## Tabla de Interpretación

| Rango | Clasificación | Nuestro Resultado |
|---|---|---|
| > 80.3 | Excelente (A) | ⭐ **87.5** |
| 68 - 80.3 | Bueno (B) | |
| 51 - 68 | Regular (C) | |
| 25.1 - 51 | Pobre (D) | |
| < 25.1 | Terrible (F) | |

## Conclusión SUS
El sistema obtuvo una calificación **Excelente**, indicando que los usuarios lo consideran fácil de usar, con funciones bien integradas y que puede ser aprendido rápidamente.

---

# Testing Automatizado

## Resumen de Pruebas

| Tipo | Backend | Frontend | Total |
|---|---|---|---|
| Unitarias | 186 | 206 | 392 |
| Integración | 36 | 10 | 46 |
| E2E (Cypress) | 2 | — | 2 |
| **Total** | **224** | **206** | **430** |

---

# Cobertura de Código

## Frontend (Vitest)

```
All files          | 100% Stmts | 93.23% Branch | 100% Funcs | 100% Lines
 pages/dashboard   |     100%   |      100%     |    100%    |    100%
 pages/login       |     100%   |      100%     |    100%    |    100%
 services          |     100%   |     89.14%    |    100%    |    100%
```

## Backend (Pytest)

```
TOTAL | 988 stmts | 32 missed | 96.76% Coverage
```

## Cobertura Global SonarQube: 97.1%

---

# Correcciones Implementadas

## Backend (Python)

| Archivo | Corrección | Regla SonarQube |
|---|---|---|
| `apis/*.py` (8 archivos) | HTTPException responses + Annotated types | python:S5754 |
| `sustainability.py` | Ternarios anidados → if/elif/else + aiofiles | python:S1301 |
| `app.py` | host="0.0.0.0" → host="127.0.0.1" | python:S5547 |
| `horario_repository.py` | Refactorización completa (complejidad ≤15) | python:S3776 |
| `test_repositories_bulk.py` | assertTrue(isinstance()) → assertIsInstance() | python:S5906 |
| `matricula_api.py` | Query(None) → Query() = None | python:S5765 |
| `horario_api.py` | Query(default=...) → Query(...) = default | python:S5765 |

## Frontend (TypeScript/Angular)

| Archivo | Corrección | Regla SonarQube |
|---|---|---|
| `dashboard.css` / `login.css` | Colores sólidos opacos para contraste WCAG | css:S6845 |
| `dashboard.html` | Eliminados tabindex, keyboard handlers | web:S6845 |
| `dashboard.html` / `login.html` | 26 labels con for/id | web:S6845 |
| `dashboard.ts` | Imports no usados, readonly params | typescript:S3827 |
| `login.ts` | Params readonly | typescript:S3827 |
| `auth.service.ts` | Signals readonly, optional chaining | typescript:S3827 |
| `academic.service.ts` | Signals readonly, Number.parseInt | typescript:S3827 |

---

# Antes vs Después

## Métricas de Calidad

| Métrica | Antes | Después |
|---|---|---|
| Issues SonarQube | 99 | **0** |
| Bugs | 0 | **0** |
| Vulnerabilities | 0 | **0** |
| Code Smells | 0 | **0** |
| Coverage Global | 85.2% | **97.1%** |
| Coverage Frontend | 87.6% | **97.6%** |
| Coverage Backend | 96.8% | **96.8%** |
| Duplications | 0.5% | **0.5%** |
| Security Hotspots | 1 TO_REVIEW | **0** (100% reviewed) |
| Quality Gate | ERROR | **OK** |
| Deuda Técnica | 30 min | **0 horas** |

---

# Conclusión General

## Calidad Alcanzada

| Dimensión | Resultado | Evidencia |
|---|---|---|
| **Seguridad** | Excelente | 0 bugs, 0 vulnerabilities, OWASP 9/10 mitigado |
| **Mantenibilidad** | Excelente | 0 code smells, deuda técnica 0h, rating A |
| **Accesibilidad** | Mejorada | WCAG contraste, keyboard, labels |
| **Usabilidad** | Excelente | SUS 87.5/100 (A) |
| **Verificabilidad** | Excelente | 430 pruebas, 97.1% coverage |
| **Calidad Arquitectónica** | Excelente | Arquitectura en capas, sin duplicaciones |

## Entregables

| Entregable | Estado |
|---|---|
| Repositorio GitHub público | ✅ |
| Código fuente completo | ✅ |
| Análisis SonarQube | ✅ |
| Análisis OWASP Top 10 2025 | ✅ |
| Validación WCAG | ✅ |
| Evaluación SUS | ✅ |
| Pruebas automatizadas | ✅ (430) |
| Cobertura de pruebas | ✅ (97.1%) |
| Informe técnico | ✅ |
| Evidencias verificables | ✅ |

---

# Muchas Gracias

## Preguntas

**Dashboard SonarQube:** http://localhost:9000/dashboard?id=matricula-universidad-continental

**Proyecto:** Matrícula - Universidad Continental

**Curso:** Taller de Proyectos 2 – Ingeniería de Sistemas e Informática
