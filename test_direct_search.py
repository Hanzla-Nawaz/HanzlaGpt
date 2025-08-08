#!/usr/bin/env python3
"""
Test Direct Vector Store Search
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

def test_direct_search():
    """Test direct vector store search."""
    logger.info("🔍 Testing direct vector store search...")
    
    try:
        from app.core.vectorstore import create_vector_store
        
        # Create vector store
        vector_store = create_vector_store()
        if not vector_store:
            logger.error("❌ Failed to create vector store")
            return False
        
        logger.info("✅ Vector store created successfully")
        
        # Test different queries
        test_queries = [
            "projects",
            "cybersecurity",
            "AI",
            "machine learning",
            "work experience",
            "education",
            "skills"
        ]
        
        for query in test_queries:
            logger.info(f"\n🔍 Testing query: '{query}'")
            
            try:
                docs = vector_store.similarity_search(query, k=2)
                if docs:
                    logger.info(f"✅ Found {len(docs)} results")
                    for i, doc in enumerate(docs):
                        content = doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
                        logger.info(f"   {i+1}. {content}")
                else:
                    logger.warning("⚠️ No results found")
            except Exception as e:
                logger.error(f"❌ Search failed for '{query}': {str(e)}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Direct search test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Direct Search Test")
    success = test_direct_search()
    if success:
        logger.info("✅ Direct search test passed")
    else:
        logger.error("❌ Direct search test failed")
