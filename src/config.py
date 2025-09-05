import os
from dotenv import load_dotenv
load_dotenv()

COLLECTION_NAME = os.getenv("COLLECTION_NAME")
CONNECTION_STRING = os.getenv("DATABASE_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL","models/embedding-001")
PDF_PATH = os.getenv("PDF_PATH")

def get_pdf_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_dir, os.getenv("PDF_PATH"))

    if not PDF_PATH or not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF file not found at path: {pdf_path}")

    return pdf_path

