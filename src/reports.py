import pandas as pd
import json

def to_dataframe(findings):
    return pd.DataFrame(findings)

def summary(findings):
    total = len(findings)
    pii = sum(1 for f in findings if f["is_pii"])
    return {
        "columns_scanned": total,
        "pii_columns_found": pii,
        "pii_ratio": round(pii / total * 100, 1) if total else 0,
    }

def to_json(findings, path="pii_report.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(findings, f, ensure_ascii=False, indent=2, default=str)
