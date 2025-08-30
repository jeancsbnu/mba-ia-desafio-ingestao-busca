# Desafio MBA Engenharia de Software com IA - Full Cycle

Este projeto implementa um sistema de Ingestão e Busca Semântica utilizando LangChain, PostgreSQL com pgVector e modelos de linguagem do Google (Gemini). O sistema é capaz de ler um arquivo PDF, armazenar seu conteúdo de forma vetorizada e responder a perguntas com base exclusivamente nas informações contidas no documento.

## Tecnologias Utilizadas

- **Linguagem:** Python
- **Framework:** LangChain
- **Banco de Dados:** PostgreSQL + pgVector
- **Orquestração:** Docker & Docker Compose
- **LLM e Embeddings:** Google Gemini (via `langchain-google-genai`)

## Estrutura do Projeto

```
├── docker-compose.yml      # Configuração do serviço PostgreSQL com pgVector
├── requirements.txt      # Dependências do projeto Python
├── .env.example          # Arquivo de exemplo para variáveis de ambiente
├── src/
│   ├── ingest.py         # Script para ingestão e vetorização do PDF
│   ├── search.py         # Script que monta a chain de busca e resposta (RAG)
│   ├── chat.py           # CLI para interação com o usuário
├── document.pdf          # PDF a ser ingerido (coloque seu PDF aqui)
└── README.md             # Este arquivo
```

## Como Executar a Solução

Siga os passos abaixo para configurar e executar o projeto.

### 1. Pré-requisitos

- Docker e Docker Compose instalados.
- Python 3.10+ instalado.
- Uma API Key do Google AI Studio.

### 2. Configuração do Ambiente

**a. Crie e ative um ambiente virtual:**
```bash
python3 -m venv venv
source venv/bin/activate
# No Windows, use: venv\Scripts\activate
```

**b. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**c. Configure as variáveis de ambiente:**
Crie um arquivo chamado `.env` na raiz do projeto, copiando o conteúdo de `.env.example`:
```bash
cp .env.example .env
```
Agora, edite o arquivo `.env` e preencha com seus valores.

**d. Adicione o PDF:**
Coloque o arquivo PDF que você deseja consultar na raiz do projeto e certifique-se de que o nome dele é `document.pdf` (ou atualize a variável `PDF_PATH` no arquivo `.env`).

### 3. Execução

**a. Suba o banco de dados:**
Com o Docker em execução, execute o seguinte comando na raiz do projeto:
```bash
docker compose up -d
```

**b. Execute a ingestão do PDF:**
Este script irá ler, dividir, vetorizar e salvar o conteúdo do `document.pdf` no banco de dados.
```bash
python src/ingest.py
```

**c. Inicie o chat:**
```bash
python src/chat.py
```