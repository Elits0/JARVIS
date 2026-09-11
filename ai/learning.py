import json
import os
from typing import List, Dict, Optional


class LearningSystem:

    def __init__(
        self,
        file_path="data/learned_intents.json"
    ):

        self.file_path = file_path
        self.learned_intents: List[Dict] = []

        self.load()

    def load(self):

        if not os.path.exists(self.file_path):
            self.learned_intents = []
            return

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    self.learned_intents = data
                else:
                    self.learned_intents = []

        except (
            json.JSONDecodeError,
            OSError
        ):

            self.learned_intents = []

    def save(self):

        directory = os.path.dirname(self.file_path)

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.learned_intents,
                file,
                ensure_ascii=False,
                indent=4
            )

    def get_intent(
        self,
        intent: str
    ) -> Optional[Dict]:

        intent = intent.strip().lower()

        for item in self.learned_intents:

            if item.get("intent") == intent:
                return item

        return None

    def create_intent(
        self,
        intent: str,
        example: str,
        action: Optional[Dict] = None
    ):

        intent = intent.strip().lower()
        example = example.strip()

        if not intent or not example:
            return False

        if self.get_intent(intent):
            return False

        new_intent = {
            "intent": intent,
            "examples": [example]
        }

        if action is not None:
            new_intent["action"] = action

        self.learned_intents.append(
            new_intent
        )

        self.save()

        return True

    def add_example(
        self,
        intent: str,
        example: str
    ):

        intent = intent.strip().lower()
        example = example.strip()

        item = self.get_intent(intent)

        if not item or not example:
            return False

        examples = item.setdefault(
            "examples",
            []
        )

        if example not in examples:
            examples.append(example)
            self.save()

        return True

    def update_action(
        self,
        intent: str,
        action: Dict
    ):

        item = self.get_intent(intent)

        if not item:
            return False

        item["action"] = action

        self.save()

        return True

    def get_action(
        self,
        intent: str
    ) -> Optional[Dict]:

        item = self.get_intent(intent)

        if item:
            return item.get("action")

        return None

    def get_all(self):

        return self.learned_intents