from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from util import get_required_env_vars

def ingest_pdf():
    # Get and validate environment variables
    print("0 - Validating environment variables")
    env_vars = get_required_env_vars()
    # Start ingestion process
    print("1 - Starting ingestion process")
    #load pdf and chunking 
    docs = PyPDFLoader(str(env_vars["PDF_PATH"])).load()
    splits = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=150,
    add_start_index=False).split_documents(docs)

    if not splits:
        raise ValueError("No documents were created from the PDF. Please check the PDF file.")

    #pipeline cleaning empyt and None metadata 
    enriched = [
        Document(
            page_content=doc.page_content,
            metadata={k: v for k, v in doc.metadata.items() if v not in ("", None)}
        ) for doc in splits
    ]
    
    #creating idexes for documents
    ids =[f"doc-{i}" for i in range (len(enriched))]

    #embeddings with google genai
    embeddings = GoogleGenerativeAIEmbeddings(api_key=env_vars["GOOGLE_API_KEY"], model=env_vars["GOOGLE_EMBEDDING_MODEL"])

    # configure pgvector
    store = PGVector(
        embeddings=embeddings,
        collection_name=env_vars["PG_VECTOR_COLLECTION_NAME"],
        connection=env_vars["DATABASE_URL"],
        use_jsonb=True,
    )

    # save embeddings to pgvector
    store.add_documents(enriched, ids=ids)

    print("2 - Ingestion process completed successfully")


if __name__ == "__main__":
    ingest_pdf()