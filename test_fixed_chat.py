#!/usr/bin/env python3
"""
Test Fixed Chat System
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

def test_fixed_chat():
    """Test if the fixed chat system retrieves actual project data."""
    logger.info("💬 Testing fixed chat system...")
    
    try:
        from app.api.endpoints.chat import get_response_by_intent, detect_intent
        from app.core.vectorstore import create_vector_store
        
        # Test the exact query from your chat
        test_queries = [
            "tell me hanzla projects",
            "what projects have you worked on",
            "tell me about your major projects"
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
            
            # Check if response contains actual project data
            if any(keyword in response.lower() for keyword in ['melanoma', 'breast', 'diabetes', 'cancer', 'nutrition', 'project']):
                logger.info("   ✅ Response contains actual project data from Pinecone")
            elif "don't have that specific information" in response:
                logger.warning("   ⚠️ Response says it doesn't have information")
            else:
                logger.warning("   ⚠️ Response may not contain actual project data")
        
        return True
    except Exception as e:
        logger.error(f"❌ Fixed chat test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Fixed Chat Test")
    success = test_fixed_chat()
    if success:
        logger.info("✅ Fixed chat test completed")
    else:
        logger.error("❌ Fixed chat test failed")
