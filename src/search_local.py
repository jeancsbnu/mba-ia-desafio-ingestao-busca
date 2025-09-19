import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Carregar variáveis do ambiente
load_dotenv()

def search_documents(query: str, top_k: int = 5) -> list:
    """Buscar documentos similares no banco vetorial"""
    
    # Configurações
    pgvector_url = os.getenv("PGVECTOR_URL", "postgresql://postgres:postgres@localhost:5432/rag")
    collection_name = os.getenv("PGVECTOR_COLLECTION", "documents")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    # Usar embeddings locais (mesmo modelo da ingestão)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Conectar ao banco vetorial
    store = PGVector(
        embeddings=embeddings,
        connection=pgvector_url,
        collection_name=collection_name,
        use_jsonb=True
    )
    
    # Buscar documentos similares
    results = store.similarity_search_with_score(query, k=top_k)
    
    return results

def create_rag_chain():
    """Criar cadeia RAG com Google Gemini e embeddings locais"""
    
    # Configurações
    pgvector_url = os.getenv("PGVECTOR_URL", "postgresql://postgres:postgres@localhost:5432/rag")
    collection_name = os.getenv("PGVECTOR_COLLECTION", "documents")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    # Embeddings locais
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Banco vetorial
    store = PGVector(
        embeddings=embeddings,
        connection=pgvector_url,
        collection_name=collection_name,
        use_jsonb=True
    )
    
    # Retriever
    retriever = store.as_retriever(search_kwargs={"k": 5})
    
    # LLM (Google Gemini)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=google_api_key,
        temperature=0.1
    )
    
    # Template do prompt
    template = """
Você é um assistente especializado em responder perguntas baseadas nos documentos fornecidos.

Contexto dos documentos:
{context}

Pergunta: {question}

Instruções:
- Responda baseado APENAS no contexto fornecido
- Se a informação não estiver nos documentos, diga "Não encontrei essa informação nos documentos"
- Seja preciso e cite trechos relevantes quando possível
- Use português brasileiro

Resposta:"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    # Criar cadeia RAG
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )
    
    return qa_chain

def main():
    print("🔍 Sistema de Busca RAG - Teste")
    print("=" * 50)
    
    # Teste de busca simples
    query = "What is the main topic of this document?"
    print(f"\n📝 Consulta: {query}")
    
    results = search_documents(query)
    
    print(f"\n📚 Encontrados {len(results)} documentos similares:")
    for i, (doc, score) in enumerate(results, 1):
        print(f"\n{i}. Score: {score:.4f}")
        print(f"   Conteúdo: {doc.page_content[:200]}...")
        print(f"   Metadados: {doc.metadata}")
    
    # Teste da cadeia RAG
    print("\n" + "=" * 50)
    print("🤖 Teste da Cadeia RAG")
    
    qa_chain = create_rag_chain()
    response = qa_chain.run(query)
    
    print(f"\n❓ Pergunta: {query}")
    print(f"\n💬 Resposta: {response}")

if __name__ == "__main__":
    main()