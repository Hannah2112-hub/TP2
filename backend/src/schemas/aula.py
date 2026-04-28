from pydantic import BaseModel, Field
from typing import Optional


class AulaBase(BaseModel):
    nombre: str = Field(..., max_length=50)
    capacidad: int
    edificio: str = Field(..., max_length=100)
    equipamiento: Optional[str] = Field(None, max_length=200)


class AulaCreate(AulaBase):
    pass


class AulaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=50)
    capacidad: Optional[int] = None
    edificio: Optional[str] = Field(None, max_length=100)
    equipamiento: Optional[str] = Field(None, max_length=200)


class AulaResponse(AulaBase):
    id: int
    activo: bool = True

    class Config:
        from_attributes = True
