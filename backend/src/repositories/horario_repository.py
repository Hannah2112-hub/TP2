from typing import List, Dict, Any, Optional
from ..config.database import execute_query


class HorarioRepository:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return execute_query("""
            SELECT h.*, c.nombre as nombrecurso, a.nombre as nombreaula, c.carreraid
            FROM horarios h
            JOIN cursos c ON h.cursoid = c.cursoid
            JOIN aulas a ON h.aulaid = a.aulaid
            WHERE h.activo = TRUE
            ORDER BY h.diasemana, h.horainicio
        """)

    @staticmethod
    def _validar_traslape_aula(aula_id: int, dia_semana: str, hora_inicio: str, hora_fin: str) -> bool:
        traslape = execute_query("""
            SELECT 1 FROM horarios
            WHERE aulaid = %s AND diasemana = %s AND activo = TRUE
              AND (horainicio::TIME, horafin::TIME) OVERLAPS (%s::TIME, %s::TIME)
        """, [aula_id, dia_semana, hora_inicio, hora_fin])
        return bool(traslape)

    @staticmethod
    def _validar_traslape_docente(curso_id: int, dia_semana: str, hora_inicio: str, hora_fin: str) -> bool:
        docente = execute_query("SELECT docenteid FROM cursos WHERE cursoid = %s", [curso_id])
        if not docente or not docente[0].get('docenteid'):
            return False
        docente_id = docente[0]['docenteid']
        traslape = execute_query("""
            SELECT 1 FROM horarios h
            JOIN cursos c ON h.cursoid = c.cursoid
            WHERE c.docenteid = %s AND h.diasemana = %s AND h.activo = TRUE
              AND (h.horainicio::TIME, h.horafin::TIME) OVERLAPS (%s::TIME, %s::TIME)
        """, [docente_id, dia_semana, hora_inicio, hora_fin])
        return bool(traslape)

    @staticmethod
    def create(
        curso_id: int, aula_id: int, dia_semana: str, hora_inicio: str, hora_fin: str
    ) -> Dict[str, Any]:
        if HorarioRepository._validar_traslape_aula(aula_id, dia_semana, hora_inicio, hora_fin):
            return {"Exito": False, "Mensaje": "El aula ya está ocupada en ese horario"}

        if HorarioRepository._validar_traslape_docente(curso_id, dia_semana, hora_inicio, hora_fin):
            return {"Exito": False, "Mensaje": "El docente ya tiene una clase asignada en ese horario"}

        result = execute_query(
            """INSERT INTO horarios (cursoid, aulaid, diasemana, horainicio, horafin)
               VALUES (%s, %s, %s, %s, %s) RETURNING horarioid""",
            [curso_id, aula_id, dia_semana, hora_inicio, hora_fin],
        )
        if result:
            return {
                "Exito": True,
                "ID": result[0]["horarioid"],
                "Mensaje": "Horario registrado exitosamente sin cruces",
            }
        return {"Exito": False, "Mensaje": "Error al registrar"}

    @staticmethod
    def delete(horario_id: int) -> bool:
        execute_query(
            "UPDATE horarios SET activo = FALSE WHERE horarioid = %s", [horario_id]
        )
        return True

    @staticmethod
    def _obtener_cursos(carrera_id: Optional[int]) -> List[Dict[str, Any]]:
        if carrera_id:
            return execute_query("SELECT * FROM cursos WHERE activo = TRUE AND carreraid = %s", [carrera_id])
        return execute_query("SELECT * FROM cursos WHERE activo = TRUE")

    @staticmethod
    def _obtener_aulas() -> List[Dict[str, Any]]:
        return execute_query("SELECT * FROM aulas WHERE activo = TRUE")

    @staticmethod
    def _generar_slots(hora_inicio_base: str, bloques_horas: int) -> List[tuple]:
        dias = [1, 2, 3, 4, 5]
        hora_inicio_int = int(hora_inicio_base.split(':')[0])
        hora_fin_limite = 22
        slots = []
        for d in dias:
            for h in range(hora_inicio_int, hora_fin_limite, bloques_horas):
                if h + bloques_horas <= hora_fin_limite:
                    slots.append((d, h, h + bloques_horas))
        return slots

    @staticmethod
    def _construir_modelo(model, cursos, aulas, slots):
        from ortools.sat.python import cp_model

        x = {}
        for c_idx, c in enumerate(cursos):
            cupos = c.get('cupos') or 0
            for a_idx, a in enumerate(aulas):
                capacidad = a.get('capacidad') or 0
                if capacidad < cupos:
                    continue
                for s_idx in range(len(slots)):
                    x[(c_idx, a_idx, s_idx)] = model.NewBoolVar(f'x_c{c["cursoid"]}_a{a["aulaid"]}_s{s_idx}')
        return x

    @staticmethod
    def _restriccion_sesiones(model, x, cursos):
        sesiones_por_curso = 2
        errores = []
        for c_idx, c in enumerate(cursos):
            vars_curso = [x[key] for key in x if key[0] == c_idx]
            if not vars_curso:
                errores.append(f"El curso '{c.get('nombre')}' no tiene aulas con capacidad suficiente.")
                continue
            model.Add(sum(vars_curso) == sesiones_por_curso)
        return errores

    @staticmethod
    def _restriccion_una_sesion_por_dia(model, x, cursos, slots):
        dias = [1, 2, 3, 4, 5]
        for c_idx in range(len(cursos)):
            for d in dias:
                slots_del_dia = [s_idx for s_idx, slot in enumerate(slots) if slot[0] == d]
                vars_curso_dia = [x[key] for key in x if key[0] == c_idx and key[2] in slots_del_dia]
                if vars_curso_dia:
                    model.Add(sum(vars_curso_dia) <= 1)

    @staticmethod
    def _restriccion_una_clase_por_aula(model, x, aulas, slots):
        for a_idx in range(len(aulas)):
            for s_idx in range(len(slots)):
                vars_aula_slot = [x[key] for key in x if key[1] == a_idx and key[2] == s_idx]
                if vars_aula_slot:
                    model.Add(sum(vars_aula_slot) <= 1)

    @staticmethod
    def _restriccion_una_clase_por_docente(model, x, cursos, slots):
        docente_cursos = {}
        for c_idx, c in enumerate(cursos):
            d_id = c.get('docenteid')
            if d_id is not None:
                docente_cursos.setdefault(d_id, []).append(c_idx)
        for cursos_del_docente in docente_cursos.values():
            for s_idx in range(len(slots)):
                vars_docente_slot = [x[key] for key in x if key[0] in cursos_del_docente and key[2] == s_idx]
                if vars_docente_slot:
                    model.Add(sum(vars_docente_slot) <= 1)

    @staticmethod
    def _aplicar_restricciones(model, x, cursos, aulas, slots):
        errores = HorarioRepository._restriccion_sesiones(model, x, cursos)
        HorarioRepository._restriccion_una_sesion_por_dia(model, x, cursos, slots)
        HorarioRepository._restriccion_una_clase_por_aula(model, x, aulas, slots)
        HorarioRepository._restriccion_una_clase_por_docente(model, x, cursos, slots)
        return errores

    @staticmethod
    def _insertar_horarios(solver, x, cursos, aulas, slots, carrera_id):
        if carrera_id:
            execute_query(
                "DELETE FROM horarios WHERE cursoid IN (SELECT cursoid FROM cursos WHERE carreraid = %s) AND activo = TRUE",
                [carrera_id]
            )
        else:
            execute_query("DELETE FROM horarios WHERE activo = TRUE")

        horarios_creados = 0
        for (c_idx, a_idx, s_idx), var in x.items():
            if solver.Value(var) == 1:
                c_id = cursos[c_idx]['cursoid']
                a_id = aulas[a_idx]['aulaid']
                dia, h_inicio, h_fin = slots[s_idx]
                str_inicio = f"{h_inicio:02d}:00"
                str_fin = f"{h_fin:02d}:00"
                execute_query(
                    """INSERT INTO horarios (cursoid, aulaid, diasemana, horainicio, horafin)
                       VALUES (%s, %s, %s, %s, %s)""",
                    [c_id, a_id, dia, str_inicio, str_fin]
                )
                horarios_creados += 1
        return horarios_creados

    @staticmethod
    def generar(hora_inicio_base: str = "08:00", bloques_horas: int = 2, carrera_id: int | None = None) -> Dict[str, Any]:
        try:
            from ortools.sat.python import cp_model
            import random

            cursos = HorarioRepository._obtener_cursos(carrera_id)
            aulas = HorarioRepository._obtener_aulas()

            if not cursos:
                return {"Exito": False, "Mensaje": "No hay cursos activos para programar"}
            if not aulas:
                return {"Exito": False, "Mensaje": "No hay aulas activas disponibles"}

            slots = HorarioRepository._generar_slots(hora_inicio_base, bloques_horas)
            if not slots:
                return {"Exito": False, "Mensaje": "Configuración de horas no permite generar slots"}

            model = cp_model.CpModel()
            x = HorarioRepository._construir_modelo(model, cursos, aulas, slots)

            if not x:
                return {"Exito": False, "Mensaje": "No se pudieron crear variables de asignación"}

            errores = HorarioRepository._aplicar_restricciones(model, x, cursos, aulas, slots)

            solver = cp_model.CpSolver()
            solver.parameters.random_seed = random.randint(1, 1000)
            solver.parameters.max_time_in_seconds = 10.0

            status = solver.Solve(model)

            if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
                return {
                    "Exito": False,
                    "Mensaje": "No se encontró una solución factible para generar los horarios. Intente agregar más aulas o verificar cupos."
                }

            horarios_creados = HorarioRepository._insertar_horarios(solver, x, cursos, aulas, slots, carrera_id)
            mensaje = f"Se generaron {horarios_creados} horario(s) exitosamente usando OR-Tools (CSP)."
            if errores:
                mensaje += f" Problemas ignorados: {len(errores)} curso(s) sin aulas disponibles."

            return {
                "Exito": True,
                "Mensaje": mensaje,
                "HorariosCreados": horarios_creados,
                "Detalles": errores,
            }

        except ImportError:
            return {"Exito": False, "Mensaje": "Falta instalar ortools. Ejecute: uv add ortools"}
        except Exception as e:
            return {"Exito": False, "Mensaje": f"Error en el algoritmo CSP: {str(e)}"}

    @staticmethod
    def validar() -> Dict[str, Any]:
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
