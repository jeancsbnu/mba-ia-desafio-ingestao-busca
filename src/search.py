import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

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
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    """
    Initializes and returns a RAG chain for answering questions based on a vector store.
    """
    CONNECTION_STRING = os.getenv("PGVECTOR_CONNECTION_STRING")
    COLLECTION_NAME = os.getenv("PGVECTOR_COLLECTION_NAME")

    if not all([CONNECTION_STRING, COLLECTION_NAME, os.getenv("GOOGLE_API_KEY")]):
        print("Erro: Verifique se as variáveis de ambiente PGVECTOR_CONNECTION_STRING, PGVECTOR_COLLECTION_NAME e GOOGLE_API_KEY estão definidas.")
        return None

    try:
        # Inicializa embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # Conecta ao PGVector para ser usado como retriever
        store = PGVector(
            embeddings=embeddings,
            collection_name=COLLECTION_NAME,
            connection=CONNECTION_STRING,
        )

        # Cria o retriever com k=10, conforme requisito
        retriever = store.as_retriever(search_kwargs={"k": 10})

        # Inicializa o LLM
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

        # Cria o prompt a partir do template
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        # Função para formatar os documentos do retriever em uma string única
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # Monta a RAG chain usando LCEL (LangChain Expression Language)
        rag_chain = (
            {"contexto": retriever | format_docs, "pergunta": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return rag_chain
    except Exception as e:
        print(f"Ocorreu um erro ao inicializar a chain: {e}")
        return None