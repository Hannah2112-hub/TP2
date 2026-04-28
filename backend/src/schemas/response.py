from pydantic import BaseModel
from typing import Optional, Any


class DashboardResponse(BaseModel):
    totalEstudiantes: int
    totalDocentes: int
    totalCursos: int
    totalAulas: int
    matriculasAprobadas: int
    matriculasRechazadas: int


class GenericResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
