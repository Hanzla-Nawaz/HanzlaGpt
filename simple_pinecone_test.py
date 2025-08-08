#!/usr/bin/env python3
"""
Simple Pinecone Test
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

def test_basic_pinecone():
    """Test basic Pinecone functionality."""
    logger.info("🔗 Testing basic Pinecone connection...")
    
    try:
        # Test imports
        from app.core.config import settings
        logger.info("✅ Config loaded")
        logger.info(f"   Pinecone Index: {settings.PINECONE_INDEX}")
        logger.info(f"   Pinecone API Key: {'Set' if settings.PINECONE_API_KEY else 'Not set'}")
        
        # Test vectorstore imports
        from app.core.vectorstore import get_namespace_stats
        logger.info("✅ Vectorstore imports successful")
        
        # Test namespace stats
        stats = get_namespace_stats()
        if stats:
            logger.info("✅ Namespace stats retrieved")
            logger.info(f"   Stats: {stats}")
            total = sum(stats.values())
            logger.info(f"   Total vectors: {total}")
        else:
            logger.warning("⚠️ No namespace stats returned")
        
        return True
    except Exception as e:
        logger.error(f"❌ Basic Pinecone test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Simple Pinecone Test")
    success = test_basic_pinecone()
    if success:
        logger.info("✅ Basic test passed")
    else:
        logger.error("❌ Basic test failed")
