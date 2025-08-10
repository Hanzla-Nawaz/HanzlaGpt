"""
Provider Router for Automatic Provider Assignment
Automatically assigns different AI providers to different users to distribute load
"""
import hashlib
import time
from typing import Dict, List, Optional
from loguru import logger
from app.core.llm_providers import provider_manager
from app.core.database import get_user_provider, set_user_provider

class ProviderRouter:
    """Routes users to different providers automatically."""
    
    def __init__(self):
        self.provider_names = [
            "OpenAI",
            "Groq", 
            "Together AI",
            "Replicate",
            "HuggingFace",
            "Ollama"
        ]
        self.user_provider_cache: Dict[str, str] = {}
        self.provider_usage: Dict[str, int] = {name: 0 for name in self.provider_names}
        self.last_rotation = time.time()
        self.rotation_interval = 3600  # Rotate every hour
        self._counter = 0  # for simple round-robin fallback
    
    def _hash_user_id(self, user_id: str) -> int:
        """Create a hash of user ID for consistent provider assignment."""
        return int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    
    def _get_available_providers(self) -> List[str]:
        """Get list of available providers."""
        available = []
        for provider_name in self.provider_names:
            if provider_name == "OpenAI" and provider_manager.current_chat_provider and provider_manager.current_chat_provider.get_name() == "OpenAI":
                available.append(provider_name)
            elif provider_name == "Groq" and any(p.get_name() == "Groq" for p in provider_manager.providers if p.is_available()):
                available.append(provider_name)
            elif provider_name == "Together AI" and any(p.get_name() == "Together AI" for p in provider_manager.providers if p.is_available()):
                available.append(provider_name)
            elif provider_name == "Replicate" and any(p.get_name() == "Replicate" for p in provider_manager.providers if p.is_available()):
                available.append(provider_name)
            elif provider_name == "HuggingFace" and any(p.get_name() == "HuggingFace" for p in provider_manager.providers if p.is_available()):
                available.append(provider_name)
            elif provider_name == "Ollama" and any(p.get_name() == "Ollama" for p in provider_manager.providers if p.is_available()):
                available.append(provider_name)
        return available
    
    def _get_provider_by_name(self, provider_name: str):
        """Get provider instance by name."""
        for provider in provider_manager.providers:
            if provider.get_name() == provider_name:
                return provider
        return None
    
    def get_provider_for_user(self, user_id: str, session_id: str = None) -> Optional[str]:
        """
        Get the best provider for a specific user.
        Uses consistent hashing to assign the same provider to the same user.
        """
        # Check if we need to rotate providers
        current_time = time.time()
        if current_time - self.last_rotation > self.rotation_interval:
            self._rotate_providers()
            self.last_rotation = current_time
        # Create a unique identifier for the user
        user_key = f"{user_id}_{session_id}" if session_id else user_id
        # Check cache first
        if user_key in self.user_provider_cache:
            cached_provider = self.user_provider_cache[user_key]
            if cached_provider in self._get_available_providers():
                return cached_provider
        # Get available providers
        available_providers = self._get_available_providers()
        if not available_providers:
            logger.warning("No providers available, using fallback")
            return "Intent-based fallback"
        # Use consistent hashing to assign provider
        user_hash = self._hash_user_id(user_key)
        provider_index = user_hash % len(available_providers)
        selected_provider = available_providers[provider_index]
        # Cache the assignment
        self.user_provider_cache[user_key] = selected_provider
        # Update usage stats
        self.provider_usage[selected_provider] = self.provider_usage.get(selected_provider, 0) + 1
        logger.info(f"Assigned provider {selected_provider} to user {user_id}")
        return selected_provider
    
    def get_chat_model_for_user(self, user_id: str, session_id: str = None, requested: str | None = None):
        """Return chat model honouring a requested provider or persisted mapping."""
        # Requested provider overrides & persists
        if requested:
            set_user_provider(user_id, requested)
            self.user_provider_cache[user_id] = requested
            return provider_manager.get_chat_model_by_name(requested)
        # Check in-memory cache
        if user_id in self.user_provider_cache:
            provider_name = self.user_provider_cache[user_id]
        else:
            # Check DB
            provider_name = get_user_provider(user_id)
            if not provider_name:
                provider_name = self._assign_next_provider()
                set_user_provider(user_id, provider_name)
            self.user_provider_cache[user_id] = provider_name
        return provider_manager.get_chat_model_by_name(provider_name)
    
    def get_embeddings_for_user(self, user_id: str, session_id: str = None):
        """Get embeddings for specific user."""
        # For embeddings, we can use any available provider
        # Prefer the current embedding provider
        if provider_manager.current_embedding_provider:
            return provider_manager.current_embedding_provider.get_embeddings()
        
        # Fallback to any available embedding provider
        for provider in provider_manager.providers:
            if provider.is_available():
                embeddings = provider.get_embeddings()
                if embeddings:
                    return embeddings
        return None
    
    def _rotate_providers(self):
        """Rotate provider assignments to distribute load."""
        logger.info("Rotating provider assignments...")
        self.user_provider_cache.clear()
        self.provider_usage = {name: 0 for name in self.provider_names}
    
    def get_provider_stats(self) -> Dict:
        """Get statistics about provider usage."""
        available_providers = self._get_available_providers()
        total_usage = sum(self.provider_usage.values())
        
        stats = {
            "available_providers": available_providers,
            "total_assignments": total_usage,
            "provider_usage": self.provider_usage,
            "cache_size": len(self.user_provider_cache),
            "last_rotation": self.last_rotation
        }
        
        # Calculate distribution percentages
        if total_usage > 0:
            stats["distribution"] = {
                provider: (count / total_usage) * 100 
                for provider, count in self.provider_usage.items() 
                if count > 0
            }
        else:
            stats["distribution"] = {}
        
        return stats
    
    def force_provider_for_user(self, user_id: str, provider_name: str, session_id: str = None):
        """Force a specific provider for a user (for testing)."""
        user_key = f"{user_id}_{session_id}" if session_id else user_id
        self.user_provider_cache[user_key] = provider_name
        logger.info(f"Forced provider {provider_name} for user {user_id}")
    
    def clear_user_cache(self, user_id: str, session_id: str = None):
        """Clear cached provider for a user."""
        user_key = f"{user_id}_{session_id}" if session_id else user_id
        if user_key in self.user_provider_cache:
            del self.user_provider_cache[user_key]
            logger.info(f"Cleared provider cache for user {user_id}")

    def _assign_next_provider(self) -> str:
        """Round-robin pick next provider from preferred list."""
        name = self.provider_names[self._counter % len(self.provider_names)]
        self._counter += 1
        logger.info(f"Assigned provider {name} via round-robin")
        return name

# Global provider router instance
provider_router = ProviderRouter()
