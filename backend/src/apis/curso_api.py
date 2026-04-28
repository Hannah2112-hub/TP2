from fastapi import APIRouter, HTTPException
from ..schemas import CursoCreate, CursoUpdate, GenericResponse
from ..services import CursoService

router = APIRouter(prefix="/cursos", tags=["Cursos"])


@router.get("", response_model=GenericResponse)
def get_cursos():
    data = CursoService.get_all()
    return {"success": True, "data": data}


@router.post("", response_model=GenericResponse)
def create_curso(curso: CursoCreate):
    result = CursoService.create(
        curso.codigo,
        curso.nombre,
        curso.creditosReq,
        curso.prerequisitoID,
        curso.docenteID,
        curso.cupos,
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.put("/{curso_id}", response_model=GenericResponse)
def update_curso(curso_id: int, curso: CursoUpdate):
    result = CursoService.update(
        curso_id,
        curso.codigo or "",
        curso.nombre or "",
        curso.creditosReq or 0,
        curso.prerequisitoID,
        curso.docenteID or 0,
        curso.cupos or 30,
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.delete("/{curso_id}", response_model=GenericResponse)
def delete_curso(curso_id: int):
    result = CursoService.delete(curso_id)
    return result
