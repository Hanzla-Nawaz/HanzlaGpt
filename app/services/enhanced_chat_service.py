"""
Enhanced Chat Service for HanzlaGPT
Professional, comprehensive, robust, and scalable chat implementation
"""

import json
import time
import asyncio
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from loguru import logger
import pickle
from app.core.vectorstore import get_category_specific_context, smart_retrieve
from app.core.llm_providers import provider_manager
from app.core.provider_router import provider_router
from app.templates.enhanced_prompts import (
    ENHANCED_INTENT_ROUTING_PROMPT as INTENT_ROUTING_PROMPT,
    ENHANCED_RAG_PROMPT as RAG_PROMPT,
    ENHANCED_CAREER_PROMPT as CAREER_PROMPT,
    ENHANCED_AI_PROMPT as AI_PROMPT,
    ENHANCED_CYBER_PROMPT as CYBER_PROMPT,
    ENHANCED_PERSONAL_PROMPT as PERSONAL_PROMPT,
    ENHANCED_SYSTEM_PROMPT as SYSTEM_PROMPT
)
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

class IntentType(Enum):
    """Enum for different intent types."""
    CAREER_GUIDANCE = "career_guidance"
    AI_ADVICE = "ai_advice"
    CYBERSECURITY_ADVICE = "cybersecurity_advice"
    PERSONAL_INFO = "personal_info"
    GENERAL_RAG = "general_rag"
    USER_INFO = "user_info"
    USER_LAST_QUESTION = "user_last_question"
    GREETING = "greeting"
    UNKNOWN = "unknown"

@dataclass
class ChatContext:
    """Context for chat interactions."""
    user_id: str
    session_id: str
    query: str
    intent: IntentType
    confidence: float
    context_chunks: List[str]
    provider: str
    response_time_ms: int
    timestamp: datetime
    response: str

@dataclass
class ChatResponse:
    """Structured chat response."""
    response: str
    intent: str
    confidence: float
    response_time_ms: int
    sources: List[str]
    provider: str
    context_used: bool
    error: Optional[str] = None

class EnhancedChatService:
    """Enhanced chat service with professional features.

    Uses a simple in-memory cache for chat responses. The cache key is based on user_id, session_id, and query.
    """
    
    def __init__(self):
        self.max_retries = 3
        self.timeout_seconds = 30
        self.max_context_length = 4000
        self.cache = {}  # Simple in-memory cache
        self.user_query_counts = {}
        self.max_queries_per_user = 3
        # NOTE: For production/distributed deployments, replace this with a persistent store (e.g., Redis) for rate limiting.
    
    def _cache_key(self, user_id: str, session_id: str, query: str) -> str:
        """
        Generate a cache key for a chat response.
        Args:
            user_id: The user's unique identifier.
            session_id: The session identifier.
            query: The user's query string.
        Returns:
            A string key for cache storage.
        """
        return f"chat_cache:{user_id}:{session_id}:{query.lower().strip()}"

    async def process_chat_query(
        self, 
        query: str, 
        user_id: str, 
        session_id: str,
        use_cache: bool = True
    ) -> 'ChatResponse':
        """
        Process a chat query with enhanced error handling and features.
        Checks the in-memory cache for a previous response. If not found, processes the query and stores the result in the cache.
        Args:
            query: User's query.
            user_id: User identifier.
            session_id: Session identifier.
            use_cache: Whether to use response caching.
        Returns:
            ChatResponse with structured response data.
        """
        start_time = time.time()
        try:
            # Use user_id if available, else session_id
            user_key = user_id or session_id or 'anonymous'
            count = self.user_query_counts.get(user_key, 0)
            if count >= self.max_queries_per_user:
                # Return a user-friendly error JSON for frontend display
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Query limit reached",
                        "detail": f"You have reached the maximum of {self.max_queries_per_user} free queries. Please contact the site owner for more access."
                    }
                )
            self.user_query_counts[user_key] = count + 1

            cache_key = self._cache_key(user_id, session_id, query)
            if use_cache and cache_key in self.cache:
                cached_response = self.cache[cache_key]
                logger.info(f"Cache hit for query: {query[:50]}...")
                return cached_response
            # Step 1: Intent Detection
            intent_result = await self._detect_intent_async(query)
            intent = IntentType(intent_result.get("intent", "unknown"))
            confidence = intent_result.get("confidence", 0.5)
            # Step 2: Context Retrieval
            context_chunks = await self._retrieve_context_async(query, intent)
            # Step 3: Response Generation
            response = await self._generate_response_async(
                query, intent, context_chunks, user_id, session_id
            )
            # Step 4: Provider Information
            provider = self._get_provider_info(user_id, session_id)
            logger.info(f"[LLM] Provider used for query '{query}': {provider}")
            # Step 5: Calculate timing
            response_time_ms = int((time.time() - start_time) * 1000)
            # Create response object
            chat_response = ChatResponse(
                response=response,
                intent=intent.value,
                confidence=confidence,
                response_time_ms=response_time_ms,
                sources=self._extract_sources(context_chunks),
                provider=provider,
                context_used=len(context_chunks) > 0
            )
            # Cache the response in memory
            if use_cache:
                self.cache[cache_key] = chat_response
            return chat_response
        except Exception as e:
            logger.error(f"Error processing chat query: {str(e)}")
            return ChatResponse(
                response="I apologize, but I'm experiencing technical difficulties. Please try again in a moment.",
                intent="unknown",
                confidence=0.0,
                response_time_ms=int((time.time() - start_time) * 1000),
                sources=[],
                provider="error",
                context_used=False,
                error=str(e)
            )
    
    async def _detect_intent_async(self, query: str) -> Dict[str, Any]:
        """Detect intent asynchronously with retry logic."""
        for attempt in range(self.max_retries):
            try:
                # Get LLM for intent detection
                llm = self._get_llm_for_user()
                if not llm:
                    return self._fallback_intent_detection(query)
                
                # Create intent chain
                intent_chain = INTENT_ROUTING_PROMPT | llm
                
                # Execute with timeout
                result = await asyncio.wait_for(
                    asyncio.to_thread(intent_chain.invoke, {"query": query}),
                    timeout=self.timeout_seconds
                )
                
                # Parse result
                intent_result = self._parse_intent_result(result)
                logger.info(f"Intent detected: {intent_result.get('intent')} (confidence: {intent_result.get('confidence')})")
                return intent_result
                
            except asyncio.TimeoutError:
                logger.warning(f"Intent detection timeout on attempt {attempt + 1}")
                if attempt == self.max_retries - 1:
                    return self._fallback_intent_detection(query)
            except Exception as e:
                logger.error(f"Intent detection error on attempt {attempt + 1}: {str(e)}")
                if attempt == self.max_retries - 1:
                    return self._fallback_intent_detection(query)
        
        return self._fallback_intent_detection(query)
    
    def _parse_intent_result(self, result) -> Dict[str, Any]:
        """Parse intent detection result with error handling."""
        try:
            if hasattr(result, 'content'):
                content = result.content
            elif isinstance(result, str):
                content = result
            else:
                content = str(result)
            
            # Try to parse as JSON
            try:
                intent_result = json.loads(content)
                return intent_result
            except json.JSONDecodeError:
                # Fallback to keyword-based detection
                return self._fallback_intent_detection(content)
                
        except Exception as e:
            logger.error(f"Error parsing intent result: {str(e)}")
            return self._fallback_intent_detection("")
    
    def _fallback_intent_detection(self, query: str) -> Dict[str, Any]:
        """Fallback intent detection using keyword matching."""
        query_lower = query.lower()
        
        # Define keyword patterns
        patterns = {
            IntentType.CAREER_GUIDANCE: [
                'career', 'job', 'work', 'employment', 'professional', 'resume', 'cv',
                'experience', 'skill', 'development', 'degree', 'university', 'college', 'education'
            ],
            IntentType.AI_ADVICE: [
                'ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning',
                'neural network', 'tensorflow', 'pytorch', 'data science', 'python', 'programming'
            ],
            IntentType.CYBERSECURITY_ADVICE: [
                'cybersecurity', 'security', 'hack', 'vulnerability', 'threat', 'malware',
                'firewall', 'grc', 'compliance', 'certification', 'certificate'
            ],
            IntentType.PERSONAL_INFO: [
                'about', 'background', 'personal', 'myself', 'who are you', 'tell me about',
                'your experience', 'hanzala', 'hanzla', 'journey', 'story', 'github', 'repo'
            ],
            IntentType.GREETING: [
                'hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening'
            ]
        }
        
        # Check patterns
        for intent_type, keywords in patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                return {
                    "intent": intent_type.value,
                    "confidence": 0.8
                }
        
        return {
            "intent": IntentType.GENERAL_RAG.value,
            "confidence": 0.6
        }
    
    async def _retrieve_context_async(self, query: str, intent: IntentType) -> List[str]:
        """Retrieve context asynchronously with namespace optimization."""
        try:
            # Tuned namespace mapping
            namespace_mapping = {
                IntentType.CAREER_GUIDANCE: ['background', 'programs', 'projects'],
                IntentType.AI_ADVICE: ['ai_ml', 'projects', 'background'],
                IntentType.CYBERSECURITY_ADVICE: ['cybersecurity', 'programs', 'background'],
                IntentType.PERSONAL_INFO: ['background', 'personality', 'projects', 'programs'],
                IntentType.GENERAL_RAG: ['projects', 'ai_ml', 'cybersecurity', 'background', 'programs', 'personality']
            }
            logger.info(f"[RAG] Query: '{query}' | Intent: {intent.value} | Target namespaces: {namespace_mapping.get(intent, ['background', 'projects'])}")
            # Use new metadata-aware retriever
            context_chunks = smart_retrieve(query, top_k=8)
            # If still empty, fallback to old per-namespace logic
            if not context_chunks:
                target_namespaces = namespace_mapping.get(intent, ["background", "projects"])
                for ns in target_namespaces:
                    try:
                        logger.info(f"[RAG] Fallback: Querying namespace '{ns}' for query '{query}'")
                        chunks = get_category_specific_context(query, ns, top_k=2)
                        context_chunks.extend(chunks)
                    except Exception:
                        continue
            logger.info(f"[RAG] Context chunks retrieved: {len(context_chunks)}")
            return context_chunks[:8]
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return []
    
    async def _generate_response_async(
        self, 
        query: str, 
        intent: IntentType, 
        context_chunks: List[str], 
        user_id: str, 
        session_id: str
    ) -> str:
        """Generate response asynchronously with intent-specific prompts."""
        try:
            # Get LLM
            llm = self._get_llm_for_user()
            if not llm:
                return self._get_fallback_response(intent, query)
            
            # Select appropriate prompt based on intent
            prompt_mapping = {
                IntentType.CAREER_GUIDANCE: CAREER_PROMPT,
                IntentType.AI_ADVICE: AI_PROMPT,
                IntentType.CYBERSECURITY_ADVICE: CYBER_PROMPT,
                IntentType.PERSONAL_INFO: PERSONAL_PROMPT,
                IntentType.GENERAL_RAG: RAG_PROMPT
            }
            
            prompt = prompt_mapping.get(intent, SYSTEM_PROMPT)
            
            # Prepare context
            context = "\n\n".join(context_chunks) if context_chunks else ""
            
            # Create chain
            chain = prompt | llm
            
            # Execute with timeout
            result = await asyncio.wait_for(
                asyncio.to_thread(chain.invoke, {"query": query, "context": context}),
                timeout=self.timeout_seconds
            )
            
            # Extract response
            if hasattr(result, 'content'):
                response = result.content
            elif isinstance(result, str):
                response = result
            else:
                response = str(result)
            
            logger.info(f"Generated response for intent: {intent.value}")
            return response
            
        except asyncio.TimeoutError:
            logger.error("Response generation timeout")
            return self._get_fallback_response(intent, query)
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return self._get_fallback_response(intent, query)
    
    def _get_fallback_response(self, intent: IntentType, query: str) -> str:
        """Get fallback response when LLM is unavailable."""
        fallback_responses = {
            IntentType.CAREER_GUIDANCE: "I'm Hanzala Nawaz, an AI Engineer and Cybersecurity Analyst. I can help you with career guidance in AI, ML, cybersecurity, and software development. What specific area would you like to discuss?",
            IntentType.AI_ADVICE: "I specialize in AI and Machine Learning. I've worked on projects like CyberShield, GenEval, and Skin Cancer Predictor. What would you like to know about AI or my experience?",
            IntentType.CYBERSECURITY_ADVICE: "I have extensive experience in cybersecurity, including penetration testing, security analysis, and developing security tools. What cybersecurity topic would you like to discuss?",
            IntentType.PERSONAL_INFO: "I'm Hanzala Nawaz, an AI Engineer and Cybersecurity Analyst. I've worked with companies like Omdena, Al Nafi Cloud, BCG X, and PwC on projects like CyberShield, GenEval, and Skin Cancer Predictor. How can I assist you today?",
            IntentType.GREETING: "Hello! I'm Hanzala Nawaz, an AI Engineer and Cybersecurity Analyst. I'm here to help you with your career journey in technology. What would you like to know about AI, cybersecurity, or my experience?",
            IntentType.GENERAL_RAG: "I have knowledge about various topics including AI, cybersecurity, career development, and my personal experience. What specific information are you looking for?"
        }
        
        return fallback_responses.get(intent, "Hello! I'm Hanzala Nawaz, an AI Engineer and Cybersecurity Analyst. I'm here to help you with career guidance, technical questions, or share my experience. What would you like to know?")
    
    def _get_llm_for_user(self) -> Optional[Any]:
        """Get LLM instance for user with provider management."""
        try:
            # Force re-initialization to detect environment changes
            provider_manager.reinitialize_providers()
            
            # Get LLM from provider router
            llm = provider_router.get_chat_model_for_user("default", "default")
            if llm is None:
                # Fallback to default provider
                llm = provider_manager.get_chat_model()
            
            return llm
        except Exception as e:
            logger.error(f"Error getting LLM: {str(e)}")
            return None
    
    def _get_provider_info(self, user_id: str, session_id: str) -> str:
        """Get provider information for response."""
        try:
            provider = provider_router.get_provider_for_user(user_id, session_id)
            return provider if provider else "Intent-based fallback"
        except Exception as e:
            logger.error(f"Error getting provider info: {str(e)}")
            return "Unknown"
    
    def _extract_sources(self, context_chunks: List[str]) -> List[str]:
        """Extract source information from context chunks."""
        sources = []
        for chunk in context_chunks:
            # Extract source from chunk metadata if available
            if hasattr(chunk, 'metadata') and chunk.metadata:
                source = chunk.metadata.get('source', 'Unknown')
                sources.append(source)
            else:
                sources.append("Hanzla's Knowledge Base")
        return sources
    
    def clear_cache(self):
        """
        Clear all chat response cache entries from memory.
        """
        self.cache.clear()
        logger.info("Response cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the in-memory chat response cache.
        Returns:
            A dictionary with cache size.
        """
        size = len(self.cache)
        return {
            "cache_size": size,
            "cache_hits": None,  # Not tracked in in-memory version
            "cache_misses": None
        } 

def add_debug_endpoint(router: APIRouter, chat_service: EnhancedChatService):
    if os.getenv("ENABLE_DEBUG_ENDPOINTS", "false").lower() == "true":
        @router.post("/debug/query-info")
        async def debug_query_info(request: dict):
            query = request.get("query", "")
            intent = await chat_service._detect_intent_async(query)
            intent_type = IntentType(intent.get("intent", "unknown"))
            # Get namespaces
            namespace_mapping = {
                IntentType.CAREER_GUIDANCE: ['background', 'programs'],
                IntentType.AI_ADVICE: ['ai_ml', 'projects'],
                IntentType.CYBERSECURITY_ADVICE: ['cybersecurity', 'programs'],
                IntentType.PERSONAL_INFO: ['background', 'personality', 'projects'],
                IntentType.GENERAL_RAG: ['background', 'projects', 'ai_ml', 'cybersecurity', 'programs', 'personality']
            }
            namespaces = namespace_mapping.get(intent_type, ["background", "projects"])
            provider = chat_service._get_provider_info("web_user", "web_session")
            return {
                "query": query,
                "intent": intent_type.value,
                "namespaces": namespaces,
                "provider": provider
            } 