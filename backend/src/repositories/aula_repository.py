from typing import List, Dict, Any, Optional
from ..config.database import execute_query


class AulaRepository:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return execute_query("SELECT * FROM aulas WHERE activo = TRUE ORDER BY nombre")

    @staticmethod
    def get_by_id(aula_id: int) -> Optional[Dict[str, Any]]:
        result = execute_query("SELECT * FROM aulas WHERE aulaid = %s", [aula_id])
        return result[0] if result else None

    @staticmethod
    def create(
        nombre: str, capacidad: int, edificio: str, equipamiento: Optional[str] = None
    ) -> Dict[str, Any]:
        result = execute_query(
            """INSERT INTO aulas (nombre, capacidad, edificio, equipamiento) 
               VALUES (%s, %s, %s, %s) RETURNING aulaid""",
            [nombre, capacidad, edificio, equipamiento],
        )
        if result:
            return {
                "Exito": True,
                "ID": result[0]["aulaid"],
                "Mensaje": "Aula registrada",
            }
        return {"Exito": False, "Mensaje": "Error al registrar"}

    @staticmethod
    def update(
        aula_id: int,
        nombre: str,
        capacidad: int,
        edificio: str,
        equipamiento: Optional[str],
    ) -> Dict[str, Any]:
        execute_query(
            """UPDATE aulas SET nombre = %s, capacidad = %s, edificio = %s, equipamiento = %s 
               WHERE aulaid = %s""",
            [nombre, capacidad, edificio, equipamiento, aula_id],
        )
        return {"Exito": True, "Mensaje": "Aula actualizada"}

    @staticmethod
    def delete(aula_id: int) -> bool:
        execute_query("DELETE FROM aulas WHERE aulaid = %s", [aula_id])
        return True
