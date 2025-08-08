#!/usr/bin/env python3
"""
Test script to verify enhanced vectors are working correctly
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.core.vectorstore import search_across_namespaces, get_namespace_stats, get_category_specific_context
from loguru import logger

def test_vector_retrieval():
    """Test vector retrieval functionality."""
    logger.info("🧪 Testing Enhanced Vector Retrieval")
    logger.info("=" * 50)
    
    # Test queries for different categories
    test_queries = [
        "What is Hanzla's cybersecurity experience?",
        "Tell me about Hanzla's AI and machine learning background",
        "What projects has Hanzla worked on?",
        "What is Hanzla's educational background?",
        "What certifications does Hanzla have?",
        "Tell me about Hanzla's personality and characteristics"
    ]
    
    for query in test_queries:
        logger.info(f"\n🔍 Testing query: '{query}'")
        
        try:
            # Test cross-namespace search
            results = search_across_namespaces(query, top_k=2)
            
            if results:
                logger.info(f"✅ Found {len(results)} results:")
                for i, result in enumerate(results[:2]):
                    category = result['category']
                    score = result['score']
                    content = result['document'].page_content[:200] + "..."
                    logger.info(f"   {i+1}. [{category}] (score: {score:.3f})")
                    logger.info(f"      Content: {content}")
            else:
                logger.warning("❌ No results found")
                
        except Exception as e:
            logger.error(f"❌ Error testing query '{query}': {str(e)}")
    
    # Test namespace statistics
    logger.info(f"\n📊 Namespace Statistics:")
    try:
        stats = get_namespace_stats()
        for namespace, count in stats.items():
            logger.info(f"   {namespace}: {count} vectors")
    except Exception as e:
        logger.error(f"❌ Error getting namespace stats: {str(e)}")
    
    # Test category-specific context
    logger.info(f"\n🎯 Testing Category-Specific Context:")
    test_categories = ['cybersecurity', 'ai_ml', 'projects', 'background']
    
    for category in test_categories:
        try:
            context = get_category_specific_context("experience", category, top_k=1)
            if context:
                logger.info(f"✅ {category}: Found context")
                logger.info(f"   Content: {context[0][:150]}...")
            else:
                logger.warning(f"⚠️ {category}: No context found")
        except Exception as e:
            logger.error(f"❌ Error testing {category}: {str(e)}")

if __name__ == "__main__":
    test_vector_retrieval()
