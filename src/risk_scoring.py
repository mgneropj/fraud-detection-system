import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# 1. Load dataset
df = pd.read_csv("data/creditcard.csv")

# 2. Separate features and target
X = df.drop("Class", axis=1)
y = df["Class"]

# 3. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 4. Load trained model
model = joblib.load("models/xgboost_fraud_model.pkl")

# 5. Scale Time and Amount
scaler = StandardScaler()

X_train[["Time", "Amount"]] = scaler.fit_transform(
    X_train[["Time", "Amount"]]
)

X_test[["Time", "Amount"]] = scaler.transform(
    X_test[["Time", "Amount"]]
)

# 6. Get fraud probabilities
fraud_probability = model.predict_proba(X_test)[:, 1]

# 7. Convert probability to risk score
risk_score = fraud_probability * 100

# 8. Convert score into risk level
def get_risk_level(score):
    if score < 30:
        return "LOW"
    elif score < 70:
        return "MEDIUM"
    else:
        return "HIGH"


risk_level = [get_risk_level(score) for score in risk_score]

# 9. Create results dataframe
results = pd.DataFrame({
    "Actual": y_test.values,
    "Fraud_Probability": fraud_probability,
    "Risk_Score": risk_score,
    "Risk_Level": risk_level
})

# 10. Display sample predictions
print("\n" + "=" * 70)
print("FRAUD RISK SCORING")
print("=" * 70)

print(results.head(20).to_string(index=False))

# 11. Display risk-level distribution
print("\n" + "=" * 70)
print("RISK LEVEL DISTRIBUTION")
print("=" * 70)

print(results["Risk_Level"].value_counts())

# 12. Display high-risk transactions
print("\n" + "=" * 70)
print("HIGH-RISK TRANSACTIONS")
print("=" * 70)

high_risk = results[results["Risk_Level"] == "HIGH"]

print(high_risk.head(20).to_string(index=False))

print("\nRisk scoring completed successfully!")