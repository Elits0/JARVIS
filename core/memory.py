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

    def search(self, query: str) -> List[Dict[str, str]]:

        query = query.lower().strip()

        if not query:
            return []

        stop_words = {
            "el", "la", "los", "las",
            "un", "una", "unos", "unas",
            "de", "del", "al", "a",
            "en", "y", "o",
            "que", "qué",
            "como", "cómo",
            "es",
            "mi", "mis",
            "tu", "tus",
            "me", "te", "se",
            "su", "sus",
            "por", "para",
            "con", "sobre",
            "cuál", "cuáles",
            "dime",
            "háblame"
        }

        words = [
            word.strip("¿?¡!.,;:()[]{}")
            for word in query.split()
        ]

        keywords = [
            word
            for word in words
            if word and word not in stop_words
        ]

        if not keywords:
            return []

        results = []

        for memory in self.history:

            message = memory.get(
                "message",
                ""
            ).lower()

            score = 0

            for keyword in keywords:

                if keyword in message:
                    score += 1

            if score > 0:
                results.append(
                    (score, memory)
                )

        results.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            memory
            for score, memory in results
        ]