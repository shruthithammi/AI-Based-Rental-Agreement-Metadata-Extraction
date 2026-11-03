
import pandas as pd
from pathlib import Path

# Dataset paths
train_path = Path("data/train.csv")
test_path = Path("data/test.csv")

# Check files
if not train_path.exists() or not test_path.exists():
    raise FileNotFoundError("Check whether train.csv and test.csv exist inside data/")

# Read CSV files
train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

print("\n========== TRAINING DATASET ==========")
print("Shape:", train_df.shape)
print("\nColumns:")
print(train_df.columns.tolist())

print("\nTraining records:")
print(train_df.to_string(index=False))

print("\nMissing values in training data:")
print(train_df.isnull().sum())

print("\n========== TEST DATASET ==========")
print("Shape:", test_df.shape)
print("\nColumns:")
print(test_df.columns.tolist())

print("\nTesting records:")
print(test_df.to_string(index=False))

print("\nMissing values in testing data:")
print(test_df.isnull().sum())

# Check which training files actually exist
print("\n========== TRAINING FILE CHECK ==========")

for filename in train_df.iloc[:, 0]:
    matches = list(Path("data/train").glob(f"{filename}.*"))
    print(filename, "->", "Found" if matches else "Not found")

print("\nDataset inspection completed!")
