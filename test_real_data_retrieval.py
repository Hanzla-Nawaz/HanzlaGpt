#!/usr/bin/env python3
"""
Test Real Data Retrieval from Pinecone
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

def test_real_data_retrieval():
    """Test if the system is retrieving your actual data from Pinecone."""
    logger.info("🔍 Testing real data retrieval from Pinecone...")
    
    try:
        from app.core.vectorstore import search_across_namespaces, get_category_specific_context
        
        # Test queries that should retrieve your actual data
        test_queries = [
            "major projects hanzla worked",
            "tell me about his experiences",
            "what projects have you worked on",
            "cybersecurity experience",
            "AI machine learning projects",
            "XEVEN Solutions",
            "Omdena",
            "melanoma cancer prediction",
            "breast cancer project",
            "diabetes project"
        ]
        
        for query in test_queries:
            logger.info(f"\n🔍 Testing query: '{query}'")
            
            # Test cross-namespace search
            results = search_across_namespaces(query, top_k=3)
            if results:
                logger.info(f"✅ Found {len(results)} results")
                for i, result in enumerate(results[:2]):
                    category = result.get('category', 'unknown')
                    content = result['document'].page_content[:200] + "..." if len(result['document'].page_content) > 200 else result['document'].page_content
                    score = result.get('score', 0.0)
                    logger.info(f"   {i+1}. Category: {category} (Score: {score:.3f})")
                    logger.info(f"      Content: {content}")
                    
                    # Check if it contains actual project data
                    if any(keyword in content.lower() for keyword in ['melanoma', 'breast', 'diabetes', 'cancer', 'xeven', 'omdena', 'project']):
                        logger.info("   ✅ Contains actual project/work data")
                    else:
                        logger.warning("   ⚠️ May not contain relevant data")
            else:
                logger.warning("⚠️ No results found")
        
        # Test specific project queries
        logger.info("\n🔍 Testing specific project queries...")
        project_queries = [
            "melanoma cancer prediction",
            "breast cancer project",
            "diabetes project",
            "nutrition project"
        ]
        
        for query in project_queries:
            logger.info(f"\n🔍 Testing project query: '{query}'")
            
            # Search specifically in projects namespace
            context = get_category_specific_context(query, 'projects', top_k=2)
            if context:
                logger.info(f"✅ Found {len(context)} results in projects namespace")
                for i, content in enumerate(context[:2]):
                    logger.info(f"   {i+1}. {content[:200]}...")
                    
                    # Check for specific project keywords
                    if any(keyword in content.lower() for keyword in ['melanoma', 'breast', 'diabetes', 'nutrition', 'cancer']):
                        logger.info("   ✅ Contains specific project data")
                    else:
                        logger.warning("   ⚠️ May not contain specific project data")
            else:
                logger.warning("⚠️ No results found in projects namespace")
        
        return True
    except Exception as e:
        logger.error(f"❌ Real data retrieval test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Real Data Retrieval Test")
    success = test_real_data_retrieval()
    if success:
        logger.info("✅ Real data retrieval test completed")
    else:
        logger.error("❌ Real data retrieval test failed")
