from fastapi import APIRouter

api_router = APIRouter()

from app.api.endpoints.chat import chat_router
api_router.include_router(chat_router, prefix="/chat", tags=["Chat"])