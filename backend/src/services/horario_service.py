from typing import List, Dict, Any
from ..repositories import HorarioRepository, DashboardRepository


class HorarioService:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return HorarioRepository.get_all()

    @staticmethod
    def generar(hora_inicio: str = "08:00", bloques_horas: int = 2) -> Dict[str, Any]:
        result = HorarioRepository.generar(hora_inicio, bloques_horas)
        if result.get("Exito"):
            return {
                "success": True,
                "message": result.get("Mensaje"),
                "data": {
                    "horarios_creados": result.get("HorariosCreados", 0),
                    "detalles": result.get("Detalles", []),
                },
            }
        return {"success": False, "message": result.get("Mensaje")}

    @staticmethod
    def validar() -> Dict[str, Any]:
        return HorarioRepository.validar()


class DashboardService:
    @staticmethod
    def get_metrics() -> Dict[str, int]:
        return DashboardRepository.get_metrics()

