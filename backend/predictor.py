import os
import joblib
import pandas as pd

from src.rules_engine import calculate_rule_score


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_fraud_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


FEATURES = [
    "Time",
    "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9",
    "V10", "V11", "V12", "V13", "V14", "V15", "V16", "V17",
    "V18", "V19", "V20", "V21", "V22", "V23", "V24", "V25",
    "V26", "V27", "V28",
    "Amount",
]


def predict_transaction(transaction):
    missing_features = [
        feature for feature in FEATURES
        if feature not in transaction
    ]

    if missing_features:
        raise ValueError(f"Missing features: {missing_features}")

    df = pd.DataFrame(
        [[transaction[feature] for feature in FEATURES]],
        columns=FEATURES
    )

    df_scaled = df.copy()

    df_scaled[["Time", "Amount"]] = scaler.transform(
        df[["Time", "Amount"]]
    )

    fraud_probability = float(
        model.predict_proba(df_scaled)[0][1]
    )

    ml_score = round(fraud_probability * 100, 2)

    rule_score, reasons = calculate_rule_score(transaction)

    final_score = round(
        (ml_score * 0.70) + (rule_score * 0.30),
        2
    )

    # Strong rule signals can escalate a transaction.
    if rule_score >= 80:
        final_score = max(final_score, rule_score)

        reasons.append(
            "Strong rule-based risk escalation"
        )

    # Moderate rule signals should trigger manual review.
    elif rule_score >= 30:
        final_score = max(final_score, 50)

        reasons.append(
            "Moderate rule-based risk escalation"
        )

    # Very high ML confidence should also block.
    if fraud_probability >= 0.90:
        final_score = max(final_score, ml_score)

        reasons.append(
            "High-confidence ML fraud detection"
        )

    final_score = min(round(final_score, 2), 100)

    if final_score >= 70:
        risk_level = "HIGH"
        decision = "BLOCK"

    elif final_score >= 30:
        risk_level = "MEDIUM"
        decision = "REVIEW"

    else:
        risk_level = "LOW"
        decision = "APPROVE"

    return {
        "fraud_probability": round(fraud_probability, 4),
        "ml_score": ml_score,
        "rule_score": rule_score,
        "final_risk_score": final_score,
        "risk_level": risk_level,
        "decision": decision,
        "reasons": reasons,
    }
