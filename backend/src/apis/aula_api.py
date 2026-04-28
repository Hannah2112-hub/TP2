from fastapi import APIRouter, HTTPException
from ..schemas import AulaCreate, AulaUpdate, GenericResponse
from ..services import AulaService

router = APIRouter(prefix="/aulas", tags=["Aulas"])


@router.get("", response_model=GenericResponse)
def get_aulas():
    data = AulaService.get_all()
    return {"success": True, "data": data}


@router.post("", response_model=GenericResponse)
def create_aula(aula: AulaCreate):
    result = AulaService.create(
        aula.nombre, aula.capacidad, aula.edificio, aula.equipamiento
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.put("/{aula_id}", response_model=GenericResponse)
def update_aula(aula_id: int, aula: AulaUpdate):
    result = AulaService.update(
        aula_id,
        aula.nombre or "",
        aula.capacidad or 0,
        aula.edificio or "",
        aula.equipamiento,
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.delete("/{aula_id}", response_model=GenericResponse)
def delete_aula(aula_id: int):
    result = AulaService.delete(aula_id)
    return result
