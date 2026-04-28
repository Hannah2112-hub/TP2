from fastapi import APIRouter
from .estudiante_api import router as estudiante_router
from .docente_api import router as docente_router
from .aula_api import router as aula_router
from .curso_api import router as curso_router
from .matricula_api import router as matricula_router
from .horario_api import router as horario_router

router = APIRouter()

router.include_router(estudiante_router)
router.include_router(docente_router)
router.include_router(aula_router)
router.include_router(curso_router)
router.include_router(matricula_router)
router.include_router(horario_router)
