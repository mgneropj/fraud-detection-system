import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score


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

# 4. Scale Time and Amount
scaler = StandardScaler()

X_train[["Time", "Amount"]] = scaler.fit_transform(
    X_train[["Time", "Amount"]]
)

X_test[["Time", "Amount"]] = scaler.transform(
    X_test[["Time", "Amount"]]
)

# 5. Load trained XGBoost model
model = joblib.load("models/xgboost_fraud_model.pkl")

# 6. Get fraud probabilities
probabilities = model.predict_proba(X_test)[:, 1]

# 7. Test different thresholds
thresholds = [
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
    0.80,
    0.90
]

print("=" * 90)
print("FRAUD DETECTION THRESHOLD ANALYSIS")
print("=" * 90)

print(
    f"{'Threshold':<12}"
    f"{'Precision':<12}"
    f"{'Recall':<12}"
    f"{'F1 Score':<12}"
    f"{'False Pos':<15}"
    f"{'False Neg':<15}"
)

print("-" * 90)

# 8. Evaluate every threshold
for threshold in thresholds:

    predictions = (probabilities >= threshold).astype(int)

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    false_positives = (
        (predictions == 1) & (y_test == 0)
    ).sum()

    false_negatives = (
        (predictions == 0) & (y_test == 1)
    ).sum()

    print(
        f"{threshold:<12.2f}"
        f"{precision:<12.3f}"
        f"{recall:<12.3f}"
        f"{f1:<12.3f}"
        f"{false_positives:<15}"
        f"{false_negatives:<15}"
    )

print("-" * 90)

print("\nThreshold analysis completed successfully!")