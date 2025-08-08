#!/usr/bin/env python3
"""
Add only the new hanzala_courses_summary.txt file to existing Pinecone vectors
"""

import sys
import os
from pathlib import Path
from uuid import uuid4
from typing import List, Dict, Any

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.core.vectorstore import create_vector_store
from loguru import logger

def add_courses_only():
    """Add only the hanzala_courses_summary.txt file to the programs namespace."""
    logger.info("🚀 Adding hanzala_courses_summary.txt to existing vectors")
    logger.info("=" * 60)
    
    try:
        # Initialize text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        # Load only the courses file
        courses_file_path = os.path.join('app', 'data', 'textdata', 'hanzala_courses_summary.txt')
        
        if not os.path.exists(courses_file_path):
            logger.error(f"❌ File not found: {courses_file_path}")
            return False
            
        logger.info(f"📖 Loading file: hanzala_courses_summary.txt")
        
        # Load the document
        loader = TextLoader(courses_file_path, encoding='utf-8')
        docs = loader.load()
        
        # Add metadata
        for doc in docs:
            doc.metadata.update({
                'source': 'hanzala_courses_summary.txt',
                'type': 'text',
                'category': 'programs',
                'content_type': 'courses_summary'
            })
        
        logger.info(f"✅ Loaded {len(docs)} documents from courses file")
        
        # Split into chunks
        all_chunks = []
        for doc in docs:
            chunks = text_splitter.split_documents([doc])
            for chunk in chunks:
                chunk.metadata.update({
                    'namespace': 'programs',
                    'chunk_id': str(uuid4()),
                    'original_source': 'hanzala_courses_summary.txt'
                })
            all_chunks.extend(chunks)
        
        logger.info(f"📝 Created {len(all_chunks)} chunks from courses file")
        
        # Upload to programs namespace only
        logger.info(f"📤 Uploading {len(all_chunks)} chunks to 'programs' namespace")
        
        vector_store = create_vector_store(namespace='programs')
        if vector_store:
            vector_store.add_documents(all_chunks)
            logger.info(f"✅ Successfully uploaded {len(all_chunks)} chunks to 'programs' namespace")
            
            # Get updated stats
            from app.core.vectorstore import get_namespace_stats
            stats = get_namespace_stats()
            if 'programs' in stats:
                logger.info(f"📊 Programs namespace now has {stats['programs']} total vectors")
            
            return True
        else:
            logger.error("❌ Failed to create vector store for programs namespace")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error adding courses file: {str(e)}")
        return False

def main():
    """Main function to add courses file only."""
    success = add_courses_only()
    
    if success:
        logger.info("✅ SUCCESS: Courses file added to existing vectors!")
        logger.info("🎯 The hanzala_courses_summary.txt file is now available in the 'programs' namespace")
        logger.info("💡 You can now ask about Hanzla's courses and certifications!")
    else:
        logger.error("❌ FAILED: Could not add courses file to vectors")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
