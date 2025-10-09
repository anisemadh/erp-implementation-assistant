import streamlit as st
from agent import ERPAgent
from langchain_core.messages import HumanMessage, AIMessage

# Page configuration
st.set_page_config(
    page_title="ERP Implementation Assistant",
    page_icon="🏢",
    layout="centered"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "agent" not in st.session_state:
    st.session_state.agent = ERPAgent()

# App title and description
st.title("🏢 Infor ERP Implementation Assistant")
st.markdown("""
Ask questions about Infor ERP configuration, implementation best practices, 
and common challenges. This assistant uses your documented knowledge and experience.
""")

# Sidebar with info
# Sidebar with info
with st.sidebar:
    st.header("About")
    st.markdown("""
    This AI assistant helps with:
    - Customer Order Management
    - Purchasing & Inventory
    - Supplier Workflows
    - Vendor Rebates
    - And more...
    """)
    
    st.divider()
    
    st.header("Example Questions")
    example_questions = [
        "How do I configure supplier approval workflows?",
        "What are common mistakes in PO receiving?",
        "How does soft allocation work?",
        "What is demand time fence?",
    ]
    
    for question in example_questions:
        if st.button(question, key=question, use_container_width=True):
            # Add question to messages
            st.session_state.messages.append({"role": "user", "content": question})
            
            # Get response
            with st.spinner("Thinking..."):
                try:
                    docs = st.session_state.agent.vectorstore.similarity_search(question, k=3)
                    response, updated_history = st.session_state.agent.run(
                        question, 
                        st.session_state.conversation_history
                    )
                    st.session_state.conversation_history = updated_history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.divider()
    
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.rerun()
    
    st.divider()
    
    st.header("Session Stats")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Queries", len([m for m in st.session_state.messages if m["role"] == "user"]))
    
    st.markdown("---")
    st.caption("Powered by LangChain + LangGraph")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
# Chat input
if prompt := st.chat_input("Ask about Infor ERP implementation..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Retrieving relevant information..."):
            try:
                # Get retrieved documents for display
                docs = st.session_state.agent.vectorstore.similarity_search(prompt, k=3)
                
                response, updated_history = st.session_state.agent.run(
                    prompt, 
                    st.session_state.conversation_history
                )
                st.markdown(response)
                
                # Show sources in expander
                with st.expander("📚 View Sources"):
                    for i, doc in enumerate(docs, 1):
                        st.markdown(f"**Source {i}:**")
                        st.text(doc.page_content[:300] + "...")
                        st.divider()
                
                st.session_state.conversation_history = updated_history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})