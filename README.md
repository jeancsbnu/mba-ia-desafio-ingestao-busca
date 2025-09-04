# MBA | Engenharia de Software com IA - Chat Semântico com LangChain e PGVector

> 🇬🇧 **English version available:** [README_EN.md](README_EN.md)

Este projeto é uma aplicação de chat com busca semântica (RAG - Retrieval-Augmented Generation) desenvolvida como parte do MBA em Engenharia de Software com IA. A aplicação permite que o usuário faça perguntas em linguagem natural sobre o conteúdo de um documento PDF, e o sistema utiliza um modelo de linguagem (LLM) para fornecer respostas precisas com base exclusivamente no contexto encontrado no documento.

## Visão Geral

A aplicação implementa um fluxo de RAG completo:
1.  **Ingestão de Dados:** Um documento PDF (`document.pdf`) é lido, dividido em trechos (chunks) e processado.
2.  **Geração de Embeddings:** Para cada trecho, um embedding vetorial é gerado usando modelos de embedding (Google Gemini ou OpenAI).
3.  **Armazenamento:** Os trechos de texto e seus embeddings correspondentes são armazenados em um banco de dados PostgreSQL com a extensão `pgvector`.
4.  **Busca Semântica:** Quando o usuário faz uma pergunta, ela é convertida em um embedding e usada para buscar os trechos mais relevantes (semanticamente similares) no banco de dados.
5.  **Geração de Resposta:** Os trechos recuperados são injetados como contexto em um prompt, que é então enviado a um LLM (Google Gemini ou OpenAI) para gerar uma resposta coesa e baseada nos fatos.

## Arquitetura e Tecnologias

-   **Linguagem:** Python
-   **Orquestrador de LLM:** LangChain
-   **Modelos de Linguagem (LLM):** Google Gemini (via `langchain-google-genai`) ou OpenAI (via `langchain-openai`)
-   **Modelos de Embedding:** Google Embedding API ou OpenAI Embeddings
-   **Banco de Dados Vetorial:** PostgreSQL com a extensão `pgvector`
-   **Containerização:** Docker e Docker Compose
-   **Interface:** Aplicação de linha de comando (CLI)

## Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados:
-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/) (geralmente incluído na instalação do Docker)
-   [Python 3.10+](https://www.python.org/downloads/)

## Configuração

1.  **Clone o Repositório**
    ```bash
    git clone https://github.com/juniordsi/mba-ai-langchain-postgres-semantic-search.git
    cd mba-ai-langchain-postgres-semantic-search
    ```

2.  **Configure as Variáveis de Ambiente**
    
    A aplicação suporta tanto modelos do Google Gemini quanto da OpenAI. Use o arquivo `.env.example` como base para criar seu arquivo `.env`:

    ```bash
    cp .env.example .env
    ```

    ### Opção 1: Usando Google Gemini (Recomendado)
    
    Edite o arquivo `.env` e configure as seguintes variáveis:

    ```env
    # Obtenha sua chave em https://aistudio.google.com/app/apikey
    GOOGLE_API_KEY="SUA_CHAVE_DE_API_DO_GOOGLE"
    GOOGLE_MODEL="gemini-1.5-flash"
    GOOGLE_EMBEDDING_MODEL="models/embedding-001"
    
    # Configurações do banco de dados
    DATABASE_URL="postgresql://postgres:postgres@localhost:5432/rag"
    PG_VECTOR_COLLECTION_NAME="documentos"
    PDF_PATH="document.pdf"
    ```

    ### Opção 2: Usando OpenAI
    
    Alternativamente, para usar modelos da OpenAI, configure:

    ```env
    # Obtenha sua chave em https://platform.openai.com/api-keys
    OPENAI_API_KEY="SUA_CHAVE_DE_API_DA_OPENAI"
    OPENAI_MODEL="gpt-3.5-turbo"
    OPENAI_EMBEDDING_MODEL="text-embedding-3-small"
    
    # Configurações do banco de dados
    DATABASE_URL="postgresql://postgres:postgres@localhost:5432/rag"
    PG_VECTOR_COLLECTION_NAME="documentos"
    PDF_PATH="document.pdf"
    ```

    **Importante:** Você deve configurar **apenas um** dos provedores (Google OU OpenAI), não ambos.

## Execução da Aplicação

Para simplificar a inicialização, foi criado um script `start.py` que automatiza todo o processo.

**Para iniciar a aplicação, execute o seguinte comando no seu terminal:**

```bash
python3 start.py chat
```

Este comando irá realizar as seguintes etapas automaticamente:
1.  **Iniciar o Docker:** Executa `docker compose up -d` para iniciar o banco de dados PostgreSQL em segundo plano.
2.  **Criar Ambiente Virtual:** Cria um ambiente virtual `venv` na raiz do projeto (se não existir).
3.  **Instalar Dependências:** Instala todas as bibliotecas Python necessárias a partir do arquivo `requirements.txt`.
4.  **Ingerir os Dados:** Executa o script `src/ingest.py` para processar o `document.pdf` e popular o banco de dados.
5.  **Iniciar o Chat:** Executa o script `src/chat.py`, permitindo que você comece a interagir com a aplicação.

Após a inicialização, você poderá fazer perguntas diretamente no terminal. Para encerrar, digite `sair`.