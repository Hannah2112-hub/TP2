# Generador de Horarios Académicos

## Tabla de Contenido
- [Nombre del proyecto](#nombre-del-proyecto)
- [Integrantes del equipo](#integrantes-del-equipo)
- [Problemática abordada](#problemática-abordada)
- [Justificación del PMV](#justificación-del-pmv)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Arquitectura del sistema](#arquitectura-del-sistema)
- [Instrucciones de instalación](#instrucciones-de-instalación)
- [Instrucciones de build](#instrucciones-de-build)
- [Instrucciones de despliegue](#instrucciones-de-despliegue)
- [Video explicativo](#video-explicativo)
- [Documentación](#documentación)

---

## Nombre del proyecto

**HorarioSmart – Generador de Horarios Académicos**

---

## Integrantes del equipo

- Escobar Benbezú Aldrin Edwin
- Lopez Rodriguez Axel Andre
- Meza Calderon Ana Cristina

---

## Problemática abordada

La planificación de horarios académicos en instituciones educativas suele realizarse de forma manual, lo que genera diversos problemas como conflictos entre cursos, cruces de docentes, mala asignación de aulas y un alto consumo de tiempo. Además, este proceso es propenso a errores humanos, afectando la eficiencia operativa y la calidad del servicio educativo.

---

## Justificación del PMV

El Producto Mínimo Viable (PMV) de **HorarioSmart** se enfoca en resolver el problema principal: la generación automática de horarios sin conflictos. Esto permite validar rápidamente la utilidad del sistema, reduciendo tiempos de planificación y mejorando la organización académica. El PMV prioriza funcionalidades clave como el registro de datos básicos y la generación automática de horarios, dejando mejoras avanzadas para futuras iteraciones.

---

## Tecnologías utilizadas

| Componente          | Tecnología   |
|---------------------|--------------|
| Backend             | FastAPI      |
| Frontend            | Angular      |
| Base de datos       | SQL Server   |
| Control de versiones| GitHub       |
| Lenguaje principal  | Python       |

---

## Arquitectura del sistema

El sistema sigue una arquitectura cliente-servidor:

- **Frontend:** Interfaz desarrollada en Angular para la interacción con el usuario.
- **Backend:** API REST construida con FastAPI que gestiona la lógica del sistema.
- **Base de datos:** SQL Server para almacenamiento de información.
- **Comunicación:** HTTP/JSON entre cliente y servidor.

---

## Instrucciones de instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Hannah2112-hub/TP2
   ```

2. Acceder al proyecto:
   ```bash
   cd TP2
   ```

3. Instalar dependencias del backend:
   ```bash
   pip install -r requirements.txt
   ```

4. Instalar dependencias del frontend:
   ```bash
   npm install
   ```

---

## Instrucciones de build

**Backend:**
```bash
uvicorn main:app --reload
```

**Frontend:**
```bash
npm run build
```

---

## Instrucciones de despliegue

1. Configurar la base de datos en SQL Server.
2. Actualizar variables de entorno (credenciales, puertos, etc.).
3. Ejecutar el backend en un servidor (ej: Uvicorn o Docker).
4. Desplegar el frontend en un servidor web (ej: Nginx).

---

## Video explicativo

👉 *(Agregar enlace al video – máximo 5 minutos)*

---

## Documentación

👉 Revisar la carpeta [`docs/`](./docs) dentro del repositorio para más detalles técnicos y funcionales.
