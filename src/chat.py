from search import search_prompt

def main():
    print("Inicializando o sistema de chat...")
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização e as variáveis de ambiente.")
        return

    print("\nChat iniciado. Faça sua pergunta ou digite 'sair' para encerrar.")
    print("-" * 30)

    while True:
        try:
            question = input("PERGUNTA: ")
            if question.lower().strip() in ['sair', 'exit', 'quit']:
                print("Encerrando o chat. Até logo!")
                break
            if not question.strip():
                continue

            print("\nBuscando resposta...")
            response = chain.invoke(question)
            print(f"RESPOSTA: {response}\n")
            print("-" * 30)

        except KeyboardInterrupt:
            print("\n\nEncerrando o chat. Até logo!")
            break

if __name__ == "__main__":
    main()