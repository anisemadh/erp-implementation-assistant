import streamlit as st
import os

# Debug: Check if secrets exist
st.write("DEBUG: Checking secrets...")
if "OPENAI_API_KEY" in st.secrets:
    st.write("✅ API key found in secrets")
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    st.write(f"✅ Set in environment: {os.environ.get('OPENAI_API_KEY')[:10]}...")
else:
    st.error("❌ OPENAI_API_KEY not found in Streamlit secrets!")
    st.stop()

# Verify it's in environment
if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ API key not in environment after setting!")
    st.stop()

st.write("✅ API key verified in environment")

# Now import agent
from agent import ERPAgent
import time

st.write("✅ Imports successful")

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

# Load agent into variable
agent = load_agent()

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