from vector_store import load_vector_store

def test_search(query):
    """Test similarity search"""
    vectorstore = load_vector_store()
    
    results = vectorstore.similarity_search(query, k=3)
    
    print(f"\nQuery: {query}")
    print("="*50)
    for i, doc in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(doc.page_content[:300])
        print("...")

if __name__ == "__main__":
    # Test with queries relevant to your Infor knowledge
    test_queries = [
        "How do I configure supplier approval?",
        "Purchase requisition setup",
        "Common implementation mistakes"
    ]
    
    for query in test_queries:
        test_search(query)