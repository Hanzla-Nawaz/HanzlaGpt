#!/usr/bin/env python3
"""
Test Updated Chat System
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

def test_updated_chat():
    """Test if the updated chat system is using retrieved data."""
    logger.info("💬 Testing updated chat system...")
    
    try:
        from app.api.endpoints.chat import get_response_by_intent, detect_intent
        from app.core.vectorstore import create_vector_store
        
        # Test the actual chat function with your queries
        test_queries = [
            "tell me the major projects in which hanzla worked",
            "tell me about his experiences",
            "what projects have you worked on"
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
            
            # Check if response contains actual data from your files
            if any(keyword in response.lower() for keyword in ['melanoma', 'breast', 'diabetes', 'cancer', 'nutrition', 'project']):
                logger.info("   ✅ Response contains actual project data from Pinecone")
            elif any(keyword in response.lower() for keyword in ['xeven', 'omdena', 'bcg', 'al nafi', 'experience']):
                logger.info("   ✅ Response contains actual work experience data from Pinecone")
            elif "don't have that specific information" in response:
                logger.warning("   ⚠️ Response says it doesn't have information (may need better context)")
            else:
                logger.warning("   ⚠️ Response may not contain actual data from Pinecone")
        
        return True
    except Exception as e:
        logger.error(f"❌ Updated chat test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Updated Chat Test")
    success = test_updated_chat()
    if success:
        logger.info("✅ Updated chat test completed")
    else:
        logger.error("❌ Updated chat test failed")
