from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from app.api.endpoints.router import api_router
from app.core.config import settings
import uvicorn
import time
from loguru import logger
import sys
from typing import List
from contextlib import asynccontextmanager
from fastapi import APIRouter

debug_router = APIRouter()

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/hanzlagpt.log",
    rotation="10 MB",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting HanzlaGPT application without DB...")
    yield
    logger.info("Shutting down HanzlaGPT application...")

app = FastAPI(
    title="HanzlaGPT",
    description="Personal AI assistant using FastAPI (No DB)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS setup
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]
allowed_hosts: List[str] = [h.strip() for h in settings.ALLOWED_HOSTS.split(",") if h.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if allowed_hosts and allowed_hosts != ["*"]:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=allowed_hosts
    )

@app.middleware("http")
async def add_process_time_header(request: Request, call_next) -> JSONResponse:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred",
            "timestamp": time.time()
        }
    )

# API routes (may still have DB usage internally)
app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Root"])
async def root() -> dict:
    return {
        "message": "Welcome to HanzlaGPT API (No DB)",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

if __name__ == "__main__":
    logger.info("Starting HanzlaGPT server...")
    uvicorn.run(
        app, 
        host="0.0.0.0",  
        port=int(os.environ.get("PORT", 8000)),
        log_level="info",
        access_log=True
    )
