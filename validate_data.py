#!/usr/bin/env python3
"""
Validate Hanzala's data loading and ensure all information is accessible.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.data.vector_loader import VectorLoader
from app.core.vectorstore import create_vector_store
from loguru import logger

def validate_data():
    """Validate that all of Hanzala's data is properly loaded."""
    
    print("🔍 Validating Hanzala's data...\n")
    
    try:
        # Test vector store access
        print("1. Testing vector store access...")
        vector_store = create_vector_store()
        if vector_store:
            print("   ✅ Vector store accessible")
            
            # Test similarity search
            test_queries = [
                "Machine learning Engineer at xeven solutions"
                "Hanzala education university",
                "Omdena work experience",
                "CyberShield project",
                "certifications",
                
                "skills Python TensorFlow"
            ]
            
            print("\n2. Testing data retrieval...")
            for query in test_queries:
                try:
                    docs = vector_store.similarity_search(query, k=2)
                    if docs:
                        print(f"   ✅ Found data for: {query}")
                        print(f"      Sample: {docs[0].page_content[:100]}...")
                    else:
                        print(f"   ⚠️  No data found for: {query}")
                except Exception as e:
                    print(f"   ❌ Error searching for '{query}': {e}")
        else:
            print("   ❌ Vector store not accessible")
            
        # Test data loader
        print("\n3. Testing data loader...")
        loader = VectorLoader()
        stats = loader.get_processing_stats()
        print(f"   📊 Data Statistics:")
        print(f"      - Documents processed: {stats.get('total_docs', 0)}")
        print(f"      - Text chunks created: {stats.get('total_chunks', 0)}")
        print(f"      - Categories: {stats.get('categories', {})}")
        
        # Test specific data categories
        print("\n4. Testing data categories...")
        categories = stats.get('categories', {})
        expected_categories = ['personal', 'experience', 'resume', 'certificates', 'projects']
        
        for category in expected_categories:
            count = categories.get(category, 0)
            if count > 0:
                print(f"   ✅ {category}: {count} documents")
            else:
                print(f"   ⚠️  {category}: No documents found")
                
        print("\n✅ Data validation complete!")
        
    except Exception as e:
        print(f"❌ Data validation failed: {str(e)}")
        logger.error(f"Data validation failed: {str(e)}")

if __name__ == "__main__":
    validate_data()
