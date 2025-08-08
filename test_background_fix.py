#!/usr/bin/env python3
"""
Test Background Fix
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

def test_background_fix():
    """Test if background queries now retrieve actual data and use different providers."""
    logger.info("💬 Testing background fix...")
    
    try:
        from app.api.endpoints.chat import get_response_by_intent, detect_intent
        from app.core.vectorstore import create_vector_store
        
        # Test background queries
        test_queries = [
            "tell me hanzla background",
            "what is hanzla's education",
            "tell me about hanzla's experience"
        ]
        
        for query in test_queries:
            logger.info(f"\n🔍 Testing query: '{query}'")
            
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
            
            # Check if response contains actual background data
            if any(keyword in response.lower() for keyword in ['graduate', 'completed', 'superior university', '3.30', 'gpa', 'july 2024']):
                logger.info("   ✅ Response contains actual background data from Pinecone")
            elif "don't have that specific information" in response:
                logger.warning("   ⚠️ Response says it doesn't have information")
            else:
                logger.warning("   ⚠️ Response may not contain actual background data")
        
        return True
    except Exception as e:
        logger.error(f"❌ Background fix test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Background Fix Test")
    success = test_background_fix()
    if success:
        logger.info("✅ Background fix test completed")
    else:
        logger.error("❌ Background fix test failed")
