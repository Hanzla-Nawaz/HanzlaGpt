#!/usr/bin/env python3
"""
Test Chat Retrieval
"""

import os
from loguru import logger

# Configure logging
logger.remove()
logger.add(
    lambda msg: print(msg, end=""),
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="INFO"
)

def test_chat_retrieval():
    """Test if chat is using retrieved data."""
    logger.info("💬 Testing chat retrieval...")
    
    try:
        from app.api.endpoints.chat import get_response_by_intent, detect_intent
        from app.core.vectorstore import create_vector_store
        
        # Test the actual chat function with your queries
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
            logger.info(f"   Response: {response[:500]}...")
            
            # Check if response contains actual data
            if "CyberShield" in response or "GenEval" in response or "Skin Cancer" in response:
                logger.info("   ✅ Response contains actual project data")
            elif "Omdena" in response or "Al Nafi" in response or "BCG X" in response:
                logger.info("   ✅ Response contains actual experience data")
            else:
                logger.warning("   ⚠️ Response may not contain actual data")
        
        return True
    except Exception as e:
        logger.error(f"❌ Chat retrieval test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Chat Retrieval Test")
    success = test_chat_retrieval()
    if success:
        logger.info("✅ Chat retrieval test passed")
    else:
        logger.error("❌ Chat retrieval test failed")
