# PDF Search System - Easy Document Search with AI

A simple system that lets you upload PDF documents and ask questions about their content using artificial intelligence.


## Detailed Documentation (For Advanced Users)

A comprehensive Retrieval-Augmented Generation (RAG) system for PDF document ingestion, vector storage, and semantic search using AI models.

## Features

- **PDF Processing**: Load, validate, and chunk PDF documents
- **AI Integration**: Support for OpenAI and Google Gemini models
- **Vector Storage**: PostgreSQL with pgVector extension for embeddings
- **Semantic Search**: Find relevant document chunks using vector similarity
- **RAG Pipeline**: Generate contextual responses using retrieved content
- **CLI Interface**: Command-line tools for all operations
- **Comprehensive Testing**: 100% test coverage with performance validation

## Architecture

This project follows Clean Architecture principles with SOLID design:

```
src/
├── core/                    # Business logic and domain entities
│   ├── domain/             # Domain models (Document, Chunk)
│   ├── interfaces/          # Abstract interfaces
│   └── use_cases/          # Business use cases
├── infrastructure/          # External dependencies
│   ├── database/           # Database models and repositories
│   ├── services/           # AI service implementations
│   └── text_processing/    # PDF and text processing
└── presentation/           # User interface (CLI)
```

## Prerequisites

- Python 3.11+
- PostgreSQL 13+ with pgVector extension
- Docker and Docker Compose
- OpenAI API key or Google Gemini API key

### System Requirements

- **Operating System**: Linux, macOS, or Windows with WSL2
- **Memory**: Minimum 4GB RAM (8GB recommended for large documents)
- **Storage**: At least 2GB free space
- **Network**: Internet connection for API calls

### Required Software

1. **Python 3.11+**: Download from [python.org](https://python.org)
2. **Docker**: Download from [docker.com](https://docker.com)
3. **Docker Compose**: Usually included with Docker Desktop
4. **Git**: For cloning the repository

## Installation

### Prerequisites

Before installing, ensure you have:
- Python 3.11+ installed
- Docker and Docker Compose installed
- Git installed
- Internet connection for API calls

### Option 1: Automatic Installation (Recommended)

The easiest way to set up the system is using the automated setup script:

```bash
# 1. Clone the repository
git clone <repository-url>
cd mba-ia-desafio-ingestao-busca

# 2. Run the automated setup
./setup.sh
```

The setup script will automatically:
- Check prerequisites
- Create virtual environment
- Install dependencies
- Configure AI service (Google Gemini)
- Start database
- Initialize database schema
- Make scripts executable

### Option 2: Manual Installation (Advanced Users)

If you prefer to install manually or need custom configuration:

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd mba-ia-desafio-ingestao-busca
```

#### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
# Required environment variables:
```

```env
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=rag

# OpenAI (choose one)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_LLM_MODEL=gpt-5-nano

# Google Gemini (alternative)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_EMBEDDING_MODEL=models/embedding-001
GOOGLE_LLM_MODEL=gemini-2.5-flash-lite
```

#### 5. Configure AI Service

```bash
# Set Google Gemini as preferred service
python src/setup.py google

# Or set OpenAI
python src/setup.py openai
```

#### 6. Start Database

```bash
docker-compose up -d
```

#### 7. Initialize Database

```bash
export PYTHONPATH=$(pwd)
python -m src.config.database
```

### Obtaining API Keys

#### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the generated key (starts with `sk-`)
6. Paste it in your `.env` file as `OPENAI_API_KEY=sk-your-key-here`

**Note**: OpenAI requires a valid payment method and may charge for API usage.

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key (starts with `AIza`)
5. Paste it in your `.env` file as `GOOGLE_API_KEY=AIza-your-key-here`

**Note**: Google Gemini offers free tier usage with quotas.

## Quick Start

After completing the installation, you can start using the system immediately:

### Upload a PDF Document
```bash
# Replace "document.pdf" with your file name
./ingest.sh document.pdf
```

### Ask Questions
```bash
# Ask any question about your document
./search.sh "What companies are mentioned in the document?"
./search.sh "What is the revenue of Company X?"
./search.sh "What type of data is in this document?"
```

### Check System Status
```bash
# See if everything is working
./status.sh
```

### List Your Documents
```bash
# See all documents you've uploaded
./list.sh
```

### Interactive Chat
```bash
# Start interactive chat session
./chat.sh
```

### Example Questions to Try
- "What companies are mentioned in the document?"
- "What is the main topic of this document?"
- "What numbers or amounts are mentioned?"
- "What dates are in this document?"
- "What type of data is in this document?"

## Help & Troubleshooting

### Common Issues and Simple Solutions

**"Permission denied" error:**
```bash
# Make scripts executable
chmod +x *.sh
```

**"File not found" error:**
- Make sure your PDF file is in the same folder as the scripts
- Check the file name is spelled correctly

**"Virtual environment not found" error:**
```bash
# Re-run the installation process
./setup.sh
```

**"Database connection failed" error:**
```bash
# Restart the database
docker-compose down
docker-compose up -d
```

**"No documents found" error:**
- Make sure you uploaded a PDF first using `./ingest.sh document.pdf`
- Check if the upload was successful with `./status.sh`

### Getting Help

1. **First, check system status:** `./status.sh`
2. **If something is wrong, re-run installation:** `./setup.sh`
3. **For more help, see the detailed documentation below**

---

## Detailed Usage

### 0. Quick Setup Check

Before starting, ensure you have completed the installation steps and run this quick check:

```bash
# 1. Set PYTHONPATH
export PYTHONPATH=$(pwd)

# 2. Check system status
python -m src.presentation.cli.interface status

# 3. Verify Docker is running
docker-compose ps
```

### 1. Configure AI Service Preference
```bash
# Set OpenAI as preferred service
python src/setup.py openai

# Set Google Gemini as preferred service  
python src/setup.py google

# Enable auto-detection (use first available)
python src/setup.py auto

# Show current configuration
python src/setup.py status
```

### 2. Start Database
```bash
docker-compose up -d
```

### 3. Initialize Database
```bash
python -m src.config.database
```

### 4. Test System
```bash
python -m src.presentation.cli.interface status
```

### 5. Ingest a PDF Document

**Simple Commands (Recommended):**
```bash
# Basic ingestion - just replace "document.pdf" with your file name
./ingest.sh document.pdf

# List all processed documents
./list.sh
```

**Advanced Commands:**
```bash
# Basic ingestion
PYTHONPATH=$(pwd) python src/ingest.py document.pdf

# With custom chunk size
PYTHONPATH=$(pwd) python src/ingest.py document.pdf --chunk-size 500 --chunk-overlap 100

# Using CLI command
PYTHONPATH=$(pwd) python -m src.presentation.cli.interface ingest document.pdf
```

### 6. Search Documents

**Simple Commands (Recommended):**
```bash
# Ask any question about your documents
./search.sh "What companies are mentioned in the document?"
./search.sh "What is the revenue of Aliança Energia?"
./search.sh "What companies have revenue over 100 million?"
./search.sh "What companies are in the technology sector?"
./search.sh "What type of data is in this document?"

# Check system status
./status.sh
```

**Advanced Commands:**
```bash
# Search for specific companies
PYTHONPATH=$(pwd) python src/search.py "What companies are mentioned in the document?"

# Search for financial data
PYTHONPATH=$(pwd) python src/search.py "What is the revenue of Aliança Energia?"

# Search with filters
PYTHONPATH=$(pwd) python src/search.py "What companies have revenue over 100 million?" --limit 5

# Search by industry sector
PYTHONPATH=$(pwd) python src/search.py "What companies are in the technology sector?"

# Search for data types
PYTHONPATH=$(pwd) python src/search.py "What type of data is in this document?"

# Using CLI command
PYTHONPATH=$(pwd) python -m src.presentation.cli.interface search "What companies are mentioned?"
```

#### Tips for Effective Semantic Search

**Good Questions (Specific and Data-Driven):**
- "What companies are mentioned in the document?"
- "What is the revenue of [specific company]?"
- "What companies have revenue over [amount]?"
- "What companies are in the [sector] sector?"
- "What type of data is in this document?"
- "List all companies with revenue between X and Y"

**Avoid Generic Questions:**
- "What is the main topic?" (too broad)
- "What is this document about?" (too vague)
- "Summarize the document" (requires full context)

**Best Practices:**
- Ask specific questions about data, numbers, or entities
- Use filters and constraints (e.g., "over 100 million")
- Be specific about what you're looking for
- Use industry terms or company names from the document

### 7. Interactive Chat

```bash
# Start interactive chat session
PYTHONPATH=$(pwd) python src/chat.py

# Using CLI command
PYTHONPATH=$(pwd) python -m src.presentation.cli.interface chat
```

### CLI Commands

```bash
# Show all available commands
PYTHONPATH=$(pwd) python -m src.presentation.cli.interface --help

# Check system status
PYTHONPATH=$(pwd) python -m src.presentation.cli.interface status

# List ingested documents
PYTHONPATH=$(pwd) python -m src.presentation.cli.interface list-documents

# Validate PDF before ingestion
PYTHONPATH=$(pwd) python -m src.presentation.cli.interface validate document.pdf
```

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run with Coverage

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Performance tests
pytest tests/performance/ -v
```

### Code Quality

```bash
# Format code
black src/ --line-length 88

# Lint code
flake8 src/

# Type checking
mypy src/ --ignore-missing-imports
```

## Usage Examples

### Basic Workflow

1. **Ingest Documents**
   ```python
   from src.core.use_cases.ingest_pdf import IngestPDFUseCase
   
   use_case = IngestPDFUseCase()
   document = await use_case.execute("document.pdf")
   print(f"Ingested {document.total_chunks} chunks")
   ```

2. **Search Content**
   ```python
   from src.core.use_cases.search_documents import SearchDocumentsUseCase
   
   use_case = SearchDocumentsUseCase()
   response = await use_case.execute("What is machine learning?")
   print(response)
   ```

3. **Custom Chunking**
   ```python
   from src.infrastructure.text_processing.chunker import DocumentChunker
   
   chunker = DocumentChunker(chunk_size=300, chunk_overlap=50)
   chunks = chunker.chunk_text("Your long text content here...")
   ```

### Advanced Configuration

```python
from src.config.settings import Settings

# Custom settings
settings = Settings(
    CHUNK_SIZE=500,
    CHUNK_OVERLAP=100,
    SIMILARITY_THRESHOLD=0.7
)
```

## Configuration

### Chunking Parameters

- **CHUNK_SIZE**: Maximum characters per chunk (default: 1000)
- **CHUNK_OVERLAP**: Overlap between consecutive chunks (default: 200)
- **SIMILARITY_THRESHOLD**: Minimum similarity for search results (default: 0.0)

### AI Model Settings

- **Embedding Models**: OpenAI text-embedding-3-small, Google models/embedding-001
- **LLM Models**: OpenAI gpt-5-nano, Google gemini-2.5-flash-lite
- **Token Limits**: Configurable based on model capabilities

### Database Configuration

- **Connection Pooling**: Async connection management
- **Vector Indexing**: pgVector for similarity search
- **Migration Support**: Automatic schema updates

## Performance

### Benchmarks

- **PDF Ingestion**: ~2 minutes for 100-page document
- **Search Response**: <1 second for typical queries
- **Memory Usage**: <500MB for large documents
- **Concurrent Users**: Supports 10+ simultaneous searches

### Optimization Tips

1. **Chunk Size**: Balance between context and performance
2. **Batch Processing**: Process multiple documents simultaneously
3. **Caching**: Enable embedding caching for repeated searches
4. **Indexing**: Ensure proper database indexes for vector search

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'src'**
   ```bash
   # Solution: Set PYTHONPATH before running commands
   export PYTHONPATH=$(pwd)
   
   # Or run with PYTHONPATH inline:
   PYTHONPATH=$(pwd) python src/script.py
   ```

2. **Docker Compose Command Not Found**
   ```bash
   # Use docker-compose (with hyphen) instead of docker compose
   docker-compose up -d
   
   # If docker-compose is not installed:
   # Install Docker Compose or use: docker compose up -d
   ```

3. **Database Connection Failed**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps
   
   # Restart database
   docker-compose restart postgres
   
   # Recreate database if needed
   docker-compose down
   docker-compose up -d
   ```

4. **API Key Errors**
   ```bash
   # Verify environment variables
   PYTHONPATH=$(pwd) python -m src.presentation.cli.interface status
   
   # Check if .env file exists and has correct keys
   cat .env | grep API_KEY
   ```

5. **Switching AI Services**
   ```bash
   # Change preferred service
   python src/setup.py openai    # or python src/setup.py google
   
   # Or manually edit .env file
   # Comment out one service and uncomment the other
   # Then restart the database to update embedding dimensions
   docker-compose down
   docker-compose up -d
   python -m src.config.database
   ```

6. **OpenAI Quota Exceeded (Error 429)**
   ```bash
   # This is a common issue with OpenAI API
   # Solutions:
   # 1. Check your OpenAI billing and usage limits
   # 2. Wait for quota reset (usually monthly)
   # 3. Use Google Gemini API instead (configure GOOGLE_API_KEY)
   ```

7. **PDF Loading Issues**
   ```bash
   # Validate PDF before ingestion
   PYTHONPATH=$(pwd) python -m src.presentation.cli.interface validate document.pdf
   
   # Check file permissions
   ls -la document.pdf
   ```

8. **Memory Issues**
   ```bash
   # Reduce chunk size for large documents
   PYTHONPATH=$(pwd) python src/ingest.py document.pdf --chunk-size 500
   
   # Process smaller documents first
   ```

9. **No Documents Found**
   ```bash
   # Check if documents were ingested
   PYTHONPATH=$(pwd) python -m src.presentation.cli.interface list-documents
   
   # Re-ingest documents if needed
   PYTHONPATH=$(pwd) python src/ingest.py document.pdf
   ```

10. **Search Returns "No Information Available"**
    ```bash
    # This usually means the question is too generic or vague
    # Try more specific questions:
    
    # Instead of: "What is this document about?"
    # Use: "What companies are mentioned in the document?"
    
    # Instead of: "What is the main topic?"
    # Use: "What type of data is in this document?"
    
    # Instead of: "Summarize the content"
    # Use: "What companies have revenue over 100 million?"
    
    # Check if documents are properly ingested
    PYTHONPATH=$(pwd) python -m src.presentation.cli.interface list-documents
    ```

### Debug Mode

```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG
PYTHONPATH=$(pwd) python src/ingest.py document.pdf

# Check system status with details
PYTHONPATH=$(pwd) python -m src.presentation.cli.interface status
```

### Getting Help

1. **Check System Status**: Always run `PYTHONPATH=$(pwd) python -m src.presentation.cli.interface status` first
2. **Validate Configuration**: Ensure your `.env` file has valid API keys
3. **Test with Small Files**: Start with small PDF files to test the system
4. **Check Logs**: Look for error messages in the console output
5. **Set PYTHONPATH**: Make sure to set `export PYTHONPATH=$(pwd)` before running any Python commands

**For detailed troubleshooting and advanced solutions, see the technical documentation.**

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Run tests and quality checks
5. Submit a pull request

### Code Standards

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Maintain 100% test coverage
- Follow SOLID principles
- Document all public APIs

### Testing Guidelines

- Write unit tests for all business logic
- Include integration tests for database operations
- Add performance tests for critical paths
- Mock external dependencies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for embedding and LLM APIs
- Google for Gemini model access
- PostgreSQL and pgVector communities
- LangChain for AI integration framework

## Technical Documentation

For advanced usage and technical details:

- **[API Documentation](docs/API.md)**: Internal API structure, interfaces, and data models
- **[Chunking System](docs/CHUNKING.md)**: Detailed information about text processing and chunking algorithms

## Support

For questions and support:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the test examples
- Consult the technical documentation above
