from pydantic import BaseModel, Field
from typing import Optional


class CarreraBase(BaseModel):
    nombre: str = Field(..., max_length=150)
    facultad: str = Field(..., max_length=150)


class CarreraCreate(CarreraBase):
    pass


class CarreraUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    facultad: Optional[str] = Field(None, max_length=150)


class CarreraResponse(CarreraBase):
    id: int
    activo: bool = True

    class Config:
        from_attributes = True
