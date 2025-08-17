from collections import defaultdict
from typing import List, Dict

# Super simple in-memory chat history (swap with Redis/DB in prod)
class ConversationMemory:
    def __init__(self):
        self._store: Dict[str, List[dict]] = defaultdict(list)

    def get(self, session_id: str) -> List[dict]:
        return self._store[session_id]

    def add(self, session_id: str, role: str, content: str):
        self._store[session_id].append({"role": role, "content": content})

    def truncate(self, session_id: str, max_messages: int = 20):
        history = self._store[session_id]
        if len(history) > max_messages:
            self._store[session_id] = history[-max_messages:]

memory = ConversationMemory()
