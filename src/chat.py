from search import search_prompt

def main():
    print("=== Sistema de Busca RAG ===")
    print("Inicializando sistema...")
    
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    print("Sistema pronto! Digite suas perguntas (digite 'sair' para encerrar)")
    print("-" * 50)
    
    while True:
        try:
            pergunta = input("\n🤔 Sua pergunta: ").strip()
            
            if pergunta.lower() in ['sair', 'exit', 'quit', 'q']:
                print("👋 Até mais!")
                break
            
            if not pergunta:
                print("Por favor, digite uma pergunta válida.")
                continue
            
            print("🔍 Buscando informações...")
            
            # Invocar a chain RAG
            resposta = chain.invoke(pergunta)
            
            print(f"\n💡 Resposta:")
            print(resposta)
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 Chat encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro ao processar pergunta: {e}")

if __name__ == "__main__":
    main()