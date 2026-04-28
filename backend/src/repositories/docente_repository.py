from typing import List, Dict, Any, Optional
from ..config.database import execute_query


class DocenteRepository:
    @staticmethod
    def get_all(solo_activos: bool = True) -> List[Dict[str, Any]]:
        if solo_activos:
            return execute_query(
                "SELECT * FROM docentes WHERE activo = TRUE ORDER BY apellido, nombre"
            )
        return execute_query("SELECT * FROM docentes ORDER BY apellido, nombre")

    @staticmethod
    def get_by_id(docente_id: int) -> Optional[Dict[str, Any]]:
        result = execute_query(
            "SELECT * FROM docentes WHERE docenteid = %s", [docente_id]
        )
        return result[0] if result else None

    @staticmethod
    def create(
        codigo: str,
        nombre: str,
        apellido: str,
        especialidad: str,
        correo: Optional[str] = None,
    ) -> Dict[str, Any]:
        result = execute_query(
            """INSERT INTO docentes (codigo, nombre, apellido, especialidad, correo) 
               VALUES (%s, %s, %s, %s, %s) RETURNING docenteid""",
            [codigo, nombre, apellido, especialidad, correo],
        )
        if result:
            return {
                "Exito": True,
                "ID": result[0]["docenteid"],
                "Mensaje": "Docente registrado",
            }
        return {"Exito": False, "Mensaje": "Error al registrar"}

    @staticmethod
    def update(
        docente_id: int,
        nombre: str,
        apellido: str,
        especialidad: str,
        correo: Optional[str],
    ) -> Dict[str, Any]:
        execute_query(
            """UPDATE docentes SET nombre = %s, apellido = %s, especialidad = %s, correo = %s 
               WHERE docenteid = %s""",
            [nombre, apellido, especialidad, correo, docente_id],
        )
        return {"Exito": True, "Mensaje": "Docente actualizado"}

    @staticmethod
    def delete(docente_id: int) -> bool:
        execute_query("DELETE FROM docentes WHERE docenteid = %s", [docente_id])
        return True
