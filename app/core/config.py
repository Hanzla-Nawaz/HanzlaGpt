from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load .env file if it exists
if os.path.exists('.env'):
    load_dotenv(override=True)
    # Force reload environment variables
    import os
    os.environ.update({k: v for k, v in os.environ.items() if k.startswith('HUGGINGFACE') or k.startswith('OPENAI')})
    print(f"✅ Loaded .env file with {len([k for k in os.environ.keys() if k.startswith('HUGGINGFACE') or k.startswith('OPENAI')])} AI-related environment variables")
    print(f"✅ HUGGINGFACEHUB_API_TOKEN: {'Set' if os.getenv('HUGGINGFACEHUB_API_TOKEN') else 'Not set'}")
    print(f"✅ OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
else:
    print("⚠️ No .env file found")


class Settings(BaseSettings):
    """
    This Settings class is designed to load and manage environment variables for an
    application using Pydantic's BaseSettings and python-dotenv

    write all your env variables here so you can access them easily.

    """


    OPENAI_API_KEY:str = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_MODEL_NAME:str = os.environ.get("OPENAI_MODEL_NAME", "")
    PINECONE_API_KEY : str = os.environ.get("PINECONE_API_KEY", "")
    PINECONE_ENV : str = os.environ.get("PINECONE_ENV", "")
    PINECONE_INDEX : str = os.environ.get("PINECONE_INDEX", "")
    PINECONE_NAMESPACE : str = os.environ.get("PINECONE_NAMESPACE", "")
    HUGGINGFACEHUB_API_TOKEN : str = os.environ.get("HUGGINGFACEHUB_API_TOKEN", "")
    OPENAI_API_EMBEDDING_MODEL: str = os.getenv("OPENAI_API_EMBEDDING_MODEL") or os.getenv("OPENAI_API_Embedding_MODEL", "text-embedding-3-small")
    
    # Free AI Providers
    GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.environ.get("GROQ_MODEL", "llama3-8b-8192")
    TOGETHER_API_KEY: str = os.environ.get("TOGETHER_API_KEY", "")
    TOGETHER_MODEL: str = os.environ.get("TOGETHER_MODEL", "meta-llama/Llama-2-7b-chat-hf")
    REPLICATE_API_TOKEN: str = os.environ.get("REPLICATE_API_TOKEN", "")
    REPLICATE_MODEL: str = os.environ.get("REPLICATE_MODEL", "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3")

    # CORS / security
    ALLOWED_ORIGINS: str = '*'
    ALLOWED_HOSTS: str = os.getenv("ALLOWED_HOSTS", "*")
    
    PG_HOST : str = os.environ.get("PG_HOST", "")
    PG_PORT : str = os.environ.get("PG_PORT", "")
    PG_USER : str = os.environ.get("PG_USER", "")
    PG_PASSWORD : str = os.environ.get("PG_PASSWORD", "")
    PG_DATABASE : str = os.environ.get("PG_DATABASE", "")
    PG_SSLMODE: str = os.getenv("PG_SSLMODE", "prefer")
    
    LINKEDIN_PROFILE: str = os.getenv("LINKEDIN_PROFILE") or ""
    GITHUB_PROFILE: str = os.getenv("GITHUB_PROFILE") or ""
    MEDIUM_PROFILE: str = os.getenv("MEDIUM_PROFILE") or ""
    KAGGLE_PROFILE: str = os.getenv("KAGGLE_PROFILE") or ""
    TWITTER_PROFILE: str = os.getenv("TWITTER_PROFILE") or ""



class Config:
    env_file = ".env"

settings = Settings()
