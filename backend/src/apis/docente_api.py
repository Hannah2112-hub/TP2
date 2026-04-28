from fastapi import APIRouter, HTTPException
from ..schemas import DocenteCreate, DocenteUpdate, GenericResponse
from ..services import DocenteService

router = APIRouter(prefix="/docentes", tags=["Docentes"])


@router.get("", response_model=GenericResponse)
def get_docentes(solo_activos: bool = True):
    data = DocenteService.get_all(solo_activos)
    return {"success": True, "data": data}


@router.post("", response_model=GenericResponse)
def create_docente(docente: DocenteCreate):
    result = DocenteService.create(
        docente.codigo,
        docente.nombre,
        docente.apellido,
        docente.especialidad,
        docente.correo,
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.put("/{docente_id}", response_model=GenericResponse)
def update_docente(docente_id: int, docente: DocenteUpdate):
    result = DocenteService.update(
        docente_id,
        docente.nombre,
        docente.apellido,
        docente.especialidad,
        docente.correo,
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.delete("/{docente_id}", response_model=GenericResponse)
def delete_docente(docente_id: int):
    result = DocenteService.delete(docente_id)
    return result
