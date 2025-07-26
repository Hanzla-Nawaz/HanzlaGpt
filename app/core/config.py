from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    """
    This Settings class is designed to load and manage environment variables for an
    application using Pydantic's BaseSettings and python-dotenv

    write all your env variables here so you can access them easily.

    """


    OPENAI_API_KEY:str = os.environ.get("OPENAI_API_KEY")
    OPENAI_MODEL_NAME:str = os.environ.get("OPENAI_MODEL_NAME")
    PINECONE_API_KEY : str = os.environ.get("PINECONE_API_KEY")
    PINECONE_ENV : str = os.environ.get("PINECONE_ENV")
    PINECONE_INDEX : str = os.environ.get("PINECONE_INDEX")
    PINECONE_NAMESPACE : str = os.environ.get("PINECONE_NAMESPACE")
    OPENAI_API_EMBEDDING_MODEL: str = os.getenv("OPENAI_API_Embedding_MODEL", "text-embedding-3-small")

    
    PG_HOST : str = os.environ.get("PG_HOST")
    PG_PORT : str = os.environ.get("PG_PORT")
    PG_USER : str = os.environ.get("PG_USER")
    PG_PASSWORD : str = os.environ.get("PG_PASSWORD")
    PG_DATABASE : str = os.environ.get("PG_DATABASE")
    
    LINKEDIN_PROFILE: str = os.getenv("LINKEDIN_PROFILE") or ""
    GITHUB_PROFILE: str = os.getenv("GITHUB_PROFILE") or ""
    MEDIUM_PROFILE: str = os.getenv("MEDIUM_PROFILE") or ""
    KAGGLE_PROFILE: str = os.getenv("KAGGLE_PROFILE") or ""
    TWITTER_PROFILE: str = os.getenv("TWITTER_PROFILE") or ""



class Config:
    env_file = ".env"

settings = Settings()
