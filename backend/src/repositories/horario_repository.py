from typing import List, Dict, Any, Optional
from ..config.database import execute_query


class HorarioRepository:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return execute_query("""
            SELECT h.*, c.nombre as nombrecurso, a.nombre as nombreaula
            FROM horarios h
            JOIN cursos c ON h.cursoid = c.cursoid
            JOIN aulas a ON h.aulaid = a.aulaid
            WHERE h.activo = TRUE
            ORDER BY h.diasemana, h.horainicio
        """)

    @staticmethod
    def create(
        curso_id: int, aula_id: int, dia_semana: int, hora_inicio: str, hora_fin: str
    ) -> Dict[str, Any]:
        result = execute_query(
            """INSERT INTO horarios (cursoid, aulaid, diasemana, horainicio, horafin) 
               VALUES (%s, %s, %s, %s, %s) RETURNING horarioid""",
            [curso_id, aula_id, dia_semana, hora_inicio, hora_fin],
        )
        if result:
            return {
                "Exito": True,
                "ID": result[0]["horarioid"],
                "Mensaje": "Horario registrado",
            }
        return {"Exito": False, "Mensaje": "Error al registrar"}

    @staticmethod
    def delete(horario_id: int) -> bool:
        execute_query(
            "UPDATE horarios SET activo = FALSE WHERE horarioid = %s", [horario_id]
        )
        return True

    @staticmethod
    def generar(hora_inicio_base: str = "08:00", bloques_horas: int = 2) -> Dict[str, Any]:
        try:
            # 1. Obtener datos necesarios
            cursos = execute_query("SELECT * FROM cursos WHERE activo = TRUE")
            aulas = execute_query("SELECT * FROM aulas WHERE activo = TRUE")

            if not cursos:
                return {"Exito": False, "Mensaje": "No hay cursos activos para programar"}
            if not aulas:
                return {"Exito": False, "Mensaje": "No hay aulas activas disponibles"}

            # 2. Limpiar SOLO los horarios activos previos (sin borrar historial inactivo)
            execute_query("DELETE FROM horarios WHERE activo = TRUE")

            # 3. Preparar estructuras de control
            ocupacion_aula: Dict[int, Dict[int, set]] = {}
            ocupacion_docente: Dict[int, Dict[int, set]] = {}

            dias = [1, 2, 3, 4, 5]
            hora_inicio_int = int(hora_inicio_base.split(':')[0])
            hora_fin_limite = 22
            horas_disponibles = list(range(hora_inicio_int, hora_fin_limite - bloques_horas + 1))

            horarios_creados = 0
            errores = []

            # Preparar todas las combinaciones posibles de días y horas
            slots_disponibles = [(d, h) for d in dias for h in horas_disponibles]

            import random
            random.seed()

            # Variables para round-robin de aulas
            aula_idx = 0

            for curso in cursos:
                docente_id: Optional[int] = curso.get('docenteid')
                
                sesiones_asignadas = 0
                # Aumentamos drásticamente para rellenar cada hora disponible de la semana
                sesiones_requeridas = 15 
                clases_por_dia = {} # Para limitar a un máximo de 2 veces por día

                # Barajar aleatoriamente los slots para este curso para distribuirlos por toda la semana (7am a 10pm)
                random.shuffle(slots_disponibles)

                for dia, current_h in slots_disponibles:
                    if sesiones_asignadas >= sesiones_requeridas:
                        break
                        
                    if clases_por_dia.get(dia, 0) >= 2:
                        continue # Evitar que se dicte más de 2 veces el mismo día

                    aulas_ordenadas = aulas[aula_idx:] + aulas[:aula_idx]
                    for aula in aulas_ordenadas:
                            cap_aula = aula.get('capacidad') or 0
                            cupos_curso = curso.get('cupos') or 0
                            if cap_aula < cupos_curso:
                                continue

                            conflicto = False
                            for h in range(current_h, current_h + bloques_horas):
                                # Validar que no haya NINGÚN curso en esta hora a nivel global (1 curso por bloque de hora)
                                if dia in ocupacion_aula and h in ocupacion_aula[dia] and len(ocupacion_aula[dia][h]) > 0:
                                    conflicto = True
                                    break
                                # Validar que el aula no esté ocupada en esta hora
                                if dia in ocupacion_aula and h in ocupacion_aula[dia] and aula['aulaid'] in ocupacion_aula[dia][h]:
                                    conflicto = True
                                    break
                                # Validar que el docente no esté dictando otro curso en esta hora
                                if docente_id is not None and dia in ocupacion_docente and h in ocupacion_docente[dia] and docente_id in ocupacion_docente[dia][h]:
                                    conflicto = True
                                    break

                            if not conflicto:
                                aula_idx = (aula_idx + 1) % len(aulas) # Rotar al siguiente aula para que no sea siempre la 101
                                for h in range(current_h, current_h + bloques_horas):
                                    ocupacion_aula.setdefault(dia, {}).setdefault(h, set()).add(aula['aulaid'])
                                    if docente_id is not None:
                                        ocupacion_docente.setdefault(dia, {}).setdefault(h, set()).add(docente_id)

                                str_inicio = f"{current_h:02d}:00"
                                str_fin = f"{(current_h + bloques_horas):02d}:00"

                                execute_query(
                                    """INSERT INTO horarios (cursoid, aulaid, diasemana, horainicio, horafin) 
                                       VALUES (%s, %s, %s, %s, %s)""",
                                    [curso['cursoid'], aula['aulaid'], dia, str_inicio, str_fin]
                                )

                                horarios_creados += 1
                                sesiones_asignadas += 1
                                clases_por_dia[dia] = clases_por_dia.get(dia, 0) + 1
                                break

                if sesiones_asignadas < sesiones_requeridas:
                    errores.append(
                        f"No se pudo asignar el curso '{curso.get('nombre', 'Sin nombre')}' "
                        f"las {sesiones_requeridas} sesiones. (Logradas: {sesiones_asignadas})"
                    )

            mensaje = f"Se generaron {horarios_creados} horario(s) exitosamente."
            if errores:
                mensaje += f" {len(errores)} curso(s) no pudieron ser asignados por falta de disponibilidad."

            return {
                "Exito": True,
                "Mensaje": mensaje,
                "HorariosCreados": horarios_creados,
                "Detalles": errores,
            }

        except Exception as e:
            return {"Exito": False, "Mensaje": f"Error en el algoritmo de generación: {str(e)}"}

    @staticmethod
    def validar() -> Dict[str, Any]:
        # 1. Traslapes de aula — cast ::TIME requerido en PostgreSQL para OVERLAPS con varchar
        traslapes_aula = execute_query("""
            SELECT h1.horarioid, h1.aulaid, h1.diasemana,
                   h1.horainicio, h1.horafin,
                   h2.horarioid AS colision_id
            FROM horarios h1
            JOIN horarios h2
                ON h1.aulaid = h2.aulaid
               AND h1.diasemana = h2.diasemana
               AND h1.horarioid < h2.horarioid
               AND (h1.horainicio::TIME, h1.horafin::TIME)
                    OVERLAPS
                   (h2.horainicio::TIME, h2.horafin::TIME)
            WHERE h1.activo = TRUE AND h2.activo = TRUE
        """)

        # 2. Traslapes de docente — excluir cursos sin docente (docenteid IS NULL)
        traslapes_docente = execute_query("""
            SELECT h1.horarioid, c1.docenteid, h1.diasemana,
                   h1.horainicio, h1.horafin,
                   h2.horarioid AS colision_id
            FROM horarios h1
            JOIN cursos c1 ON h1.cursoid = c1.cursoid
            JOIN horarios h2
                ON h1.diasemana = h2.diasemana
               AND h1.horarioid < h2.horarioid
            JOIN cursos c2 ON h2.cursoid = c2.cursoid
            WHERE c1.docenteid = c2.docenteid
              AND c1.docenteid IS NOT NULL
              AND (h1.horainicio::TIME, h1.horafin::TIME)
                   OVERLAPS
                  (h2.horainicio::TIME, h2.horafin::TIME)
              AND h1.activo = TRUE AND h2.activo = TRUE
        """)

        # 3. Capacidad de aula insuficiente para los cupos del curso
        errores_capacidad = execute_query("""
            SELECT h.horarioid, c.nombre AS curso, a.nombre AS aula,
                   c.cupos, a.capacidad
            FROM horarios h
            JOIN cursos c ON h.cursoid = c.cursoid
            JOIN aulas a ON h.aulaid = a.aulaid
            WHERE c.cupos > a.capacidad AND h.activo = TRUE
        """)

        es_valido = (
            len(traslapes_aula) == 0
            and len(traslapes_docente) == 0
            and len(errores_capacidad) == 0
        )

        return {
            "Valido": es_valido,
            "ConflictosAula": traslapes_aula,
            "ConflictosDocente": traslapes_docente,
            "ErroresCapacidad": errores_capacidad,
        }


class DashboardRepository:
    @staticmethod
    def get_metrics() -> Dict[str, int]:
        result = execute_query("""
            SELECT 
                (SELECT COUNT(*) FROM estudiantes WHERE activo = TRUE) AS total_estudiantes,
                (SELECT COUNT(*) FROM docentes WHERE activo = TRUE)    AS total_docentes,
                (SELECT COUNT(*) FROM cursos WHERE activo = TRUE)      AS total_cursos,
                (SELECT COUNT(*) FROM aulas WHERE activo = TRUE)       AS total_aulas,
                (SELECT COUNT(*) FROM matriculas WHERE estado = 'Aprobada')  AS matriculas_aprobadas,
                (SELECT COUNT(*) FROM matriculas WHERE estado = 'Rechazada') AS matriculas_rechazadas
        """)
        if result:
            return result[0]
        return {
            "total_estudiantes": 0,
            "total_docentes": 0,
            "total_cursos": 0,
            "total_aulas": 0,
            "matriculas_aprobadas": 0,
            "matriculas_rechazadas": 0,
        }
