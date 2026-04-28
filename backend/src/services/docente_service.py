from typing import List, Dict, Any, Optional
from ..repositories import DocenteRepository


class DocenteService:
    @staticmethod
    def get_all(solo_activos: bool = True) -> List[Dict[str, Any]]:
        return DocenteRepository.get_all(solo_activos)

    @staticmethod
    def create(
        codigo: str,
        nombre: str,
        apellido: str,
        especialidad: str,
        correo: Optional[str] = None,
    ) -> Dict[str, Any]:
        result = DocenteRepository.create(
            codigo, nombre, apellido, especialidad, correo
        )
        if result.get("Exito"):
            return {
                "success": True,
                "data": {"id": result.get("ID"), "message": result.get("Mensaje")},
            }
        return {"success": False, "message": result.get("Mensaje")}

    @staticmethod
    def update(
        docente_id: int,
        nombre: str,
        apellido: str,
        especialidad: str,
        correo: Optional[str],
    ) -> Dict[str, Any]:
        result = DocenteRepository.update(
            docente_id, nombre, apellido, especialidad, correo
        )
        if result.get("Exito"):
            return {"success": True, "data": {"message": result.get("Mensaje")}}
        return {"success": False, "message": result.get("Mensaje")}

    @staticmethod
    def delete(docente_id: int) -> Dict[str, Any]:
        DocenteRepository.delete(docente_id)
        return {"success": True, "message": "Docente eliminado."}
