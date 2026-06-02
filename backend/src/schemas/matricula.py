from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class MatriculaBase(BaseModel):
    estudianteID: int
    cursoID: int


class MatriculaCreate(MatriculaBase):
    pass


class MatriculaResponse(MatriculaBase):
    id: int
    estado: str
    fechaMatricula: datetime
    nombreEstudiante: Optional[str] = None
    nombreCurso: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
