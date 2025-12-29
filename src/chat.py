import os
import sys
from search import search_prompt

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"[{os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip()}] System: Iniciando o chat.")
    print(f"[{os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip()}] System: (Digite 'sair' para encerrar o chat)")

    user_question = input(f"[{os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip()}] System: Digite sua pergunta:\n-> ")

    while True:
        if user_question.lower() == "sair":
            print(f"[{os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip()}] System: Encerrando o chat.")
            sys.exit(0)
        if not user_question.strip():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"[{os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip()}] System: Pergunta inválida. Vamos tentar novamente...")
            user_question = input(f"\n[{os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip()}] System: Digite sua pergunta (ou 'sair' para encerrar):\n-> ")
            continue

        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"[{os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip()}] User: {user_question}\n")
            response = search_prompt(user_question)
            print(f"[{os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip()}] System: {response}")
            print(100*"-")
        except Exception as e:
            print(f"Ocorreu um erro: {e.args}")
            sys.exit(1)

        user_question = input(f"\n[{os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip()}] System: Digite sua pergunta (ou 'sair' para encerrar):\n-> ")

if __name__ == "__main__":
    main()