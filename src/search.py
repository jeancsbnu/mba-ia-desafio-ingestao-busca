from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from dotenv import load_dotenv
from utils import get_database_connection, get_llm_model

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

def format_docs_simple(docs: list[Document]):
    contexto = ""
    for (doc, score) in docs:
        contexto += f"Score: {score}\n"
        contexto += f"Conteúdo: {doc.page_content}\n"
        for k, v in doc.metadata.items():
            contexto += f"{k}: {v}\n"
    return contexto

def retrieve(question): 
  db = get_database_connection()
  results = db.similarity_search_with_score(question, k=40)
  return results

def search_prompt(question: str):
    docs = retrieve(question)
    contexto = format_docs_simple(docs)
    llm = get_llm_model()
    
    prompt = PromptTemplate(
      input_variables=["contexto", "pergunta"],
      template=PROMPT_TEMPLATE
    )
    
    pipeline = prompt | llm | StrOutputParser()

    result = pipeline.invoke({"contexto": contexto, "pergunta": question})

    return result