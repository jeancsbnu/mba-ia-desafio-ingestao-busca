# Sistema RAG - Ingestão e Busca Semântica

Sistema de ingestão e busca semântica usando LangChain, PostgreSQL com pgVector e embeddings HuggingFace.

## 📋 Funcionalidades

- **Ingestão**: Processa arquivos PDF e armazena chunks no banco vetorial
- **Busca**: Responde perguntas baseadas exclusivamente no conteúdo do PDF
- **CLI**: Interface de linha de comando simples e direta

## 🛠️ Tecnologias

- **Python** - Linguagem principal
- **LangChain** - Framework para aplicações RAG
- **PostgreSQL + pgVector** - Banco vetorial
- **HuggingFace Embeddings** - Embeddings locais (sentence-transformers)
- **Google Gemini 2.5 Flash Lite** - Modelo de linguagem
- **Docker & Docker Compose** - Execução do banco

## 📁 Estrutura do Projeto

```
├── docker-compose.yml          # Configuração PostgreSQL + pgVector
├── requirements.txt           # Dependências Python
├── .env.example              # Template de variáveis de ambiente
├── src/
│   ├── ingest.py             # Script de ingestão do PDF
│   ├── search.py             # Funções de busca vetorial
│   ├── chat.py               # Interface CLI
├── document.pdf              # PDF para ingestão
└── README.md                 # Este arquivo
```

## ⚙️ Configuração

### 1. Clonar repositório
```bash
git clone <repository-url>
cd mba-ia-desafio-ingestao-busca
```

### 2. Configurar ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```bash
GOOGLE_API_KEY=sua-chave-google-aqui
PGVECTOR_URL=postgresql://postgres:postgres@localhost:5432/rag
PGVECTOR_COLLECTION=documents
PDF_PATH=document.pdf
```

## 🚀 Execução

### 1. Iniciar banco de dados
```bash
docker compose up -d
```

### 2. Executar ingestão do PDF
```bash
python src/ingest.py
```

### 3. Iniciar chat
```bash
python src/chat.py
```

## 💬 Exemplo de Uso

```
Faça sua pergunta:

PERGUNTA: Qual o faturamento da empresa Magna Financeira Holding?
RESPOSTA: R$ 51.046.000,25

---

Faça sua pergunta:

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

## 🔧 Especificações Técnicas

### Ingestão
- **Chunk size**: 1000 caracteres
- **Overlap**: 150 caracteres
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (local)
- **Splitter**: RecursiveCharacterTextSplitter

### Busca
- **Método**: similarity_search_with_score
- **Resultados**: k=10 documentos mais relevantes
- **LLM**: Google Gemini 2.5 Flash Lite

### Prompt Template
O sistema usa um prompt rigoroso que:
- Responde apenas com base no contexto fornecido
- Retorna "Não tenho informações necessárias" para perguntas fora do contexto
- Nunca inventa informações ou usa conhecimento externo

## 🧪 Testes

Para testar o sistema:
```bash
python test_chat.py
```

## 📊 Arquivos de Configuração

### docker-compose.yml
Configura PostgreSQL com extensão pgVector para armazenamento vetorial.

### .env.example
Template com todas as variáveis de ambiente necessárias.

### requirements.txt
Lista completa de dependências Python incluindo:
- langchain
- langchain-community  
- langchain-postgres
- langchain-google-genai
- sentence-transformers
- E outras dependências necessárias

## ⚠️ Requisitos

- Python 3.8+
- Docker e Docker Compose
- Chave de API do Google Gemini
- Pelo menos 2GB de RAM livres
- Conexão com internet (para download inicial dos modelos)

## 🐛 Solução de Problemas

### Erro de conexão com banco
```bash
docker compose down
docker compose up -d
```

### Erro de modelo não encontrado
Verifique se a chave do Google API está correta no arquivo `.env`.

### Erro de dependências
```bash
pip install --upgrade -r requirements.txt
```

## 📝 Notas

- Os embeddings são processados localmente (HuggingFace)
- Apenas o LLM utiliza API externa (Google Gemini)
- O sistema funciona offline após download inicial dos modelos
- Os dados são persistidos no PostgreSQL via Docker

---

**Desenvolvido com LangChain, PostgreSQL, pgVector e HuggingFace**