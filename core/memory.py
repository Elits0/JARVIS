from datetime import datetime
from typing import List, Dict


class Memory:
    def __init__(self):
        self.history: List[Dict[str, str]] = []

    def remember(self, role: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({
            "timestamp": timestamp,
            "role": role,
            "message": message
        })

    def get_last_interaction(self) -> Dict[str, str]:
        if self.history:
            return self.history[-1]
        return {}

    def get_history(self) -> List[Dict[str, str]]:
        return self.history
