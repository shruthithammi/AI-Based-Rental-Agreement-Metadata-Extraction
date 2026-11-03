
from pathlib import Path
from src.document_reader import read_document

# Training documents folder
train_folder = Path("data/train")

# Find all DOCX documents
docx_files = list(train_folder.glob("*.docx"))

if not docx_files:
    print("No DOCX documents found in data/train")
else:
    # Select the first DOCX document
    file_path = docx_files[0]

    print("Testing document:", file_path.name)

    try:
        text = read_document(file_path)

        print("\n========== EXTRACTED DOCUMENT TEXT ==========\n")
        print(text)

        print("\n========== TEXT LENGTH ==========")
        print("Characters extracted:", len(text))

    except Exception as error:
        print("Error:", error)
