#!/usr/bin/env python3
"""
HanzlaGPT Vector Loading Script
Loads all personal documents into Pinecone for RAG functionality
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.data.vector_loader import VectorLoader
from loguru import logger
import json

def main():
    """Main function to load vectors."""
    print("🚀 HanzlaGPT Vector Loading Process")
    print("=" * 50)
    
    # Check if required environment variables are set
    required_vars = [
        'OPENAI_API_KEY',
        'PINECONE_API_KEY', 
        'PINECONE_ENV',
        'PINECONE_INDEX',
        'PINECONE_NAMESPACE'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file before running this script.")
        return 1
    
    # Check if data directory exists
    data_dir = Path("app/data")
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        print("Please ensure your documents are in the app/data directory.")
        return 1
    
    print("✅ Environment variables and data directory found")
    print(f"📁 Processing documents from: {data_dir}")
    
    try:
        # Create vector loader
        loader = VectorLoader()
        
        # Process and load documents
        print("\n🔄 Starting document processing...")
        success = loader.process_and_load()
        
        if success:
            # Get and display statistics
            stats = loader.get_processing_stats()
            print("\n📊 Processing Statistics:")
            print(json.dumps(stats, indent=2))
            
            print("\n✅ Vector loading completed successfully!")
            print("🎉 Your HanzlaGPT is now ready with personalized knowledge!")
            print("\nYou can now:")
            print("1. Start the API server: python main.py")
            print("2. Test the frontend: open frontend/index.html")
            print("3. Ask questions about your background, experience, and expertise!")
            
            return 0
        else:
            print("\n❌ Vector loading failed. Please check the logs above.")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error during vector loading: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
