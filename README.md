# Desafio MBA Engenharia de Software com IA - Full Cycle

## Instruções para Execução do Projeto

### 1. Pré-requisitos

- **Docker e Docker Compose** instalados em sua máquina.<br>
  Caso não possua, siga as instruções oficiais:<br>
  [Instalar Docker](https://docs.docker.com/get-docker/) <br>
  [Instalar Docker Compose](https://docs.docker.com/compose/install/)

### 2. Subindo o Banco de Dados Postgres (especializado para vetorização)

O projeto utiliza o `docker-compose` para configurar uma instância do **Postgres** já preparada para armazenar e buscar vetores, através da extensão adequada.

Execute o comando abaixo na raiz do projeto para iniciar o banco de dados:

```bash
docker-compose up -d
```

Isso irá:
- Baixar a imagem do Postgres caso necessário
- Inicializar o banco com as configurações corretas para uso com embeddings

### 3. Vetorizando o Documento

Certifique-se de que o arquivo **documento.pdf** que você deseja vetorizar esteja disponível no local esperado (conforme definido na variável de ambiente `PDF_PATH`).

Para realizar a vetorização do conteúdo do documento (gerar os embeddings e armazenar no banco), execute:

```bash
python3 src/ingest.py
```
Esse script será responsável por:
- Ler o arquivo PDF
- Gerar os embeddings (vetores) para cada trecho do texto
- Armazenar tais embeddings na instância do Postgres configurada acima

### 4. Interagindo com a Aplicação

Após a ingestão estar concluída, para interagir com a aplicação basta executar:

```bash
python3 src/chat.py
```
Isso abrirá um chat na linha de comando, onde você poderá digitar perguntas e receber respostas baseadas exclusivamente no conteúdo do documento vetorizado.

> **Obs:** Certifique-se de que todas as variáveis de ambiente necessárias estejam corretamente configuradas (consulte `.env.example` ou a seção correspondente do README).




Descreva abaixo como executar a sua solução.