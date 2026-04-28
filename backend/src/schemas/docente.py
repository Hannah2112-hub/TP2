from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class DocenteBase(BaseModel):
    codigo: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=100)
    apellido: str = Field(..., max_length=100)
    especialidad: str = Field(..., max_length=100)
    correo: Optional[EmailStr] = None


class DocenteCreate(DocenteBase):
    pass


class DocenteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    apellido: Optional[str] = Field(None, max_length=100)
    especialidad: Optional[str] = Field(None, max_length=100)
    correo: Optional[EmailStr] = None


class DocenteResponse(DocenteBase):
    id: int
    activo: bool = True

    class Config:
        from_attributes = True
