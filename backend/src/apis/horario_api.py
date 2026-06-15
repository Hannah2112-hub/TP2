from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from ..schemas import GenericResponse, HorarioCreate
from ..services import HorarioService, DashboardService

router = APIRouter(tags=["Horarios"])


@router.get("/horarios", response_model=GenericResponse)
def get_horarios():
    data = HorarioService.get_all()
    return {"success": True, "data": data}


@router.post("/horarios", response_model=GenericResponse, responses={400: {"description": "Error de validación"}})
def crear_horario(horario: HorarioCreate):
    result = HorarioService.create(horario)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.post("/horarios/generar", response_model=GenericResponse, responses={400: {"description": "Error de generación"}})
def generar_horarios(
    hora_inicio: Annotated[str, Query(description="Hora de inicio en formato HH:MM")] = "08:00",
    bloques_horas: Annotated[int, Query(ge=1, le=6, description="Duración del bloque en horas")] = 2,
    carrera_id: Annotated[int | None, Query(description="ID de la carrera a generar horario")] = None,
):
    result = HorarioService.generar(hora_inicio, bloques_horas, carrera_id)
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
