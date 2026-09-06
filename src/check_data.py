import pandas as pd

# Load dataset
df = pd.read_csv("data/creditcard.csv")

print("=" * 60)
print("FRAUD DETECTION SYSTEM - DATASET ANALYSIS")
print("=" * 60)

# 1. Dataset shape
print("\n1. Dataset Shape")
print(df.shape)

# 2. Columns
print("\n2. Columns")
print(df.columns.tolist())

# 3. First 5 transactions
print("\n3. First 5 Transactions")
print(df.head())

# 4. Dataset information
print("\n4. Dataset Information")
df.info()

# 5. Fraud distribution
print("\n5. Fraud Distribution")
print(df["Class"].value_counts())

# 6. Fraud percentage
fraud_percentage = df["Class"].mean() * 100
print(f"\n6. Fraud Percentage: {fraud_percentage:.4f}%")

# 7. Missing values
print("\n7. Missing Values")
print(df.isnull().sum().sum())

# 8. Missing values by column
print("\n8. Missing Values By Column")
print(df.isnull().sum()[df.isnull().sum() > 0])

# 9. Amount statistics
print("\n9. Transaction Amount Statistics")
print(df["Amount"].describe())

# 10. Fraud transaction amount statistics
print("\n10. Fraud Transaction Amount Statistics")
print(df[df["Class"] == 1]["Amount"].describe())

# 11. Legitimate transaction amount statistics
print("\n11. Legitimate Transaction Amount Statistics")
print(df[df["Class"] == 0]["Amount"].describe())

print("\n" + "=" * 60)
print("DATA ANALYSIS COMPLETE")
print("=" * 60)