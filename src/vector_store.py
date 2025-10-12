from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

def create_vector_store(chunks, persist_directory="data/chroma_db"):
    """Create and persist vector store in batches"""
    embeddings = OpenAIEmbeddings()
    
    # Process in batches to avoid token limits
    batch_size = 100  # Process 100 chunks at a time
    
    print(f"Processing {len(chunks)} chunks in batches of {batch_size}...")
    
    # Create vector store with first batch
    vectorstore = Chroma.from_documents(
        documents=chunks[:batch_size],
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    # Add remaining chunks in batches
    for i in range(batch_size, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}...")
        vectorstore.add_documents(batch)
    
    print(f"Vector store created with {len(chunks)} documents")
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