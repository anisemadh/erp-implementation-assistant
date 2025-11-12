import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.agent import ERPAgent
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
def load_agent():
    return ERPAgent()

agent = load_agent()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check for queued query from example buttons
prompt = None
from_example = False
if "process_query" in st.session_state:
    prompt = st.session_state.process_query
    from_example = True
    del st.session_state.process_query
else:
    prompt = st.chat_input("Ask about M3 configuration, troubleshooting, or best practices...")

# Process query (either from chat input or example button)
if prompt:
    # Add user message to chat history (only if not from example button, as it's already added)
    if not from_example:
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message (only for chat input, example messages already displayed in history)
        with st.chat_message("user"):
            st.markdown(prompt)
    
    # Generate assistant response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Show thinking indicator
        with st.spinner("🔍 Analyzing query and retrieving context..."):
            # Step 1: Enhance query
            from src.query_enhancer import enhance_query
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
            
            # Store sources for display
            sources = [
                {
                    'source': doc.metadata.get('source', 'Unknown'),
                    'module': doc.metadata.get('module_str', 'Unknown'),
                    'doc_type': doc.metadata.get('doc_type', 'Unknown')
                } 
                for doc in docs
            ]
            
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
            
            # Display sources
            if sources:
                st.markdown("---")
                st.markdown(f"📚 **Sources** ({len(sources)} documents)")
                for i, source in enumerate(sources, 1):
                    module_info = f" (Module: {source['module']})" if source['module'] != 'Unknown' else ""
                    doc_type_info = f" [Type: {source['doc_type']}]" if source['doc_type'] != 'Unknown' else ""
                    st.markdown(f"**{i}.** {source['source']}{module_info}{doc_type_info}")
            
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
        if st.button(eq, key=eq):
            st.session_state.messages.append({"role": "user", "content": eq})
            st.session_state.process_query = eq
            st.rerun()