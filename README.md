# AI-Based Rental Agreement Metadata Extraction

An AI-powered application that extracts important metadata from rental agreements using Optical Character Recognition (OCR) and Large Language Models (LLMs). The system supports scanned images and DOCX documents and provides structured output through a user-friendly Streamlit interface.

## Project Overview

Rental agreements contain important information such as rental value, agreement dates, renewal notice periods, and details of the involved parties. Extracting this information manually can be time-consuming, especially when documents have different formats and layouts.

This project aims to automate metadata extraction using AI-based semantic understanding rather than relying on fixed templates or hard-coded extraction rules.

The application reads rental agreement documents, processes their content, and extracts the required information into a structured JSON format.

## Objectives

- Extract metadata from rental agreements with different document layouts.
- Support scanned image documents and DOCX files.
- Use OCR to convert scanned documents into machine-readable text.
- Apply an LLM for semantic metadata extraction.
- Generate structured JSON output.
- Evaluate extraction performance using field-wise exact-match recall.

## Metadata Fields

The system extracts the following six fields:

| Field | Description |
|---|---|
| Agreement Value | Rental amount mentioned in the agreement |
| Agreement Start Date | Commencement date of the rental agreement |
| Agreement End Date | Explicitly mentioned end date |
| Renewal Notice (Days) | Notice period related to renewal |
| Party One | Landlord, owner, or lessor |
| Party Two | Tenant, resident, or lessee |

## Technologies Used

- Python
- Ollama
- Qwen 2.5 7B
- Tesseract OCR
- Pytesseract
- Python-docx
- Streamlit
- Pandas
- JSON

## System Workflow

1. **Document Upload:** The user uploads a rental agreement in a supported format.
2. **Document Reading:** DOCX content is extracted using Python-docx.
3. **OCR Processing:** Tesseract OCR converts scanned document images into text.
4. **AI-Based Extraction:** The extracted text is passed to the Qwen 2.5 7B language model through Ollama.
5. **Metadata Generation:** The model identifies the six required fields and generates structured JSON output.
6. **Evaluation:** Predictions are compared against the provided ground-truth labels using field-wise exact-match recall.

## Architecture

```text
       Rental Agreement
        (DOCX / Image)
               |
               v
       Document Reader
               |
        +------+------+
        |             |
        v             v
     DOCX Reader    Tesseract OCR
        |             |
        +------+------+
               |
               v
        Extracted Text
               |
               v
       Qwen 2.5 7B LLM
           (Ollama)
               |
               v
       Metadata Extraction
               |
               v
        Structured JSON
               |
               v
       Streamlit Interface
               |
               v
        Extraction Results
```

## Application Screenshots

### 1. Application Home Page

<!-- Add your home-page screenshot here -->

<img width="1901" height="1016" alt="Screenshot 2026-11-03 214619" src="https://github.com/user-attachments/assets/a86cc091-e5c3-44fa-9f27-167cc2115571" />


### 2. Document Upload

<!-- Add your document upload screenshot here -->

<img width="941" height="707" alt="Screenshot 2026-11-03 214708" src="https://github.com/user-attachments/assets/cd4ca1c5-8e06-42f7-a435-29d3c59601dd" />


### 3. Metadata Extraction Results

<!-- Add your extraction results screenshot here -->

<img width="1872" height="887" alt="Screenshot 2026-11-03 215635" src="https://github.com/user-attachments/assets/4a994465-9e22-4c2a-80be-70eb7cafe59e" />


### 4. Structured JSON Output

<!-- Add your JSON output screenshot here -->

<img width="700" height="328" alt="Screenshot 2026-11-03 215820" src="https://github.com/user-attachments/assets/38734040-d15c-49e7-9e69-a83c447385ea" />


## Demo Video

Watch the application demonstration:

**[Click here to watch the project demo](https://drive.google.com/file/d/1V7O8dY9vkZYJAYL7i_F3LvVNuf9nOeue/view?usp=sharing)

The demonstration covers document upload, document processing, AI-based metadata extraction, and structured output generation.

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Ollama
- Tesseract OCR
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/shruthithammi/AI-Based-Rental-Agreement-Metadata-Extraction.git
cd AI-Based-Rental-Agreement-Metadata-Extraction
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Run Ollama

Install Ollama from:

https://ollama.com/

Download the model:

```bash
ollama pull qwen2.5:7b
```

Make sure the Ollama service is running before using the application.

### 5. Configure Tesseract OCR

Install Tesseract OCR:

https://github.com/UB-Mannheim/tesseract/wiki

On Windows, configure the executable path in the document reader if required:

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

### 6. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to access the application.

### 7. Run the Command-Line Version

```bash
python main.py
```

Enter the rental agreement document path when prompted.

## Model Evaluation

The system uses field-wise exact-match recall to evaluate extraction performance.

**Formula:**

Recall = Correct Predictions / Total Evaluated Predictions

A prediction is counted as correct only when the extracted value matches the corresponding ground-truth value after the evaluation script's basic normalization.

### Test Set Results

| Metadata Field | Correct | Evaluated | Recall |
|---|---:|---:|---:|
| Agreement Value | 4 | 4 | 100% |
| Agreement Start Date | 4 | 4 | 100% |
| Agreement End Date | 2 | 4 | 50% |
| Renewal Notice (Days) | 4 | 4 | 100% |
| Party One | 1 | 4 | 25% |
| Party Two | 0 | 4 | 0% |

These results reflect the current evaluation run. The test predictions were generated independently before comparison with the test ground-truth labels.

### Evaluation Scripts

Run training extraction:

```bash
python run_training_extraction.py
```

Evaluate training results:

```bash
python evaluate_training.py
```

Generate test predictions:

```bash
python run_test_extraction.py
```

Evaluate test predictions:

```bash
python evaluate_test.py
```

The evaluation reports are generated under the `outputs/` directory when the scripts are run.

## Project Structure

```text
AI-Based-Rental-Agreement-Metadata-Extraction/
│
├── src/
│   ├── __init__.py
│   ├── document_reader.py
│   └── metadata_extractor.py
│
├── docs/
│   └── screenshots/
│
├── app.py
├── main.py
├── audit_dataset.py
├── audit_source_documents.py
├── inspect_dataset.py
├── run_training_extraction.py
├── evaluate_training.py
├── run_test_extraction.py
├── evaluate_test.py
├── test_document_reader.py
├── test_environment.py
├── test_image_reader.py
├── test_metadata_extractor.py
├── requirements.txt
└── README.md
```

## Limitations

- Extraction accuracy depends on document quality and OCR readability.
- Different agreement formats and writing styles may affect model predictions.
- Names and party details can be difficult to identify when documents contain multiple individuals or inconsistent naming.
- Some agreements do not explicitly mention an end date or renewal notice period.
- The system does not calculate missing agreement dates from rental duration.

## Future Improvements

- Improve extraction accuracy for party names and legal entities.
- Support additional document formats.
- Improve OCR performance for low-quality scanned agreements.
- Evaluate on a larger and more diverse collection of rental agreements.
- Improve handling of ambiguous legal clauses.

## Author

**Shruthi Thammi**

GitHub: https://github.com/shruthithammi

---

*This project was developed as an AI/ML assignment focused on automated metadata extraction from rental agreements.*
