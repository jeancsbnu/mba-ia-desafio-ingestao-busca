import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_postgres import PGVector

load_dotenv()

def search_documents(query, k=10):
    """
    Busca documentos similares no banco vetorial
    
    Args:
        query (str): Pergunta do usuário
        k (int): Número de resultados a retornar (default=10)
    
    Returns:
        list: Lista de tuplas (documento, score)
    """
    
    # Configurar embeddings (mesmo modelo usado na ingestão)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Conectar ao banco vetorial
    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        connection=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
    )
    
    # Buscar documentos com score (conforme especificação)
    results = store.similarity_search_with_score(query, k=k)
    
    return results

def answer_question(query):
    """
    Responde uma pergunta baseada no conteúdo do PDF
    
    Args:
        query (str): Pergunta do usuário
        
    Returns:
        str: Resposta baseada no contexto ou mensagem padrão
    """
    
    # Buscar os 10 resultados mais relevantes
    results = search_documents(query, k=10)
    
    if not results:
        return "Não tenho informações necessárias para responder sua pergunta."
    
    # Concatenar contexto dos documentos encontrados
    context = "\n\n".join([doc.page_content for doc, score in results])
    
    # Template do prompt conforme especificação
    prompt_template = """CONTEXTO:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{question}

RESPONDA A "PERGUNTA DO USUÁRIO\""""
    
    # Montar prompt final
    prompt = prompt_template.format(context=context, question=query)
    
    # Configurar LLM
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite"),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )
    
    # Chamar LLM e retornar resposta
    try:
        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        print(f"Erro ao chamar LLM: {e}")
        return "Não tenho informações necessárias para responder sua pergunta."