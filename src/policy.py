POLICY_MAP = {
    "contact": {"classification": "confidential", "encryption": "AES-256",
                "retention_days": 730, "gdpr_basis": "consent"},
    "gov_id": {"classification": "restricted", "encryption": "AES-256",
               "retention_days": 1825, "gdpr_basis": "legal"},
    "financial": {"classification": "restricted", "encryption": "AES-256",
                  "retention_days": 2555, "gdpr_basis": "legal"},
    "personal": {"classification": "confidential", "encryption": "AES-256",
                 "retention_days": 1825, "gdpr_basis": "consent"},
    "technical": {"classification": "internal", "encryption": "TLS",
                  "retention_days": 365, "gdpr_basis": "legitimate_interest"},
}

def get_policy(pii_type):
    for cat, policy in POLICY_MAP.items():
        if cat in pii_type.lower():
            return policy
    return {"classification": "internal", "encryption": "TLS",
            "retention_days": 365, "gdpr_basis": "legitimate_interest"}

def required_actions(findings):
    actions = []
    for f in findings:
        if not f["is_pii"]:
            continue
        pii_type = (f["rule_based"] or {}).get("type", f["ml_prediction"] or "unknown")
        policy = get_policy(pii_type)
        actions.append({
            "column": f["column"],
            "pii_type": pii_type,
            "classification": policy["classification"],
            "encryption": policy["encryption"],
            "retention_days": policy["retention_days"],
            "gdpr_basis": policy["gdpr_basis"],
        })
    return actions
