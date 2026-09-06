import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)

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

# 5. Create Logistic Regression model
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

print("Training Logistic Regression model...")

# 6. Train model
model.fit(X_train, y_train)

print("Model training completed!")

# 7. Make predictions
y_pred = model.predict(X_test)

# 8. Get fraud probabilities
y_probability = model.predict_proba(X_test)[:, 1]

# 9. Classification report
print("\n" + "=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)

print(classification_report(y_test, y_pred))

# 10. Confusion matrix
print("=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

cm = confusion_matrix(y_test, y_pred)
print(cm)

# 11. ROC-AUC
roc_auc = roc_auc_score(y_test, y_probability)

print("\n" + "=" * 60)
print(f"ROC-AUC SCORE: {roc_auc:.4f}")
print("=" * 60)

# 12. Save model
joblib.dump(model, "models/logistic_regression.pkl")

print("\nModel saved to models/logistic_regression.pkl")