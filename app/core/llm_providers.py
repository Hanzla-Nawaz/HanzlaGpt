import os
import time
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from loguru import logger
from app.core.config import settings

# OpenAI imports
try:
    from openai import OpenAI
    from langchain_community.chat_models import ChatOpenAI
    from langchain_community.embeddings import OpenAIEmbeddings
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not available")

# HuggingFace imports
try:
    from langchain_community.llms import HuggingFaceHub
    from langchain_community.embeddings import HuggingFaceEmbeddings
    HUGGINGFACE_AVAILABLE = True
except ImportError as e:
    HUGGINGFACE_AVAILABLE = False
    logger.warning(f"HuggingFace not available: {e}")

# Ollama imports
try:
    from langchain_community.llms import Ollama
    from langchain_community.embeddings import OllamaEmbeddings
    OLLAMA_AVAILABLE = True
except ImportError as e:
    OLLAMA_AVAILABLE = False
    logger.warning(f"Ollama not available: {e}")

# Groq imports (Free tier: 1000 requests/day)
try:
    from langchain_community.chat_models import ChatGroq
    GROQ_AVAILABLE = True
except ImportError as e:
    GROQ_AVAILABLE = False
    logger.warning(f"Groq not available: {e}")

# Together AI imports (Free tier: 1000 requests/day)
try:
    from langchain_community.chat_models import ChatTogetherAI
    TOGETHER_AVAILABLE = True
except ImportError as e:
    TOGETHER_AVAILABLE = False
    logger.warning(f"Together AI not available: {e}")

# Replicate imports (Free tier: 500 requests/day)
try:
    from langchain_community.llms import Replicate
    REPLICATE_AVAILABLE = True
except ImportError as e:
    REPLICATE_AVAILABLE = False
    logger.warning(f"Replicate not available: {e}")

# Local models (sentence-transformers)
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError as e:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning(f"Sentence transformers not available: {e}")

class BaseLLMProvider(ABC):
    """Base class for LLM providers."""
    
    @abstractmethod
    def get_chat_model(self):
        """Get chat model instance."""
        pass
    
    @abstractmethod
    def get_embeddings(self):
        """Get embeddings model instance."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get provider name."""
        pass

class OpenAIProvider(BaseLLMProvider):
    """OpenAI provider with fallback."""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model_name = settings.OPENAI_MODEL_NAME
        self.embedding_model = settings.OPENAI_API_EMBEDDING_MODEL
    
    def get_chat_model(self):
        if not OPENAI_AVAILABLE or not self.api_key:
            return None
        try:
            return ChatOpenAI(
                model=self.model_name,
                openai_api_key=self.api_key,
                temperature=0.7
            )
        except Exception as e:
            logger.error(f"OpenAI chat model error: {str(e)}")
            return None
    
    def get_embeddings(self):
        if not OPENAI_AVAILABLE or not self.api_key:
            return None
        try:
            return OpenAIEmbeddings(
                model=self.embedding_model,
                openai_api_key=self.api_key
            )
        except Exception as e:
            logger.error(f"OpenAI embeddings error: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        # Re-check environment variables directly from os.environ
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        self.model_name = os.getenv('OPENAI_MODEL_NAME', 'gpt-3.5-turbo')
        return OPENAI_AVAILABLE and bool(self.api_key)
    
    def get_name(self) -> str:
        return "OpenAI"

class GroqProvider(BaseLLMProvider):
    """Groq provider - Fast and free tier available."""
    
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY', '')
        self.model_name = os.getenv('GROQ_MODEL', 'llama3-8b-8192')
    
    def get_chat_model(self):
        if not GROQ_AVAILABLE or not self.api_key:
            return None
        try:
            return ChatGroq(
                model_name=self.model_name,
                groq_api_key=self.api_key,
                temperature=0.7
            )
        except Exception as e:
            logger.warning(f"Groq chat model not available: {str(e)}")
            return None
    
    def get_embeddings(self):
        # Groq doesn't provide embeddings, use HuggingFace as fallback
        return None
    
    def is_available(self) -> bool:
        # Re-check environment variables directly from os.environ
        self.api_key = os.getenv('GROQ_API_KEY', '')
        return GROQ_AVAILABLE and bool(self.api_key)
    
    def get_name(self) -> str:
        return "Groq"

class TogetherAIProvider(BaseLLMProvider):
    """Together AI provider - Free tier available."""
    
    def __init__(self):
        self.api_key = os.getenv('TOGETHER_API_KEY', '')
        self.model_name = os.getenv('TOGETHER_MODEL', 'meta-llama/Llama-2-7b-chat-hf')
    
    def get_chat_model(self):
        if not TOGETHER_AVAILABLE or not self.api_key:
            return None
        try:
            return ChatTogetherAI(
                model=self.model_name,
                together_api_key=self.api_key,
                temperature=0.7
            )
        except Exception as e:
            logger.warning(f"Together AI chat model not available: {str(e)}")
            return None
    
    def get_embeddings(self):
        # Together AI doesn't provide embeddings, use HuggingFace as fallback
        return None
    
    def is_available(self) -> bool:
        # Re-check environment variables directly from os.environ
        self.api_key = os.getenv('TOGETHER_API_KEY', '')
        return TOGETHER_AVAILABLE and bool(self.api_key)
    
    def get_name(self) -> str:
        return "Together AI"

class ReplicateProvider(BaseLLMProvider):
    """Replicate provider - Free tier available."""
    
    def __init__(self):
        self.api_key = os.getenv('REPLICATE_API_TOKEN', '')
        self.model_name = os.getenv('REPLICATE_MODEL', 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3')
    
    def get_chat_model(self):
        if not REPLICATE_AVAILABLE or not self.api_key:
            return None
        try:
            return Replicate(
                model=self.model_name,
                api_token=self.api_key,
                temperature=0.7
            )
        except Exception as e:
            logger.warning(f"Replicate chat model not available: {str(e)}")
            return None
    
    def get_embeddings(self):
        # Replicate doesn't provide embeddings, use HuggingFace as fallback
        return None
    
    def is_available(self) -> bool:
        # Re-check environment variables directly from os.environ
        self.api_key = os.getenv('REPLICATE_API_TOKEN', '')
        return REPLICATE_AVAILABLE and bool(self.api_key)
    
    def get_name(self) -> str:
        return "Replicate"

class HuggingFaceProvider(BaseLLMProvider):
    """HuggingFace provider using free models."""
    
    def __init__(self):
        # Try both env var names - HF library expects HUGGINGFACEHUB_API_TOKEN
        self.api_key = os.getenv('HUGGINGFACEHUB_API_TOKEN') or os.getenv('HUGGINGFACE_API_KEY')
        # Use a better model for chat
        self.chat_model_name = "microsoft/DialoGPT-large"  # Better alternative
        self.embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"  # Free embedding model
        logger.info(f"HuggingFace provider initialized with API key: {'Set' if self.api_key else 'Not set'}")
        if self.api_key:
            logger.info(f"✅ HuggingFace API key found: {self.api_key[:10]}...")
        else:
            logger.warning("❌ HuggingFace API key not found")
    
    def get_chat_model(self):
        if not HUGGINGFACE_AVAILABLE:
            logger.warning("HuggingFace not available - imports failed")
            return None
        if not self.api_key:
            logger.warning("HuggingFace API key not set")
            return None
        try:
            logger.info(f"Initializing HuggingFace model: {self.chat_model_name}")
            model = HuggingFaceHub(
                repo_id=self.chat_model_name,
                huggingfacehub_api_token=self.api_key,
                model_kwargs={"temperature": 0.7}
            )
            logger.info("✅ HuggingFace chat model initialized successfully")
            return model
        except Exception as e:
            logger.warning(f"HuggingFace chat model not available: {str(e)}")
            return None
    
    def get_embeddings(self):
        if not HUGGINGFACE_AVAILABLE:
            return None
        try:
            return HuggingFaceEmbeddings(
                model_name=self.embedding_model_name,
                model_kwargs={'device': 'cpu'}  # Use CPU for deployment
            )
        except Exception as e:
            logger.warning(f"HuggingFace embeddings not available: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        # Re-check environment variables directly from os.environ
        self.api_key = os.getenv('HUGGINGFACEHUB_API_TOKEN', '') or os.getenv('HUGGINGFACE_API_KEY', '')
        return HUGGINGFACE_AVAILABLE and bool(self.api_key)
    
    def get_name(self) -> str:
        return "HuggingFace"

class OllamaProvider(BaseLLMProvider):
    """Ollama provider for local models."""
    
    def __init__(self):
        self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model_name = os.getenv('OLLAMA_MODEL', 'llama2')
    
    def get_chat_model(self):
        if not OLLAMA_AVAILABLE:
            return None
        try:
            return Ollama(
                base_url=self.base_url,
                model=self.model_name,
                temperature=0.7
            )
        except Exception as e:
            logger.warning(f"Ollama chat model not available: {str(e)}")
            return None
    
    def get_embeddings(self):
        if not OLLAMA_AVAILABLE:
            return None
        try:
            return OllamaEmbeddings(
                base_url=self.base_url,
                model=self.model_name
            )
        except Exception as e:
            logger.warning(f"Ollama embeddings not available: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        return OLLAMA_AVAILABLE
    
    def get_name(self) -> str:
        return "Ollama"

class LocalEmbeddingsProvider(BaseLLMProvider):
    """Local embeddings using sentence-transformers."""
    
    def __init__(self):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
    
    def get_chat_model(self):
        # Local chat models are complex, so we'll use a simple fallback
        return None
    
    def get_embeddings(self):
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            return None
        try:
            # Use sentence-transformers directly for local embeddings
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer(self.model_name)
            # Create a simple wrapper for compatibility
            class LocalEmbeddings:
                def __init__(self, model):
                    self.model = model
                
                def embed_documents(self, texts):
                    return self.model.encode(texts).tolist()
                
                def embed_query(self, text):
                    return self.model.encode([text])[0].tolist()
            
            return LocalEmbeddings(model)
        except Exception as e:
            logger.error(f"Local embeddings error: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        return SENTENCE_TRANSFORMERS_AVAILABLE
    
    def get_name(self) -> str:
        return "Local Embeddings"

class LLMProviderManager:
    """Manages multiple LLM providers with fallback strategy."""
    
    def __init__(self):
        self.providers = [
            OpenAIProvider(),
            GroqProvider(),
            TogetherAIProvider(),
            ReplicateProvider(),
            HuggingFaceProvider(),
            OllamaProvider(),
            LocalEmbeddingsProvider()
        ]
        self.current_chat_provider = None
        self.current_embedding_provider = None
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize and test providers in order of preference."""
        logger.info("Initializing LLM providers...")
        
        # Initialize chat model - try each provider until one works
        for provider in self.providers:
            if provider.is_available():
                try:
                    chat_model = provider.get_chat_model()
                    if chat_model:
                        self.current_chat_provider = provider
                        logger.info(f"✅ Chat model initialized with {provider.get_name()}")
                        break
                    else:
                        logger.warning(f"❌ {provider.get_name()} returned None model")
                except Exception as e:
                    logger.warning(f"❌ {provider.get_name()} failed: {e}")
            else:
                logger.warning(f"❌ {provider.get_name()} not available")
        
        # Initialize embeddings
        for provider in self.providers:
            if provider.is_available():
                try:
                    embeddings = provider.get_embeddings()
                    if embeddings:
                        self.current_embedding_provider = provider
                        logger.info(f"✅ Embeddings initialized with {provider.get_name()}")
                        break
                except Exception as e:
                    logger.warning(f"❌ {provider.get_name()} embeddings failed: {e}")
        
        if not self.current_chat_provider:
            logger.error("❌ No chat model available!")
        if not self.current_embedding_provider:
            logger.error("❌ No embeddings model available!")
    
    def get_chat_model(self):
        """Get the current chat model with automatic fallback."""
        if self.current_chat_provider:
            try:
                model = self.current_chat_provider.get_chat_model()
                if model:
                    return model
                else:
                    # Model returned None, try fallback
                    logger.warning(f"Current chat provider {self.current_chat_provider.get_name()} returned None, trying fallback")
                    if self.fallback_to_next_provider("chat"):
                        return self.get_chat_model()  # Recursive call with new provider
            except Exception as e:
                logger.warning(f"Current chat provider {self.current_chat_provider.get_name()} failed: {e}")
                # Force fallback on error
                if self.fallback_to_next_provider("chat"):
                    return self.get_chat_model()  # Recursive call with new provider
        
        # If no current provider or fallback failed, try to initialize any available provider
        for provider in self.providers:
            if provider.is_available():
                try:
                    model = provider.get_chat_model()
                    if model:
                        self.current_chat_provider = provider
                        logger.info(f"🔄 Emergency fallback to {provider.get_name()} for chat")
                        return model
                except Exception as e:
                    logger.warning(f"Provider {provider.get_name()} failed: {e}")
                    continue
        
        return None
    
    def get_embeddings(self):
        """Get the current embeddings model."""
        if self.current_embedding_provider:
            return self.current_embedding_provider.get_embeddings()
        return None
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all providers."""
        status = {
            "chat_provider": self.current_chat_provider.get_name() if self.current_chat_provider else "None",
            "embedding_provider": self.current_embedding_provider.get_name() if self.current_embedding_provider else "None",
            "providers": {}
        }
        
        for provider in self.providers:
            status["providers"][provider.get_name()] = {
                "available": provider.is_available(),
                "chat_model": provider.get_chat_model() is not None,
                "embeddings": provider.get_embeddings() is not None
            }
        
        return status
    
    def fallback_to_next_provider(self, provider_type: str = "chat"):
        """Fallback to next available provider."""
        current_provider = self.current_chat_provider if provider_type == "chat" else self.current_embedding_provider
        current_index = next((i for i, p in enumerate(self.providers) if p == current_provider), -1)
        
        # Try next providers
        for i in range(current_index + 1, len(self.providers)):
            provider = self.providers[i]
            if provider.is_available():
                if provider_type == "chat":
                    chat_model = provider.get_chat_model()
                    if chat_model:
                        self.current_chat_provider = provider
                        logger.info(f"🔄 Fallback to {provider.get_name()} for chat")
                        return True
                else:
                    embeddings = provider.get_embeddings()
                    if embeddings:
                        self.current_embedding_provider = provider
                        logger.info(f"🔄 Fallback to {provider.get_name()} for embeddings")
                        return True
        
        logger.error(f"❌ No fallback available for {provider_type}")
        return False

    def reinitialize_providers(self):
        """Force re-initialization of providers to detect environment changes."""
        logger.info("🔄 Re-initializing providers to detect environment changes...")
        
        # Reload environment variables from .env file
        try:
            from dotenv import load_dotenv
            load_dotenv(override=True)
            logger.info("✅ Environment variables reloaded from .env file")
        except Exception as e:
            logger.warning(f"Failed to reload .env file: {e}")
        
        self.current_chat_provider = None
        self.current_embedding_provider = None
        self._initialize_providers()
        logger.info("✅ Provider re-initialization complete")

# Global provider manager instance
provider_manager = LLMProviderManager()
