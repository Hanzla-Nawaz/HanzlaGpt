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
from app.core.vectorstore import create_vector_store, search_across_namespaces, get_category_specific_context
from app.core.llm_providers import provider_manager
from app.core.provider_router import provider_router
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

def get_llm(user_id: str = None, session_id: str = None):
    """Get LLM instance for specific user with automatic provider assignment."""
    global _llm
    
    # Force re-initialization to detect environment changes
    provider_manager.reinitialize_providers()
    
    # If user_id is provided, use provider router
    if user_id:
        _llm = provider_router.get_chat_model_for_user(user_id, session_id)
        if _llm is None:
            # Fallback to default provider
            _llm = provider_manager.get_chat_model()
    else:
        # Use default provider manager
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

def get_chains(user_id: str = None, session_id: str = None):
    """Get LLM chains with fallback."""
    global _chains
    # Always refresh chains to use current LLM provider
    llm = get_llm(user_id, session_id)
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
    
    # Handle basic greetings and introductions
    greeting_keywords = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
    name_keywords = ['what is your name', 'who are you', 'introduce yourself', 'tell me about yourself', 'your name']
    
    if any(keyword in query_lower for keyword in greeting_keywords):
        return {"intent": "personal_info", "confidence": 0.9}
    elif any(keyword in query_lower for keyword in name_keywords):
        return {"intent": "personal_info", "confidence": 0.9}
    
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
        # Use user-specific LLM if user_id is provided
        if user_id:
            chains = get_chains(user_id, session_id)
        else:
            # Create a unique user ID for provider rotation
            import hashlib
            import time
            user_id = f"user_{int(time.time()) % 1000}"
            chains = get_chains(user_id, session_id)
        
        if not chains:
            # No LLM available, use intent-based responses
            return get_intent_based_response(query, intent, user_id, session_id)
        
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
        # Prepare context for RAG with enhanced namespace search
        context = ""
        
        # ALWAYS try to retrieve from Pinecone for any intent that might need context
        if vector_store:
            try:
                logger.info(f"🔍 Attempting Pinecone retrieval for intent: {intent}")
                
                # For background-related queries, prioritize background namespace
                if any(keyword in query.lower() for keyword in ['background', 'education', 'experience', 'degree', 'graduated', 'completed', 'hanzla']):
                    logger.info("🎯 Detected background-related query, prioritizing background namespace")
                    background_context = get_category_specific_context(query, 'background', top_k=3)
                    if background_context:
                        logger.info(f"✅ Found {len(background_context)} results from background namespace")
                        context = "\n\n".join(background_context)
                        logger.info(f"📝 Context length: {len(context)} characters")
                    else:
                        # Fallback to cross-namespace search
                        search_results = search_across_namespaces(query, top_k=5)
                        if search_results:
                            logger.info(f"✅ Found {len(search_results)} results from cross-namespace search")
                            context_parts = []
                            for result in search_results[:3]:  # Top 3 results
                                doc_content = result['document'].page_content
                                category = result['category']
                                context_parts.append(f"[{category.upper()}] {doc_content}")
                            context = "\n\n".join(context_parts)
                            logger.info(f"📝 Context length: {len(context)} characters")
                
                # For project-related queries, prioritize projects namespace
                elif any(keyword in query.lower() for keyword in ['project', 'work', 'developed', 'built', 'created']):
                    logger.info("🎯 Detected project-related query, prioritizing projects namespace")
                    
                    # For generic project queries, try specific project keywords
                    if 'project' in query.lower() and not any(specific in query.lower() for specific in ['melanoma', 'breast', 'diabetes', 'nutrition', 'lung', 'cancer']):
                        logger.info("🔍 Generic project query detected, trying specific project keywords")
                        # Try multiple specific project queries to get comprehensive results
                        project_keywords = [
                            "melanoma cancer prediction",
                            "breast cancer classification", 
                            "diabetes prediction",
                            "nutrition analyzer",
                            "lung cancer classification"
                        ]
                        
                        all_project_context = []
                        for keyword in project_keywords:
                            keyword_context = get_category_specific_context(keyword, 'projects', top_k=1)
                            if keyword_context:
                                all_project_context.extend(keyword_context)
                        
                        if all_project_context:
                            logger.info(f"✅ Found {len(all_project_context)} results from specific project searches")
                            context = "\n\n".join(all_project_context[:3])  # Limit to top 3
                            logger.info(f"📝 Context length: {len(context)} characters")
                        else:
                            # Fallback to original query
                            project_context = get_category_specific_context(query, 'projects', top_k=3)
                            if project_context:
                                logger.info(f"✅ Found {len(project_context)} results from projects namespace")
                                context = "\n\n".join(project_context)
                                logger.info(f"📝 Context length: {len(context)} characters")
                            else:
                                # Fallback to cross-namespace search
                                search_results = search_across_namespaces(query, top_k=5)
                                if search_results:
                                    logger.info(f"✅ Found {len(search_results)} results from cross-namespace search")
                                    context_parts = []
                                    for result in search_results[:3]:  # Top 3 results
                                        doc_content = result['document'].page_content
                                        category = result['category']
                                        context_parts.append(f"[{category.upper()}] {doc_content}")
                                    context = "\n\n".join(context_parts)
                                    logger.info(f"📝 Context length: {len(context)} characters")
                    else:
                        # For specific project queries, use original logic
                        project_context = get_category_specific_context(query, 'projects', top_k=3)
                        if project_context:
                            logger.info(f"✅ Found {len(project_context)} results from projects namespace")
                            context = "\n\n".join(project_context)
                            logger.info(f"📝 Context length: {len(context)} characters")
                        else:
                            # Fallback to cross-namespace search
                            search_results = search_across_namespaces(query, top_k=5)
                            if search_results:
                                logger.info(f"✅ Found {len(search_results)} results from cross-namespace search")
                                context_parts = []
                                for result in search_results[:3]:  # Top 3 results
                                    doc_content = result['document'].page_content
                                    category = result['category']
                                    context_parts.append(f"[{category.upper()}] {doc_content}")
                                context = "\n\n".join(context_parts)
                                logger.info(f"📝 Context length: {len(context)} characters")
                else:
                    # Use enhanced search across namespaces for other queries
                    search_results = search_across_namespaces(query, top_k=5)
                    if search_results:
                        logger.info(f"✅ Found {len(search_results)} results from Pinecone")
                        # Combine context from different namespaces
                        context_parts = []
                        for result in search_results[:3]:  # Top 3 results
                            doc_content = result['document'].page_content
                            category = result['category']
                            context_parts.append(f"[{category.upper()}] {doc_content}")
                        context = "\n\n".join(context_parts)
                        logger.info(f"📝 Context length: {len(context)} characters")
                    else:
                        logger.warning("⚠️ No results from enhanced search, trying direct search")
                        # Fallback to regular search
                        docs = vector_store.similarity_search(query, k=3)
                        if docs:
                            logger.info(f"✅ Direct search found {len(docs)} results")
                            context = "\n\n".join([doc.page_content for doc in docs])
                        else:
                            logger.warning("⚠️ No results from direct search either")
            except Exception as e:
                logger.warning(f"Enhanced vector search failed: {str(e)}")
                # Fallback to regular search
                try:
                    docs = vector_store.similarity_search(query, k=3)
                    if docs:
                        logger.info(f"✅ Fallback search found {len(docs)} results")
                        context = "\n\n".join([doc.page_content for doc in docs])
                except Exception as fallback_e:
                    logger.warning(f"Fallback vector search also failed: {str(fallback_e)}")
        
        # Add category-specific context based on intent if no context found
        if not context and intent in ['career_guidance', 'ai_advice', 'cybersecurity_advice']:
            try:
                category_map = {
                    'career_guidance': 'background',
                    'ai_advice': 'ai_ml',
                    'cybersecurity_advice': 'cybersecurity'
                }
                category = category_map.get(intent)
                if category:
                    logger.info(f"🔍 Trying category-specific search for {category}")
                    category_context = get_category_specific_context(query, category, top_k=2)
                    if category_context:
                        context = "\n\n".join(category_context)
                        logger.info(f"✅ Category-specific search found {len(category_context)} results")
            except Exception as e:
                logger.warning(f"Category-specific context failed: {str(e)}")
        
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
        # Final fallback to intent-based responses
        return get_intent_based_response(query, intent, user_id, session_id)

def get_intent_based_response(query: str, intent: str, user_id=None, session_id=None) -> str:
    """Generate response based on intent when no LLM is available."""
    query_lower = query.lower()
    
    if intent == "user_info":
        return "I understand you're sharing information about yourself. I'm Hanzala Nawaz, an AI Engineer and Cybersecurity Analyst. How can I help you today?"
    
    elif intent == "user_last_question":
        # Get chat history for context
        try:
            history = get_chat_history(user_id or "default", session_id or "default", limit=5)
            if history:
                last_query = history[0].get('query', 'your previous question')
                return f"Your last question was: '{last_query}'. How can I help you further?"
            else:
                return "I don't have access to your previous questions at the moment. How can I help you?"
        except:
            return "I don't have access to your previous questions at the moment. How can I help you?"
    
    elif intent == "career_guidance":
        return "I'm Hanzala Nawaz, an AI Engineer and Cybersecurity Analyst. I can help you with career guidance in AI, ML, cybersecurity, and software development. What specific area would you like to discuss?"
    
    elif intent == "ai_advice":
        return "I specialize in AI and Machine Learning. I've worked on projects like CyberShield, GenEval, and Skin Cancer Predictor. What would you like to know about AI or my experience?"
    
    elif intent == "cybersecurity_advice":
        return "I have extensive experience in cybersecurity, including penetration testing, security analysis, and developing security tools. What cybersecurity topic would you like to discuss?"
    
    elif intent == "personal_info":
        # Handle different types of personal info requests
        if any(word in query_lower for word in ['hi', 'hello', 'hey']):
            return "Hello! I'm Hanzala Nawaz, an AI Engineer and Cybersecurity Analyst. I'm here to help you with your career journey in technology. What would you like to know about AI, cybersecurity, or my experience?"
        elif any(word in query_lower for word in ['name', 'who are you', 'introduce']):
            return "I'm Hanzala Nawaz, an AI Engineer and Cybersecurity Analyst. I've worked with companies like Omdena, Al Nafi Cloud, BCG X, and PwC on projects like CyberShield, GenEval, and Skin Cancer Predictor. I'm passionate about AI, cybersecurity, and helping others grow in tech. How can I assist you today?"
        else:
            return "I'm Hanzala Nawaz, an AI Engineer and Cybersecurity Analyst. I've worked with companies like Omdena, Al Nafi Cloud, BCG X, and PwC. I can share my experience and help guide your career path. What would you like to know?"
    
    elif intent == "general_rag":
        return "I have knowledge about various topics including AI, cybersecurity, career development, and my personal experience. What specific information are you looking for?"
    
    else:
        return "Hello! I'm Hanzala Nawaz, an AI Engineer and Cybersecurity Analyst. I'm here to help you with career guidance, technical questions, or share my experience. What would you like to know?"

@chat_router.post("/query", response_model=QueryResponse)
async def query_chat(request: QueryRequest):
    """Process chat query with fallback support."""
    start_time = time.time()
    log_warning = None
    try:
        # Get LLM and vector store for specific user
        llm = get_llm(request.user_id, request.session_id)
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
        # Get user-specific provider information
        user_provider = provider_router.get_provider_for_user(request.user_id, request.session_id)
        provider_info = f"{user_provider}"
        
        # Check if we're using intent-based fallback (no LLM available)
        if user_provider == "Intent-based fallback":
            provider_info = "Intent-based fallback"
        # Add fallback indicator if using intent-based response
        elif "I have knowledge about various topics" in response or "Hello! I'm Hanzala Nawaz" in response:
            provider_info = f"{user_provider} (Intent-based fallback)"
        
        return QueryResponse(
            response=response if not log_warning else f"{response}\n\n{log_warning}",
            intent=intent,
            confidence=confidence,
            response_time_ms=response_time_ms,
            sources=[],  # TODO: Add source tracking
            provider=provider_info
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
    # Force re-initialization to get accurate provider status
    provider_manager.reinitialize_providers()
    current_provider = provider_manager.current_chat_provider.get_name() if provider_manager.current_chat_provider else "None"
    
    # Check if we're using intent-based fallback
    if not provider_manager.current_chat_provider or not provider_manager.current_chat_provider.is_available():
        current_provider = "Intent-based fallback"
    
    return {
        "message": GREETING_MESSAGE,
        "timestamp": time.time(),
        "provider": current_provider
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

@chat_router.get("/provider-status")
async def get_provider_status():
    """Get current provider status."""
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
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Failed to get provider status: {str(e)}")
        return {
            "error": "Failed to get provider status",
            "timestamp": time.time()
        }

@chat_router.post("/provider-reload")
async def reload_providers():
    """Manually trigger provider re-initialization."""
    try:
        provider_manager.reinitialize_providers()
        return {
            "message": "Providers reloaded successfully",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Failed to reload providers: {str(e)}")
        return {
            "error": "Failed to reload providers",
            "timestamp": time.time()
        }

@chat_router.get("/provider-stats")
async def get_provider_stats():
    """Get provider usage statistics and distribution."""
    try:
        stats = provider_router.get_provider_stats()
        return {
            "stats": stats,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Failed to get provider stats: {str(e)}")
        return {
            "error": "Failed to get provider stats",
            "timestamp": time.time()
        }

@chat_router.post("/force-provider")
async def force_provider_for_user(user_id: str, provider_name: str, session_id: str = None):
    """Force a specific provider for a user (for testing)."""
    try:
        provider_router.force_provider_for_user(user_id, provider_name, session_id)
        return {
            "message": f"Forced provider {provider_name} for user {user_id}",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Failed to force provider: {str(e)}")
        return {
            "error": "Failed to force provider",
            "timestamp": time.time()
        }

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



