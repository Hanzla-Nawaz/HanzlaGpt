#!/usr/bin/env python3
"""
Debug Context Content
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

def debug_context_content():
    """Debug what context is being retrieved and why LLM ignores it."""
    logger.info("🔍 Debugging context content...")
    
    try:
        from app.core.vectorstore import get_category_specific_context
        from app.templates.prompts import PERSONAL_PROMPT
        
        # Test queries
        test_queries = [
            "tell me hanzla background",
            "what is hanzla's education",
            "tell me about hanzla's projects"
        ]
        
        for query in test_queries:
            logger.info(f"\n🔍 Testing query: '{query}'")
            
            # Get context from background namespace
            context_chunks = get_category_specific_context(query, 'background', top_k=3)
            
            if context_chunks:
                logger.info(f"✅ Found {len(context_chunks)} context chunks")
                for i, chunk in enumerate(context_chunks):
                    logger.info(f"\n📄 Chunk {i+1} ({len(chunk)} chars):")
                    logger.info(f"   {chunk[:200]}...")
                    
                # Combine context
                combined_context = "\n\n".join(context_chunks)
                logger.info(f"\n📝 Combined context length: {len(combined_context)} characters")
                logger.info(f"📄 First 500 chars: {combined_context[:500]}...")
                
                # Test prompt with context
                logger.info(f"\n🧪 Testing prompt with context...")
                try:
                    # Create a simple test to see what the prompt looks like
                    prompt_text = PERSONAL_PROMPT.format(
                        query=query,
                        context=combined_context
                    )
                    logger.info(f"📄 Prompt length: {len(prompt_text)} characters")
                    logger.info(f"📄 Last 500 chars of prompt: {prompt_text[-500:]}...")
                    
                except Exception as e:
                    logger.error(f"❌ Error testing prompt: {str(e)}")
            else:
                logger.warning(f"⚠️ No context found for query: '{query}'")
        
        return True
    except Exception as e:
        logger.error(f"❌ Debug failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting Context Content Debug")
    success = debug_context_content()
    if success:
        logger.info("✅ Context content debug completed")
    else:
        logger.error("❌ Context content debug failed")
