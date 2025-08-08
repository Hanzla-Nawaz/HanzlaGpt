import json
import time
import traceback
import os
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.schemas.schema import QueryRequest, QueryResponse, ChatHistoryResponse, HealthCheckResponse, ErrorResponse
from app.core.database import log_chat, get_chat_history
from app.services.enhanced_chat_service import EnhancedChatService, ChatContext, IntentType
from app.core.llm_providers import provider_manager
from app.core.provider_router import provider_router
from app.core.vectorstore import get_namespace_stats
from app.templates.prompts import GREETING_MESSAGE
from loguru import logger

# Initialize enhanced chat service
chat_service = EnhancedChatService()

enhanced_chat_router = APIRouter()

# Metrics tracking
class ChatMetrics:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.average_response_time = 0
        self.response_times = []
    
    def record_request(self, success: bool, response_time: int):
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        
        self.response_times.append(response_time)
        if len(self.response_times) > 100:  # Keep last 100
            self.response_times.pop(0)
        
        self.average_response_time = sum(self.response_times) / len(self.response_times)
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": self.successful_requests / max(self.total_requests, 1),
            "average_response_time_ms": self.average_response_time,
            "cache_stats": chat_service.get_cache_stats()
        }

metrics = ChatMetrics()

async def log_chat_async(chat_context: ChatContext):
    """Log chat interaction asynchronously."""
    try:
        await asyncio.to_thread(
            log_chat,
            user_id=chat_context.user_id,
            session_id=chat_context.session_id,
            query=chat_context.query,
            answer=chat_context.response,
            intent=chat_context.intent.value,
            response_time_ms=chat_context.response_time_ms
        )
    except Exception as e:
        logger.error(f"Failed to log chat: {str(e)}")

@enhanced_chat_router.post("/query", response_model=QueryResponse)
async def enhanced_query_chat(
    request: QueryRequest,
    background_tasks: BackgroundTasks
):
    """Enhanced chat query endpoint with professional features."""
    start_time = time.time()
    
    try:
        # Process chat query using enhanced service
        chat_response = await chat_service.process_chat_query(
            query=request.query,
            user_id=request.user_id,
            session_id=request.session_id,
            use_cache=True
        )
        
        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)
        
        # Record metrics
        success = not bool(chat_response.error)
        metrics.record_request(success, response_time_ms)
        
        # Log chat interaction in background
        chat_context = ChatContext(
            user_id=request.user_id,
            session_id=request.session_id,
            query=request.query,
            intent=chat_response.intent,
            confidence=chat_response.confidence,
            context_chunks=chat_response.sources,
            provider=chat_response.provider,
            response_time_ms=response_time_ms,
            timestamp=datetime.now()
        )
        
        background_tasks.add_task(log_chat_async, chat_context)
        
        # Return enhanced response
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
        logger.error(traceback.format_exc())
        
        # Record failure
        response_time_ms = int((time.time() - start_time) * 1000)
        metrics.record_request(False, response_time_ms)
        
        # Try fallback to next provider
        try:
            if provider_manager.fallback_to_next_provider("chat"):
                # Retry with new provider
                return await enhanced_query_chat(request, background_tasks)
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {str(fallback_error)}")
        
        raise HTTPException(
            status_code=500,
            detail="Internal server error. Please try again later."
        )

@enhanced_chat_router.get("/greeting")
async def get_enhanced_greeting():
    """Get enhanced greeting with provider status."""
    try:
        # Force re-initialization to get accurate provider status
        provider_manager.reinitialize_providers()
        current_provider = provider_manager.current_chat_provider.get_name() if provider_manager.current_chat_provider else "None"
        
        # Check if we're using intent-based fallback
        if not provider_manager.current_chat_provider or not provider_manager.current_chat_provider.is_available():
            current_provider = "Intent-based fallback"
        
        return {
            "message": GREETING_MESSAGE,
            "timestamp": time.time(),
            "provider": current_provider,
            "system_status": "enhanced"
        }
    except Exception as e:
        logger.error(f"Failed to get enhanced greeting: {str(e)}")
        return {
            "message": GREETING_MESSAGE,
            "timestamp": time.time(),
            "provider": "Unknown",
            "system_status": "fallback"
        }

@enhanced_chat_router.get("/history/{user_id}/{session_id}", response_model=ChatHistoryResponse)
async def get_enhanced_chat_history(
    user_id: str, 
    session_id: str, 
    limit: int = 50
):
    """Get enhanced chat history with error handling."""
    try:
        messages = get_chat_history(user_id, session_id, limit)
        if not messages:
            return ChatHistoryResponse(
                messages=[],
                total_count=0,
                session_id=session_id
            )
        return ChatHistoryResponse(
            messages=messages,
            total_count=len(messages),
            session_id=session_id
        )
    except Exception as e:
        logger.error(f"Failed to get enhanced chat history: {str(e)}", exc_info=True)
        return ChatHistoryResponse(
            messages=[{"error": "Failed to retrieve chat history. Please check your database connection."}],
            total_count=0,
            session_id=session_id
        )

@enhanced_chat_router.get("/provider-status")
async def get_enhanced_provider_status():
    """Get enhanced provider status with detailed information."""
    try:
        # Force re-initialization to get current status
        provider_manager.reinitialize_providers()
        provider_status = provider_manager.get_provider_status()
        
        # Get accurate current provider
        current_chat_provider = provider_status.get("chat_provider", "None")
        if current_chat_provider == "None" or not provider_manager.current_chat_provider or not provider_manager.current_chat_provider.is_available():
            current_chat_provider = "Intent-based fallback"
        
        return {
            "current_chat_provider": current_chat_provider,
            "current_embedding_provider": provider_status.get("embedding_provider", "None"),
            "all_providers": provider_status.get("providers", {}),
            "environment_vars": {
                "OPENAI_API_KEY": "Set" if os.getenv('OPENAI_API_KEY') else "Not set",
                "HUGGINGFACEHUB_API_TOKEN": "Set" if os.getenv('HUGGINGFACEHUB_API_TOKEN') else "Not set",
                "GROQ_API_KEY": "Set" if os.getenv('GROQ_API_KEY') else "Not set",
                "TOGETHER_API_KEY": "Set" if os.getenv('TOGETHER_API_KEY') else "Not set",
                "REPLICATE_API_TOKEN": "Set" if os.getenv('REPLICATE_API_TOKEN') else "Not set"
            },
            "timestamp": time.time(),
            "system_status": "enhanced"
        }
    except Exception as e:
        logger.error(f"Failed to get enhanced provider status: {str(e)}")
        return {
            "error": "Failed to get provider status",
            "timestamp": time.time(),
            "system_status": "fallback"
        }

@enhanced_chat_router.post("/provider-reload")
async def reload_enhanced_providers():
    """Manually trigger enhanced provider re-initialization."""
    try:
        provider_manager.reinitialize_providers()
        return {
            "message": "Providers reloaded successfully",
            "timestamp": time.time(),
            "system_status": "enhanced"
        }
    except Exception as e:
        logger.error(f"Failed to reload enhanced providers: {str(e)}")
        return {
            "error": "Failed to reload providers",
            "timestamp": time.time(),
            "system_status": "fallback"
        }

@enhanced_chat_router.get("/provider-stats")
async def get_enhanced_provider_stats():
    """Get enhanced provider usage statistics and distribution."""
    try:
        stats = provider_router.get_provider_stats()
        return {
            "stats": stats,
            "timestamp": time.time(),
            "system_status": "enhanced"
        }
    except Exception as e:
        logger.error(f"Failed to get enhanced provider stats: {str(e)}")
        return {
            "error": "Failed to get provider stats",
            "timestamp": time.time(),
            "system_status": "fallback"
        }

@enhanced_chat_router.post("/force-provider")
async def force_enhanced_provider_for_user(
    user_id: str, 
    provider_name: str, 
    session_id: str = None
):
    """Force a specific provider for a user (for testing)."""
    try:
        provider_router.force_provider_for_user(user_id, provider_name, session_id)
        return {
            "message": f"Forced provider {provider_name} for user {user_id}",
            "timestamp": time.time(),
            "system_status": "enhanced"
        }
    except Exception as e:
        logger.error(f"Failed to force enhanced provider: {str(e)}")
        return {
            "error": "Failed to force provider",
            "timestamp": time.time(),
            "system_status": "fallback"
        }

@enhanced_chat_router.get("/metrics")
async def get_chat_metrics():
    """Get enhanced chat metrics and performance statistics."""
    try:
        return {
            "metrics": metrics.get_stats(),
            "timestamp": time.time(),
            "system_status": "enhanced"
        }
    except Exception as e:
        logger.error(f"Failed to get enhanced metrics: {str(e)}")
        return {
            "error": "Failed to get metrics",
            "timestamp": time.time(),
            "system_status": "fallback"
        }

@enhanced_chat_router.post("/cache/clear")
async def clear_enhanced_cache():
    """Clear the enhanced response cache."""
    try:
        chat_service.clear_cache()
        return {
            "message": "Cache cleared successfully",
            "timestamp": time.time(),
            "system_status": "enhanced"
        }
    except Exception as e:
        logger.error(f"Failed to clear enhanced cache: {str(e)}")
        return {
            "error": "Failed to clear cache",
            "timestamp": time.time(),
            "system_status": "fallback"
        }

@enhanced_chat_router.get("/health", response_model=HealthCheckResponse)
async def enhanced_health_check():
    """Enhanced health check endpoint with detailed component status."""
    try:
        # Get provider status
        provider_status = provider_manager.get_provider_status()
        
        # Check database
        db_healthy = True
        try:
            from app.core.database import get_connection_pool
            pool = get_connection_pool()
            if pool:
                with pool.getconn() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT 1")
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            db_healthy = False
        
        # Check vector store
        vector_healthy = True
        try:
            from app.core.vectorstore import get_namespace_stats
            stats = get_namespace_stats()
            if not stats:
                vector_healthy = False
        except Exception as e:
            logger.error(f"Vector store health check failed: {str(e)}")
            vector_healthy = False
        
        # Check chat service
        chat_healthy = True
        try:
            cache_stats = chat_service.get_cache_stats()
        except Exception as e:
            logger.error(f"Chat service health check failed: {str(e)}")
            chat_healthy = False
        
        # Shape providers status for frontend expectations
        providers = {
            "chat": {
                "active": provider_status.get("chat_provider", "None"),
                "available": [name for name, meta in provider_status.get("providers", {}).items() if meta.get("chat_model")]
            },
            "embeddings": {
                "active": provider_status.get("embedding_provider", "None"),
                "available": [name for name, meta in provider_status.get("providers", {}).items() if meta.get("embeddings")]
            }
        }

        return HealthCheckResponse(
            status="healthy" if (db_healthy and vector_healthy and chat_healthy) else "degraded",
            timestamp=datetime.now(),
            version="2.0.0",
            components={
                "database": "healthy" if db_healthy else "unhealthy",
                "vector_store": "healthy" if vector_healthy else "unhealthy",
                "chat_service": "healthy" if chat_healthy else "unhealthy"
            },
            providers=providers
        )
        
    except Exception as e:
        logger.error(f"Enhanced health check failed: {str(e)}")
        return HealthCheckResponse(
            status="unhealthy",
            timestamp=datetime.now(),
            version="2.0.0",
            components={
                "database": "unknown",
                "vector_store": "unknown",
                "chat_service": "unknown"
            },
            providers={
                "chat": {"active": "None", "available": []},
                "embeddings": {"active": "None", "available": []}
            }
        )

@enhanced_chat_router.get("/system-status")
async def get_system_status():
    """Get comprehensive system status including all components."""
    try:
        # Get various system statuses
        provider_status = provider_manager.get_provider_status()
        vector_stats = get_namespace_stats()
        cache_stats = chat_service.get_cache_stats()
        metrics_stats = metrics.get_stats()
        
        return {
            "system_status": "enhanced",
            "timestamp": time.time(),
            "components": {
                "providers": provider_status,
                "vector_store": {
                    "namespaces": vector_stats,
                    "total_vectors": sum(vector_stats.values()) if vector_stats else 0
                },
                "chat_service": {
                    "cache": cache_stats,
                    "metrics": metrics_stats
                }
            },
            "version": "2.0.0"
        }
    except Exception as e:
        logger.error(f"Failed to get system status: {str(e)}")
        return {
            "system_status": "fallback",
            "timestamp": time.time(),
            "error": str(e),
            "version": "2.0.0"
        }

@enhanced_chat_router.post("/debug/query")
async def debug_query(request: QueryRequest):
    """Debug endpoint for testing query processing step by step."""
    try:
        # Step 1: Intent Detection
        intent_result = await chat_service._detect_intent_async(request.query)
        intent = IntentType(intent_result.get("intent", "unknown"))
        confidence = intent_result.get("confidence", 0.5)
        
        # Step 2: Context Retrieval
        context_chunks = await chat_service._retrieve_context_async(request.query, intent)
        
        # Step 3: Response Generation (simulated)
        response = await chat_service._generate_response_async(
            request.query, intent, context_chunks, request.user_id, request.session_id
        )
        
        return {
            "debug_info": {
                "query": request.query,
                "intent": intent.value,
                "confidence": confidence,
                "context_chunks_count": len(context_chunks),
                "context_chunks": context_chunks[:2],  # First 2 chunks for debugging
                "response_length": len(response),
                "provider": chat_service._get_provider_info(request.user_id, request.session_id)
            },
            "timestamp": time.time(),
            "system_status": "enhanced"
        }
    except Exception as e:
        logger.error(f"Debug query failed: {str(e)}")
        return {
            "error": str(e),
            "timestamp": time.time(),
            "system_status": "fallback"
        }
         