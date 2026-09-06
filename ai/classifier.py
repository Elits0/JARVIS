import joblib


class IntentClassifier:

    def __init__(
        self,
        model_path="models/intent_model.pkl"
    ):

        self.model = joblib.load(
            model_path
        )

    def predict(self, text):

        prediction = self.model.predict(
            [text]
        )

        probabilities = self.model.predict_proba(
            [text]
        )[0]

        classes = self.model.classes_

        confidence = max(
            probabilities
        )

        return {
            "intent": prediction[0],
            "confidence": float(confidence)
        }