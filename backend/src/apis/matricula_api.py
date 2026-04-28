from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..schemas import MatriculaCreate, GenericResponse
from ..services import MatriculaService

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])


@router.get("", response_model=GenericResponse)
def get_matriculas(estudiante_id: Optional[int] = Query(None)):
    data = MatriculaService.get_all(estudiante_id)
    return {"success": True, "data": data}


@router.post("", response_model=GenericResponse)
def create_matricula(matricula: MatriculaCreate):
    result = MatriculaService.create(matricula.estudianteID, matricula.cursoID)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.put("/{matricula_id}/estado", response_model=GenericResponse)
def update_estado_matricula(matricula_id: int, estado: str):
    result = MatriculaService.update_estado(matricula_id, estado)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result
