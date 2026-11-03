import json
from pathlib import Path

import pandas as pd

CSV_PATH = Path("data/train.csv")
PREDICTIONS_PATH = Path("outputs/training_extraction_results.json")

FIELD_MAPPING = {
    "Agreement Value": "Aggrement Value",
    "Agreement Start Date": "Aggrement Start Date",
    "Agreement End Date": "Aggrement End Date",
    "Renewal Notice (Days)": "Renewal Notice (Days)",
    "Party One": "Party One",
    "Party Two": "Party Two",
}


def normalize(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value.endswith(".0") and value[:-2].isdigit():
        value = value[:-2]

    return value.casefold() if value else None


train_df = pd.read_csv(CSV_PATH)

with open(PREDICTIONS_PATH, "r", encoding="utf-8") as file:
    predictions = json.load(file)

predictions_df = pd.DataFrame(predictions)

merged = train_df.merge(
    predictions_df,
    on="File Name",
    how="inner",
    suffixes=("_actual", "_predicted")
)

print("Matched labelled documents:", len(merged))
print("\nFIELD-WISE EVALUATION")
print("=" * 65)

evaluation = []

for predicted_field, actual_field in FIELD_MAPPING.items():

    if actual_field == predicted_field:
        actual_column = f"{actual_field}_actual"
        predicted_column = f"{predicted_field}_predicted"
    else:
        actual_column = actual_field
        predicted_column = predicted_field

    correct = 0
    total = 0

    print(f"\n{predicted_field}")

    for _, row in merged.iterrows():
        actual = normalize(row[actual_column])
        predicted = normalize(row[predicted_column])

        if actual is None:
            continue

        total += 1

        if actual == predicted:
            correct += 1
        else:
            print(
                f"  MISMATCH | {row['File Name']}"
                f" | Actual: {actual}"
                f" | Predicted: {predicted}"
            )

    recall = correct / total if total else 0

    evaluation.append({
        "Field": predicted_field,
        "Correct": correct,
        "Evaluated": total,
        "Recall (%)": round(recall * 100, 2),
    })

    print(f"  Correct: {correct}/{total}")
    print(f"  Recall: {recall * 100:.2f}%")

report = pd.DataFrame(evaluation)

print("\nFINAL RECALL SUMMARY")
print("=" * 65)
print(report.to_string(index=False))

report.to_csv(
    "outputs/training_recall_report.csv",
    index=False
)

print("\nSaved: outputs/training_recall_report.csv")