import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from rules_engine import calculate_rule_score


# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv("data/creditcard.csv")

print("Dataset loaded:", df.shape)


# ============================================================
# 2. SEPARATE FEATURES AND TARGET
# ============================================================

X = df.drop("Class", axis=1)
y = df["Class"]


# ============================================================
# 3. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ============================================================
# 4. LOAD TRAINED XGBOOST MODEL
# ============================================================

model = joblib.load(
    "models/xgboost_fraud_model.pkl"
)

print("XGBoost model loaded successfully.")


# ============================================================
# 5. LOAD TRAINING SCALER
# ============================================================

scaler = joblib.load(
    "models/scaler.pkl"
)

print("Scaler loaded successfully.")


# ============================================================
# 6. SCALE TEST DATA
# ============================================================

X_test_scaled = X_test.copy()

X_test_scaled[["Time", "Amount"]] = scaler.transform(
    X_test_scaled[["Time", "Amount"]]
)


# ============================================================
# 7. GET ML FRAUD PROBABILITY
# ============================================================

ml_probability = model.predict_proba(
    X_test_scaled
)[:, 1]


# ============================================================
# 8. RISK LEVEL FUNCTION
# ============================================================

def get_risk_level(score):

    if score < 30:
        return "LOW"

    elif score < 70:
        return "MEDIUM"

    else:
        return "HIGH"


# ============================================================
# 9. DECISION FUNCTION
# ============================================================

def get_decision(score):

    if score < 30:
        return "APPROVE"

    elif score < 70:
        return "REVIEW"

    else:
        return "BLOCK"


# ============================================================
# 10. CALCULATE FINAL RISK
# ============================================================

results = []

for index, (_, transaction) in enumerate(X_test.iterrows()):

    # Convert transaction to dictionary
    transaction_data = transaction.to_dict()

    # Rule engine score
    rule_score, reasons = calculate_rule_score(
        transaction_data
    )

    # ML score
    ml_score = ml_probability[index] * 100

    # Combine ML + rule scores
    final_score = (
        (ml_score * 0.70)
        + (rule_score * 0.30)
    )

    # Keep score between 0 and 100
    final_score = min(
        max(final_score, 0),
        100
    )

    # Risk level
    risk_level = get_risk_level(
        final_score
    )

    # Final decision
    decision = get_decision(
        final_score
    )

    results.append({
        "Actual": y_test.loc[transaction.name],
        "ML_Score": round(ml_score, 2),
        "Rule_Score": rule_score,
        "Final_Risk_Score": round(final_score, 2),
        "Risk_Level": risk_level,
        "Decision": decision,
        "Reasons": "; ".join(reasons)
    })


# ============================================================
# 11. CREATE RESULTS DATAFRAME
# ============================================================

results_df = pd.DataFrame(results)


# ============================================================
# 12. DISPLAY SAMPLE RESULTS
# ============================================================

print("\n" + "=" * 90)
print("FINAL RISK ENGINE RESULTS")
print("=" * 90)

print(
    results_df.head(20).to_string(
        index=False
    )
)


# ============================================================
# 13. RISK DISTRIBUTION
# ============================================================

print("\n" + "=" * 90)
print("RISK LEVEL DISTRIBUTION")
print("=" * 90)

print(
    results_df["Risk_Level"].value_counts()
)


# ============================================================
# 14. DECISION DISTRIBUTION
# ============================================================

print("\n" + "=" * 90)
print("DECISION DISTRIBUTION")
print("=" * 90)

print(
    results_df["Decision"].value_counts()
)


# ============================================================
# 15. HIGH-RISK TRANSACTIONS
# ============================================================

print("\n" + "=" * 90)
print("HIGH-RISK TRANSACTIONS")
print("=" * 90)

high_risk = results_df[
    results_df["Risk_Level"] == "HIGH"
]

print(
    high_risk.head(20).to_string(
        index=False
    )
)


# ============================================================
# 16. SAVE RESULTS
# ============================================================

results_df.to_csv(
    "data/risk_results.csv",
    index=False
)

print("\nRisk results saved to:")
print("data/risk_results.csv")


print("\n" + "=" * 90)
print("FINAL RISK ENGINE COMPLETED SUCCESSFULLY!")
print("=" * 90)