import os
import re
from dotenv import load_dotenv
from num2words import num2words

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from search import search_prompt

load_dotenv()

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai").lower()
OPENAI_LLM_MODEL = os.getenv("OPENAI_LLM_MODEL", " gpt-5-nano")
GOOGLE_LLM_MODEL = os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite")

def _get_chat_model():
    """Inicializa o modelo de chat de acordo com o provedor."""
    if EMBEDDING_PROVIDER == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY não definido.")
        return ChatOpenAI(model=OPENAI_LLM_MODEL, api_key=api_key)

    if EMBEDDING_PROVIDER == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY não definido.")
        return ChatGoogleGenerativeAI(model=GOOGLE_LLM_MODEL, google_api_key=api_key)

    raise ValueError("EMBEDDING_PROVIDER deve ser 'openai' ou 'gemini'.")

def _numero_para_texto(resposta: str) -> str:
    """
    Converte valores monetários como: R$ 10.000.000,00 para 10 milhões de reais      
    """
    padrao = r"R\$\s?([0-9]{1,3}(?:\.[0-9]{3})*(?:,[0-9]{2})?)"

    def _converter(match):
        numero_str = match.group(1).replace(".", "").replace(",", ".")
        try:
            valor = float(numero_str)

            if valor >= 1_000_000_000:
                escala = valor / 1_000_000_000
                texto = f"{escala:.1f}".rstrip("0").rstrip(".")
                unidade = "bilhão" if escala < 2 else "bilhões"
                return f"{texto} {unidade} de reais"
            elif valor >= 1_000_000:
                escala = valor / 1_000_000
                texto = f"{escala:.1f}".rstrip("0").rstrip(".")
                unidade = "milhão" if escala < 2 else "milhões"
                return f"{texto} {unidade} de reais"
            elif valor >= 1_000:
                escala = valor / 1_000
                texto = f"{escala:.1f}".rstrip("0").rstrip(".")
                return f"{texto} mil reais"
            else:
                return f"{int(valor)} reais"

        except Exception:
            return match.group(0)

    return re.sub(padrao, _converter, resposta)

def main():    
    print("Faça sua pergunta:\n")

    llm = _get_chat_model()

    while True:
        pergunta = input("PERGUNTA: ").strip()
        if not pergunta:
            continue
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("\nEncerrando chat.")
            break
        
        prompt = search_prompt(pergunta, k=10)
        resposta = llm.invoke(prompt)
        conteudo = resposta.content if hasattr(resposta, "content") else str(resposta)
        conteudo = _numero_para_texto(conteudo)
        
        print(f"RESPOSTA: {conteudo}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEncerrando chat.")
