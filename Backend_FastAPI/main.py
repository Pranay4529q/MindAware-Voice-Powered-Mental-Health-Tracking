import torch
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from core.config import get_settings
from services.ml_service import MLService
from api.routes import audio, auth, profile

# Logger
logger = logging.getLogger("uvicorn.error")

# Load environment variables
load_dotenv()

# Global ML service instance
ml_service: MLService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global ml_service

    settings = get_settings()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    try:
        ml_service = MLService(settings.model_path, device)
        await ml_service.load_model()
        logger.info(f"✅ Model loaded successfully on {device}")
    except Exception as e:
        logger.error("❌ Failed to load model", exc_info=True)
        raise

    yield

    # Shutdown
    logger.info("🔄 Shutting down...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""

    settings = get_settings()

    app = FastAPI(
        title="Mental Health Analysis API",
        description="API for depression level analysis from audio recordings",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://mentalhealth-pkam.onrender.com",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(audio.router, prefix="/api", tags=["audio API's"])
    app.include_router(auth.router, prefix="/api", tags=["auth API's"])
    app.include_router(profile.router, prefix="/api", tags=["profile API's"])

    return app


app = create_app()


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={"error": "Not found"})


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    return JSONResponse(status_code=500, content={"error": "Internal server error"})

@app.get("/")
async def root():
    return {"message": "Mental Health Analysis API", "status": "running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global ml_service
    return {
        "status": "healthy",
        "model_loaded": ml_service is not None and ml_service.model is not None,
    }
