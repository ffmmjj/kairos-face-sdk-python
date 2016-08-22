class RecognizedFaceCandidate:
    def __init__(self, subject, confidence):
        self.subject = subject
        self.confidence = confidence

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<Face "{}" with confidence. {}>'.format(self.subject, self.confidence)