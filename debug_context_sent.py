#!/usr/bin/env python3
"""
Debug Context Sent to LLM
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

def debug_context_sent():
    """Debug what context is actually being sent to the LLM."""
    logger.info("🔍 Debugging context sent to LLM...")
    
    try:
        from app.core.vectorstore import get_category_specific_context
        
        # Test the exact query from your chat
        query = "tell me hanzla projects"
        logger.info(f"🔍 Testing query: '{query}'")
        
        # Get context from projects namespace
        context = get_category_specific_context(query, 'projects', top_k=3)
        if context:
            logger.info(f"✅ Found {len(context)} results from projects namespace")
            
            # Show the exact context that would be sent to LLM
            full_context = "\n\n".join(context)
            logger.info(f"📝 Full context being sent to LLM:")
            logger.info("=" * 80)
            logger.info(full_context)
            logger.info("=" * 80)
            
            # Check if context contains project information
            if any(keyword in full_context.lower() for keyword in ['melanoma', 'breast', 'diabetes', 'cancer', 'nutrition', 'project']):
                logger.info("✅ Context contains project information")
            else:
                logger.warning("⚠️ Context does not contain project information")
                
        else:
            logger.warning("⚠️ No results found in projects namespace")
        
        return True
    except Exception as e:
        logger.error(f"❌ Context debug failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Context Debug")
    success = debug_context_sent()
    if success:
        logger.info("✅ Context debug completed")
    else:
        logger.error("❌ Context debug failed")
