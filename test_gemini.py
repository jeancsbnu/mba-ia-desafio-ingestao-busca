import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Carregar variáveis do ambiente
load_dotenv()

def test_gemini_model():
    """Testar especificamente o modelo Gemini 2.5 Flash Lite"""
    
    # Configurações
    pgvector_url = os.getenv("PGVECTOR_URL", "postgresql://postgres:postgres@localhost:5432/rag")
    collection_name = os.getenv("PGVECTOR_COLLECTION", "documents")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    print("🤖 Inicializando embeddings locais...")
    
    # Embeddings locais
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    print("🔌 Conectando ao banco vetorial...")
    
    # Banco vetorial
    store = PGVector(
        embeddings=embeddings,
        connection=pgvector_url,
        collection_name=collection_name,
        use_jsonb=True
    )
    
    # Retriever
    retriever = store.as_retriever(search_kwargs={"k": 3})
    
    print("🧠 Testando Google Gemini 2.5 Flash Lite...")
    
    # LLM (Google Gemini)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=google_api_key,
        temperature=0.3
    )
    
    # Template do prompt mais específico
    template = """
Com base no contexto fornecido, responda à pergunta de forma clara e objetiva.

CONTEXTO:
{context}

PERGUNTA: {question}

INSTRUÇÕES:
- Use apenas as informações do contexto fornecido
- Se você conseguir identificar informações relevantes no contexto, forneça uma resposta baseada nelas
- Seja específico e cite dados quando relevantes
- Use português brasileiro

RESPOSTA:"""

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
    
    # Testes específicos
    perguntas = [
        "Quais são algumas empresas listadas no documento?",
        "Que tipo de informações o documento contém sobre as empresas?",
        "Qual é o ano de fundação mais antigo mencionado?",
        "Existem valores em reais no documento?"
    ]
    
    print("\n" + "="*60)
    print("🔬 TESTE DO MODELO GEMINI 2.5 FLASH LITE")
    print("="*60)
    
    for i, pergunta in enumerate(perguntas, 1):
        print(f"\n{i}. 📝 Pergunta: {pergunta}")
        print("   🔍 Processando...")
        
        try:
            resposta = qa_chain.invoke(pergunta)
            print(f"   🤖 Resposta: {resposta['result']}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        print("   " + "-"*50)

if __name__ == "__main__":
    test_gemini_model()