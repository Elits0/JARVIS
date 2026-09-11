class LearningSession:

    def __init__(self):

        self.pending_learning = None

    def set_pending(self, learning_data):

        self.pending_learning = learning_data

    def get_pending(self):

        return self.pending_learning

    def clear(self):

        self.pending_learning = None

    def has_pending(self):

        return self.pending_learning is not None
        