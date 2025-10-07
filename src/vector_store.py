from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

def create_vector_store(chunks, persist_directory="data/chroma_db"):
    """Create and persist vector store"""
    embeddings = OpenAIEmbeddings()
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    print(f"Vector store created with {vectorstore._collection.count()} documents")
    return vectorstore

def load_vector_store(persist_directory="data/chroma_db"):
    """Load existing vector store"""
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    return vectorstore

if __name__ == "__main__":
    from ingest_docs import load_all_documents
    
    # Load and chunk documents
    chunks = load_all_documents()
    
    # Create vector store
    vectorstore = create_vector_store(chunks)
    print("Vector store created successfully!")