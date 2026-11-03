
import json
from pathlib import Path

import pandas as pd


LABELS_PATH = Path("data/test.csv")
PREDICTIONS_PATH = Path("outputs/test_predictions.json")
OUTPUT_PATH = Path("outputs/test_recall_report.csv")

FIELD_MAPPING = {
    "Agreement Value": "Aggrement Value",
    "Agreement Start Date": "Aggrement Start Date",
    "Agreement End Date": "Aggrement End Date",
    "Renewal Notice (Days)": "Renewal Notice (Days)",
    "Party One": "Party One",
    "Party Two": "Party Two",
}


def is_missing(value):
    return pd.isna(value) or str(value).strip() == ""


def normalize(value, field):
    if is_missing(value):
        return None

    value = str(value).strip().lower()

    if field in ["Agreement Value", "Renewal Notice (Days)"]:
        try:
            return str(float(value)).rstrip("0").rstrip(".")
        except ValueError:
            return value

    return value


labels = pd.read_csv(LABELS_PATH)

with open(PREDICTIONS_PATH, "r", encoding="utf-8") as file:
    predictions = pd.DataFrame(json.load(file))

merged = labels.merge(
    predictions,
    on="File Name",
    how="inner",
    suffixes=("_actual", "_predicted")
)

print(f"Matched test documents: {len(merged)}")

report = []
summary = []

for predicted_field, actual_field in FIELD_MAPPING.items():

    actual_col = (
        f"{actual_field}_actual"
        if f"{actual_field}_actual" in merged.columns
        else actual_field
    )

    predicted_col = (
        f"{predicted_field}_predicted"
        if f"{predicted_field}_predicted" in merged.columns
        else predicted_field
    )

    correct = 0
    evaluated = 0

    for _, row in merged.iterrows():

        actual = row[actual_col]
        predicted = row[predicted_col]

        if is_missing(actual):
            continue

        evaluated += 1

        actual_normalized = normalize(actual, predicted_field)
        predicted_normalized = normalize(predicted, predicted_field)

        match = actual_normalized == predicted_normalized

        if match:
            correct += 1

        report.append({
            "File Name": row["File Name"],
            "Field": predicted_field,
            "Actual": actual,
            "Predicted": predicted,
            "Correct": match
        })

    recall = correct / evaluated * 100 if evaluated else 0

    summary.append({
        "Field": predicted_field,
        "Correct": correct,
        "Evaluated": evaluated,
        "Recall (%)": round(recall, 2)
    })

    print(f"\n{predicted_field}")
    print(f"Correct: {correct}/{evaluated}")
    print(f"Recall: {recall:.2f}%")


pd.DataFrame(report).to_csv(OUTPUT_PATH, index=False)

summary_path = Path("outputs/test_recall_summary.csv")
pd.DataFrame(summary).to_csv(summary_path, index=False)

print("\nFINAL TEST RECALL SUMMARY")
print(pd.DataFrame(summary).to_string(index=False))

print("\nDetailed report saved:", OUTPUT_PATH)
print("Summary saved:", summary_path)
