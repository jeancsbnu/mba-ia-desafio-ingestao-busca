from search import search_prompt


def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("=" * 50)
    print("Chat RAG iniciado!")
    print("Digite sua pergunta ou 'sair' para encerrar.")
    print("=" * 50)

    while True:
        try:
            pergunta = input("\nVocê: ").strip()

            if not pergunta:
                continue

            if pergunta.lower() in ["sair", "exit", "quit"]:
                print("Encerrando chat. Até logo!")
                break

            print("\nAssistente: ", end="", flush=True)
            resposta = chain.invoke(pergunta)
            print(resposta)

        except KeyboardInterrupt:
            print("\n\nChat encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"\nErro ao processar pergunta: {e}")


if __name__ == "__main__":
    main()