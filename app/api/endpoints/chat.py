import json
import time
import traceback
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.schemas.schema import QueryRequest, QueryResponse, ChatHistoryResponse, HealthCheckResponse, ErrorResponse
from app.core.database import log_chat, get_chat_history
from app.core.vectorstore import create_vector_store
from app.core.llm_providers import provider_manager
from app.templates.prompts import (
    INTENT_ROUTING_PROMPT, RAG_PROMPT, CAREER_PROMPT,
    AI_PROMPT, CYBER_PROMPT, PERSONAL_PROMPT, SYSTEM_PROMPT, GREETING_MESSAGE
)
from loguru import logger

chat_router = APIRouter()

# Global variables for singleton pattern
_llm = None
_vector_store = None
_chains = None

def get_llm():
    """Get LLM instance with fallback."""
    global _llm
    # Always get the current provider to allow for fallback
    _llm = provider_manager.get_chat_model()
    if _llm is None:
        logger.error("No LLM provider available")
        raise HTTPException(status_code=503, detail="LLM service unavailable")
    return _llm

def get_vector_store():
    """Get vector store instance."""
    global _vector_store
    if _vector_store is None:
        _vector_store = create_vector_store()
    return _vector_store

def get_chains():
    """Get LLM chains with fallback."""
    global _chains
    # Always refresh chains to use current LLM provider
    llm = get_llm()
    if llm is None:
        raise HTTPException(status_code=503, detail="LLM service unavailable")
    
    _chains = {
        'intent': INTENT_ROUTING_PROMPT | llm,
        'rag': RAG_PROMPT | llm,
        'career': CAREER_PROMPT | llm,
        'ai': AI_PROMPT | llm,
        'cyber': CYBER_PROMPT | llm,
        'personal': PERSONAL_PROMPT | llm,
        'system': SYSTEM_PROMPT | llm
    }
    return _chains

def detect_intent(query: str) -> Dict[str, Any]:
    """Detect intent using LLM with fallback."""
    try:
        chains = get_chains()
        intent_chain = chains.get('intent')
        if intent_chain:
            result = intent_chain.invoke({"query": query})
            try:
                # Handle AIMessage object
                if hasattr(result, 'content'):
                    content = result.content
                    # Try to parse as JSON
                    try:
                        intent_result = json.loads(content)
                    except json.JSONDecodeError:
                        intent_result = fallback_intent_detection(query)
                # Handle string response
                elif isinstance(result, str):
                    intent_result = json.loads(result)
                # Handle dictionary response
                elif isinstance(result, dict):
                    intent_result = result
                else:
                    intent_result = fallback_intent_detection(query)
            except (json.JSONDecodeError, TypeError, AttributeError):
                # Fallback to simple keyword matching
                intent_result = fallback_intent_detection(query)
        else:
            intent_result = fallback_intent_detection(query)
    except Exception as e:
        logger.error(f"Intent detection failed: {str(e)}")
        intent_result = fallback_intent_detection(query)

    # Enhanced: Detect if user is sharing their name
    user_name_phrases = [
        'my name is',
        "i am ",
        "i'm ",
        "this is ",
        "call me "
    ]
    q_lower = query.lower()
    if any(phrase in q_lower for phrase in user_name_phrases):
        return {"intent": "user_info", "confidence": 0.95}
    # Enhanced: Detect if user is asking about their last question
    last_question_phrases = [
        'what was my last question',
        'what did i ask last',
        'my previous question',
        'last thing i asked',
        'previous question'
    ]
    if any(phrase in q_lower for phrase in last_question_phrases):
        return {"intent": "user_last_question", "confidence": 0.95}
    return intent_result

def fallback_intent_detection(query: str) -> Dict[str, Any]:
    """Simple keyword-based intent detection as fallback."""
    query_lower = query.lower()
    
    # Define keywords for each intent - focused on Hanzala's personal information
    career_keywords = ['career', 'job', 'work', 'employment', 'professional', 'resume', 'cv', 'experience', 'skill', 'development', 'bs', 'degree', 'university', 'college', 'education']
    ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 'neural network', 'tensorflow', 'pytorch', 'data science', 'python', 'programming']
    cyber_keywords = ['cybersecurity', 'security', 'hack', 'vulnerability', 'threat', 'malware', 'firewall', 'grc', 'compliance', 'certification', 'certificate']
    personal_keywords = ['about', 'background', 'personal', 'myself', 'who are you', 'tell me about', 'your experience', 'hanzala', 'hanzla', 'journey', 'story', 'github', 'repo', 'repository', 'project']
    
    # Check for keywords
    if any(keyword in query_lower for keyword in career_keywords):
        return {"intent": "career_guidance", "confidence": 0.8}
    elif any(keyword in query_lower for keyword in ai_keywords):
        return {"intent": "ai_advice", "confidence": 0.8}
    elif any(keyword in query_lower for keyword in cyber_keywords):
        return {"intent": "cybersecurity_advice", "confidence": 0.8}
    elif any(keyword in query_lower for keyword in personal_keywords):
        return {"intent": "personal_info", "confidence": 0.8}
    else:
        return {"intent": "general_rag", "confidence": 0.6}

def get_response_by_intent(query: str, intent: str, vector_store=None, user_id=None, session_id=None) -> str:
    """Get response based on intent with fallback."""
    try:
        chains = get_chains()
        # Map intent to chain
        intent_map = {
            'career_guidance': 'career',
            'ai_advice': 'ai',
            'cybersecurity_advice': 'cyber',
            'personal_info': 'personal',
            'general_rag': 'rag'
        }
        # Custom handler for user_info intent
        if intent == 'user_info':
            # Try to extract the user's name
            import re
            match = re.search(r"my name is ([a-zA-Z0-9_\- ]+)", query, re.IGNORECASE)
            if match:
                user_name = match.group(1).strip()
                return f"Nice to meet you, {user_name}! If you have any questions or need help, just let me know."
            # Try other patterns
            match = re.search(r"i am ([a-zA-Z0-9_\- ]+)", query, re.IGNORECASE)
            if match:
                user_name = match.group(1).strip()
                return f"Nice to meet you, {user_name}! If you have any questions or need help, just let me know."
            match = re.search(r"i'm ([a-zA-Z0-9_\- ]+)", query, re.IGNORECASE)
            if match:
                user_name = match.group(1).strip()
                return f"Nice to meet you, {user_name}! If you have any questions or need help, just let me know."
            match = re.search(r"call me ([a-zA-Z0-9_\- ]+)", query, re.IGNORECASE)
            if match:
                user_name = match.group(1).strip()
                return f"Nice to meet you, {user_name}! If you have any questions or need help, just let me know."
            match = re.search(r"this is ([a-zA-Z0-9_\- ]+)", query, re.IGNORECASE)
            if match:
                user_name = match.group(1).strip()
                return f"Nice to meet you, {user_name}! If you have any questions or need help, just let me know."
            # Fallback
            return "Nice to meet you! If you have any questions or need help, just let me know."
        # Custom handler for user_last_question intent
        if intent == 'user_last_question' and user_id and session_id:
            try:
                history = get_chat_history(user_id, session_id, limit=2)
                # The most recent is the current question, so get the second most recent
                if len(history) > 1:
                    last_q = history[1].get('query')
                    if last_q:
                        return f"Your last question was: '{last_q}'"
                return "I couldn't find your previous question in this session."
            except Exception as e:
                logger.error(f"Failed to fetch chat history for last question: {str(e)}")
                return "Sorry, I couldn't retrieve your previous question due to a technical issue."
        # Contradiction/clarification handling
        contradiction_phrases = [
            'you initially told me',
            'earlier you said',
            'before you said',
            'previously you said',
            'now you are telling',
            'contradict',
            'changed your answer',
            'last time you said',
            'first you said',
            'you said before'
        ]
        q_lower = query.lower()
        contradiction_context = ""
        if user_id and session_id and any(phrase in q_lower for phrase in contradiction_phrases):
            try:
                history = get_chat_history(user_id, session_id, limit=2)
                if len(history) > 1:
                    prev_q = history[1].get('query')
                    prev_a = history[1].get('answer')
                    if prev_q and prev_a:
                        contradiction_context = f"Previous user question: {prev_q}\nPrevious assistant answer: {prev_a}\n"
            except Exception as e:
                logger.error(f"Failed to fetch chat history for contradiction context: {str(e)}")
        chain_name = intent_map.get(intent, 'system')
        chain = chains.get(chain_name)
        if not chain:
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."
        # Prepare context for RAG
        context = ""
        if vector_store and intent in ['general_rag', 'personal_info']:
            try:
                # Get relevant documents
                docs = vector_store.similarity_search(query, k=3)
                context = "\n\n".join([doc.page_content for doc in docs])
            except Exception as e:
                logger.warning(f"Vector search failed: {str(e)}")
        # Add contradiction context if present
        if contradiction_context:
            context = f"{contradiction_context}\n{context}" if context else contradiction_context
        # Generate response
        if context:
            response = chain.invoke({"query": query, "context": context})
        else:
            # Always provide context, even if empty, to avoid template errors
            response = chain.invoke({"query": query, "context": ""})
        # Extract content from response
        if hasattr(response, 'content'):
            return response.content
        elif isinstance(response, str):
            return response
        else:
            return str(response)
    except Exception as e:
        logger.error(f"Response generation failed: {str(e)}")
        # Try fallback to system prompt
        try:
            fallback_chains = get_chains()  # Get chains again for fallback
            system_chain = fallback_chains.get('system') if fallback_chains else None
            if system_chain:
                fallback_response = system_chain.invoke({"query": query, "context": ""})
                if hasattr(fallback_response, 'content'):
                    return fallback_response.content
                elif isinstance(fallback_response, str):
                    return fallback_response
                else:
                    return str(fallback_response)
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {str(fallback_error)}")
        return "I apologize, but I'm experiencing technical difficulties. Please try again later."

@chat_router.post("/query", response_model=QueryResponse)
async def query_chat(request: QueryRequest):
    """Process chat query with fallback support."""
    start_time = time.time()
    log_warning = None
    try:
        # Get LLM and vector store
        llm = get_llm()
        vector_store = None
        try:
            vector_store = get_vector_store()
        except Exception as e:
            logger.warning(f"Vector store not available: {str(e)}")
        # Detect intent
        intent_result = detect_intent(request.query)
        intent = intent_result.get("intent", "general_rag")
        confidence = intent_result.get("confidence", 0.5)
        # Get response (pass user_id/session_id for last question intent)
        response = get_response_by_intent(request.query, intent, vector_store, user_id=request.user_id, session_id=request.session_id)
        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)
        # Log the interaction
        try:
            log_chat(
                user_id=request.user_id,
                session_id=request.session_id,
                query=request.query,
                answer=response,
                intent=intent,
                response_time_ms=response_time_ms
            )
        except Exception as e:
            logger.error(f"Failed to log chat: {str(e)}")
            log_warning = "Warning: Your message was not saved to chat history due to a server/database error."
        return QueryResponse(
            response=response if not log_warning else f"{response}\n\n{log_warning}",
            intent=intent,
            confidence=confidence,
            response_time_ms=response_time_ms,
            sources=[],  # TODO: Add source tracking
            provider=provider_manager.current_chat_provider.get_name() if provider_manager.current_chat_provider else None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Query processing failed: {str(e)}")
        logger.error(traceback.format_exc())
        # Try fallback to next provider
        try:
            if provider_manager.fallback_to_next_provider("chat"):
                # Retry with new provider
                return await query_chat(request)
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {str(fallback_error)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error. Please try again later."
        )

@chat_router.get("/greeting")
async def get_greeting():
    """Get the initial greeting message."""
    return {
        "message": GREETING_MESSAGE,
        "timestamp": time.time(),
        "provider": provider_manager.current_chat_provider.get_name() if provider_manager.current_chat_provider else "None"
    }

@chat_router.get("/history/{user_id}/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history_endpoint(
    user_id: str, 
    session_id: str, 
    limit: int = 50
):
    """Get chat history for a user session."""
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
        logger.error(f"Failed to get chat history: {str(e)}", exc_info=True)
        # Return a helpful error message in the response
        return ChatHistoryResponse(
            messages=[{"error": "Failed to retrieve chat history. Please check your database schema or connection."}],
            total_count=0,
            session_id=session_id
        )

@chat_router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint with provider status."""
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
            vector_store = get_vector_store()
            if not vector_store:
                vector_healthy = False
        except Exception as e:
            logger.error(f"Vector store health check failed: {str(e)}")
            vector_healthy = False
        
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
            status="healthy" if (db_healthy and vector_healthy) else "degraded",
            timestamp=datetime.now(),
            version="1.0.0",
            components={
                "database": "healthy" if db_healthy else "unhealthy",
                "vector_store": "healthy" if vector_healthy else "unhealthy"
            },
            providers=providers
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthCheckResponse(
            status="unhealthy",
            timestamp=datetime.now(),
            version="1.0.0",
            components={
                "database": "unknown",
                "vector_store": "unknown"
            },
            providers={
                "chat": {"active": "None", "available": []},
                "embeddings": {"active": "None", "available": []}
            }
        )



