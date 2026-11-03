
from pathlib import Path
from src.document_reader import read_document

TRAIN_FOLDER = Path("data/train")

DOCUMENTS_TO_CHECK = [
    "18325926-Rental-Agreement-1",
    "36199312-Rental-Agreement",
    "47854715-RENTAL-AGREEMENT",
    "44737744-Maddireddy-Bhargava-Reddy-Rental-Agreement",
]

output_folder = Path("outputs")
output_folder.mkdir(exist_ok=True)

for document_name in DOCUMENTS_TO_CHECK:

    print("\n" + "=" * 80)
    print("DOCUMENT:", document_name)
    print("=" * 80)

    matching_files = [
        path for path in TRAIN_FOLDER.glob("*")
        if path.is_file() and path.stem == document_name
    ]

    if not matching_files:
        print("Document not found in training folder.")
        continue

    file_path = matching_files[0]

    try:
        extracted_text = read_document(file_path)

        print(extracted_text)

        # Save extracted text for detailed inspection
        output_file = output_folder / f"{document_name}.txt"
        output_file.write_text(
            extracted_text,
            encoding="utf-8"
        )

        print("\nSaved extracted text to:", output_file)

    except Exception as error:
        print("Error reading document:", error)

print("\nSource document audit completed!")
