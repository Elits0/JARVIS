import json
import os
from datetime import datetime
from typing import List, Dict


class Memory:

    def __init__(self, file_path="data/memory.json"):

        self.file_path = file_path
        self.history: List[Dict[str, str]] = []

        self.load()

    def remember(self, role: str, message: str):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.history.append({
            "timestamp": timestamp,
            "role": role,
            "message": message
        })

        self.save()

    def save(self):

        directory = os.path.dirname(self.file_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.history,
                file,
                ensure_ascii=False,
                indent=4
            )

    def load(self):

        if not os.path.exists(self.file_path):
            self.history = []
            return

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    self.history = data
                else:
                    self.history = []

        except (
            json.JSONDecodeError,
            OSError
        ):

            self.history = []

    def get_last_interaction(self) -> Dict[str, str]:

        if self.history:
            return self.history[-1]

        return {}

    def get_history(self) -> List[Dict[str, str]]:

        return self.history