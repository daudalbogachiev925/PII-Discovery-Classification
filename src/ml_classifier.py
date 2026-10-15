from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from src.detectors import DETECTORS

def build_training_data():
    samples = []
    labels = []
    for d in DETECTORS:
        if d.name == "email":
            for i in range(20):
                samples.append(f"user{i}@example.com")
                labels.append("email")
        elif d.name == "phone_intl":
            for i in range(20):
                samples.append(f"+7900123{4000+i}")
                labels.append("phone")
        elif d.name == "credit_card":
            for i in range(20):
                samples.append(f"4111 1111 1111 {1000+i}")
                labels.append("credit_card")
        elif d.name == "ipv4":
            for i in range(20):
                samples.append(f"192.168.1.{i}")
                labels.append("ip")
    for i in range(50):
        samples.append(f"random_text_{i}")
        labels.append("non_pii")
    return samples, labels

class MLPIIClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4))
        self.clf = LogisticRegression(max_iter=1000)
        self.trained = False

    def train(self):
        X, y = build_training_data()
        X_vec = self.vectorizer.fit_transform(X)
        self.clf.fit(X_vec, y)
        self.trained = True

    def predict(self, values):
        if not self.trained:
            self.train()
        X = self.vectorizer.transform(values)
        return self.clf.predict(X).tolist()

    def predict_proba(self, values):
        if not self.trained:
            self.train()
        X = self.vectorizer.transform(values)
        return self.clf.predict_proba(X).max(axis=1).tolist()
