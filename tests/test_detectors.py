from src.detectors import detect_pii, classify_column

def test_email_detection():
    assert any(m["type"] == "email" for m in detect_pii("user@example.com"))

def test_phone_detection():
    assert any(m["type"] == "phone_ru" for m in detect_pii("+79001234567"))

def test_credit_card():
    assert any(m["type"] == "credit_card" for m in detect_pii("4111 1111 1111 1111"))

def test_classify_column():
    values = ["a@b.com", "c@d.com", "e@f.com"]
    result = classify_column(values)
    assert result["type"] == "email"
