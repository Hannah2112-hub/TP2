from typing import List, Dict, Any, Optional
from ..repositories import AulaRepository


class AulaService:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return AulaRepository.get_all()

    @staticmethod
    def create(
        nombre: str, capacidad: int, edificio: str, equipamiento: Optional[str] = None
    ) -> Dict[str, Any]:
        result = AulaRepository.create(nombre, capacidad, edificio, equipamiento)
        if result.get("Exito"):
            return {
                "success": True,
                "data": {"id": result.get("ID"), "message": result.get("Mensaje")},
            }
        return {"success": False, "message": result.get("Mensaje")}

    @staticmethod
    def update(
        aula_id: int,
        nombre: str,
        capacidad: int,
        edificio: str,
        equipamiento: Optional[str],
    ) -> Dict[str, Any]:
        result = AulaRepository.update(
            aula_id, nombre, capacidad, edificio, equipamiento
        )
        if result.get("Exito"):
            return {"success": True, "data": {"message": result.get("Mensaje")}}
        return {"success": False, "message": result.get("Mensaje")}

    @staticmethod
    def delete(aula_id: int) -> Dict[str, Any]:
        AulaRepository.delete(aula_id)
        return {"success": True, "message": "Aula eliminada."}
