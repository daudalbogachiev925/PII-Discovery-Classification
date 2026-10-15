import re
from dataclasses import dataclass

@dataclass
class PIIDetector:
    name: str
    category: str
    pattern: str
    confidence: float = 0.9

    def match(self, value):
        if not isinstance(value, str):
            value = str(value)
        return bool(re.search(self.pattern, value, re.IGNORECASE))

DETECTORS = [
    PIIDetector("email", "contact", r"^[\w\.\-]+@[\w\.\-]+\.\w{2,}$"),
    PIIDetector("phone_ru", "contact", r"^(\+7|8)\d{10}$"),
    PIIDetector("phone_intl", "contact", r"^\+\d{10,15}$"),
    PIIDetector("ssn_us", "gov_id", r"^\d{3}-\d{2}-\d{4}$"),
    PIIDetector("passport_ru", "gov_id", r"^\d{4}\s?\d{6}$"),
    PIIDetector("credit_card", "financial", r"^\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}$"),
    PIIDetector("iban", "financial", r"^[A-Z]{2}\d{2}[A-Z0-9]{10,30}$"),
    PIIDetector("ipv4", "technical", r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    PIIDetector("date_of_birth", "personal", r"^\d{4}-\d{2}-\d{2}$"),
    PIIDetector("full_name_ru", "personal", r"^[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+"),
    PIIDetector("address", "personal", r"\d+\s?[а-я]*,?\s?(ул|st|street|avenue|пр)"),
]

def detect_pii(value):
    matches = []
    for d in DETECTORS:
        if d.match(value):
            matches.append({"type": d.name, "category": d.category,
                            "confidence": d.confidence})
    return matches

def classify_column(values):
    """Определить доминирующий PII-тип колонки."""
    counts = {}
    for v in values[:200]:
        for m in detect_pii(v):
            counts[m["type"]] = counts.get(m["type"], 0) + 1
    if not counts:
        return None
    top = max(counts.items(), key=lambda x: x[1])
    return {"type": top[0], "coverage": top[1] / min(len(values), 200)}
