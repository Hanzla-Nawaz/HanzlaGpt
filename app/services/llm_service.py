from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from app.core.config import settings

# settings is already imported from app.core.config

def get_openai_model(model_name: str):
    """
    Initialize an OpenAI chat model (e.g., "gpt-4", "gpt-3.5-turbo").
    """
    try:
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0,
            api_key=settings.OPENAI_API_KEY
        )
    except Exception as e:
        raise Exception(f"Failed to initialize OpenAI model: {e}")
    return llm

def get_embedding_model():
    """
    Initialize the OpenAI embedding model.
    """
    try:
        return OpenAIEmbeddings(
            model=settings.OPENAI_API_EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
    except Exception as e:
        raise Exception(f"Failed to initialize OpenAI embeddings: {e}")

def get_chain(prompt_template, llm, parser):
    """
    Build and return an LCEL RAG chain:
        prompt_template | llm | parser
    """
    try:
        return prompt_template | llm | parser
    except Exception as e:
        raise Exception(f"Failed to create RAG chain: {e}")
