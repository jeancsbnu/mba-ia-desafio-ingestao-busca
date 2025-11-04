import os
import sys
from dotenv import load_dotenv

from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

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

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION = os.getenv("PGVECTOR_COLLECTION", "docs_pdf")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai").lower()
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "text-embedding-004")
  
def _get_embeddings():
    """Seleciona o provedor de embeddings conforme o .env"""
    if EMBEDDING_PROVIDER == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY não definido.")
        return OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL, api_key=api_key)

    if EMBEDDING_PROVIDER == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY não definido.")
        return GoogleGenerativeAIEmbeddings(model=GEMINI_EMBEDDING_MODEL, google_api_key=api_key)

    raise ValueError("EMBEDDING_PROVIDER deve ser 'openai' ou 'gemini'.")


def search_prompt(question: str, k: int = 10):
    """Realiza a busca semântica e monta o prompt com o contexto encontrado."""
    if not question:
        raise ValueError("Forneça uma pergunta para buscar.")

    embeddings = _get_embeddings()
    
    vectorstore = PGVector(
        connection=DATABASE_URL,
        collection_name=COLLECTION,
        embeddings=embeddings,
        use_jsonb=True,
    )    
    
    results = vectorstore.similarity_search_with_score(question, k=k)

    if not results:
        print("Nenhum resultado encontrado.")
        return PROMPT_TEMPLATE.format(contexto="(vazio)", pergunta=question)

    contexto = "\n---\n".join([doc.page_content for doc, _ in results])

    prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)
    return prompt

if __name__ == "__main__":
    
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        print("Uso: python src/search.py 'sua pergunta'")
        sys.exit(1)

    prompt = search_prompt(question)
    print("\nPROMPT GERADO:\n")
    print(prompt)