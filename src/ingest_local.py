import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_postgres import PGVector

# Carregar variáveis do ambiente
load_dotenv()

def main():
    # Configurações
    pdf_path = os.getenv("PDF_PATH", "document.pdf")
    pgvector_url = os.getenv("PGVECTOR_URL", "postgresql://postgres:postgres@localhost:5432/rag")
    collection_name = os.getenv("PGVECTOR_COLLECTION", "documents")
    
    print(f"📄 Carregando PDF: {pdf_path}")
    
    # Carregar e dividir o documento
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    print(f"📑 Carregadas {len(documents)} páginas")
    
    # Dividir em chunks menores
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    
    split_docs = text_splitter.split_documents(documents)
    print(f"📚 Documento dividido em {len(split_docs)} chunks")
    
    # Usar embeddings locais do HuggingFace (gratuito)
    print("🤖 Inicializando embeddings locais...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Conectar ao banco vetorial
    print("🔌 Conectando ao banco vetorial...")
    store = PGVector(
        embeddings=embeddings,
        connection=pgvector_url,
        collection_name=collection_name,
        use_jsonb=True
    )
    
    # Adicionar documentos ao banco
    print("💾 Adicionando documentos ao banco...")
    
    # Enriquecer metadados
    enriched = []
    ids = []
    
    for i, doc in enumerate(split_docs):
        doc.metadata.update({
            'chunk_id': i,
            'source_file': pdf_path,
            'chunk_size': len(doc.page_content)
        })
        enriched.append(doc)
        ids.append(f"doc_{i}")
    
    # Adicionar ao banco
    store.add_documents(documents=enriched, ids=ids)
    
    print(f"✅ Ingestão concluída! {len(enriched)} chunks adicionados ao banco.")
    print(f"📊 Coleção: {collection_name}")

if __name__ == "__main__":
    main()