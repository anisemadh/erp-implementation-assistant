from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from pathlib import Path
import os

def detect_module_from_content(text: str, source: str) -> list:
    """
    Detect which M3 modules are mentioned in a chunk
    Returns list of relevant modules
    """
    text_lower = text.lower()
    source_lower = source.lower()
    modules = []
    
    # Module detection patterns
    module_patterns = {
        'OIS': ['ois', 'customer order', 'sales order', 'order entry', 'ois100', 'ois010'],
        'PPS': ['pps', 'purchase order', 'purchasing', 'procurement', 'supplier', 'pps200', 'pps095'],
        'MMS': ['mms', 'inventory', 'warehouse', 'item master', 'stock', 'mms001', 'mms002'],
        'CRS': ['crs', 'customer master', 'customer relations', 'crs610'],
        'ARS': ['ars', 'accounts receivable', 'invoice', 'ars100'],
        'APS': ['aps', 'accounts payable', 'vendor invoice'],
        'MWS': ['mws', 'warehouse management', 'picking', 'delivery', 'mws410'],
        'GLS': ['gls', 'general ledger', 'gl account'],
    }
    
    # Check content and source for module indicators
    for module, patterns in module_patterns.items():
        if any(pattern in text_lower or pattern in source_lower for pattern in patterns):
            modules.append(module)
    
    # Default to 'GENERAL' if no specific module detected
    if not modules:
        modules.append('GENERAL')
    
    return modules


def detect_document_type(source: str) -> str:
    """Detect type of document from filename"""
    source_lower = source.lower()
    
    if 'sales' in source_lower or 'order management' in source_lower:
        return 'sales_orders'
    elif 'purchas' in source_lower or 'procurement' in source_lower:
        return 'purchasing'
    elif 'supply chain' in source_lower or 'execution' in source_lower:
        return 'supply_chain'
    elif 'bre' in source_lower:
        return 'business_rules'
    else:
        return 'general'

def load_and_split_documents(file_path):
    """Load markdown file and split into chunks with metadata"""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=500,
        length_function=len,
    )
    
    # Create document
    doc = Document(page_content=text, metadata={"source": file_path.split('/')[-1]})
    chunks = text_splitter.split_documents([doc])
    
    # Add enhanced metadata
    source_name = file_path.split('/')[-1]
    doc_type = 'knowledge_base'
    
    for chunk in chunks:
        modules = detect_module_from_content(chunk.page_content, source_name)
        chunk.metadata['source'] = source_name
        chunk.metadata['doc_type'] = doc_type
        chunk.metadata['module_str'] = ','.join(modules)  # Only string, not list
    
    print(f"Created {len(chunks)} chunks from {file_path}")
    
    return chunks

def load_and_split_pdf(file_path):
    """Load PDF file and split into chunks with metadata"""
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=500,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    
    # Add enhanced metadata to each chunk
    source_name = file_path.split('/')[-1]
    doc_type = detect_document_type(source_name)
    
    for chunk in chunks:
        # Detect modules mentioned in this chunk
        modules = detect_module_from_content(chunk.page_content, source_name)
        
        # Add metadata (only strings, not lists)
        chunk.metadata['source'] = source_name
        chunk.metadata['doc_type'] = doc_type
        chunk.metadata['module_str'] = ','.join(modules)  # Only store as comma-separated string
    
    print(f"Created {len(chunks)} chunks from {file_path}")
    print(f"  Document type: {doc_type}")
    print(f"  Sample modules detected: {chunks[0].metadata.get('modules', [])}")
    
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