from typing import List, Dict, Any, Optional
from ..config.database import execute_query


class CursoRepository:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return execute_query("""
            SELECT c.*, d.nombre || ' ' || d.apellido as nombredocente 
            FROM cursos c 
            LEFT JOIN docentes d ON c.docenteid = d.docenteid 
            WHERE c.activo = TRUE 
            ORDER BY c.nombre
        """)

    @staticmethod
    def get_by_id(curso_id: int) -> Optional[Dict[str, Any]]:
        result = execute_query("SELECT * FROM cursos WHERE cursoid = %s", [curso_id])
        return result[0] if result else None

    @staticmethod
    def create(
        codigo: str,
        nombre: str,
        creditos_req: int,
        prerequisito_id: Optional[int],
        docente_id: int,
        cupos: int,
    ) -> Dict[str, Any]:
        prerequisito = prerequisito_id if prerequisito_id else None
        result = execute_query(
            """INSERT INTO cursos (codigo, nombre, creditosreq, prerequisitoid, docenteid, cupos) 
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING cursoid""",
            [codigo, nombre, creditos_req, prerequisito, docente_id, cupos],
        )
        if result:
            return {
                "Exito": True,
                "ID": result[0]["cursoid"],
                "Mensaje": "Curso registrado",
            }
        return {"Exito": False, "Mensaje": "Error al registrar"}

    @staticmethod
    def update(
        curso_id: int,
        codigo: str,
        nombre: str,
        creditos_req: int,
        prerequisito_id: Optional[int],
        docente_id: int,
        cupos: int,
    ) -> Dict[str, Any]:
        prerequisito = prerequisito_id if prerequisito_id else None
        execute_query(
            """UPDATE cursos SET codigo = %s, nombre = %s, creditosreq = %s, prerequisitoid = %s, docenteid = %s, cupos = %s 
               WHERE cursoid = %s""",
            [codigo, nombre, creditos_req, prerequisito, docente_id, cupos, curso_id],
        )
        return {"Exito": True, "Mensaje": "Curso actualizado"}

    @staticmethod
    def delete(curso_id: int) -> bool:
        execute_query("DELETE FROM cursos WHERE cursoid = %s", [curso_id])
        return True
