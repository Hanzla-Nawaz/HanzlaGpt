#!/usr/bin/env python3
"""
Debug Projects Content
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

def debug_projects_content():
    """Debug what content is actually in the projects namespace."""
    logger.info("🔍 Debugging projects namespace content...")
    
    try:
        from app.core.vectorstore import get_category_specific_context
        
        # Test with very specific project keywords
        test_queries = [
            "melanoma cancer prediction",
            "breast cancer classification",
            "diabetes prediction",
            "nutrition analyzer",
            "lung cancer",
            "skin cancer"
        ]
        
        for query in test_queries:
            logger.info(f"\n🔍 Testing query: '{query}'")
            
            # Get context from projects namespace
            context = get_category_specific_context(query, 'projects', top_k=2)
            if context:
                logger.info(f"✅ Found {len(context)} results")
                for i, content in enumerate(context):
                    logger.info(f"   {i+1}. {content[:300]}...")
                    
                    # Check for specific project keywords
                    if any(keyword in content.lower() for keyword in ['melanoma', 'breast', 'diabetes', 'nutrition', 'cancer', 'project']):
                        logger.info("   ✅ Contains actual project data")
                    else:
                        logger.warning("   ⚠️ May not contain actual project data")
            else:
                logger.warning("⚠️ No results found")
        
        return True
    except Exception as e:
        logger.error(f"❌ Projects content debug failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Projects Content Debug")
    success = debug_projects_content()
    if success:
        logger.info("✅ Projects content debug completed")
    else:
        logger.error("❌ Projects content debug failed")
