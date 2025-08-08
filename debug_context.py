#!/usr/bin/env python3
"""
Debug Context Retrieval
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

def debug_context():
    """Debug what context is being retrieved."""
    logger.info("🔍 Debugging context retrieval...")
    
    try:
        from app.core.vectorstore import search_across_namespaces
        
        # Test query
        query = "tell me the major projects in which hanzla worked"
        logger.info(f"🔍 Testing query: '{query}'")
        
        # Get search results
        results = search_across_namespaces(query, top_k=5)
        
        if results:
            logger.info(f"✅ Found {len(results)} results")
            
            # Show the actual context that would be sent to LLM
            context_parts = []
            for result in results[:3]:
                category = result.get('category', 'unknown')
                content = result['document'].page_content
                context_parts.append(f"[{category.upper()}] {content}")
            
            full_context = "\n\n".join(context_parts)
            logger.info(f"📝 Full context being sent to LLM:")
            logger.info("=" * 60)
            logger.info(full_context)
            logger.info("=" * 60)
            
            # Check if context contains project information
            if "project" in full_context.lower() or "CyberShield" in full_context or "GenEval" in full_context:
                logger.info("✅ Context contains project information")
            else:
                logger.warning("⚠️ Context does not contain project information")
                
        else:
            logger.warning("⚠️ No results found")
        
        return True
    except Exception as e:
        logger.error(f"❌ Context debug failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Context Debug")
    success = debug_context()
    if success:
        logger.info("✅ Context debug completed")
    else:
        logger.error("❌ Context debug failed")
