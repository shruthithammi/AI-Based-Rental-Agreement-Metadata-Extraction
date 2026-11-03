from pathlib import Path
import json
import csv

from src.document_reader import read_document
from src.metadata_extractor import extract_metadata, REQUIRED_FIELDS


TEST_DIR = Path("data/test")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

SUPPORTED_FORMATS = {".docx", ".png", ".jpg", ".jpeg"}

results = []

documents = sorted(
    file for file in TEST_DIR.iterdir()
    if file.is_file() and file.suffix.lower() in SUPPORTED_FORMATS
)

if not documents:
    raise FileNotFoundError("No supported test documents found.")

for document_path in documents:
    print(f"\nProcessing: {document_path.name}")

    try:
        document_text = read_document(document_path)
        metadata = extract_metadata(document_text)

        # Remove the extra .pdf part from filenames ending in .pdf.docx
        file_name = document_path.name
        if file_name.lower().endswith(".pdf.docx"):
            file_name = file_name[:-len(".pdf.docx")]
        else:
            file_name = document_path.stem

        record = {
            "File Name": file_name,
            **{field: metadata.get(field) for field in REQUIRED_FIELDS}
        }

        results.append(record)
        print("Extraction completed.")

    except Exception as error:
        print(f"Failed: {error}")

# Save JSON predictions
json_path = OUTPUT_DIR / "test_predictions.json"

with open(json_path, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

# Save CSV predictions
csv_path = OUTPUT_DIR / "test_predictions.csv"

columns = ["File Name"] + REQUIRED_FIELDS

with open(csv_path, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(results)

print("\nTEST EXTRACTION SUMMARY")
print("=======================")
print(f"Documents found: {len(documents)}")
print(f"Documents processed: {len(results)}")
print(f"JSON saved: {json_path}")
print(f"CSV saved: {csv_path}")
