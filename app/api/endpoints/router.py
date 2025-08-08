from fastapi import APIRouter

api_router = APIRouter()

# Include both original and enhanced chat routers
from app.api.endpoints.chat import chat_router
from app.api.endpoints.enhanced_chat import enhanced_chat_router

api_router.include_router(chat_router, prefix="/chat", tags=["Chat"])
api_router.include_router(enhanced_chat_router, prefix="/enhanced-chat", tags=["Enhanced Chat"])