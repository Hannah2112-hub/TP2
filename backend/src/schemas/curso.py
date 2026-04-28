from pydantic import BaseModel, Field
from typing import Optional


class CursoBase(BaseModel):
    codigo: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=150)
    creditosReq: int = 0
    prerequisitoID: Optional[int] = None
    docenteID: int
    cupos: int = 30


class CursoCreate(CursoBase):
    pass


class CursoUpdate(BaseModel):
    codigo: Optional[str] = Field(None, max_length=20)
    nombre: Optional[str] = Field(None, max_length=150)
    creditosReq: Optional[int] = None
    prerequisitoID: Optional[int] = None
    docenteID: Optional[int] = None
    cupos: Optional[int] = None


class CursoResponse(CursoBase):
    id: int
    activo: bool = True
    nombreDocente: Optional[str] = None

    class Config:
        from_attributes = True
