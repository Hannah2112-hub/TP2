from typing import List, Dict, Any
from ..repositories import EstudianteRepository


class EstudianteService:
    @staticmethod
    def get_all(solo_activos: bool = True) -> List[Dict[str, Any]]:
        return EstudianteRepository.get_all(solo_activos)

    @staticmethod
    def create(
        codigo: str, nombre: str, apellido: str, correo: str, creditos_acum: int = 0
    ) -> Dict[str, Any]:
        result = EstudianteRepository.create(
            codigo, nombre, apellido, correo, creditos_acum
        )
        if result.get("Exito"):
            return {
                "success": True,
                "data": {"id": result.get("ID"), "message": result.get("Mensaje")},
            }
        return {"success": False, "message": result.get("Mensaje")}

    @staticmethod
    def update(
        estudiante_id: int, nombre: str, apellido: str, correo: str, creditos_acum: int
    ) -> Dict[str, Any]:
        result = EstudianteRepository.update(
            estudiante_id, nombre, apellido, correo, creditos_acum
        )
        if result.get("Exito"):
            return {"success": True, "data": {"message": result.get("Mensaje")}}
        return {"success": False, "message": result.get("Mensaje")}

    @staticmethod
    def delete(estudiante_id: int) -> Dict[str, Any]:
        EstudianteRepository.delete(estudiante_id)
        return {"success": True, "message": "Estudiante eliminado."}
