from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

from config import (
    COLLECTION_NAME,
    CONNECTION_STRING,
    GOOGLE_API_KEY,
    GOOGLE_EMBEDDING_MODEL,
    get_pdf_path,
)

def ingest_pdf():
    pdf_path = get_pdf_path()
    print(f"Ingesting PDF from path: {pdf_path}")

    # --- 1. Load PDF ---
    loader = PyPDFLoader("example.pdf")
    documents = loader.load()

    # --- 2. Split into chunks ---
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(documents)

    # --- 3. Google Embeddings ---
    embeddings = GoogleGenerativeAIEmbeddings(
        model=GOOGLE_EMBEDDING_MODEL,   # current Google embedding model
        google_api_key=GOOGLE_API_KEY,
    )

    # --- 4. Setup Postgres + pgvector ---
    vectorstore = PGVector(
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )

    # --- 5. Ingest into pgvector ---
    vectorstore.add_documents(docs)

    print("✅ PDF ingested with Google embeddings + stored in Postgres/pgvector")

if __name__ == "__main__":
    ingest_pdf()