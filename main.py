
import json
from pathlib import Path

from src.document_reader import read_document
from src.metadata_extractor import extract_metadata


def main():
    print("\nAI-Based Rental Agreement Metadata Extraction")
    print("-" * 50)

    file_path = input("Enter the rental agreement file path: ").strip()
    file_path = Path(file_path.strip('"'))

    if not file_path.exists():
        print("Error: File not found.")
        return

    supported_formats = [".docx", ".png", ".jpg", ".jpeg"]

    if file_path.suffix.lower() not in supported_formats:
        print("Error: Supported formats are DOCX, PNG, JPG and JPEG.")
        return

    try:
        # Step 1: Read document text
        print("\nReading document...")
        document_text = read_document(str(file_path))

        if not document_text or not document_text.strip():
            print("Error: No text could be extracted from the document.")
            return

        # Step 2: Extract metadata using the AI model
        print("Extracting metadata using AI...")
        metadata = extract_metadata(document_text)

        # Step 3: Display results
        print("\nExtracted Metadata")
        print("-" * 50)

        for field, value in metadata.items():
            print(f"{field}: {value}")

        # Step 4: Save results
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / f"{file_path.stem}_metadata.json"

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=4, ensure_ascii=False)

        print("\nExtraction completed successfully.")
        print(f"Results saved to: {output_file}")

    except Exception as error:
        print(f"\nAn error occurred: {error}")


if __name__ == "__main__":
    main()
