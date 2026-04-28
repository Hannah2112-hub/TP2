from typing import List, Dict, Any, Optional
from ..repositories import MatriculaRepository


class MatriculaService:
    @staticmethod
    def get_all(estudiante_id: Optional[int] = None) -> List[Dict[str, Any]]:
        return MatriculaRepository.get_all(estudiante_id)

    @staticmethod
    def create(estudiante_id: int, curso_id: int) -> Dict[str, Any]:
        result = MatriculaRepository.create(estudiante_id, curso_id)
        if result.get("Exito"):
            return {
                "success": True,
                "data": {"id": result.get("ID"), "message": result.get("Mensaje")},
            }
        return {"success": False, "message": result.get("Mensaje")}

    @staticmethod
    def update_estado(matricula_id: int, estado: str) -> Dict[str, Any]:
        valid_states = ["Pendiente", "Aprobada", "Rechazada", "Retirada"]
        if estado not in valid_states:
            return {
                "success": False,
                "message": f"Estado inválido. Estados válidos: {valid_states}",
            }
        result = MatriculaRepository.update_estado(matricula_id, estado)
        return {"success": True, "message": result.get("Mensaje")}
