# MBA | AI Software Engineering - Semantic Chat with LangChain and PGVector

This project is a semantic search chat application (RAG - Retrieval-Augmented Generation) developed as part of the MBA in AI Software Engineering. The application allows users to ask questions in natural language about the content of a PDF document, and the system uses a language model (LLM) to provide accurate answers based exclusively on the context found in the document.

## Overview

The application implements a complete RAG flow:
1.  **Data Ingestion:** A PDF document (`document.pdf`) is read, split into chunks, and processed.
2.  **Embedding Generation:** For each chunk, a vector embedding is generated using embedding models (Google Gemini or OpenAI).
3.  **Storage:** Text chunks and their corresponding embeddings are stored in a PostgreSQL database with the `pgvector` extension.
4.  **Semantic Search:** When a user asks a question, it is converted into an embedding and used to search for the most relevant (semantically similar) chunks in the database.
5.  **Response Generation:** The retrieved chunks are injected as context into a prompt, which is then sent to an LLM (Google Gemini or OpenAI) to generate a cohesive and fact-based response.

## Architecture and Technologies

-   **Language:** Python
-   **LLM Orchestrator:** LangChain
-   **Language Models (LLM):** Google Gemini (via `langchain-google-genai`) or OpenAI (via `langchain-openai`)
-   **Embedding Models:** Google Embedding API or OpenAI Embeddings
-   **Vector Database:** PostgreSQL with `pgvector` extension
-   **Containerization:** Docker and Docker Compose
-   **Interface:** Command Line Interface (CLI)

## Prerequisites

Before getting started, make sure you have the following software installed:
-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker installation)
-   [Python 3.10+](https://www.python.org/downloads/)

## Configuration

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/juniordsi/mba-ai-langchain-postgres-semantic-search.git
    cd mba-ai-langchain-postgres-semantic-search
    ```

2.  **Configure Environment Variables**
    
    The application supports both Google Gemini and OpenAI models. Use the `.env.example` file as a base to create your `.env` file:

    ```bash
    cp .env.example .env
    ```

    ### Option 1: Using Google Gemini (Recommended)
    
    Edit the `.env` file and configure the following variables:

    ```env
    # Get your key at https://aistudio.google.com/app/apikey
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    GOOGLE_MODEL="gemini-1.5-flash"
    GOOGLE_EMBEDDING_MODEL="models/embedding-001"
    
    # Database configuration
    DATABASE_URL="postgresql://postgres:postgres@localhost:5432/rag"
    PG_VECTOR_COLLECTION_NAME="documents"
    PDF_PATH="document.pdf"
    ```

    ### Option 2: Using OpenAI
    
    Alternatively, to use OpenAI models, configure:

    ```env
    # Get your key at https://platform.openai.com/api-keys
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    OPENAI_MODEL="gpt-3.5-turbo"
    OPENAI_EMBEDDING_MODEL="text-embedding-3-small"
    
    # Database configuration
    DATABASE_URL="postgresql://postgres:postgres@localhost:5432/rag"
    PG_VECTOR_COLLECTION_NAME="documents"
    PDF_PATH="document.pdf"
    ```

    **Important:** You must configure **only one** provider (Google OR OpenAI), not both.

3.  **Add Your Document**
    Place the PDF file you want to use as your knowledge base in the project root with the name `document.pdf`.

## Running the Application

To simplify initialization, a `start.py` script has been created that automates the entire process.

**To start the application, run the following command in your terminal:**

```bash
python3 start.py chat
```

This command will automatically perform the following steps:
1.  **Start Docker:** Runs `docker compose up -d` to start the PostgreSQL database in the background.
2.  **Create Virtual Environment:** Creates a `venv` virtual environment in the project root (if it doesn't exist).
3.  **Install Dependencies:** Installs all necessary Python libraries from the `requirements.txt` file.
4.  **Ingest Data:** Runs the `src/ingest.py` script to process `document.pdf` and populate the database.
5.  **Start Chat:** Runs the `src/chat.py` script, allowing you to start interacting with the application.

After initialization, you can ask questions directly in the terminal. To exit, type `quit` or `exit`.

## Project Structure

```
mba-ai-langchain-postgres-semantic-search/
├── README.md                 # Portuguese documentation
├── README_EN.md             # English documentation (this file)
├── .env.example             # Environment variables template
├── docker-compose.yml       # PostgreSQL container configuration
├── requirements.txt         # Python dependencies
├── start.py                 # Automated startup script
├── document.pdf             # Your PDF document (add this file)
└── src/
    ├── chat.py              # Main chat interface
    ├── ingest.py            # Document processing and ingestion
    ├── search.py            # Semantic search implementation
    └── utils.py             # Utility functions
```

## Features

- **Multi-provider Support:** Works with both Google Gemini and OpenAI models
- **Semantic Search:** Uses vector embeddings for intelligent document retrieval
- **Containerized Database:** PostgreSQL with pgvector extension running in Docker
- **Automated Setup:** Single command to set up and run the entire application
- **Cross-platform:** Compatible with Windows, macOS, and Linux

## Troubleshooting

- **Docker Issues:** Make sure Docker is running and you have sufficient permissions
- **API Key Issues:** Verify your API keys are correctly set in the `.env` file
- **Python Version:** Ensure you're using Python 3.10 or higher
- **Dependencies:** If you encounter package conflicts, try creating a fresh virtual environment

## License

This project is developed for educational purposes as part of the MBA in AI Software Engineering program.
