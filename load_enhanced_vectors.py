#!/usr/bin/env python3
"""
Enhanced Vector Loading Script for HanzlaGPT
This script loads all detailed data about Hanzla and creates optimized vectors in Pinecone
with proper namespacing for better retrieval during chat.
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.core.enhanced_data_loader import load_enhanced_data_to_vector_store
from loguru import logger

def main():
    """Main function to load enhanced vectors to Pinecone."""
    logger.info("🚀 Starting Enhanced Vector Loading for HanzlaGPT")
    logger.info("=" * 60)
    
    try:
        # Load enhanced data to vector store
        success = load_enhanced_data_to_vector_store()
        
        if success:
            logger.info("✅ SUCCESS: Enhanced vectors loaded to Pinecone!")
            logger.info("📊 Data has been organized into namespaces:")
            logger.info("   - cybersecurity: Security and cybersecurity expertise")
            logger.info("   - ai_ml: AI and machine learning background")
            logger.info("   - projects: Detailed project summaries")
            logger.info("   - background: Personal and academic background")
            logger.info("   - personality: Personal characteristics and traits")
            logger.info("   - programs: Program and certification details")
            logger.info("   - general: Other relevant information")
            logger.info("")
            logger.info("🎯 Your HanzlaGPT will now have much better context and retrieval!")
            
        else:
            logger.error("❌ FAILED: Enhanced vector loading failed!")
            logger.error("Please check your Pinecone configuration and try again.")
            return 1
            
    except Exception as e:
        logger.error(f"❌ ERROR: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
