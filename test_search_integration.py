#!/usr/bin/env python3
"""
Teste de integração para verificar problema na busca semântica
"""

import sys
import os
sys.path.append('src')

from infrastructure.services.gemini_embedding_service import GeminiEmbeddingService
from infrastructure.services.gemini_llm_service import GeminiLLMService
from infrastructure.database.repositories.postgres_document_repository import PostgresDocumentRepository
from config.database import SyncSessionLocal
from core.use_cases.search_documents import SearchDocumentsUseCase

def test_search_supertch():
    """Teste específico para busca da SuperTechIABrazil"""
    
    print("=== TESTE DE INTEGRAÇÃO - BUSCA SEMÂNTICA ===")
    
    # 1. Verificar se a empresa existe no PDF
    print("\n1. Verificando se SuperTechIABrazil existe no PDF...")
    from infrastructure.services.pdf_loader_service import PDFLoaderService
    
    loader = PDFLoaderService()
    pages = loader.extract_text_from_pages('document.pdf')
    
    found = False
    for page in pages:
        if 'SuperTechIABrazil' in page['content']:
            print(f"✓ SuperTechIABrazil encontrada no PDF (página {page['page_number']})")
            print(f"  Conteúdo: {page['content'][:200]}...")
            found = True
            break
    
    if not found:
        print("✗ SuperTechIABrazil NÃO encontrada no PDF")
        return False
    
    # 2. Testar geração de embedding
    print("\n2. Testando geração de embedding...")
    try:
        embedding_service = GeminiEmbeddingService()
        question = "Qual o faturamento da Empresa SuperTechIABrazil?"
        
        embedding = embedding_service.generate_single_embedding(question)
        print(f"✓ Embedding gerado: {len(embedding)} dimensões")
        print(f"  Primeiros 5 valores: {embedding[:5]}")
    except Exception as e:
        print(f"✗ Erro ao gerar embedding: {e}")
        return False
    
    # 3. Testar busca no banco de dados
    print("\n3. Testando busca no banco de dados...")
    try:
        with SyncSessionLocal() as session:
            repository = PostgresDocumentRepository(session)
            
            # Buscar chunks similares
            similar_chunks = repository.search_similar_chunks(embedding, limit=10)
            print(f"✓ Chunks encontrados: {len(similar_chunks)}")
            
            # Verificar se algum chunk contém SuperTechIABrazil
            supertech_found = False
            for i, chunk in enumerate(similar_chunks):
                if 'SuperTechIABrazil' in chunk.content:
                    print(f"✓ SuperTechIABrazil encontrada no chunk {i+1}")
                    print(f"  Similaridade: {chunk.similarity}")
                    print(f"  Conteúdo: {chunk.content[:200]}...")
                    supertech_found = True
                    break
            
            if not supertech_found:
                print("✗ SuperTechIABrazil NÃO encontrada nos chunks similares")
                print("  Chunks encontrados:")
                for i, chunk in enumerate(similar_chunks[:3]):
                    print(f"    Chunk {i+1} (similaridade: {chunk.similarity}): {chunk.content[:100]}...")
    
    except Exception as e:
        print(f"✗ Erro na busca no banco: {e}")
        return False
    
    # 4. Testar busca completa
    print("\n4. Testando busca completa...")
    try:
        llm_service = GeminiLLMService()
        search_use_case = SearchDocumentsUseCase(repository, embedding_service, llm_service)
        
        result = search_use_case.execute(question)
        print(f"✓ Busca completa executada")
        print(f"  Resposta: {result}")
        
        if "SuperTechIABrazil" in result or "10.000.000" in result:
            print("✓ Resposta contém informações sobre SuperTechIABrazil")
        else:
            print("✗ Resposta NÃO contém informações sobre SuperTechIABrazil")
            
    except Exception as e:
        print(f"✗ Erro na busca completa: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_search_supertch()
    if success:
        print("\n✓ TESTE DE INTEGRAÇÃO CONCLUÍDO COM SUCESSO")
    else:
        print("\n✗ TESTE DE INTEGRAÇÃO FALHOU")

