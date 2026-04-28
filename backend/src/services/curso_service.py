from typing import List, Dict, Any, Optional
from ..repositories import CursoRepository


class CursoService:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return CursoRepository.get_all()

    @staticmethod
    def create(
        codigo: str,
        nombre: str,
        creditos_req: int,
        prerequisito_id: Optional[int],
        docente_id: int,
        cupos: int,
    ) -> Dict[str, Any]:
        result = CursoRepository.create(
            codigo, nombre, creditos_req, prerequisito_id, docente_id, cupos
        )
        if result.get("Exito"):
            return {
                "success": True,
                "data": {"id": result.get("ID"), "message": result.get("Mensaje")},
            }
        return {"success": False, "message": result.get("Mensaje")}

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
        result = CursoRepository.update(
            curso_id, codigo, nombre, creditos_req, prerequisito_id, docente_id, cupos
        )
        if result.get("Exito"):
            return {"success": True, "data": {"message": result.get("Mensaje")}}
        return {"success": False, "message": result.get("Mensaje")}

    @staticmethod
    def delete(curso_id: int) -> Dict[str, Any]:
        CursoRepository.delete(curso_id)
        return {"success": True, "message": "Curso eliminado."}
