import sys
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_postgres import PGVector
from util import get_required_env_vars
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

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

def generate_response(contexto, pergunta, google_api_key, google_model, temperature=0.5):
    prompt_template = PromptTemplate.from_template(PROMPT_TEMPLATE)
    model = ChatGoogleGenerativeAI(
        google_api_key=google_api_key,
        model=google_model,
        temperature=temperature
    )
    chain = prompt_template | model | StrOutputParser()
    response = chain.invoke({"contexto": contexto, "pergunta": pergunta})
    return response

def search_prompt(question=None):
    # get environment variables
    env_vars = get_required_env_vars()    
    #embeddings query
    embeddings = GoogleGenerativeAIEmbeddings(api_key=env_vars["GOOGLE_API_KEY"], model=env_vars["GOOGLE_EMBEDDING_MODEL"])
    store = PGVector(
      embeddings=embeddings, 
      collection_name=env_vars["PG_VECTOR_COLLECTION_NAME"], 
      connection=env_vars["DATABASE_URL"],
      use_jsonb=True
      )
    
    results = store.similarity_search(question)
    
    # Combine all document contents into a single context string
    contexto = "\n\n".join([doc.page_content for doc in results])
    
    # Generate response using chain
    response = generate_response(contexto, question, env_vars["GOOGLE_API_KEY"], env_vars["GOOGLE_MODEL"])
    return response


#TODO: just for testing - should be removed
if __name__ == "__main__":
    search_prompt("Qual o faturamento da empresa Alfa Energia Holding ?")
