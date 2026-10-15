import pandas as pd
from src.detectors import classify_column, detect_pii
from src.ml_classifier import MLPIIClassifier

class PIIScanner:
    def __init__(self, use_ml=True):
        self.use_ml = use_ml
        self.ml = MLPIIClassifier() if use_ml else None

    def scan_dataframe(self, df: pd.DataFrame):
        findings = []
        for col in df.columns:
            values = df[col].dropna().astype(str).tolist()
            if not values:
                continue
            rule_result = classify_column(values)
            ml_labels = self.ml.predict(values[:50]) if self.ml else []
            ml_dominant = max(set(ml_labels), key=ml_labels.count) if ml_labels else None
            findings.append({
                "column": col,
                "rule_based": rule_result,
                "ml_prediction": ml_dominant,
                "sample_size": len(values),
                "is_pii": bool(rule_result) or (ml_dominant not in (None, "non_pii")),
            })
        return findings

    def scan_value(self, value):
        return detect_pii(value)
