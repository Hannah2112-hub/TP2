from fastapi import APIRouter, HTTPException
from ..schemas import EstudianteCreate, EstudianteUpdate, GenericResponse
from ..services import EstudianteService

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.get("", response_model=GenericResponse)
def get_estudiantes(solo_activos: bool = True):
    data = EstudianteService.get_all(solo_activos)
    return {"success": True, "data": data}


@router.post("", response_model=GenericResponse)
def create_estudiante(estudiante: EstudianteCreate):
    result = EstudianteService.create(
        estudiante.codigo,
        estudiante.nombre,
        estudiante.apellido,
        estudiante.correo,
        estudiante.creditosAcum,
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.put("/{estudiante_id}", response_model=GenericResponse)
def update_estudiante(estudiante_id: int, estudiante: EstudianteUpdate):
    result = EstudianteService.update(
        estudiante_id,
        estudiante.nombre or "",
        estudiante.apellido or "",
        estudiante.correo or "",
        estudiante.creditosAcum or 0,
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.delete("/{estudiante_id}", response_model=GenericResponse)
def delete_estudiante(estudiante_id: int):
    result = EstudianteService.delete(estudiante_id)
    return result
