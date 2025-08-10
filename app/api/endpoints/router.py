from fastapi import APIRouter

api_router = APIRouter()

# Include both original and enhanced chat routers
from app.api.endpoints.enhanced_chat import enhanced_chat_router
from app.api.endpoints.auth import auth_router

# Unified chat endpoint (streaming & non-stream)
api_router.include_router(enhanced_chat_router, prefix="/chat", tags=["Chat"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])