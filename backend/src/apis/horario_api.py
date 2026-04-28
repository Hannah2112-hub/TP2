from fastapi import APIRouter, HTTPException, Query
from ..schemas import GenericResponse
from ..services import HorarioService, DashboardService

router = APIRouter(tags=["Horarios"])


@router.get("/horarios", response_model=GenericResponse)
def get_horarios():
    data = HorarioService.get_all()
    return {"success": True, "data": data}


@router.post("/horarios/generar", response_model=GenericResponse)
def generar_horarios(
    hora_inicio: str = Query(default="08:00", description="Hora de inicio en formato HH:MM"),
    bloques_horas: int = Query(default=2, ge=1, le=6, description="Duración del bloque en horas"),
):
    result = HorarioService.generar(hora_inicio, bloques_horas)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.get("/horarios/validar", response_model=GenericResponse)
def validar_horarios():
    data = HorarioService.validar()
    return {"success": True, "data": data}


@router.get("/dashboard", response_model=GenericResponse)
def get_dashboard():
    data = DashboardService.get_metrics()
    return {"success": True, "data": data}
