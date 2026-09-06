import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)
from xgboost import XGBClassifier


# 1. Load dataset
df = pd.read_csv("data/creditcard.csv")

print("Dataset loaded:", df.shape)


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

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)


# 4. Scale Time and Amount
scaler = StandardScaler()

X_train[["Time", "Amount"]] = scaler.fit_transform(
    X_train[["Time", "Amount"]]
)

X_test[["Time", "Amount"]] = scaler.transform(
    X_test[["Time", "Amount"]]
)


# 5. Calculate class imbalance ratio
negative_count = (y_train == 0).sum()
positive_count = (y_train == 1).sum()

scale_pos_weight = negative_count / positive_count

print("\nClass imbalance ratio:", scale_pos_weight)


# 6. Create XGBoost model
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    eval_metric="logloss",
    n_jobs=-1
)


# 7. Train model
print("\nTraining XGBoost model...")

model.fit(X_train, y_train)

print("XGBoost training completed!")


# 8. Predictions
y_pred = model.predict(X_test)

y_probability = model.predict_proba(X_test)[:, 1]


# 9. Classification report
print("\n" + "=" * 60)
print("XGBOOST CLASSIFICATION REPORT")
print("=" * 60)

print(classification_report(y_test, y_pred))


# 10. Confusion matrix
print("=" * 60)
print("XGBOOST CONFUSION MATRIX")
print("=" * 60)

cm = confusion_matrix(y_test, y_pred)

print(cm)


# 11. ROC-AUC
roc_auc = roc_auc_score(y_test, y_probability)

print("\n" + "=" * 60)
print(f"XGBOOST ROC-AUC SCORE: {roc_auc:.4f}")
print("=" * 60)


# 12. Save model
joblib.dump(model, "models/xgboost_fraud_model.pkl")

print("\nModel saved to models/xgboost_fraud_model.pkl")