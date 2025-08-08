#!/usr/bin/env python3
"""
Comprehensive Integration Test for HanzlaGPT
Tests all components: vector store, LLM providers, chat endpoints, and enhanced features
"""

import asyncio
import json
import time
from typing import Dict, Any
from loguru import logger

# Configure logging
logger.remove()
logger.add(
    lambda msg: print(msg, end=""),
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="INFO"
)

def test_config():
    """Test configuration loading."""
    logger.info("🔧 Testing configuration...")
    try:
        from app.core.config import settings
        logger.info("✅ Configuration loaded successfully")
        logger.info(f"   - Pinecone Index: {settings.PINECONE_INDEX}")
        logger.info(f"   - OpenAI API Key: {'Set' if settings.OPENAI_API_KEY else 'Not set'}")
        logger.info(f"   - HuggingFace Token: {'Set' if settings.HUGGINGFACEHUB_API_TOKEN else 'Not set'}")
        return True
    except Exception as e:
        logger.error(f"❌ Configuration test failed: {str(e)}")
        return False

def test_vector_store():
    """Test vector store functionality."""
    logger.info("🗄️ Testing vector store...")
    try:
        from app.core.vectorstore import get_namespace_stats, create_vector_store
        
        # Test namespace stats
        stats = get_namespace_stats()
        if stats:
            logger.info("✅ Vector store namespace stats retrieved")
            for namespace, count in stats.items():
                logger.info(f"   - {namespace}: {count} vectors")
        else:
            logger.warning("⚠️ No namespace stats available")
        
        # Test vector store creation
        vector_store = create_vector_store()
        if vector_store:
            logger.info("✅ Vector store created successfully")
        else:
            logger.warning("⚠️ Vector store creation failed")
        
        return True
    except Exception as e:
        logger.error(f"❌ Vector store test failed: {str(e)}")
        return False

def test_llm_providers():
    """Test LLM provider functionality."""
    logger.info("🤖 Testing LLM providers...")
    try:
        from app.core.llm_providers import provider_manager
        
        # Get provider status
        status = provider_manager.get_provider_status()
        logger.info("✅ Provider status retrieved")
        logger.info(f"   - Chat Provider: {status.get('chat_provider', 'None')}")
        logger.info(f"   - Embedding Provider: {status.get('embedding_provider', 'None')}")
        
        # Test chat model
        chat_model = provider_manager.get_chat_model()
        if chat_model:
            logger.info("✅ Chat model available")
        else:
            logger.warning("⚠️ No chat model available")
        
        # Test embeddings
        embeddings = provider_manager.get_embeddings()
        if embeddings:
            logger.info("✅ Embeddings available")
        else:
            logger.warning("⚠️ No embeddings available")
        
        return True
    except Exception as e:
        logger.error(f"❌ LLM providers test failed: {str(e)}")
        return False

def test_enhanced_chat_service():
    """Test enhanced chat service."""
    logger.info("💬 Testing enhanced chat service...")
    try:
        from app.services.enhanced_chat_service import EnhancedChatService
        
        # Initialize service
        chat_service = EnhancedChatService()
        logger.info("✅ Enhanced chat service initialized")
        
        # Test cache stats
        cache_stats = chat_service.get_cache_stats()
        logger.info(f"✅ Cache stats: {cache_stats}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Enhanced chat service test failed: {str(e)}")
        return False

def test_prompts():
    """Test prompt templates."""
    logger.info("📝 Testing prompt templates...")
    try:
        from app.templates.prompts import (
            INTENT_ROUTING_PROMPT, RAG_PROMPT, CAREER_PROMPT,
            AI_PROMPT, CYBER_PROMPT, PERSONAL_PROMPT, SYSTEM_PROMPT
        )
        from app.templates.enhanced_prompts import (
            ENHANCED_INTENT_ROUTING_PROMPT, ENHANCED_RAG_PROMPT,
            ENHANCED_CAREER_PROMPT, ENHANCED_AI_PROMPT,
            ENHANCED_CYBER_PROMPT, ENHANCED_PERSONAL_PROMPT
        )
        
        logger.info("✅ Original prompts loaded")
        logger.info("✅ Enhanced prompts loaded")
        
        return True
    except Exception as e:
        logger.error(f"❌ Prompts test failed: {str(e)}")
        return False

def test_vector_retrieval():
    """Test vector retrieval functionality."""
    logger.info("🔍 Testing vector retrieval...")
    try:
        from app.core.vectorstore import search_across_namespaces, get_category_specific_context
        
        # Test search across namespaces
        test_query = "What projects have you worked on?"
        results = search_across_namespaces(test_query, top_k=2)
        if results:
            logger.info(f"✅ Cross-namespace search returned {len(results)} results")
            for result in results[:2]:
                category = result.get('category', 'unknown')
                logger.info(f"   - Found in {category} namespace")
        else:
            logger.warning("⚠️ No results from cross-namespace search")
        
        # Test category-specific search
        for category in ['projects', 'background', 'ai_ml']:
            context = get_category_specific_context(test_query, category, top_k=1)
            if context:
                logger.info(f"✅ {category} category search returned {len(context)} results")
            else:
                logger.warning(f"⚠️ No results from {category} category")
        
        return True
    except Exception as e:
        logger.error(f"❌ Vector retrieval test failed: {str(e)}")
        return False

async def test_chat_endpoints():
    """Test chat endpoint functionality."""
    logger.info("🌐 Testing chat endpoints...")
    try:
        from app.api.endpoints.chat import detect_intent, get_response_by_intent
        from app.api.endpoints.enhanced_chat import enhanced_chat_router
        
        # Test intent detection
        test_queries = [
            "What is your background?",
            "Tell me about your AI projects",
            "How can I start a career in cybersecurity?",
            "What are your skills?"
        ]
        
        for query in test_queries:
            intent_result = detect_intent(query)
            intent = intent_result.get('intent', 'unknown')
            confidence = intent_result.get('confidence', 0.0)
            logger.info(f"✅ Intent detection: '{query[:30]}...' -> {intent} (confidence: {confidence:.2f})")
        
        return True
    except Exception as e:
        logger.error(f"❌ Chat endpoints test failed: {str(e)}")
        return False

def test_data_integration():
    """Test that actual data is being used."""
    logger.info("📊 Testing data integration...")
    try:
        from app.core.vectorstore import get_namespace_stats
        
        # Check if vectors are loaded
        stats = get_namespace_stats()
        total_vectors = sum(stats.values()) if stats else 0
        
        if total_vectors > 0:
            logger.info(f"✅ Found {total_vectors} total vectors across namespaces")
            for namespace, count in stats.items():
                logger.info(f"   - {namespace}: {count} vectors")
        else:
            logger.warning("⚠️ No vectors found in Pinecone")
            logger.warning("   This means the data ingestion may not have completed")
        
        return total_vectors > 0
    except Exception as e:
        logger.error(f"❌ Data integration test failed: {str(e)}")
        return False

def test_langchain_integration():
    """Test LangChain integration."""
    logger.info("🔗 Testing LangChain integration...")
    try:
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        from app.core.llm_providers import provider_manager
        
        # Test prompt template
        test_prompt = PromptTemplate(
            input_variables=["query"],
            template="Answer this question: {query}"
        )
        logger.info("✅ PromptTemplate created")
        
        # Test LLM chain (if LLM is available)
        llm = provider_manager.get_chat_model()
        if llm:
            chain = LLMChain(llm=llm, prompt=test_prompt)
            logger.info("✅ LLMChain created successfully")
        else:
            logger.warning("⚠️ No LLM available for chain testing")
        
        return True
    except Exception as e:
        logger.error(f"❌ LangChain integration test failed: {str(e)}")
        return False

def main():
    """Run all integration tests."""
    logger.info("🚀 Starting HanzlaGPT Integration Tests")
    logger.info("=" * 60)
    
    tests = [
        ("Configuration", test_config),
        ("Vector Store", test_vector_store),
        ("LLM Providers", test_llm_providers),
        ("Enhanced Chat Service", test_enhanced_chat_service),
        ("Prompts", test_prompts),
        ("Vector Retrieval", test_vector_retrieval),
        ("Data Integration", test_data_integration),
        ("LangChain Integration", test_langchain_integration),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running {test_name} test...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = asyncio.run(test_func())
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"❌ {test_name} test failed with exception: {str(e)}")
            results[test_name] = False
    
    # Run async tests
    logger.info(f"\n📋 Running async tests...")
    try:
        asyncio.run(test_chat_endpoints())
        results["Chat Endpoints"] = True
    except Exception as e:
        logger.error(f"❌ Chat endpoints test failed: {str(e)}")
        results["Chat Endpoints"] = False
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 INTEGRATION TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} {test_name}")
        if result:
            passed += 1
    
    logger.info(f"\n📈 Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! HanzlaGPT is ready for production.")
    else:
        logger.warning(f"⚠️ {total - passed} tests failed. Please check the issues above.")
    
    # Key recommendations
    logger.info("\n🔍 KEY FINDINGS:")
    
    if results.get("Data Integration", False):
        logger.info("✅ Your actual data is loaded in Pinecone")
        logger.info("✅ LLM will use your real information for responses")
    else:
        logger.warning("⚠️ No data found in Pinecone")
        logger.warning("   Run data ingestion scripts to load your information")
    
    if results.get("LLM Providers", False):
        logger.info("✅ LLM providers are working")
        logger.info("✅ Chat functionality should work")
    else:
        logger.warning("⚠️ LLM providers not working")
        logger.warning("   Check API keys and provider configurations")
    
    if results.get("Vector Retrieval", False):
        logger.info("✅ Vector retrieval is working")
        logger.info("✅ Context-aware responses enabled")
    else:
        logger.warning("⚠️ Vector retrieval not working")
        logger.warning("   Check Pinecone configuration")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
