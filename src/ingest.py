import os
from dotenv import load_dotenv
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_postgres import PGVector

import psycopg

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION = os.getenv("PG_VECTOR_COLLECTION_NAME")

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER").lower()
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 150))

def _ensure_vector_extension():
    """Cria a extensão pgvector."""
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL não definido no .env")    
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        conn.commit()

def _get_embeddings():
    if EMBEDDING_PROVIDER == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY não definido no .env")
        return OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL, api_key=api_key)

    if EMBEDDING_PROVIDER == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY não definido no .env")
        return GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL, google_api_key=api_key)
    raise ValueError("EMBEDDING_PROVIDER deve ser 'openai' ou 'gemini'")

def _load_and_split_pdf() -> List:
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF não encontrado em {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(docs)

def ingest_pdf():
    print("1. Preparando banco de dados - pgvector")
    _ensure_vector_extension()


    print("2. Carregando e chunkando PDF…")
    chunks = _load_and_split_pdf()
    print(f" - Chunks gerados: {len(chunks)}")


    print("3. Inicializando embeddings…")
    embeddings = _get_embeddings()


    print(f"4. Gravando no Postgres (coleção='{COLLECTION}')…")    
    vectorstore = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION,
        connection=DATABASE_URL,
        use_jsonb=True,
    )
    
    print("\n\nIngestão concluída!")

if __name__ == "__main__":
    ingest_pdf()