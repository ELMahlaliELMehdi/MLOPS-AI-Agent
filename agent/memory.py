from collections import deque
from datetime import datetime

class ConversationMemory:
    """
    Simple conversation memory - stores last N interactions per user.
    """
    def __init__(self, max_history: int = 3):
        self.conversations = {}  # user_id -> deque of messages
        self.max_history = max_history
    
    def add_interaction(self, user_id: str, query: str, response: dict):
        """
        Store a user interaction.
        """
        if user_id not in self.conversations:
            self.conversations[user_id] = deque(maxlen=self.max_history)
        
        self.conversations[user_id].append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response
        })
    
    def get_history(self, user_id: str) -> list:
        """
        Get conversation history for a user.
        """
        return list(self.conversations.get(user_id, []))
    
    def clear_history(self, user_id: str):
        """
        Clear history for a user.
        """
        if user_id in self.conversations:
            del self.conversations[user_id]

# Global memory instance
memory = ConversationMemory(max_history=3)