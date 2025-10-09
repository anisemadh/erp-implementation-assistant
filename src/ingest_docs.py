from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from pathlib import Path
import os

def load_and_split_documents(file_path):
    """Load markdown file and split into chunks"""
    loader = TextLoader(file_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from {file_path}")
    
    return chunks

def load_and_split_pdf(file_path):
    """Load PDF file and split into chunks"""
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from {file_path}")
    
    return chunks

def load_all_documents(docs_dir="docs"):
    """Load all markdown and PDF files from docs directory"""
    all_chunks = []
    docs_path = Path(docs_dir)
    
    # Process markdown files
    for file_path in docs_path.glob("*.md"):
        print(f"Processing markdown: {file_path}")
        chunks = load_and_split_documents(str(file_path))
        all_chunks.extend(chunks)
    
    # Process PDF files
    for file_path in docs_path.glob("*.pdf"):
        print(f"Processing PDF: {file_path}")
        try:
            chunks = load_and_split_pdf(str(file_path))
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue
    
    print(f"\nTotal chunks created: {len(all_chunks)}")
    return all_chunks

if __name__ == "__main__":
    chunks = load_all_documents()