from pinecone import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from app.core.config import settings
import pinecone


pc = pinecone.Pinecone(
    api_key=settings.PINECONE_API_KEY,
    environment=settings.PINECONE_ENV)

def create_vector_store():
    """
    Create a vector store using Pinecone and OpenAI embeddings.
    """
    embeddings = OpenAIEmbeddings(model=settings.OPENAI_API_EMBEDDING_MODEL)
    
    vector_store = PineconeVectorStore(
        index_name=settings.PINECONE_INDEX,
        namespace=settings.PINECONE_NAMESPACE,
        embedding=embeddings,
    )

    
    