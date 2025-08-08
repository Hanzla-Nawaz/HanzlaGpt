#!/usr/bin/env python3
"""
Test Namespace-Specific Search
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

def test_namespace_search():
    """Test namespace-specific search."""
    logger.info("🔍 Testing namespace-specific search...")
    
    try:
        from app.core.vectorstore import get_namespaced_vector_store
        
        # Test different namespaces
        namespaces = ['projects', 'background', 'ai_ml', 'cybersecurity', 'personality', 'programs']
        
        for namespace in namespaces:
            logger.info(f"\n🔍 Testing namespace: '{namespace}'")
            
            try:
                # Get namespace-specific vector store
                vector_store = get_namespaced_vector_store(namespace)
                if not vector_store:
                    logger.warning(f"⚠️ No vector store for namespace '{namespace}'")
                    continue
                
                logger.info(f"✅ Vector store created for '{namespace}'")
                
                # Test simple search
                docs = vector_store.similarity_search("test", k=1)
                if docs:
                    logger.info(f"✅ Found {len(docs)} results in '{namespace}'")
                    content = docs[0].page_content[:100] + "..." if len(docs[0].page_content) > 100 else docs[0].page_content
                    logger.info(f"   Sample content: {content}")
                else:
                    logger.warning(f"⚠️ No results in '{namespace}'")
                    
            except Exception as e:
                logger.error(f"❌ Error testing '{namespace}': {str(e)}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Namespace search test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Namespace Search Test")
    success = test_namespace_search()
    if success:
        logger.info("✅ Namespace search test passed")
    else:
        logger.error("❌ Namespace search test failed")
