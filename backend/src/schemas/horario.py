from pydantic import BaseModel, Field
from typing import Optional


class HorarioBase(BaseModel):
    cursoID: int
    aulaID: int
    diaSemana: str = Field(..., max_length=20)
    horaInicio: str = Field(..., max_length=5)
    horaFin: str = Field(..., max_length=5)


class HorarioCreate(HorarioBase):
    pass


class HorarioResponse(HorarioBase):
    id: int
    nombreCurso: Optional[str] = None
    nombreAula: Optional[str] = None

    class Config:
        from_attributes = True
