import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Carregar variáveis do ambiente
load_dotenv()

def create_rag_chain():
    """Criar cadeia RAG com Google Gemini e embeddings locais"""
    
    # Configurações
    pgvector_url = os.getenv("PGVECTOR_URL", "postgresql://postgres:postgres@localhost:5432/rag")
    collection_name = os.getenv("PGVECTOR_COLLECTION", "documents")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    print("🤖 Inicializando embeddings locais...")
    
    # Embeddings locais (mesmo modelo da ingestão)
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
    retriever = store.as_retriever(search_kwargs={"k": 5})
    
    print("🧠 Inicializando Google Gemini...")
    
    # LLM (Google Gemini)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=google_api_key,
        temperature=0.1
    )
    
    # Template do prompt em português
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
- Mantenha suas respostas claras e concisas

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
    print("💬 Sistema de Chat RAG")
    print("=" * 50)
    print("📋 Instruções:")
    print("- Digite suas perguntas sobre o documento")
    print("- Digite 'quit' ou 'sair' para encerrar")
    print("- Digite 'help' para ver comandos disponíveis")
    print("=" * 50)
    
    try:
        # Inicializar a cadeia RAG
        qa_chain = create_rag_chain()
        print("✅ Sistema RAG inicializado com sucesso!")
        print("\n💡 Exemplo de perguntas:")
        print("   - Qual é o assunto principal do documento?")
        print("   - Quais são os pontos principais abordados?")
        print("   - Há alguma conclusão ou recomendação?")
        print("\n" + "=" * 50)
        
        while True:
            # Obter pergunta do usuário
            question = input("\n❓ Sua pergunta: ").strip()
            
            if not question:
                continue
                
            # Comandos especiais
            if question.lower() in ['quit', 'exit', 'sair', 'q']:
                print("\n👋 Encerrando chat. Até logo!")
                break
            elif question.lower() in ['help', 'ajuda', 'h']:
                print("\n📋 Comandos disponíveis:")
                print("   - quit/sair: Encerrar o chat")
                print("   - help/ajuda: Mostrar esta ajuda")
                print("   - Qualquer outra coisa: Fazer pergunta sobre o documento")
                continue
            
            # Processar pergunta
            print("\n🔍 Buscando informações...")
            
            try:
                response = qa_chain.run(question)
                print(f"\n🤖 Resposta:\n{response}")
            except Exception as e:
                print(f"\n❌ Erro ao processar pergunta: {e}")
                print("Tente reformular sua pergunta.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Chat interrompido. Até logo!")
    except Exception as e:
        print(f"\n❌ Erro ao inicializar sistema: {e}")
        print("Verifique se:")
        print("- O banco PostgreSQL está rodando")
        print("- A chave do Google API está configurada")
        print("- Os documentos foram ingeridos corretamente")

if __name__ == "__main__":
    main()