#!/usr/bin/env python3
"""
Check Raw Vector Data in Pinecone
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

def check_raw_vectors():
    """Check raw vector data in Pinecone."""
    logger.info("🔍 Checking raw vector data in Pinecone...")
    
    try:
        from app.core.config import settings
        import pinecone
        
        # Initialize Pinecone
        pc = pinecone.Pinecone(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENV
        )
        
        index = pc.Index(settings.PINECONE_INDEX)
        
        # Get index stats
        stats = index.describe_index_stats()
        logger.info("✅ Index stats retrieved")
        logger.info(f"   Total vector count: {stats.get('total_vector_count', 0)}")
        
        # Check namespaces
        namespaces = stats.get('namespaces', {})
        logger.info(f"   Namespaces found: {list(namespaces.keys())}")
        
        for namespace, info in namespaces.items():
            vector_count = info.get('vector_count', 0)
            logger.info(f"   - {namespace}: {vector_count} vectors")
        
        # Try to fetch some vectors from each namespace
        for namespace in namespaces.keys():
            logger.info(f"\n🔍 Checking vectors in namespace: '{namespace}'")
            
            try:
                # Fetch a few vectors from this namespace
                fetch_response = index.fetch(ids=["test"], namespace=namespace)
                logger.info(f"   Fetch test completed for '{namespace}'")
                
                # Try to query with a simple vector (all zeros)
                import numpy as np
                test_vector = np.zeros(1536).tolist()  # Assuming 1536 dimensions
                
                query_response = index.query(
                    vector=test_vector,
                    top_k=2,
                    namespace=namespace,
                    include_metadata=True
                )
                
                if query_response.matches:
                    logger.info(f"   ✅ Found {len(query_response.matches)} matches in '{namespace}'")
                    for match in query_response.matches[:1]:
                        logger.info(f"      Score: {match.score}")
                        if hasattr(match, 'metadata') and match.metadata:
                            logger.info(f"      Metadata: {match.metadata}")
                else:
                    logger.warning(f"   ⚠️ No matches found in '{namespace}'")
                    
            except Exception as e:
                logger.error(f"   ❌ Error checking '{namespace}': {str(e)}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Raw vector check failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Raw Vector Check")
    success = check_raw_vectors()
    if success:
        logger.info("✅ Raw vector check completed")
    else:
        logger.error("❌ Raw vector check failed")
