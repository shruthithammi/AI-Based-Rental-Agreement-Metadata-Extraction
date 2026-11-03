
from pathlib import Path

from src.document_reader import read_document
from src.metadata_extractor import extract_metadata


document_path = Path(
    "data/train/36199312-Rental-Agreement.png"
)

print("Reading rental agreement...")

document_text = read_document(document_path)

print("Running AI metadata extraction...")

metadata = extract_metadata(document_text)

print("\nExtracted Metadata")
print("-" * 50)

for field, value in metadata.items():
    print(f"{field}: {value}")
