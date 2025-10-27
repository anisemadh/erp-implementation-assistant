import streamlit as st
import os

# Page config MUST be first Streamlit command
st.set_page_config(
    page_title="ERP Assistant",
    page_icon="🤖",
    layout="wide"
)

# Now handle API key (after page config)
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
elif "OPENAI_API_KEY" not in os.environ:
    st.error("⚠️ OpenAI API key not found. Please add it in Streamlit Cloud secrets.")
    st.stop()

# Import agent (after setting API key)
from agent import ERPAgent
import time

# Title
st.title("🤖 ERP Implementation Assistant")
st.markdown("Ask questions about Infor M3 implementation, configuration, and troubleshooting.")

# Initialize agent
@st.cache_resource
def load_agent():
    return ERPAgent()

agent = load_agent()

# Rest of your app continues...

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
    
    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("🔍 Thinking..."):
            try:
                # Use the agent to get response
                response, messages = agent.run(prompt, st.session_state.get("conversation_history", []))
                
                # Display response
                message_placeholder.markdown(response)
                
                # Update conversation history
                if "conversation_history" not in st.session_state:
                    st.session_state.conversation_history = []
                st.session_state.conversation_history = messages
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                message_placeholder.error(error_msg)
                response = error_msg
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

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