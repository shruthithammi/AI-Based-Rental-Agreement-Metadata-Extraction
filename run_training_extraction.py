from pathlib import Path
import json

import pandas as pd

from src.document_reader import read_document
from src.metadata_extractor import extract_metadata


TRAIN_DIR = Path("data/train")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

results = []

documents = sorted(
    file for file in TRAIN_DIR.rglob("*")
    if file.suffix.lower() in [".docx", ".png", ".jpg", ".jpeg"]
)

for document_path in documents:
    print(f"\nProcessing: {document_path.name}")

    try:
        document_text = read_document(document_path)
        metadata = extract_metadata(document_text)

        results.append({
            "File Name": document_path.stem,
            **metadata
        })

        print("Extraction completed.")

    except Exception as error:
        print(f"Failed: {error}")

output_path = OUTPUT_DIR / "training_extraction_results.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

print(f"\nProcessed documents: {len(results)}")
print(f"Results saved to: {output_path}")