import os
from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

def get_llm_model() -> BaseChatModel:
    if os.getenv("LLM_MODEL") is None:
        raise ValueError("Você deve especificar modelo nas variáveis de ambiente.")
    
    if os.getenv("LLM_MODEL").strip() == "ollama":
        return ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3.1"), base_url=os.getenv("OLLAMA_MODEL_SERVER"), temperature=0)
    elif os.getenv("LLM_MODEL").strip() == "google" and os.getenv("GOOGLE_API_KEY").strip() is not None:
        return ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"), temperature=0)
    elif os.getenv("LLM_MODEL").strip() == "openai" and os.getenv("OPENAI_API_KEY").strip() is not None:
        return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-5-nano"), temperature=0)
    else:
        raise ValueError("Você deve especificar uma chave de API nas variáveis de ambiente.")

def get_llm_model_embeddings():
    if os.getenv("LLM_MODEL") is None:
        raise ValueError("Você deve especificar modelo nas variáveis de ambiente.")
    
    if os.getenv("LLM_MODEL").strip() == "ollama":
        return OllamaEmbeddings(model=os.getenv("OLLAMA_EMBEDDING_MODEL", "mxbai-embed-large"), base_url=os.getenv("OLLAMA_EMBEDDING_SERVER"))
    elif os.getenv("LLM_MODEL").strip() == "google" and os.getenv("GOOGLE_API_KEY").strip() is not None:
        return GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"))
    elif os.getenv("LLM_MODEL").strip() == "openai" and os.getenv("OPENAI_API_KEY").strip() is not None:
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
    else:
        raise ValueError("Você deve especificar uma chave de API nas variáveis de ambiente.")

def get_database_connection():
    if os.getenv("DATABASE_URL") is None or os.getenv("PG_VECTOR_COLLECTION_NAME") is None:
        raise ValueError("Você deve especificar DATABASE_URL e PG_VECTOR_COLLECTION_NAME nas variáveis de ambiente.")
    
    embeddings = get_llm_model_embeddings()
    db = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
    
    return db

def get_pdf_path() -> str:
    if os.getenv("PDF_PATH") is None:
        raise ValueError("Você deve especificar PDF_PATH nas variáveis de ambiente.")
    return os.getenv("PDF_PATH")