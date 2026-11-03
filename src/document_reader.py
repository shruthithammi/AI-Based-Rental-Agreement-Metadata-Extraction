
from pathlib import Path

import pytesseract
from PIL import Image, ImageOps
from docx import Document


# Tesseract executable location on Windows
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def read_docx(file_path):
    """
    Extract text from DOCX paragraphs, tables,
    headers and footers.
    """

    document = Document(file_path)
    extracted_text = []

    # Read paragraphs
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            extracted_text.append(text)

    # Read tables
    for table in document.tables:
        for row in table.rows:
            row_text = [
                cell.text.strip()
                for cell in row.cells
                if cell.text.strip()
            ]

            if row_text:
                extracted_text.append(" | ".join(row_text))

    # Read headers and footers
    for section in document.sections:

        for paragraph in section.header.paragraphs:
            if paragraph.text.strip():
                extracted_text.append(paragraph.text.strip())

        for paragraph in section.footer.paragraphs:
            if paragraph.text.strip():
                extracted_text.append(paragraph.text.strip())

    return "\n".join(extracted_text)


def read_image(file_path):
    """
    Extract text from scanned images using Tesseract OCR.
    """

    image = Image.open(file_path)

    # Convert image to grayscale
    image = ImageOps.grayscale(image)

    # Improve contrast for OCR
    image = ImageOps.autocontrast(image)

    extracted_text = pytesseract.image_to_string(
        image,
        lang="eng"
    )

    return extracted_text.strip()


def read_document(file_path):
    """
    Read either a DOCX document or a PNG image.
    Returns extracted text.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    extension = file_path.suffix.lower()

    if extension == ".docx":
        return read_docx(file_path)

    elif extension in [".png", ".jpg", ".jpeg"]:
        return read_image(file_path)

    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )
