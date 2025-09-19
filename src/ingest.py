import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

def main():
    # Verificar variáveis obrigatórias
    for k in ("PGVECTOR_URL", "PGVECTOR_COLLECTION"):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set")

    # Caminho do PDF
    current_dir = Path(__file__).parent.parent
    pdf_path = current_dir / os.getenv("PDF_PATH", "document.pdf")
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")

    print(f"📄 Carregando PDF: {pdf_path}")
    
    # Carregar PDF
    docs = PyPDFLoader(str(pdf_path)).load()
    
    print(f"📑 Carregadas {len(docs)} páginas")
    
    # Dividir em chunks de 1000 caracteres com overlap de 150
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150,
        add_start_index=False
    )
    
    splits = text_splitter.split_documents(docs)
    
    if not splits:
        print("❌ Nenhum documento foi processado")
        raise SystemExit(1)
    
    print(f"📚 Documento dividido em {len(splits)} chunks")

    # Preparar documentos
    enriched = []
    for d in splits:
        metadata = {k: v for k, v in d.metadata.items() if v not in ("", None)}
        enriched.append(Document(
            page_content=d.page_content,
            metadata=metadata
        ))

    # IDs únicos para cada chunk
    ids = [f"doc-{i}" for i in range(len(enriched))]

    print("🤖 Inicializando embeddings locais (HuggingFace)...")
    
    # Usar embeddings locais HuggingFace (mantendo conforme solicitado)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )

    print("🔌 Conectando ao banco vetorial...")
    
    # Configurar PGVector
    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        connection=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
    )

    print("💾 Adicionando documentos ao banco...")
    
    # Adicionar documentos ao banco
    store.add_documents(documents=enriched, ids=ids)

    print(f"✅ Ingestão concluída! {len(enriched)} chunks adicionados ao banco.")
    print(f"📊 Coleção: {os.getenv('PGVECTOR_COLLECTION')}")

if __name__ == "__main__":
    main()












# enriched = []
# for d in splits:
#     meta = {k: v for k, v in d.metadata.items() if v not in ("", None)}
#     new_doc = Document(
#         page_content=d.page_content,
#         metadata=meta
#     )
#     enriched.append(new_doc)