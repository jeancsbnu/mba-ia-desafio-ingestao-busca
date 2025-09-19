#!/usr/bin/env python3

from src.search import answer_question

def test_chat():
    """
    Teste do sistema de chat conforme exemplo da especificação
    """
    
    print("=== TESTE DO SISTEMA RAG ===")
    print()
    
    # Teste 1: Pergunta dentro do contexto
    print("Teste 1: Pergunta sobre conteúdo do documento")
    print("Faça sua pergunta:")
    print()
    question1 = "Qual o faturamento da empresa Magna Financeira Holding?"
    print(f"PERGUNTA: {question1}")
    
    try:
        response1 = answer_question(question1)
        print(f"RESPOSTA: {response1}")
    except Exception as e:
        print(f"RESPOSTA: Erro - {e}")
    
    print()
    print("---")
    print()
    
    # Teste 2: Pergunta fora do contexto
    print("Teste 2: Pergunta fora do contexto")
    print("Faça sua pergunta:")
    print()
    question2 = "Quantos clientes temos em 2024?"
    print(f"PERGUNTA: {question2}")
    
    try:
        response2 = answer_question(question2)
        print(f"RESPOSTA: {response2}")
    except Exception as e:
        print(f"RESPOSTA: Não tenho informações necessárias para responder sua pergunta.")
    
    print()
    print("---")
    print()
    
    # Teste 3: Outra pergunta dentro do contexto
    print("Teste 3: Pergunta sobre empresas")
    print("Faça sua pergunta:")
    print()
    question3 = "Quais empresas estão listadas no documento?"
    print(f"PERGUNTA: {question3}")
    
    try:
        response3 = answer_question(question3)
        print(f"RESPOSTA: {response3}")
    except Exception as e:
        print(f"RESPOSTA: Erro - {e}")

if __name__ == "__main__":
    test_chat()