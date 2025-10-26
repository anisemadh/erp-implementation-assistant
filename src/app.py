import streamlit as st
import os

# Load API key from Streamlit secrets
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Import after setting env var
from agent import ERPAgent
import time

# Page config
st.set_page_config(
    page_title="ERP Assistant",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 ERP Implementation Assistant")
st.markdown("Ask questions about Infor M3 implementation, configuration, and troubleshooting.")

# Initialize agent
@st.cache_resource

@st.cache_resource
def load_agent():
    import os
    from pathlib import Path
    
    # Check if vector store exists
    vector_store_path = Path("data/chroma_db")
    
    if not vector_store_path.exists():
        st.info("🔨 First-time setup: Building vector store from documentation...")
        st.warning("⏱️ This will take 15-20 minutes on first deployment. Please wait...")
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Build vector store
        import sys
        sys.path.append('src')
        
        from vector_store import create_vector_store
        from ingest_docs import load_all_documents
        
        with st.spinner("📚 Loading and processing documents..."):
            chunks = load_all_documents()
            st.info(f"Loaded {len(chunks)} document chunks")
        
        with st.spinner("🔧 Creating vector store (this takes a while)..."):
            vectorstore = create_vector_store(chunks)
        
        st.success("✅ Vector store created! App is ready to use.")
        st.balloons()
    
    return ERPAgent()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about M3 configuration, troubleshooting, or best practices..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate assistant response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Show thinking indicator
        with st.spinner("🔍 Analyzing query and retrieving context..."):
            # Step 1: Enhance query
            from query_enhancer import enhance_query
            enhanced_query = enhance_query(prompt)
            
            # Step 2: Detect modules
            relevant_modules = agent.detect_relevant_modules(prompt)
            
            # Step 3: Retrieve context
            if relevant_modules:
                docs = agent.vectorstore.similarity_search(enhanced_query, k=8)
                
                # Filter by modules
                filtered_docs = []
                for doc in docs:
                    module_str = doc.metadata.get('module_str', '')
                    doc_modules = module_str.split(',') if module_str else []
                    if any(module in doc_modules for module in relevant_modules):
                        filtered_docs.append(doc)
                docs = filtered_docs[:5]
            else:
                docs = agent.vectorstore.similarity_search(enhanced_query, k=5)
            
            # Build context
            context = "\n\n".join([
                f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
                for doc in docs
            ])
            
            # Classify query
            query_type = agent.classify_query_type(prompt)
        
        # Show generating indicator with module info
        status_text = "💭 Generating response"
        if relevant_modules:
            status_text += f" (Modules: {', '.join(relevant_modules)})"
        st.caption(status_text)
        
        # Stream response
        try:
            for chunk in agent.generate_response_stream(prompt, context, query_type):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            
            # Final response without cursor
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            error_msg = f"❌ Error generating response: {str(e)}"
            message_placeholder.error(error_msg)
            full_response = error_msg
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This assistant helps with:
    - **Configuration**: Setting up M3 modules
    - **Troubleshooting**: Diagnosing issues
    - **Best Practices**: Recommendations
    
    **Features:**
    - Cites specific M3 programs
    - Structured, detailed responses
    - Context-aware filtering
    """)
    
    st.header("📊 Session Info")
    st.metric("Messages", len(st.session_state.messages))
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.header("💡 Example Questions")
    example_questions = [
        "How do I configure a customer order type?",
        "Why can't I allocate inventory?",
        "What's the best way to handle backorders?",
        "How do I set up a new customer?",
        "Why doesn't pricing populate on order lines?"
    ]
    
    for eq in example_questions:
        if st.button(eq, key=eq, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": eq})
            st.rerun()