# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema RAG (Retrieval-Augmented Generation) para ingestão de documentos PDF e consulta via CLI utilizando LangChain, OpenAI e PostgreSQL com pgvector.

## Pré-requisitos

- Python 3.12+
- Poetry (gerenciador de dependências)
- Docker e Docker Compose
- Chave de API da OpenAI

## Configuração do Ambiente

### 1. Instalar o Poetry (se necessário)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Clonar o repositório e instalar dependências

```bash
git clone <url-do-repositorio>
cd mba-ia-desafio-ingestao-busca
```

### 3. Ativar o ambiente virtual e instalar dependências

```bash
poetry env activate
poetry install
```

Ou adicionar as dependências manualmente:

```bash
poetry add langchain==0.3.27
poetry add python-dotenv==1.1.1
poetry add pypdf==6.0.0
poetry add langchain-community==0.3.27
poetry add langchain-google-genai==2.1.9
poetry add langchain-postgres==0.0.15
poetry add psycopg==3.2.9
poetry add psycopg-binary==3.2.9
poetry add langchain-openai==0.3.30
```

### 4. Configurar variáveis de ambiente

Copie o arquivo de exemplo e configure suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
OPENAI_API_KEY=sua-chave-openai
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documents
PDF_PATH=document.pdf
```

## Configuração do Banco de Dados

### Iniciar o PostgreSQL com pgvector

O projeto inclui um `docker-compose.yml` que configura o PostgreSQL com a extensão pgvector:

```bash
docker-compose up -d
```

Isso irá:
- Criar um container PostgreSQL com pgvector (porta 5432)
- Criar automaticamente a extensão `vector` no banco de dados

Para verificar se o banco está rodando:

```bash
docker-compose ps
```

## Execução

### 1. Ingestão do PDF

Coloque o arquivo PDF na raiz do projeto (ou configure o caminho no `.env`) e execute:

```bash
poetry run python src/ingest.py
```

Este comando irá:
- Carregar o PDF especificado em `PDF_PATH`
- Dividir o documento em chunks de 1000 caracteres
- Gerar embeddings usando OpenAI
- Armazenar os vetores no PostgreSQL

### 2. Consulta via CLI

Após a ingestão, inicie o chat:

```bash
poetry run python src/chat.py
```

O sistema irá:
- Buscar os 10 documentos mais relevantes para cada pergunta
- Gerar respostas baseadas apenas no contexto do PDF
- Responder "Não tenho informações necessárias" para perguntas fora do contexto

**Comandos do chat:**
- Digite sua pergunta e pressione Enter
- Digite `sair`, `exit` ou `quit` para encerrar

## Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
├── src/
│   ├── ingest.py      # Script de ingestão do PDF
│   ├── chat.py        # Interface CLI do chat
│   └── search.py      # Lógica de busca e RAG
├── docker-compose.yml # Configuração do PostgreSQL
├── pyproject.toml     # Dependências do projeto
├── .env.example       # Exemplo de variáveis de ambiente
└── document.pdf       # PDF para ingestão
```

## Tecnologias Utilizadas

- **LangChain**: Framework para aplicações com LLM
- **OpenAI**: Embeddings e modelo de linguagem (GPT)
- **PostgreSQL + pgvector**: Banco de dados vetorial
- **Poetry**: Gerenciamento de dependências Python
- **Docker**: Containerização do banco de dados