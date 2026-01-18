import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

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


def format_docs_with_score(docs_with_score):
    """Formata os documentos recuperados (com score) em uma string de contexto."""
    return "\n\n".join(doc.page_content for doc, score in docs_with_score)


def search_prompt():
    """
    Cria e retorna uma chain RAG que:
    1. Vetoriza a pergunta
    2. Busca os 10 resultados mais relevantes (k=10) no banco vetorial
    3. Monta o prompt e chama a LLM
    4. Retorna a resposta ao usuário
    """
    try:
        # Configurar embeddings
        embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small"))

        # Conectar ao banco vetorial
        store = PGVector(
            embeddings=embeddings,
            collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
            connection=os.getenv("DATABASE_URL"),
            use_jsonb=True,
        )

        # Função para buscar documentos com score
        def search_with_score(query: str) -> str:
            docs_with_score = store.similarity_search_with_score(query, k=10)
            return format_docs_with_score(docs_with_score)

        # Configurar o modelo LLM
        llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

        # Criar o prompt template
        prompt = PromptTemplate(
            input_variables=["contexto", "pergunta"],
            template=PROMPT_TEMPLATE
        )

        # Definir as entradas da chain
        contexto = RunnableLambda(search_with_score)
        pergunta = RunnablePassthrough()

        # Montar a chain RAG
        chain = (
            {"contexto": contexto, "pergunta": pergunta}
            | prompt
            | llm
            | StrOutputParser()
        )

        return chain

    except Exception as e:
        print(f"Erro ao inicializar a chain: {e}")
        return None