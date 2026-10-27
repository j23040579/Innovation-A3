import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.services.weather_query_service import weather_service
from app.services.inference_service import inference_service
from app.api.routes_metadata import router as metadata_router
from app.api.routes_weather import router as weather_router
from app.api.routes_predict import router as predict_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger("app.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    Loads the pre-generated future weather dataset into memory before receiving requests.
    """
    logger.info("Initializing Japan Disaster & Weather Intelligence API...")
    try:
        weather_service.load_dataset()
        logger.info("Weather Query Engine is ready to serve requests.")
    except Exception as e:
        logger.error(f"Failed to load weather dataset on startup: {e}")
        raise e

    # Optional: Try to plug in Backend 2's model registry if it exists
    try:
        from app.services.model_registry import model_registry
        if hasattr(model_registry, "load_all_models"):
            model_registry.load_all_models()
            inference_service.initialize_backend2(model_registry)
    except ImportError:
        logger.info("Backend 2 model registry not present yet. Using Backend 1 mock inference service.")
    except Exception as e:
        logger.warning(f"Backend 2 model registry initialization encountered an issue: {e}")

    yield

    logger.info("Shutting down API server...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="FastAPI Backend for querying pre-generated future weather attributes and serving multi-hazard disaster predictions for Japan.",
    lifespan=lifespan
)

# Configure CORS Middleware for React + Vite Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(metadata_router, prefix=settings.API_PREFIX)
app.include_router(weather_router, prefix=settings.API_PREFIX)
app.include_router(predict_router, prefix=settings.API_PREFIX)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "api_prefix": settings.API_PREFIX,
        "dataset_ready": weather_service.is_loaded
    }

@app.get("/api/health", tags=["Health"])
def health_check():
    min_date, max_date, total_days = weather_service.get_date_range()
    return {
        "status": "healthy",
        "dataset_loaded": weather_service.is_loaded,
        "prefectures_count": len(weather_service.get_prefectures_and_towns()),
        "forecast_period": {
            "start": min_date,
            "end": max_date,
            "total_days": total_days
        }
    }
