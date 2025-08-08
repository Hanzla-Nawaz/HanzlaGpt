#!/usr/bin/env python3
"""
Test Search Functionality
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

def test_search_functions():
    """Test search functions."""
    logger.info("🔍 Testing search functions...")
    
    try:
        from app.core.vectorstore import search_across_namespaces, get_category_specific_context
        
        # Test query
        test_query = "major projects hanzla worked"
        logger.info(f"🔍 Testing query: '{test_query}'")
        
        # Test cross-namespace search
        results = search_across_namespaces(test_query, top_k=3)
        if results:
            logger.info(f"✅ Cross-namespace search returned {len(results)} results")
            for i, result in enumerate(results[:2]):
                category = result.get('category', 'unknown')
                content = result['document'].page_content[:200] + "..." if len(result['document'].page_content) > 200 else result['document'].page_content
                logger.info(f"   {i+1}. Category: {category}")
                logger.info(f"      Content: {content}")
        else:
            logger.warning("⚠️ No results from cross-namespace search")
        
        # Test specific namespace
        logger.info("🔍 Testing projects namespace...")
        context = get_category_specific_context(test_query, 'projects', top_k=2)
        if context:
            logger.info(f"✅ Projects namespace returned {len(context)} results")
            for i, content in enumerate(context[:2]):
                logger.info(f"   {i+1}. {content[:200]}...")
        else:
            logger.warning("⚠️ No results from projects namespace")
        
        return True
    except Exception as e:
        logger.error(f"❌ Search test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Search Test")
    success = test_search_functions()
    if success:
        logger.info("✅ Search test passed")
    else:
        logger.error("❌ Search test failed")
