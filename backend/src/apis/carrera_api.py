from fastapi import APIRouter, HTTPException
from ..schemas.carrera import CarreraCreate, CarreraUpdate
from ..schemas.response import GenericResponse
from ..repositories.carrera_repository import CarreraRepository

router = APIRouter(prefix="/carreras", tags=["Carreras"])

@router.get("/", response_model=GenericResponse)
def obtener_carreras():
    data = CarreraRepository.get_all()
    return {"success": True, "data": data}

@router.get("/{carrera_id}", response_model=GenericResponse, responses={404: {"description": "Carrera no encontrada"}})
def obtener_carrera(carrera_id: int):
    carrera = CarreraRepository.get_by_id(carrera_id)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return {"success": True, "data": carrera}

@router.post("/", response_model=GenericResponse)
def registrar_carrera(carrera: CarreraCreate):
    result = CarreraRepository.create(carrera.nombre, carrera.facultad)
    if result.get("Exito"):
        return {"success": True, "message": result.get("Mensaje"), "data": {"id": result.get("ID")}}
    return {"success": False, "message": result.get("Mensaje")}

@router.put("/{carrera_id}", response_model=GenericResponse, responses={400: {"description": "Error al actualizar"}})
def actualizar_carrera(carrera_id: int, carrera: CarreraUpdate):
    if CarreraRepository.update(carrera_id, carrera.nombre, carrera.facultad):
        return {"success": True, "message": "Carrera actualizada"}
    raise HTTPException(status_code=400, detail="Error al actualizar")

@router.delete("/{carrera_id}", response_model=GenericResponse, responses={400: {"description": "Error al eliminar"}})
def eliminar_carrera(carrera_id: int):
    if CarreraRepository.delete(carrera_id):
        return {"success": True, "message": "Carrera eliminada lógicamente"}
    raise HTTPException(status_code=400, detail="Error al eliminar")
