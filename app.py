import streamlit as st
import PyPDF2
from summarizer import Summarizer
import spacy

# Load SpaCy model
try:
    nlp = spacy.load('en_core_web_md')
except OSError:
    st.write("Downloading SpaCy model...")
    from spacy.cli import download
    download('en_core_web_md')
    nlp = spacy.load('en_core_web_md')

# Initialize BERT summarizer
model = Summarizer()

st.title("PDF Summarization Tool")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# Summarize using BERT
def summarize_text(text):
    try:
        summary = model.summarize(text, min_length=60)  # ✅ Corrected usage
        return summary
    except Exception as e:
        st.error(f"Summarization failed: {e}")
        return ""

# Main logic
if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)

    if pdf_text:
        st.subheader("Original Text")
        st.write(pdf_text)

        if st.button("Summarize"):
            summary = summarize_text(pdf_text)
            if summary:
                st.subheader("Summary")
                st.write(summary)
    else:
        st.warning("No text extracted from PDF.")
else:
    st.info("Upload a PDF file to begin.")




