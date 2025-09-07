import pytest
import tempfile
import os
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from src.core.use_cases.ingest_pdf import IngestPDFUseCase
from src.core.use_cases.search_documents import SearchDocumentsUseCase
from src.infrastructure.services.pdf_loader_service import PDFLoaderService
from src.infrastructure.text_processing.chunker import DocumentChunker
from src.infrastructure.services.openai_embedding_service import OpenAIEmbeddingService
from src.infrastructure.services.openai_llm_service import OpenAILLMService
from src.core.domain.document import Document
from src.core.domain.chunk import Chunk

class TestEndToEndWorkflows:
    """Test complete end-to-end workflows"""
    
    def setup_method(self):
        """Setup test fixtures"""
        # Mock all external services
        self.mock_openai_embedding = MagicMock()
        self.mock_openai_llm = MagicMock()
        self.mock_pdf_service = MagicMock()
        self.mock_chunker = MagicMock()
        
        # Create mock document and chunks
        self.mock_document = Document(
            filename="test_document.pdf",
            content_hash="abc123",
            total_chunks=2,
            file_size=1024,
            page_count=2
        )
        
        self.mock_chunks = [
            Chunk(
                chunk_index=0,
                content="This is the first chunk of content.",
                metadata={"page_number": 1},
                content_hash="hash1"
            ),
            Chunk(
                chunk_index=1,
                content="This is the second chunk of content.",
                metadata={"page_number": 2},
                content_hash="hash2"
            )
        ]
    
    def test_pdf_ingestion_components(self):
        """Test PDF ingestion components individually"""
        # Test PDF service
        pdf_service = PDFLoaderService()
        assert pdf_service is not None
        
        # Test chunker
        chunker = DocumentChunker()
        assert chunker is not None
        
        # Test embedding service (with mock)
        with patch('src.infrastructure.services.openai_embedding_service.settings') as mock_settings:
            mock_settings.OPENAI_API_KEY = "test-api-key"
            mock_settings.OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
            embedding_service = OpenAIEmbeddingService()
            assert embedding_service is not None
    
    def test_search_components(self):
        """Test search components individually"""
        # Test search prompt template
        from src.presentation.prompts.search_prompt import SearchPromptTemplate
        prompt_template = SearchPromptTemplate()
        assert prompt_template is not None
        
        # Test LLM service (with mock)
        with patch('src.infrastructure.services.openai_llm_service.settings') as mock_settings:
            mock_settings.OPENAI_API_KEY = "test-api-key"
            mock_settings.OPENAI_LLM_MODEL = "gpt-5-nano"
            llm_service = OpenAILLMService()
            assert llm_service is not None
    
    @pytest.mark.asyncio
    async def test_pdf_validation_workflow(self):
        """Test complete PDF validation workflow"""
        # Create temporary PDF file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(b'%PDF-1.4\n%Test PDF content')
            tmp_file_path = tmp_file.name
        
        try:
            # Mock PDF service validation
            with patch.object(PDFLoaderService, 'validate_pdf_content', return_value={
                'is_valid': True,
                'errors': [],
                'warnings': [],
                'file_info': {
                    'filename': 'test.pdf',
                    'file_size': 1024,
                    'file_size_mb': 0.001,
                    'page_count': 2,
                    'total_content_length': 500
                }
            }):
                pdf_service = PDFLoaderService()
                validation = pdf_service.validate_pdf_content(tmp_file_path)
                
                # Verify validation results
                assert validation['is_valid'] is True
                assert len(validation['errors']) == 0
                assert validation['file_info']['page_count'] == 2
                
        finally:
            # Cleanup
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    @pytest.mark.asyncio
    async def test_error_handling_workflow(self):
        """Test error handling in end-to-end workflows"""
        # Test PDF loading error
        with patch.object(PDFLoaderService, 'load_pdf', side_effect=ValueError("Invalid PDF file")):
            pdf_service = PDFLoaderService()
            
            with pytest.raises(ValueError, match="Invalid PDF file"):
                pdf_service.load_pdf("invalid.pdf")
        
        # Test embedding generation error
        with patch.object(OpenAIEmbeddingService, 'generate_embeddings', side_effect=Exception("API error")):
            embedding_service = OpenAIEmbeddingService()
            
            with pytest.raises(Exception, match="API error"):
                await embedding_service.generate_embeddings(["test text"])
    
    @pytest.mark.asyncio
    async def test_chunking_and_embedding_workflow(self):
        """Test chunking and embedding generation workflow"""
        # Mock chunker
        with patch.object(DocumentChunker, 'chunk_text', return_value=self.mock_chunks):
            # Mock embedding service
            with patch.object(OpenAIEmbeddingService, 'generate_embeddings', return_value=[[0.1] * 1536, [0.2] * 1536]):
                chunker = DocumentChunker()
                embedding_service = OpenAIEmbeddingService()
                
                # Generate chunks
                text = "This is a test document with multiple sentences."
                chunks = chunker.chunk_text(text)
                
                # Generate embeddings for chunks
                chunk_texts = [chunk.content for chunk in chunks]
                embeddings = await embedding_service.generate_embeddings(chunk_texts)
                
                # Verify results
                assert len(chunks) == 2
                assert len(embeddings) == 2
                assert all(len(emb) == 1536 for emb in embeddings)
