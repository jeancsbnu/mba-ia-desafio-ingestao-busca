import os
from utils import get_database_connection, get_pdf_path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Open document
def open_document(path: str) -> tuple[str, Document]:
    pdf_path = os.path.join(path)
    filename = os.path.basename(pdf_path).replace(" ", "_").lower()
    return filename, PyPDFLoader(pdf_path).load()

# Split it into chunks
def split_document(doc: Document) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(doc)
    return chunks

# Sanitize metadata
def sanitize_chunks(chunks: list[Document]) -> list[Document]:
    return [
        Document(
            page_content=chunk.page_content,
            metadata={k: v for k, v in chunk.metadata.items() if v not in ("", None)}
        )
        for chunk in chunks
    ]

# Embed and store in the vector database
def embed_and_store_documents(chunks: list[Document], filename: str):
    db = get_database_connection()
    ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
    db.add_documents(documents=chunks, ids=ids)

def ingest_pdf():
    print("Iniciando o processo de ingestão do PDF...")
    filename, pdf = open_document(get_pdf_path())
    print(f"Documento '{filename}' carregado com sucesso.")
    print("Dividindo o documento em chunks...")
    chunks = split_document(pdf)
    print(f"{len(chunks)} chunks criados.")
    sanitized = sanitize_chunks(chunks)
    print("Chunks sanitizados.")
    print("Iniciando o processo de embed e armazenamento no banco de dados...")
    embed_and_store_documents(sanitized, filename)
    print("Processo de ingestão concluído com sucesso.")

if __name__ == "__main__":
    ingest_pdf()