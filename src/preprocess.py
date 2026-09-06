import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Load dataset
df = pd.read_csv("data/creditcard.csv")

print("Dataset loaded:", df.shape)

# 2. Separate features and target
X = df.drop("Class", axis=1)
y = df["Class"]

print("Features:", X.shape)
print("Target:", y.shape)

# 3. Split data BEFORE scaling
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)

# 4. Create scaler
scaler = StandardScaler()

# 5. Fit scaler ONLY on training data
X_train[["Time", "Amount"]] = scaler.fit_transform(
    X_train[["Time", "Amount"]]
)

# 6. Transform test data using the training scaler
X_test[["Time", "Amount"]] = scaler.transform(
    X_test[["Time", "Amount"]]
)

print("\nTime and Amount scaled successfully.")
print("Scaler fitted only on training data.")

# 7. Check class distribution
print("\nTraining class distribution:")
print(y_train.value_counts())

print("\nTesting class distribution:")
print(y_test.value_counts())

# 8. Save scaler for later API predictions
joblib.dump(scaler, "models/scaler.pkl")

print("\nScaler saved to models/scaler.pkl")

print("\nPreprocessing completed successfully!")