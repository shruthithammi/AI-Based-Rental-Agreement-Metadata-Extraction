import json
import html
import tempfile
from pathlib import Path

import streamlit as st

from src.document_reader import read_document
from src.metadata_extractor import extract_metadata


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="LEASE AI | Rental Agreement Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# PROFESSIONAL DARK THEME
# ==========================================================

st.html("""
<style>
    /* Main application */
    .stApp {
        background: #080D18;
        color: #F1F5F9;
    }

    [data-testid="stHeader"] {
        background: #080D18;
    }

    [data-testid="stSidebar"] {
        background: #101827;
        border-right: 1px solid #263449;
    }

    [data-testid="stSidebar"] * {
        color: #E2E8F0;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    .brand-label {
        color: #60A5FA;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 3px;
        margin-bottom: 18px;
    }

    .brand-title {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .brand-subtitle {
        color: #94A3B8;
        font-size: 13px;
    }

    .sidebar-heading {
        color: #F8FAFC;
        font-size: 13px;
        font-weight: 750;
        letter-spacing: 1px;
        margin: 25px 0 12px;
    }

    .sidebar-info {
        color: #94A3B8;
        font-size: 13px;
        line-height: 2.2;
    }

    .sidebar-divider {
        border-top: 1px solid #263449;
        margin: 28px 0;
    }

    /* Hero */
    .hero {
        background: linear-gradient(
            120deg,
            #142B52,
            #1746A2,
            #2563EB
        );
        border: 1px solid #315BA8;
        border-radius: 18px;
        padding: 42px;
        margin-bottom: 38px;
    }

    .hero-label {
        color: #BFDBFE;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 3px;
        margin-bottom: 18px;
    }

    .hero-title {
        color: #FFFFFF;
        font-size: 34px;
        font-weight: 800;
        line-height: 1.3;
        margin-bottom: 13px;
    }

    .hero-description {
        color: #DBEAFE;
        font-size: 15px;
        line-height: 1.8;
    }

    /* Section labels */
    .section-label {
        color: #60A5FA;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }

    /* Information cards */
    .info-card {
        background: #111B2B;
        border: 1px solid #263449;
        border-radius: 14px;
        padding: 24px;
    }

    .info-title {
        color: #F8FAFC;
        font-size: 17px;
        font-weight: 750;
        margin-bottom: 15px;
    }

    .info-item {
        color: #A9B8CC;
        font-size: 14px;
        padding: 11px 0;
        border-bottom: 1px solid #263449;
    }

    .info-item:last-child {
        border-bottom: none;
    }

    /* Metadata cards */
    .metadata-card {
        background: #111B2B;
        border: 1px solid #263449;
        border-radius: 13px;
        padding: 23px;
        min-height: 125px;
        margin-bottom: 16px;
    }

    .metadata-label {
        color: #94A3B8;
        font-size: 12px;
        font-weight: 750;
        letter-spacing: 0.5px;
        margin-bottom: 13px;
    }

    .metadata-value {
        color: #F8FAFC;
        font-size: 19px;
        font-weight: 650;
        line-height: 1.5;
        overflow-wrap: anywhere;
    }

    .metadata-missing {
        color: #FBBF24;
        font-size: 16px;
        font-weight: 600;
    }

    /* Upload area */
    [data-testid="stFileUploader"] {
        background: #111B2B;
        border: 1px dashed #3B82F6;
        border-radius: 12px;
        padding: 15px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(
            90deg,
            #2563EB,
            #3B82F6
        );
        color: #FFFFFF;
        border: none;
        border-radius: 9px;
        min-height: 47px;
        font-size: 15px;
        font-weight: 700;
        width: 100%;
    }

    .stButton > button:hover {
        background: #1D4ED8;
        color: #FFFFFF;
        border: 1px solid #60A5FA;
    }

    .stDownloadButton > button {
        background: #17243A;
        color: #FFFFFF;
        border: 1px solid #3B82F6;
        border-radius: 9px;
        font-weight: 650;
    }

    /* Text */
    h1, h2, h3, h4 {
        color: #F8FAFC !important;
    }

    p, label {
        color: #CBD5E1;
    }

    [data-testid="stCaptionContainer"] {
        color: #94A3B8;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748B;
        font-size: 12px;
        line-height: 2;
        padding-top: 28px;
        margin-top: 45px;
        border-top: 1px solid #263449;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }
</style>
""")


# ==========================================================
# HTML RENDERING HELPER
# ==========================================================

def render_html(content):
    """Render HTML directly without Markdown code-block parsing."""
    st.html(content)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    render_html("""
        <div class="brand-label">DOCUMENT INTELLIGENCE</div>
        <div class="brand-title">LEASE AI</div>
        <div class="brand-subtitle">Rental Agreement Analyzer</div>
        <div class="sidebar-divider"></div>
        <div class="sidebar-heading">WORKSPACE</div>
    """)

    page = st.radio(
        "Navigation",
        ["Metadata Extraction", "About Project"],
        label_visibility="collapsed"
    )

    render_html("""
        <div class="sidebar-divider"></div>
        <div class="sidebar-heading">AI CONFIGURATION</div>
        <div class="sidebar-info">
            Language Model: Qwen 2.5 7B<br>
            Runtime: Ollama<br>
            Document Reading: OCR / DOCX<br>
            Extraction: AI Semantic Analysis
        </div>
        <div class="sidebar-divider"></div>
        <div class="sidebar-info">
            AI-Based Rental Agreement<br>
            Metadata Extraction
        </div>
    """)


# ==========================================================
# HERO SECTION
# ==========================================================

def show_hero():

    render_html("""
        <div class="hero">
            <div class="hero-label">
                AI DOCUMENT PROCESSING
            </div>

            <div class="hero-title">
                Rental Agreement Metadata Extraction
            </div>

            <div class="hero-description">
                Extract six important fields from rental agreements
                using AI-powered semantic analysis. Upload a document
                and receive structured metadata.
            </div>
        </div>
    """)


# ==========================================================
# METADATA DISPLAY
# ==========================================================

def display_metadata(metadata, filename):

    fields = [
        "Agreement Value",
        "Agreement Start Date",
        "Agreement End Date",
        "Renewal Notice (Days)",
        "Party One",
        "Party Two"
    ]

    st.divider()

    render_html("""
        <div class="section-label">EXTRACTION RESULTS</div>
    """)

    st.subheader("Extracted Metadata")
    st.caption(f"Source document: {filename}")

    columns = st.columns(2, gap="large")

    for index, field in enumerate(fields):

        value = metadata.get(field)

        if value is None or str(value).strip() == "":
            value_text = "Not found"
            value_class = "metadata-missing"
        else:
            value_text = html.escape(str(value))
            value_class = "metadata-value"

        safe_field = html.escape(field)

        card_html = f"""
            <div class="metadata-card">
                <div class="metadata-label">
                    {safe_field}
                </div>
                <div class="{value_class}">
                    {value_text}
                </div>
            </div>
        """

        with columns[index % 2]:
            render_html(card_html)

    st.subheader("Export Results")

    json_data = json.dumps(
        {
            "document": filename,
            "extracted_metadata": metadata
        },
        indent=4,
        ensure_ascii=False
    )

    st.download_button(
        label="⬇ Download Metadata as JSON",
        data=json_data,
        file_name="rental_agreement_metadata.json",
        mime="application/json",
        width="content"
    )


# ==========================================================
# METADATA EXTRACTION PAGE
# ==========================================================

if page == "Metadata Extraction":

    show_hero()

    render_html("""
        <div class="section-label">DOCUMENT WORKSPACE</div>
    """)

    st.title("Document Processing")

    st.caption(
        "Upload a scanned rental agreement or DOCX document "
        "to extract the six required metadata fields."
    )

    left_column, right_column = st.columns(
        [1.7, 1],
        gap="large"
    )

    with left_column:

        st.subheader("Upload Agreement")

        uploaded_file = st.file_uploader(
            "Select your rental agreement",
            type=["docx", "png", "jpg", "jpeg"],
            help="Supported formats: DOCX, PNG, JPG and JPEG"
        )

        if uploaded_file:

            st.success(
                f"Document selected: {uploaded_file.name}"
            )

            file_size = uploaded_file.size / (1024 * 1024)

            st.caption(f"File size: {file_size:.2f} MB")

            extract_button = st.button(
                "Extract Metadata",
                width="stretch"
            )

            if extract_button:

                temporary_path = None

                try:

                    with st.spinner(
                        "Reading document and extracting metadata using AI..."
                    ):

                        suffix = Path(
                            uploaded_file.name
                        ).suffix.lower()

                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=suffix
                        ) as temporary_file:

                            temporary_file.write(
                                uploaded_file.getvalue()
                            )

                            temporary_path = Path(
                                temporary_file.name
                            )

                        # Step 1: Read document using existing reader
                        document_text = read_document(
                            str(temporary_path)
                        )

                        if not document_text or not document_text.strip():
                            raise ValueError(
                                "No readable text found in the document."
                            )

                        # Step 2: AI semantic extraction
                        metadata = extract_metadata(document_text)

                        if not isinstance(metadata, dict):
                            raise ValueError(
                                "AI did not return a valid metadata dictionary."
                            )

                        # Step 3: Retain exactly the six required fields
                        required_fields = [
                            "Agreement Value",
                            "Agreement Start Date",
                            "Agreement End Date",
                            "Renewal Notice (Days)",
                            "Party One",
                            "Party Two"
                        ]

                        metadata = {
                            field: metadata.get(field)
                            for field in required_fields
                        }

                        st.session_state["metadata"] = metadata
                        st.session_state["filename"] = uploaded_file.name

                    st.success(
                        "Metadata extraction completed successfully."
                    )

                except Exception as error:

                    st.error(f"Extraction failed: {error}")

                finally:

                    if temporary_path and temporary_path.exists():
                        temporary_path.unlink()

    with right_column:

        st.subheader("Extraction Information")

        render_html("""
            <div class="info-card">

                <div class="info-title">
                    Supported Documents
                </div>

                <div class="info-item">DOCX documents</div>
                <div class="info-item">Scanned PNG images</div>
                <div class="info-item">JPG and JPEG images</div>

                <br>

                <div class="info-title">
                    Extraction Pipeline
                </div>

                <div class="info-item">
                    01 &nbsp; Document reading
                </div>

                <div class="info-item">
                    02 &nbsp; AI semantic analysis
                </div>

                <div class="info-item">
                    03 &nbsp; Structured metadata
                </div>

                <div class="info-item">
                    04 &nbsp; JSON export
                </div>

            </div>
        """)

    # Show extraction results
    if "metadata" in st.session_state:

        display_metadata(
            st.session_state["metadata"],
            st.session_state["filename"]
        )


# ==========================================================
# ABOUT PROJECT PAGE
# ==========================================================

elif page == "About Project":

    show_hero()

    st.title("About the Project")

    st.write(
        """
        This project uses AI-based semantic analysis to extract
        structured metadata from rental agreement documents.
        """
    )

    st.subheader("Project Objective")

    st.write(
        """
        Automatically identify six required metadata fields
        from different rental agreement formats.
        """
    )

    st.subheader("Metadata Fields")

    st.markdown("""
    1. Agreement Value
    2. Agreement Start Date
    3. Agreement End Date
    4. Renewal Notice (Days)
    5. Party One
    6. Party Two
    """)

    st.subheader("Technology Stack")

    st.markdown("""
    - Python
    - Streamlit
    - Ollama
    - Qwen 2.5 7B
    - Tesseract OCR
    - python-docx
    """)

    st.subheader("Processing Workflow")

    st.markdown("""
    1. Upload a scanned image or DOCX document.
    2. Read document content using OCR or DOCX parsing.
    3. Send the extracted text to the AI model.
    4. Extract the six required metadata fields.
    5. Display and download the structured JSON results.
    """)


# ==========================================================
# FOOTER
# ==========================================================

render_html("""
    <div class="footer">
        LEASE AI | AI-Based Rental Agreement Metadata Extraction
        <br>
        Powered by Python, Streamlit and Ollama
    </div>
""")
