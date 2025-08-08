#!/usr/bin/env python3
"""
Debug Pinecone Retrieval
Test if Pinecone is working and retrieving your actual data
"""

import sys
import os
from loguru import logger

# Configure logging
logger.remove()
logger.add(
    lambda msg: print(msg, end=""),
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="INFO"
)

def test_pinecone_connection():
    """Test basic Pinecone connection."""
    logger.info("🔗 Testing Pinecone connection...")
    try:
        from app.core.vectorstore import get_namespace_stats, create_vector_store
        
        # Test namespace stats
        stats = get_namespace_stats()
        if stats:
            logger.info("✅ Pinecone connection successful")
            logger.info(f"📊 Namespace stats: {stats}")
            total_vectors = sum(stats.values())
            logger.info(f"📈 Total vectors: {total_vectors}")
            return True
        else:
            logger.error("❌ No namespace stats returned")
            return False
    except Exception as e:
        logger.error(f"❌ Pinecone connection failed: {str(e)}")
        return False

def test_vector_search():
    """Test vector search functionality."""
    logger.info("🔍 Testing vector search...")
    try:
        from app.core.vectorstore import search_across_namespaces, get_category_specific_context
        
        # Test query that should retrieve projects
        test_query = "major projects hanzla worked"
        logger.info(f"🔍 Testing query: '{test_query}'")
        
        # Test cross-namespace search
        results = search_across_namespaces(test_query, top_k=5)
        if results:
            logger.info(f"✅ Cross-namespace search returned {len(results)} results")
            for i, result in enumerate(results[:3]):
                category = result.get('category', 'unknown')
                content = result['document'].page_content[:200] + "..." if len(result['document'].page_content) > 200 else result['document'].page_content
                logger.info(f"   {i+1}. Category: {category}")
                logger.info(f"      Content: {content}")
        else:
            logger.warning("⚠️ No results from cross-namespace search")
        
        # Test specific namespace searches
        for namespace in ['projects', 'background', 'ai_ml']:
            logger.info(f"🔍 Testing {namespace} namespace...")
            context = get_category_specific_context(test_query, namespace, top_k=2)
            if context:
                logger.info(f"✅ {namespace} namespace returned {len(context)} results")
                for i, content in enumerate(context[:2]):
                    logger.info(f"   {i+1}. {content[:200]}...")
            else:
                logger.warning(f"⚠️ No results from {namespace} namespace")
        
        return True
    except Exception as e:
        logger.error(f"❌ Vector search failed: {str(e)}")
        return False

def test_direct_vector_store():
    """Test direct vector store operations."""
    logger.info("🗄️ Testing direct vector store...")
    try:
        from app.core.vectorstore import create_vector_store
        
        # Create vector store
        vector_store = create_vector_store()
        if not vector_store:
            logger.error("❌ Failed to create vector store")
            return False
        
        logger.info("✅ Vector store created successfully")
        
        # Test direct similarity search
        test_query = "projects hanzla worked on"
        logger.info(f"🔍 Testing direct search: '{test_query}'")
        
        docs = vector_store.similarity_search(test_query, k=3)
        if docs:
            logger.info(f"✅ Direct search returned {len(docs)} results")
            for i, doc in enumerate(docs):
                content = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                logger.info(f"   {i+1}. {content}")
        else:
            logger.warning("⚠️ No results from direct search")
        
        return True
    except Exception as e:
        logger.error(f"❌ Direct vector store test failed: {str(e)}")
        return False

def test_enhanced_search():
    """Test enhanced search functions."""
    logger.info("🚀 Testing enhanced search...")
    try:
        from app.core.vectorstore import search_across_namespaces, get_category_specific_context
        
        # Test multiple queries
        test_queries = [
            "major projects hanzla worked",
            "tell me about his experiences",
            "what projects have you worked on",
            "cybersecurity projects",
            "AI machine learning projects"
        ]
        
        for query in test_queries:
            logger.info(f"\n🔍 Testing query: '{query}'")
            
            # Test cross-namespace search
            results = search_across_namespaces(query, top_k=3)
            if results:
                logger.info(f"✅ Found {len(results)} results")
                for result in results[:2]:
                    category = result.get('category', 'unknown')
                    content = result['document'].page_content[:150] + "..." if len(result['document'].page_content) > 150 else result['document'].page_content
                    logger.info(f"   - {category}: {content}")
            else:
                logger.warning("⚠️ No results found")
        
        return True
    except Exception as e:
        logger.error(f"❌ Enhanced search test failed: {str(e)}")
        return False

def test_chat_integration():
    """Test the actual chat integration."""
    logger.info("💬 Testing chat integration...")
    try:
        from app.api.endpoints.chat import get_response_by_intent, detect_intent
        from app.core.vectorstore import create_vector_store
        
        # Test the actual chat function
        test_queries = [
            "tell me the major projects in which hanzla worked",
            "tell me about his experiences"
        ]
        
        for query in test_queries:
            logger.info(f"\n🔍 Testing chat query: '{query}'")
            
            # Detect intent
            intent_result = detect_intent(query)
            intent = intent_result.get('intent', 'unknown')
            confidence = intent_result.get('confidence', 0.0)
            logger.info(f"   Intent: {intent} (confidence: {confidence:.2f})")
            
            # Get vector store
            vector_store = create_vector_store()
            
            # Get response
            response = get_response_by_intent(query, intent, vector_store)
            logger.info(f"   Response: {response[:300]}...")
        
        return True
    except Exception as e:
        logger.error(f"❌ Chat integration test failed: {str(e)}")
        return False

def main():
    """Run all Pinecone debug tests."""
    logger.info("🚀 Starting Pinecone Debug Tests")
    logger.info("=" * 60)
    
    tests = [
        ("Pinecone Connection", test_pinecone_connection),
        ("Vector Search", test_vector_search),
        ("Direct Vector Store", test_direct_vector_store),
        ("Enhanced Search", test_enhanced_search),
        ("Chat Integration", test_chat_integration),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running {test_name} test...")
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"❌ {test_name} test failed with exception: {str(e)}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 PINECONE DEBUG SUMMARY")
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
        logger.info("🎉 All Pinecone tests passed!")
    else:
        logger.warning(f"⚠️ {total - passed} tests failed. Check the issues above.")
    
    # Key findings
    logger.info("\n🔍 KEY FINDINGS:")
    
    if results.get("Pinecone Connection", False):
        logger.info("✅ Pinecone connection is working")
    else:
        logger.error("❌ Pinecone connection failed - check API keys and configuration")
    
    if results.get("Vector Search", False):
        logger.info("✅ Vector search is working")
    else:
        logger.error("❌ Vector search failed - check search functions")
    
    if results.get("Chat Integration", False):
        logger.info("✅ Chat integration is working")
    else:
        logger.error("❌ Chat integration failed - check chat endpoint logic")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
