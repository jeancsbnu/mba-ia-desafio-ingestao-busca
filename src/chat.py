import os
import sys
from search import search_prompt

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Iniciando o chat.")
    print("(Digite 'sair' para encerrar o chat)")

    user_question = input("Digite sua pergunta:\n-> ")

    while True:
        if user_question.lower() == "sair":
            print("Encerrando o chat.")
            sys.exit(0)
        if not user_question.strip():
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Pergunta inválida. Vamos tentar novamente...")
            user_question = input("\nDigite sua pergunta (ou 'sair' para encerrar):\n-> ")
            continue

        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"-> {user_question}\n")
            print(search_prompt(user_question))
            print(100*"-")
        except Exception as e:
            print(f"Ocorreu um erro: {e.args}")
            sys.exit(1)

        user_question = input("\nDigite sua pergunta (ou 'sair' para encerrar):\n-> ")
        
if __name__ == "__main__":
    main()