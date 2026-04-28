from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class EstudianteBase(BaseModel):
    codigo: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=100)
    apellido: str = Field(..., max_length=100)
    correo: EmailStr
    creditosAcum: int = 0


class EstudianteCreate(EstudianteBase):
    pass


class EstudianteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    apellido: Optional[str] = Field(None, max_length=100)
    correo: Optional[EmailStr] = None
    creditosAcum: Optional[int] = None


class EstudianteResponse(EstudianteBase):
    id: int
    activo: bool = True
    fechaCreacion: Optional[datetime] = None

    class Config:
        from_attributes = True
