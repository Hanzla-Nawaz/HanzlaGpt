#!/usr/bin/env python3
"""
Test script to verify courses data retrieval from the programs namespace
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.core.vectorstore import get_category_specific_context, get_namespace_stats
from loguru import logger

def test_courses_retrieval():
    """Test courses data retrieval from programs namespace."""
    logger.info("🧪 Testing Courses Data Retrieval")
    logger.info("=" * 50)
    
    # Test queries related to courses and certifications
    test_queries = [
        "What courses has Hanzla taken?",
        "What certifications does Hanzla have?",
        "Tell me about Hanzla's educational programs",
        "What training programs has Hanzla completed?",
        "What courses and certifications does Hanzla have?",
        "Hanzla's educational background and courses"
    ]
    
    for query in test_queries:
        logger.info(f"\n🔍 Testing query: '{query}'")
        
        try:
            # Test programs namespace specifically
            context = get_category_specific_context(query, 'programs', top_k=2)
            
            if context:
                logger.info(f"✅ Found {len(context)} results from programs namespace:")
                for i, content in enumerate(context[:2]):
                    logger.info(f"   {i+1}. Content: {content[:200]}...")
            else:
                logger.warning("❌ No results found in programs namespace")
                
        except Exception as e:
            logger.error(f"❌ Error testing query '{query}': {str(e)}")
    
    # Test namespace statistics
    logger.info(f"\n📊 Current Namespace Statistics:")
    try:
        stats = get_namespace_stats()
        for namespace, count in stats.items():
            logger.info(f"   {namespace}: {count} vectors")
            
        if 'programs' in stats and stats['programs'] > 0:
            logger.info(f"✅ Programs namespace has {stats['programs']} vectors - courses data is available!")
        else:
            logger.warning("⚠️ Programs namespace has no vectors")
            
    except Exception as e:
        logger.error(f"❌ Error getting namespace stats: {str(e)}")
    
    # Test specific course-related queries
    logger.info(f"\n🎯 Testing Specific Course Queries:")
    specific_queries = [
        "CISSP",
        "ISO 27001",
        "machine learning",
        "cybersecurity",
        "certification",
        "training"
    ]
    
    for query in specific_queries:
        try:
            context = get_category_specific_context(query, 'programs', top_k=1)
            if context:
                logger.info(f"✅ Found content for '{query}': {context[0][:150]}...")
            else:
                logger.warning(f"⚠️ No content found for '{query}'")
        except Exception as e:
            logger.error(f"❌ Error testing '{query}': {str(e)}")

if __name__ == "__main__":
    test_courses_retrieval()
