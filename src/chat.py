import sys
from search import search_prompt


def print_welcome():
    print("=" * 80)
    print("🤖 [MBA - IA - Desafio de Ingestão e Busca] - Assistente de Perguntas e Respostas")
    print("=" * 80)
    print("\nVocê pode fazer perguntas sobre o documento PDF que foi processado.")
    print("Digite 'sair', 'exit' ou 'quit' para encerrar o chat.\n")


def print_separator():
    print("-" * 80)


def main():
    print_welcome()
    
    try:
        while True:
            # Get user input
            question = input("\n💬 Sua pergunta: ").strip()
            
            # Check for exit commands
            if question.lower() in ['sair', 'exit', 'quit', 'q']:
                print("\n👋 Obrigado por usar o chat! Até logo!\n")
                break
            
            # Check for empty input
            if not question:
                print("⚠️  Por favor, digite uma pergunta válida.")
                continue
            
            # Process the question
            try:
                print("\n🔍 Buscando informações...")
                print_separator()
                
                response = search_prompt(question)
                
                print_separator()
                print(f"\n📝 Resposta:\n{response}\n")
                print_separator()
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Operação cancelada pelo usuário.")
                break
            except Exception as e:
                print(f"\n❌ Erro ao processar sua pergunta: {e}")
                print("Por favor, tente novamente ou digite 'sair' para encerrar.\n")
                continue
                
    except KeyboardInterrupt:
        print("\n\n👋 Chat encerrado. Até logo!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
