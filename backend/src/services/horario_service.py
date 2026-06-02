from typing import List, Dict, Any
from ..repositories import HorarioRepository, DashboardRepository


class HorarioService:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return HorarioRepository.get_all()

    @staticmethod
    def create(horario) -> Dict[str, Any]:
        result = HorarioRepository.create(
            curso_id=horario.cursoID,
            aula_id=horario.aulaID,
            dia_semana=horario.diaSemana,
            hora_inicio=horario.horaInicio,
            hora_fin=horario.horaFin,
        )
        if result.get("Exito"):
            return {
                "success": True,
                "message": result.get("Mensaje"),
                "data": {"id": result.get("ID")},
            }
        return {"success": False, "message": result.get("Mensaje")}

    @staticmethod
    def generar(hora_inicio: str = "08:00", bloques_horas: int = 2, carrera_id: int | None = None) -> Dict[str, Any]:
        result = HorarioRepository.generar(hora_inicio, bloques_horas, carrera_id)
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

