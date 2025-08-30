import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

# Get config from environment variables
PDF_PATH = os.getenv("PDF_PATH")
CONNECTION_STRING = os.getenv("PGVECTOR_CONNECTION_STRING")
COLLECTION_NAME = os.getenv("PGVECTOR_COLLECTION_NAME")

def ingest_pdf():
    """
    Ingests a PDF document into a PGVector store.
    It loads the PDF, splits it into chunks, creates embeddings,
    and stores them in the specified PostgreSQL collection.
    """
    if not all([PDF_PATH, CONNECTION_STRING, COLLECTION_NAME, os.getenv("GOOGLE_API_KEY")]):
        print("Erro: Verifique se as variáveis de ambiente PDF_PATH, PGVECTOR_CONNECTION_STRING, PGVECTOR_COLLECTION_NAME e GOOGLE_API_KEY estão definidas.")
        return

    if not os.path.exists(PDF_PATH):
        print(f"Erro: Arquivo PDF não encontrado em '{PDF_PATH}'")
        return

    print(f"Iniciando ingestão do arquivo: {PDF_PATH}")

    # 1. Carregar o PDF
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"Carregadas {len(documents)} páginas do PDF.")

    # 2. Dividir em chunks conforme os requisitos do desafio
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    print(f"Documento dividido em {len(chunks)} chunks.")

    # 3. Criar embeddings e armazenar no PGVector
    print("Inicializando embeddings do Google GenAI...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    print(f"Criando ou acessando a coleção '{COLLECTION_NAME}' e adicionando documentos...")
    PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        pre_delete_collection=True, # Deleta a coleção antiga para garantir dados frescos
    )

    print("\nIngestão concluída com sucesso!")

if __name__ == "__main__":
    ingest_pdf()