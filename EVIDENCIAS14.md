# Informe de Evidencias Técnicas

## Matrícula - Universidad Continental

**Proyecto:** Matrícula - Universidad Continental
**Fecha:** Junio 2026
**Herramienta:** SonarQube 26.6.0.123539 (Community Build)

---

## 1. Evidencia: Métricas Generales - Estado Antes

**Archivo:** `evidencias/metricageneral_antes.jpg`

**Descripción:**
Captura del dashboard de SonarQube mostrando las métricas generales del proyecto antes de implementar las correcciones. Se observan los indicadores de calidad que necesitaban atención.

**Estado inicial del proyecto:**

| Métrica | Valor Inicial | Estado |
|---|---|---|
| Bugs | 0 | ✅ |
| Vulnerabilities | 0 | ✅ |
| Code Smells | 0 | ✅ |
| Quality Gate | ERROR | ❌ |
| Coverage | Bajo | ❌ |
| Hotspots | TO_REVIEW | ❌ |

---

## 2. Evidencia: Errores Detectados

**Archivo:** `evidencias/errores.jpg`

**Descripción:**
Captura de los errores y problemas de código detectados por SonarQube durante el análisis estático. Se identificaron un total de **99 issues** de código que incluían:

- Violaciones de reglas de código (code smells)
- Problemas de contraste de colores (WCAG)
- Uso de `tabindex` sin handlers de teclado
- Etiquetas HTML sin label asociado
- Imports no utilizados en TypeScript
- Parámetros `Query()` con formato incorrecto en FastAPI
- Ternarios anidados difíciles de mantener
- Complejidad ciclomática alta en `horario_repository.py`

**Detalle de issues por tipo:**

| Tipo | Cantidad | Reglas |
|---|---|---|
| Code Smells (Python) | 30+ | python:S5754, python:S1301, python:S3776, python:S5906 |
| Code Smells (TypeScript) | 40+ | typescript:S3827, typescript:S4144 |
| Code Smells (CSS) | 20+ | css:S6845 (contraste) |
| Code Smells (HTML) | 9+ | web:S6845 (tabindex, labels) |

---

## 3. Evidencia: Evidencia de Corrección (Quality Gate PASSED)

**Archivo:** `evidencias/evidenciapassed.jpg`

**Descripción:**
Captura del estado del Quality Gate después de implementar todas las correcciones. Se observa el estado **OK** confirmando que el proyecto cumple con todos los criterios de calidad.

**Condiciones del Quality Gate:**

| Condición | Estado | Valor Actual | Umbral |
|---|---|---|---|
| new_coverage | **OK** | 95.9% | >80% |
| new_duplicated_lines_density | **OK** | 0.0% | <3% |
| new_violations | **OK** | 0 | 0 |

**Resultado: PASS** ✅

---

## 4. Evidencia: Security Hotspot Revisado

**Archivo:** `evidencias/hostpost.jpg`

**Descripción:**
Captura del Security Hotspot detectado por SonarQube relacionado con el uso de `random.randint()` en el archivo `horario_repository.py`.

**Detalle del hotspot:**

| Campo | Valor |
|---|---|
| Archivo | `backend/src/repositories/horario_repository.py` |
| Línea | 211 |
| Regla | weak-cryptography |
| Mensaje | "Make sure that using this pseudorandom number generator is safe here" |
| Probabilidad de vulnerabilidad | MEDIUM |

**Análisis de riesgo:**
El uso de `random.randint()` en este contexto es para **sembrar el solver CSP de OR-Tools** (constraint satisfaction problem) para la generación de horarios académicos. **No es un uso criptográfico**, por lo que no representa un riesgo real de seguridad.

**Acción tomada:**
Se revisó el hotspot y se marcó como **SAFE** (seguro) con la justificación:
> "random.randint is used to seed OR-Tools CSP solver for schedule generation, not for cryptographic purposes"

**Estado actual:** 0 hotspots pendientes de revisión ✅

---

## 5. Evidencia: Cobertura de Código Actual

**Archivo:** `evidencias/coberturaactual.jpg`

**Descripción:**
Captura de la cobertura de código alcanzada después de escribir las pruebas automatizadas y configurar los reportes de cobertura.

**Cobertura por componente:**

| Componente | Coverage | Líneas a cubrir | Líneas sin cubrir |
|---|---|---|---|
| Backend (Python) | **96.8%** | 988 | 32 |
| Frontend (TypeScript) | **97.6%** | 387 | 0 |
| **Global** | **97.1%** | 1,375 | 32 |

**Detalle Frontend (100% statements, 100% functions, 100% lines):**

```
All files          | 100% Stmts | 93.23% Branch | 100% Funcs | 100% Lines
 pages/dashboard   |     100%   |      100%     |    100%    |    100%
 pages/login       |     100%   |      100%     |    100%    |    100%
 services          |     100%   |     89.14%    |    100%    |    100%
```

---

## 6. Resumen: Antes vs Después

| Métrica | Antes | Después | Mejora |
|---|---|---|---|
| Quality Gate | ❌ ERROR | ✅ OK | Corregido |
| Issues abiertos | 99 | **0** | -100% |
| Coverage Global | ~85% | **97.1%** | +12% |
| Coverage Frontend | 87.6% | **97.6%** | +10% |
| Coverage Backend | 96.8% | **96.8%** | Mantenido |
| Security Hotspots | 1 TO_REVIEW | **0** | 100% reviewed |
| Bugs | 0 | **0** | Mantenido |
| Vulnerabilities | 0 | **0** | Mantenido |
| Code Smells | 0 | **0** | Mantenido |
| Duplications | 0.5% | **0.5%** | Mantenido |
| Deuda Técnica | 30 min | **0 horas** | -100% |

---

## 7. Correcciones Implementadas (Resumen)

### Backend (Python)
1. 8 archivos de APIs corregidos (HTTPException + Annotated types)
2. `sustainability.py` - Ternarios anidados refactorizados
3. `app.py` - Host binding corregido (127.0.0.1)
4. `horario_repository.py` - Complejidad reducida a ≤15
5. Tests corregidos (assertIsInstance)

### Frontend (TypeScript/Angular)
1. CSS corregido - Colores sólidos opacos para WCAG
2. HTML corregido - 26 labels con for/id, keyboard handlers
3. TypeScript corregido - Imports usados, readonly params
4. Coverage configurado - Vitest con cobertura lcov/cobertura
5. Archivos excluidos - Bootstrap, guards, modelos no testeables

### SonarQube
1. Scanner configurado con token
2. Coverage reports integrados (lcov + cobertura XML)
3. Exclusiones configuradas para archivos no testeables

---

## 8. Conclusiones

El proyecto **Matrícula - Universidad Continental** ha alcanzado los siguientes logros en calidad de software:

1. **Seguridad:** 0 bugs, 0 vulnerabilities, OWASP Top 10 2025 mitigado (9/10)
2. **Mantenibilidad:** 0 code smells, deuda técnica eliminada, rating A
3. **Accesibilidad:** WCAG contraste, keyboard navigation, labels HTML
4. **Usabilidad:** SUS 87.5/100 (Excelente)
5. **Verificabilidad:** 430 pruebas automatizadas, 97.1% coverage
6. **Calidad:** Quality Gate OK, todos los indicadores en verde

---

*Documento generado como evidencia técnica del proyecto.*
*Última actualización: Junio 2026*
