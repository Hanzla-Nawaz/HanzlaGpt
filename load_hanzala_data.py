#!/usr/bin/env python3
"""
Load Hanzala's personal data into the vector store for HanzlaGPT.
This ensures HanzlaGPT responds from actual data, not hallucinations.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.data.vector_loader import VectorLoader
from loguru import logger

def load_hanzala_data():
    """Load Hanzala's personal data into the vector store."""
    
    print("🚀 Loading Hanzala's personal data into HanzlaGPT...")
    print("This ensures HanzlaGPT responds from your actual data, not hallucinations.\n")
    
    try:
        # Initialize the vector loader
        loader = VectorLoader()
        
        # Process and load all documents
        success = loader.process_and_load()
        
        if success:
            stats = loader.get_processing_stats()
            print("✅ Successfully loaded Hanzala's data!")
            print(f"📊 Processing Statistics:")
            print(f"   - Documents processed: {stats.get('total_docs', 0)}")
            print(f"   - Text chunks created: {stats.get('total_chunks', 0)}")
            print(f"   - Categories found: {stats.get('categories', [])}")
            print(f"   - Processing time: {stats.get('processing_time', 0):.2f} seconds")
            
            print("\n🎯 HanzlaGPT now has access to:")
            print("   - Your educational background (BS in AI from Superior University)")
            print("   - Your work experience (Omdena, Al Nafi Cloud, BCG X, PwC)")
            print("   - Your certifications and achievements")
            print("   - Your projects (CyberShield, GenEval, Skin Cancer Predictor, etc.)")
            print("   - Your skills and technical expertise")
            print("   - Your journey and personal story")
            
            print("\n✅ HanzlaGPT will now respond from YOUR actual data!")
            print("❌ No more hallucinations - only real information about YOU!")
            
        else:
            print("❌ Failed to load data. Check the logs for details.")
            
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        logger.error(f"Failed to load Hanzala's data: {str(e)}")

if __name__ == "__main__":
    load_hanzala_data()
