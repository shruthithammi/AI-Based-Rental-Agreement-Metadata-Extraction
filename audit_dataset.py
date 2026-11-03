
import pandas as pd
from pathlib import Path
from datetime import datetime
import hashlib

# Dataset paths
train_csv = pd.read_csv("data/train.csv", dtype={"File Name": str})
test_csv = pd.read_csv("data/test.csv", dtype={"File Name": str})

train_folder = Path("data/train")
test_folder = Path("data/test")


def find_document(filename):
    """Find a document in either dataset folder."""

    train_matches = list(train_folder.glob(filename + ".*"))
    test_matches = list(test_folder.glob(filename + ".*"))

    return train_matches, test_matches


def get_hash(file_path):
    """Calculate SHA256 to compare document files."""

    sha = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha.update(chunk)

    return sha.hexdigest()


print("\n========== DOCUMENT AVAILABILITY ==========")

for _, row in train_csv.iterrows():

    filename = row["File Name"]
    train_files, test_files = find_document(filename)

    if train_files:
        print(f"{filename}: Found in TRAIN")

    elif test_files:
        print(f"{filename}: Found only in TEST folder")

    else:
        print(f"{filename}: DOCUMENT NOT FOUND")


print("\n========== TRAIN / TEST OVERLAP ==========")

train_names = set(train_csv["File Name"].str.strip())
test_names = set(test_csv["File Name"].str.strip())

overlap = train_names.intersection(test_names)

if overlap:
    for name in sorted(overlap):
        print("Duplicate record ID:", name)

        train_files, test_files = find_document(name)

        if train_files and test_files:
            for train_file in train_files:
                for test_file in test_files:
                    if get_hash(train_file) == get_hash(test_file):
                        print("  Exact same document in both folders!")
                    else:
                        print("  Files differ; inspect both documents.")

        elif test_files:
            print("  Source file exists only in TEST folder.")

        elif train_files:
            print("  Source file exists only in TRAIN folder.")
else:
    print("No overlapping record IDs found.")


print("\n========== INVALID DATE LABELS ==========")

date_columns = [
    "Aggrement Start Date",
    "Aggrement End Date"
]

for dataset_name, df in [
    ("TRAIN", train_csv),
    ("TEST", test_csv)
]:

    for column in date_columns:

        for _, row in df.iterrows():

            value = row[column]

            try:
                datetime.strptime(str(value).strip(), "%d.%m.%Y")

            except (ValueError, TypeError):
                print(
                    f"{dataset_name} | {row['File Name']} | "
                    f"{column} | Invalid value: {value}"
                )


print("\n========== MISSING VALUES ==========")

print("\nTraining:")
print(train_csv.isnull().sum())

print("\nTesting:")
print(test_csv.isnull().sum())

print("\nDataset audit completed!")
