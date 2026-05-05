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
            from ortools.sat.python import cp_model
            import random

            # 1. Obtener datos necesarios
            cursos = execute_query("SELECT * FROM cursos WHERE activo = TRUE")
            aulas = execute_query("SELECT * FROM aulas WHERE activo = TRUE")

            if not cursos:
                return {"Exito": False, "Mensaje": "No hay cursos activos para programar"}
            if not aulas:
                return {"Exito": False, "Mensaje": "No hay aulas activas disponibles"}

            # 2. Configurar dominios de tiempo (Slots fijos, no superpuestos)
            dias = [1, 2, 3, 4, 5]
            hora_inicio_int = int(hora_inicio_base.split(':')[0])
            hora_fin_limite = 22
            
            slots = []
            for d in dias:
                for h in range(hora_inicio_int, hora_fin_limite, bloques_horas):
                    if h + bloques_horas <= hora_fin_limite:
                        slots.append((d, h, h + bloques_horas))
            
            if not slots:
                return {"Exito": False, "Mensaje": "Configuración de horas no permite generar slots"}

            # 3. Preparar el modelo CSP
            model = cp_model.CpModel()
            
            # Variables: x[curso_id, aula_id, slot_idx] = 1 si se asigna, 0 si no
            x = {}
            for c_idx, c in enumerate(cursos):
                c_id = c['cursoid']
                cupos = c.get('cupos') or 0
                for a_idx, a in enumerate(aulas):
                    a_id = a['aulaid']
                    capacidad = a.get('capacidad') or 0
                    
                    # Filtro de restricción dura: capacidad del aula
                    if capacidad < cupos:
                        continue
                        
                    for s_idx, slot in enumerate(slots):
                        x[(c_idx, a_idx, s_idx)] = model.NewBoolVar(f'x_c{c_id}_a{a_id}_s{s_idx}')

            # Restricción 1: Sesiones requeridas por curso
            # Asignamos 2 sesiones semanales por curso (estándar)
            sesiones_por_curso = 2
            errores = []
            
            for c_idx, c in enumerate(cursos):
                vars_curso = [x[key] for key in x if key[0] == c_idx]
                if not vars_curso:
                    errores.append(f"El curso '{c.get('nombre')}' no tiene aulas con capacidad suficiente.")
                    continue
                model.Add(sum(vars_curso) == sesiones_por_curso)

            # Restricción 2: Un curso no puede estar más de una vez en el mismo día (distribución)
            for c_idx, c in enumerate(cursos):
                for d in dias:
                    slots_del_dia = [s_idx for s_idx, slot in enumerate(slots) if slot[0] == d]
                    vars_curso_dia = [x[key] for key in x if key[0] == c_idx and key[2] in slots_del_dia]
                    if vars_curso_dia:
                        model.Add(sum(vars_curso_dia) <= 1)

            # Restricción 3: Un aula solo puede tener 1 curso por slot (No traslapes de aula)
            for a_idx, a in enumerate(aulas):
                for s_idx, slot in enumerate(slots):
                    vars_aula_slot = [x[key] for key in x if key[1] == a_idx and key[2] == s_idx]
                    if vars_aula_slot:
                        model.Add(sum(vars_aula_slot) <= 1)

            # Restricción 4: Un docente no puede dictar más de un curso a la vez (No traslapes de docente)
            docente_cursos = {}
            for c_idx, c in enumerate(cursos):
                d_id = c.get('docenteid')
                if d_id is not None:
                    docente_cursos.setdefault(d_id, []).append(c_idx)
            
            for d_id, cursos_del_docente in docente_cursos.items():
                for s_idx, slot in enumerate(slots):
                    vars_docente_slot = [x[key] for key in x if key[0] in cursos_del_docente and key[2] == s_idx]
                    if vars_docente_slot:
                        model.Add(sum(vars_docente_slot) <= 1)

            # En lugar de maximizar una función aleatoria (lo cual hace que el solver intente probar optimalidad
            # sobre combinaciones masivas y se cuelgue), simplemente buscamos cualquier solución factible,
            # pero podemos randomizar la búsqueda interna del solver.
            
            # 4. Resolver el CSP
            solver = cp_model.CpSolver()
            solver.parameters.random_seed = random.randint(1, 1000)
            solver.parameters.max_time_in_seconds = 10.0
            
            status = solver.Solve(model)

            if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
                # Limpiar horarios activos anteriores si se encontró solución
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
                
                mensaje = f"Se generaron {horarios_creados} horario(s) exitosamente usando OR-Tools (CSP)."
                if errores:
                    mensaje += f" Problemas ignorados: {len(errores)} curso(s) sin aulas disponibles."

                return {
                    "Exito": True,
                    "Mensaje": mensaje,
                    "HorariosCreados": horarios_creados,
                    "Detalles": errores,
                }
            else:
                return {
                    "Exito": False,
                    "Mensaje": "No se encontró una solución factible para generar los horarios. Intente agregar más aulas o verificar cupos."
                }

        except ImportError:
            return {"Exito": False, "Mensaje": "Falta instalar ortools. Ejecute: uv add ortools"}
        except Exception as e:
            return {"Exito": False, "Mensaje": f"Error en el algoritmo CSP: {str(e)}"}

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
