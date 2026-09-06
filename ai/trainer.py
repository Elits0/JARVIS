import json
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
import joblib


DATASET_PATH = "data/intents.json"
MODEL_PATH = "models/intent_model.pkl"


def load_dataset():

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    texts = []
    labels = []

    for intent in data["intents"]:

        for example in intent["examples"]:

            texts.append(example)
            labels.append(intent["name"])

    return texts, labels


def train():

    texts, labels = load_dataset()

    model = Pipeline(
        [
            (
                "vectorizer",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2)
                )
            ),
            (
                "classifier",
                MLPClassifier(
                    hidden_layer_sizes=(32, 16),
                    max_iter=1000,
                    random_state=42
                )
            )
        ]
    )

    model.fit(texts, labels)

    os.makedirs(
        "models",
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    print("Modelo entrenado correctamente.")
    print(f"Modelo guardado en: {MODEL_PATH}")


if __name__ == "__main__":
    train()