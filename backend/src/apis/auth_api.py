from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from ..config.database import execute_query

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    email: str
    password: str
    tipo: str

@router.post("/login")
def login(request: LoginRequest):
    if request.tipo == "admin":
        if request.email == "admin@uni.edu" and request.password == "admin123":
            return {"success": True, "data": {"nombre": "Administrador", "tipo": "admin", "id": 0}}
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
    if request.tipo == "docente":
        docentes = execute_query("SELECT * FROM docentes WHERE correo = %s", [request.email])
        if docentes:
            docente = docentes[0]
            return {"success": True, "data": {"nombre": f"{docente['nombre']} {docente['apellido']}", "tipo": "docente", "id": docente["docenteid"]}}
        raise HTTPException(status_code=401, detail="Docente no encontrado")
        
    if request.tipo == "estudiante":
        estudiantes = execute_query("SELECT * FROM estudiantes WHERE correo = %s", [request.email])
        if estudiantes:
            estudiante = estudiantes[0]
            return {"success": True, "data": {"nombre": f"{estudiante['nombre']} {estudiante['apellido']}", "tipo": "estudiante", "id": estudiante["estudianteid"]}}
        raise HTTPException(status_code=401, detail="Estudiante no encontrado")
        
    raise HTTPException(status_code=400, detail="Tipo de usuario inválido")
