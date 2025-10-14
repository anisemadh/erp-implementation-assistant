from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os
import time
from datetime import datetime
load_dotenv()



def create_vector_store(chunks, persist_directory="data/chroma_db"):
    """Create and persist vector store in batches with detailed logging"""
    embeddings = OpenAIEmbeddings()
    
    # Process in batches to avoid token limits
    batch_size = 50  # CHANGED from 50 to 10
    delay_between_batches = 10  # ADDED: 5 second delay
    
    print(f"\n{'='*60}")
    print(f"Starting vector store creation at {datetime.now()}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Batch size: {batch_size}")
    print(f"Total batches: {(len(chunks)-1)//batch_size + 1}")
    print(f"{'='*60}\n")
    
    # Create vector store with first batch
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Creating initial vector store with first {batch_size} chunks...")
    start_time = time.time()
    
    try:
        vectorstore = Chroma.from_documents(
            documents=chunks[:batch_size],
            embedding=embeddings,
            persist_directory=persist_directory
        )
        elapsed = time.time() - start_time
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Batch 1 completed in {elapsed:.1f}s\n")
    except Exception as e:
        print(f"ERROR creating initial batch: {e}")
        raise
    
    # Add remaining chunks in batches
    total_batches = (len(chunks)-1)//batch_size + 1
    
    for i in range(batch_size, len(chunks), batch_size):
        batch_num = i//batch_size + 1
        batch = chunks[i:i + batch_size]
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Processing batch {batch_num}/{total_batches} ({len(batch)} chunks)...")
        start_time = time.time()
        
        try:
            vectorstore.add_documents(batch)
            elapsed = time.time() - start_time
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Batch {batch_num} completed in {elapsed:.1f}s")
            print(f"  Progress: {min(i + batch_size, len(chunks))}/{len(chunks)} chunks ({100*min(i + batch_size, len(chunks))//len(chunks)}%)\n")
            
            # ADDED: Wait between batches to avoid rate limits
            time.sleep(delay_between_batches)

        except Exception as e:
            print(f"\n❌ ERROR on batch {batch_num}: {e}")
            print(f"  Waiting 60 seconds before retry...")
            time.sleep(60)
            
            # Retry once
            try:
                print(f"  Retrying batch {batch_num}...")
                vectorstore.add_documents(batch)
                print(f"  ✓ Retry successful\n")
            except Exception as e2:
                print(f"  ❌ Retry failed: {e2}")
                print(f"  Skipping this batch and continuing...\n")
                continue
    
    print(f"\n{'='*60}")
    print(f"Vector store creation completed at {datetime.now()}")
    print(f"Total documents processed: {len(chunks)}")
    print(f"{'='*60}\n")
    
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