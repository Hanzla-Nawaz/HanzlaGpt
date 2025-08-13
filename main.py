from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from app.api.endpoints.router import api_router
from app.core.config import settings
from app.core.database import create_tables
import uvicorn
import time
from loguru import logger
import sys
from typing import List
from contextlib import asynccontextmanager

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
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - <level>{message}</level>",
    level="DEBUG"
)

# Database lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage database initialization and cleanup."""
    # Startup: Create database tables
    try:
        logger.info("Initializing database...")
        create_tables()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Database initialization failed: {e}")
        logger.warning("App will continue without database functionality")
    
    yield
    
    # Shutdown: Cleanup (if needed)
    logger.info("Shutting down...")

# Create FastAPI app instance with lifespan
app = FastAPI(
    title="HanzlaGPT",
    description="Personal AI assistant using FastAPI, LangChain, and Pinecone",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS middleware
allowed_origins = [h.strip() for h in settings.ALLOWED_ORIGINS.split(",") if h.strip()]
allowed_hosts: List[str] = [h.strip() for h in settings.ALLOWED_HOSTS.split(",") if h.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure TrustedHost middleware (only if specific hosts are set)
if allowed_hosts and allowed_hosts != ["*"]:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=allowed_hosts
    )

# Add process time middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next) -> JSONResponse:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Global exception handler
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

# Include API router
app.include_router(api_router, prefix="/api")

# Root endpoint
@app.get("/", tags=["Root"])
async def root() -> dict:
    return {
        "message": "Welcome to HanzlaGPT API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# API health check endpoint
@app.get("/api/chat/health")
def api_chat_health():
    return {"status": "ok"}

# Main entry point
if __name__ == "__main__":
    logger.info("Starting HanzlaGPT server...")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        access_log=True
    )
