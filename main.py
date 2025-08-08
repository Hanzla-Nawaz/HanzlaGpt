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

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting HanzlaGPT application...")
    try:
        # Initialize database tables
        create_tables()
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down HanzlaGPT application...")

# Create FastAPI app
app = FastAPI(
    title="HanzlaGPT",
    description="Personal AI assistant using FastAPI, LangChain, and Pinecone",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

allowed_origins = ["http://localhost:3000", "http://localhost:3001"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
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
app.include_router(api_router, prefix="/api", tags=["API"])

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint to check if the API is running.
    """
    return {
        "message": "Welcome to HanzlaGPT API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }



if __name__ == "__main__":
    logger.info("Starting HanzlaGPT server...")
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000,
        log_level="info",
        access_log=True
    )
