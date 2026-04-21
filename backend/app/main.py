from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .database import init_indexes
from .routes.auth import router as auth_router
from .routes.predictions import router as predictions_router
from .routes.analytics import router as analytics_router
from .services.model_service import model_service

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_indexes()
    try:
        model_service.load_model()
    except Exception as exc:
        print(f"Model startup warning: {exc}")
    yield


app = FastAPI(title=settings.app_name, version="3.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Sentiment Analysis API", "environment": settings.app_env}


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model_service.is_ready()}


app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(predictions_router, prefix=settings.api_prefix)
app.include_router(analytics_router, prefix=settings.api_prefix)
