import time
from fastapi import APIRouter, BackgroundTasks
from app.schemas.schema import QueryRequest, QueryResponse
from app.services.enhanced_chat_service import EnhancedChatService, add_debug_endpoint
from loguru import logger

chat_service = EnhancedChatService()
enhanced_chat_router = APIRouter()
add_debug_endpoint(enhanced_chat_router, chat_service)

@enhanced_chat_router.post("/query", response_model=QueryResponse)
async def enhanced_query_chat(
    request: QueryRequest,
    background_tasks: BackgroundTasks
):
    """Enhanced chat query endpoint with professional features."""
    start_time = time.time()
    try:
        chat_response = await chat_service.process_chat_query(
            query=request.query,
            user_id=request.user_id,
            session_id=request.session_id,
            use_cache=True
        )
        # If rate limit or error, return JSONResponse directly
        from fastapi.responses import JSONResponse
        if isinstance(chat_response, JSONResponse):
            return chat_response
        response_time_ms = int((time.time() - start_time) * 1000)
        return QueryResponse(
            response=chat_response.response,
            intent=chat_response.intent,
            confidence=chat_response.confidence,
            response_time_ms=response_time_ms,
            sources=chat_response.sources,
            provider=chat_response.provider,
            context_used=chat_response.context_used,
            error=chat_response.error
        )
    except Exception as e:
        logger.error(f"Enhanced chat query failed: {str(e)}")
        raise

@enhanced_chat_router.get("/greeting")
async def get_enhanced_greeting():
    """Get enhanced greeting with provider status."""
    try:
        from app.core.llm_providers import provider_manager
        from app.templates.prompts import GREETING_MESSAGE
        provider_manager.reinitialize_providers()
        current_provider = provider_manager.current_chat_provider.get_name() if provider_manager.current_chat_provider else "None"
        if not provider_manager.current_chat_provider or not provider_manager.current_chat_provider.is_available():
            current_provider = "Intent-based fallback"
        return {
            "message": GREETING_MESSAGE,
            "provider": current_provider,
            "system_status": "enhanced"
        }
    except Exception as e:
        logger.error(f"Failed to get enhanced greeting: {str(e)}")
        return {
            "message": "Welcome to HanzlaGPT!",
            "provider": "Unknown",
            "system_status": "fallback"
        }

@enhanced_chat_router.get("/history")
async def get_chat_history_endpoint(
    user_id: str = "anonymous",
    session_id: str = "default",
    limit: int = 50
):
    """Get chat history for a user and session."""
    try:
        from app.core.database import get_chat_history
        history = get_chat_history(user_id, session_id, limit)
        return {
            "user_id": user_id,
            "session_id": session_id,
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"Failed to get chat history: {str(e)}")
        return {
            "user_id": user_id,
            "session_id": session_id,
            "history": [],
            "count": 0,
            "error": "Failed to retrieve chat history"
        }
         