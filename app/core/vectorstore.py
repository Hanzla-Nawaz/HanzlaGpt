from typing import Optional
from loguru import logger
from langchain_pinecone import PineconeVectorStore
from app.core.config import settings
from app.core.llm_providers import provider_manager
import pinecone
try:
    # Imported for backward-compatibility with tests that patch this symbol
    from langchain_community.embeddings import OpenAIEmbeddings
except Exception:  # pragma: no cover - optional import
    OpenAIEmbeddings = None  # type: ignore

def create_vector_store() -> Optional[PineconeVectorStore]:
    """Create Pinecone vector store with fallback embeddings."""
    try:
        # Get embeddings from provider manager first
        embeddings = provider_manager.get_embeddings()
        if not embeddings and OpenAIEmbeddings:
            # Fallback to direct OpenAIEmbeddings (legacy/test path)
            logger.warning("Embeddings provider unavailable, falling back to OpenAIEmbeddings")
            embeddings = OpenAIEmbeddings(
                model=settings.OPENAI_API_EMBEDDING_MODEL,
                openai_api_key=settings.OPENAI_API_KEY
            )
        if not embeddings:
            logger.error("No embeddings provider available")
            return None
        
        # Initialize Pinecone
        pc = pinecone.Pinecone(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENV
        )
        
        # Create vector store
        vector_store = PineconeVectorStore(
            index_name=settings.PINECONE_INDEX,
            namespace=settings.PINECONE_NAMESPACE,
            embedding=embeddings,
        )
        
        logger.info("Vector store initialized successfully")
        return vector_store
        
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {str(e)}")
        
        # Try fallback to next embedding provider
        try:
            if provider_manager.fallback_to_next_provider("embeddings"):
                logger.info("Retrying vector store initialization with fallback provider")
                return create_vector_store()
        except Exception as fallback_error:
            logger.error(f"Fallback vector store initialization also failed: {str(fallback_error)}")
        
        return None
    
    
    