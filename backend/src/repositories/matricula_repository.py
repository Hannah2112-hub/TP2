from typing import List, Dict, Any, Optional
from ..config.database import execute_query


class MatriculaRepository:
    @staticmethod
    def get_all(estudiante_id: Optional[int] = None) -> List[Dict[str, Any]]:
        if estudiante_id:
            return execute_query(
                """SELECT m.*, e.nombre || ' ' || e.apellido as nombreestudiante, c.nombre as nombrecurso
                FROM matriculas m
                JOIN estudiantes e ON m.estudianteid = e.estudianteid
                JOIN cursos c ON m.cursoid = c.cursoid
                WHERE m.estudianteid = %s
                ORDER BY m.fechamatricula DESC""",
                [estudiante_id],
            )
        return execute_query("""SELECT m.*, e.nombre || ' ' || e.apellido as nombreestudiante, c.nombre as nombrecurso
            FROM matriculas m
            JOIN estudiantes e ON m.estudianteid = e.estudianteid
            JOIN cursos c ON m.cursoid = c.cursoid
            ORDER BY m.fechamatricula DESC""")

    @staticmethod
    def get_by_id(matricula_id: int) -> Optional[Dict[str, Any]]:
        result = execute_query(
            "SELECT * FROM matriculas WHERE matriculaid = %s", [matricula_id]
        )
        return result[0] if result else None

    @staticmethod
    def create(estudiante_id: int, curso_id: int) -> Dict[str, Any]:
        est = execute_query(
            "SELECT creditosacum FROM estudiantes WHERE estudianteid = %s",
            [estudiante_id],
        )
        curso = execute_query(
            "SELECT creditosreq FROM cursos WHERE cursoid = %s", [curso_id]
        )
        
        existente = execute_query(
            "SELECT 1 FROM matriculas WHERE estudianteid = %s AND cursoid = %s", 
            [estudiante_id, curso_id]
        )

        if existente:
            return {"Exito": False, "Mensaje": "El estudiante ya se encuentra matriculado en este curso"}

        if not est:
            return {"Exito": False, "Mensaje": "Estudiante no existe"}
        if not curso:
            return {"Exito": False, "Mensaje": "Curso no existe"}

        creditos_necesarios = curso[0]["creditosreq"]
        if est[0]["creditosacum"] < creditos_necesarios:
            return {
                "Exito": False,
                "Mensaje": f"Creditos insuficientes. Necesita {creditos_necesarios}, tiene {est[0]['creditosacum']}",
            }

        result = execute_query(
            """INSERT INTO matriculas (estudianteid, cursoid, estado) VALUES (%s, %s, 'Aprobada') RETURNING matriculaid""",
            [estudiante_id, curso_id],
        )
        if result:
            return {
                "Exito": True,
                "ID": result[0]["matriculaid"],
                "Mensaje": "Matrícula registrada",
            }
        return {"Exito": False, "Mensaje": "Error al matricular"}

    @staticmethod
    def update_estado(matricula_id: int, estado: str) -> Dict[str, Any]:
        execute_query(
            "UPDATE matriculas SET estado = %s WHERE matriculaid = %s",
            [estado, matricula_id],
        )
        return {"Exito": True, "Mensaje": f"Matrícula actualizada a {estado}"}

