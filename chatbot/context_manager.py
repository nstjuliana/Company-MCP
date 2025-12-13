"""
Conversation Context Manager

Manages conversation history and context for the AI agent.
Enables follow-up questions by maintaining message history per session.
"""

from typing import List, Dict, Optional
from datetime import datetime
import uuid


class ConversationContext:
    """Manages conversation history per session."""

    def __init__(self, session_id: str = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.messages: List[Dict[str, str]] = []
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
        self.metadata: Dict[str, any] = {}  # Store extracted context (entities, database, etc.)
        self.data_entities: Dict[str, any] = {}  # Store specific data values for follow-up queries
    
    def add_message(self, role: str, content: str):
        """
        Add message to conversation history.
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        self.messages.append({
            "role": role,
            "content": content
        })
        self.last_updated = datetime.now()
        
        # Keep only last 20 messages to avoid token limits
        if len(self.messages) > 20:
            self.messages = self.messages[-20:]
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history for AI context."""
        return self.messages.copy()
    
    def get_recent_history(self, n: int = 5) -> List[Dict[str, str]]:
        """Get last n messages."""
        return self.messages[-n:] if len(self.messages) > n else self.messages.copy()
    
    def set_metadata(self, key: str, value: any):
        """Store metadata (e.g., current database, last entity)."""
        self.metadata[key] = value
        self.last_updated = datetime.now()
    
    def get_metadata(self, key: str, default: any = None) -> any:
        """Get stored metadata."""
        return self.metadata.get(key, default)

    def store_data_entity(self, entity_type: str, entity_data: any):
        """
        Store specific data values for follow-up queries.

        Args:
            entity_type: Type of entity (e.g., "payment", "merchant", "user")
            entity_data: The data values (dict or list)
        """
        self.data_entities[entity_type] = entity_data
        self.last_updated = datetime.now()

    def get_data_entity(self, entity_type: str, default: any = None) -> any:
        """Get stored data entity."""
        return self.data_entities.get(entity_type, default)

    def get_all_data_entities(self) -> Dict[str, any]:
        """Get all stored data entities."""
        return self.data_entities.copy()

    def clear(self):
        """Clear conversation history, metadata, and data entities."""
        self.messages = []
        self.metadata = {}
        self.data_entities = {}
        self.last_updated = datetime.now()


class ConversationManager:
    """
    Manages multiple conversation contexts.
    In production, this would use Redis or a database.
    """
    
    def __init__(self, max_contexts: int = 1000, context_ttl_hours: int = 24):
        self.contexts: Dict[str, ConversationContext] = {}
        self.max_contexts = max_contexts
        self.context_ttl_hours = context_ttl_hours
    
    def get_or_create(self, session_id: str) -> ConversationContext:
        """Get existing context or create new one."""
        # Clean up expired contexts periodically
        self._cleanup_expired()
        
        if session_id not in self.contexts:
            self.contexts[session_id] = ConversationContext(session_id)
        
        return self.contexts[session_id]
    
    def get(self, session_id: str) -> Optional[ConversationContext]:
        """Get context if exists."""
        return self.contexts.get(session_id)
    
    def delete(self, session_id: str):
        """Delete a conversation context."""
        if session_id in self.contexts:
            del self.contexts[session_id]
    
    def _cleanup_expired(self):
        """Remove expired contexts and enforce max limit."""
        now = datetime.now()
        expired = []
        
        for session_id, context in self.contexts.items():
            hours_old = (now - context.last_updated).total_seconds() / 3600
            if hours_old > self.context_ttl_hours:
                expired.append(session_id)
        
        for session_id in expired:
            del self.contexts[session_id]
        
        # If still over limit, remove oldest
        if len(self.contexts) > self.max_contexts:
            sorted_contexts = sorted(
                self.contexts.items(),
                key=lambda x: x[1].last_updated
            )
            to_remove = len(self.contexts) - self.max_contexts
            for session_id, _ in sorted_contexts[:to_remove]:
                del self.contexts[session_id]


# Global conversation manager instance
conversation_manager = ConversationManager()

