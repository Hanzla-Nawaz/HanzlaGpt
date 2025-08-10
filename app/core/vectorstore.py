from typing import Optional, List, Dict, Any
# imports
from loguru import logger
from langchain_pinecone import PineconeVectorStore
from app.core.config import settings
from app.core.llm_providers import provider_manager

# Self-query dependencies must be imported before they are used
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.query_constructors.pinecone import PineconeTranslator
from langchain.chains.query_constructor.schema import AttributeInfo

import pinecone

# -------------------- Self-Query Retriever helpers --------------------

# Describe our metadata schema so the LLM can formulate filters.
METADATA_SCHEMA: List[AttributeInfo] = [
    AttributeInfo(
        name="namespace",
        description="Top-level grouping (projects, ai_ml, cybersecurity, background, programs, personality).",
        type="string",
    ),
    AttributeInfo(
        name="content_type",
        description="Sub-type such as project_summary, courses_summary, etc.",
        type="string",
    ),
    AttributeInfo(
        name="original_source",
        description="Original filename of the chunk.",
        type="string",
    ),
]


def get_self_query_retriever(k: int = 8) -> SelfQueryRetriever:
    """Return a Pinecone SelfQueryRetriever that understands our metadata."""
    # Use a cheap LLM just to parse the query into filters. Prefer existing provider.
    from app.core.llm_providers import provider_manager

    llm = provider_manager.get_chat_model_by_name("openai")
    if llm is None:
        # final fallback to avoid crash
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    vector_store = create_vector_store()  # default namespace; SQR overrides

    return SelfQueryRetriever.from_llm(
        llm,
        vector_store,
        document_content_description="Hanzala knowledge chunks",
        metadata_field_info=METADATA_SCHEMA,
        structured_query_translator=PineconeTranslator(),
        search_kwargs={"k": k},
    )


def smart_retrieve(query: str, top_k: int = 8) -> List[str]:
    """Retrieve chunk texts using SelfQueryRetriever with metadata filtering."""
    try:
        retriever = get_self_query_retriever(k=top_k)
        docs = retriever.get_relevant_documents(query)
        return [d.page_content for d in docs]
    except Exception as e:
        logger.error(f"SelfQueryRetriever failed, falling back: {e}")
        # fallback to old cross-namespace search
        results = search_across_namespaces(query, top_k=top_k)
        return [r["document"].page_content for r in results]

try:
    # Imported for backward-compatibility with tests that patch this symbol
    from langchain_community.embeddings import OpenAIEmbeddings
except Exception:  # pragma: no cover - optional import
    OpenAIEmbeddings = None  # type: ignore

def create_vector_store(namespace: Optional[str] = None) -> Optional[PineconeVectorStore]:
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
        
        # Use provided namespace or default
        target_namespace = namespace or settings.PINECONE_NAMESPACE
        
        # Create vector store
        vector_store = PineconeVectorStore(
            index_name=settings.PINECONE_INDEX,
            namespace=target_namespace,
            embedding=embeddings,
        )
        
        logger.info(f"Vector store initialized successfully for namespace: {target_namespace}")
        return vector_store
        
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {str(e)}")
        
        # Try fallback to next embedding provider
        try:
            if provider_manager.fallback_to_next_provider("embeddings"):
                logger.info("Retrying vector store initialization with fallback provider")
                return create_vector_store(namespace)
        except Exception as fallback_error:
            logger.error(f"Fallback vector store initialization also failed: {str(fallback_error)}")
        
        return None

def get_namespaced_vector_store(category: str) -> Optional[PineconeVectorStore]:
    """Get vector store for a specific category/namespace."""
    return create_vector_store(namespace=category)

def search_across_namespaces(query: str, categories: List[str] = None, 
                           top_k: int = 5) -> List[Dict[str, Any]]:
    """Search across multiple namespaces and return combined results."""
    if categories is None:
        # Default categories for comprehensive search
        categories = ['cybersecurity', 'ai_ml', 'projects', 'background', 
                     'personality', 'programs', 'general']
    
    all_results = []
    
    # Get embeddings for the query
    try:
        from app.core.llm_providers import provider_manager
        embeddings = provider_manager.get_embeddings()
        if not embeddings:
            logger.error("No embeddings available for search")
            return all_results
        
        # Generate query embedding
        query_embedding = embeddings.embed_query(query)
        
        # Use raw Pinecone query instead of LangChain similarity_search
        import pinecone
        pc = pinecone.Pinecone(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENV
        )
        index = pc.Index(settings.PINECONE_INDEX)
        
        for category in categories:
            try:
                # Query the specific namespace
                query_response = index.query(
                    vector=query_embedding,
                    top_k=top_k,
                    namespace=category,
                    include_metadata=True
                )
                
                if query_response.matches:
                    for match in query_response.matches:
                        # Create a document-like object for compatibility
                        from langchain.schema import Document
                        doc = Document(
                            page_content=match.metadata.get('text', ''),
                            metadata=match.metadata
                        )
                        
                        all_results.append({
                            'document': doc,
                            'score': match.score,
                            'category': category,
                            'namespace': category
                        })
                        
            except Exception as e:
                logger.error(f"Error searching namespace '{category}': {str(e)}")
                continue
        
        # Sort by score (highest first) and then by category priority
        category_priority = {'projects': 0, 'background': 1, 'cybersecurity': 2, 'ai_ml': 3, 'personality': 4, 'programs': 5, 'general': 6}
        all_results.sort(key=lambda x: (-x['score'], category_priority.get(x['category'], 999)))
        
    except Exception as e:
        logger.error(f"Error in search_across_namespaces: {str(e)}")
    
    return all_results

def get_category_specific_context(query: str, category: str, top_k: int = 3) -> List[str]:
    """Get context from a specific category."""
    try:
        # Get embeddings for the query
        from app.core.llm_providers import provider_manager
        embeddings = provider_manager.get_embeddings()
        if not embeddings:
            logger.error("No embeddings available for search")
            return []
        
        # Generate query embedding
        query_embedding = embeddings.embed_query(query)
        
        # Use raw Pinecone query instead of LangChain similarity_search
        import pinecone
        pc = pinecone.Pinecone(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENV
        )
        index = pc.Index(settings.PINECONE_INDEX)
        
        # Query the specific namespace
        query_response = index.query(
            vector=query_embedding,
            top_k=top_k,
            namespace=category,
            include_metadata=True
        )
        
        if query_response.matches:
            return [match.metadata.get('text', '') for match in query_response.matches]
        else:
            logger.warning(f"No results found in category '{category}' for query '{query}'")
            
    except Exception as e:
        logger.error(f"Error getting context from category '{category}': {str(e)}")
    
    return []

def clear_namespace(namespace: str) -> bool:
    """Clear all vectors from a specific namespace."""
    try:
        pc = pinecone.Pinecone(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENV
        )
        
        index = pc.Index(settings.PINECONE_INDEX)
        index.delete(namespace=namespace, delete_all=True)
        
        logger.info(f"Successfully cleared namespace: {namespace}")
        return True
        
    except Exception as e:
        logger.error(f"Error clearing namespace '{namespace}': {str(e)}")
        return False

def get_namespace_stats() -> Dict[str, int]:
    """Get statistics about vectors in each namespace."""
    try:
        pc = pinecone.Pinecone(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENV
        )
        
        index = pc.Index(settings.PINECONE_INDEX)
        stats = index.describe_index_stats()
        
        namespace_counts = stats.get('namespaces', {})
        return {ns: count['vector_count'] for ns, count in namespace_counts.items()}
        
    except Exception as e:
        logger.error(f"Error getting namespace stats: {str(e)}")
        return {}
    
    
    