import streamlit as st
import pandas as pd
import numpy as np
from src.scanner import PIIScanner
from src.policy import required_actions
from src.reports import summary

st.set_page_config(page_title="PII Discovery", layout="wide")
st.title("🔐 PII Discovery & Classification")

np.random.seed(42)
df = pd.DataFrame({
    "customer_id": range(1, 201),
    "email": [f"user{i}@mail.com" for i in range(200)],
    "phone": [f"+7900123{4000+i}" for i in range(200)],
    "birth_date": [f"199{i%9}-0{(i%9)+1}-1{i%9}" for i in range(200)],
    "ip": [f"192.168.{i%255}.{i%100}" for i in range(200)],
    "amount": np.random.normal(1000, 200, 200).round(2),
    "product": np.random.choice(["A", "B", "C"], 200),
    "notes": ["some free text"] * 200,
})

scanner = PIIScanner(use_ml=True)
findings = scanner.scan_dataframe(df)

s = summary(findings)
c1, c2, c3 = st.columns(3)
c1.metric("Columns scanned", s["columns_scanned"])
c2.metric("PII columns", s["pii_columns_found"])
c3.metric("PII ratio", f"{s['pii_ratio']}%")

st.subheader("Findings")
st.dataframe(pd.DataFrame(findings))

st.subheader("🛠 Required Actions")
actions = required_actions(findings)
st.dataframe(pd.DataFrame(actions))

st.subheader("🧪 Тест значения")
test = st.text_input("Проверить значение:", "user@example.com")
if test:
    st.json(scanner.scan_value(test))

st.subheader("Исходные данные")
st.dataframe(df.head(20))
