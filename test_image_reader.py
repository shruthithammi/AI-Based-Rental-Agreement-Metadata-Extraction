from pathlib import Path
from src.document_reader import read_document

document_path = Path(
    "data/train/36199312-Rental-Agreement.png"
)

print("Reading scanned rental agreement...")

document_text = read_document(document_path)

print("\nOCR Extracted Text")
print("=" * 60)
print(document_text)
print("=" * 60)