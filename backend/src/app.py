from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from dotenv import load_dotenv
from src.apis import router as api_router
from src.apis.sustainability import router as sustainability_router
from src.config.middleware import SustainabilityMiddleware
from src.repositories.metrics_repository import MetricsRepository
from src.repositories.carrera_repository import CarreraRepository
from contextlib import asynccontextmanager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        MetricsRepository.setup_table()
        MetricsRepository.reset_metrics()
        CarreraRepository.setup_table()
        print("Metricas ambientales y tablas de dominio inicializadas correctamente.")
    except Exception as e:
        print(f"Error inicializando tablas: {e}")
    yield

app = FastAPI(
    title="Sistema de Gestión Académica",
    description="API REST para la gestión académica de la Universidad Continental",
    version="1.0.0",
    lifespan=lifespan
)

# Compresión GZIP: Reduce significativamente el tamaño de transferencia y por ende, las emisiones de CO2
app.add_middleware(GZipMiddleware, minimum_size=500)

# Adicionar Sustainability Middleware
app.add_middleware(SustainabilityMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Rutas de Sostenibilidad (públicas)
app.include_router(sustainability_router)

# Resto de rutas de la API
app.include_router(api_router, prefix="/api")
@app.get("/")
def root():
    return {"message": "Sistema de Gestión Académica - API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
