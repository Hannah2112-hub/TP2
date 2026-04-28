from typing import List, Dict, Any, Optional
from ..config.database import execute_query


class EstudianteRepository:
    @staticmethod
    def get_all(solo_activos: bool = True) -> List[Dict[str, Any]]:
        if solo_activos:
            return execute_query(
                "SELECT * FROM estudiantes WHERE activo = TRUE ORDER BY apellido, nombre"
            )
        return execute_query("SELECT * FROM estudiantes ORDER BY apellido, nombre")

    @staticmethod
    def get_by_id(estudiante_id: int) -> Optional[Dict[str, Any]]:
        result = execute_query(
            "SELECT * FROM estudiantes WHERE estudianteid = %s", [estudiante_id]
        )
        return result[0] if result else None

    @staticmethod
    def create(
        codigo: str, nombre: str, apellido: str, correo: str, creditos_acum: int = 0
    ) -> Dict[str, Any]:
        result = execute_query(
            """INSERT INTO estudiantes (codigo, nombre, apellido, correo, creditosacum) 
               VALUES (%s, %s, %s, %s, %s) RETURNING estudianteid""",
            [codigo, nombre, apellido, correo, creditos_acum],
        )
        if result:
            return {
                "Exito": True,
                "ID": result[0]["estudianteid"],
                "Mensaje": "Estudiante registrado",
            }
        return {"Exito": False, "Mensaje": "Error al registrar"}

    @staticmethod
    def update(
        estudiante_id: int, nombre: str, apellido: str, correo: str, creditos_acum: int
    ) -> Dict[str, Any]:
        execute_query(
            """UPDATE estudiantes SET nombre = %s, apellido = %s, correo = %s, creditosacum = %s 
               WHERE estudianteid = %s""",
            [nombre, apellido, correo, creditos_acum, estudiante_id],
        )
        return {"Exito": True, "Mensaje": "Estudiante actualizado"}

    @staticmethod
    def delete(estudiante_id: int) -> bool:
        execute_query(
            "DELETE FROM estudiantes WHERE estudianteid = %s", [estudiante_id]
        )
        return True
