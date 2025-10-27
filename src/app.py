import streamlit as st
import os

st.set_page_config(page_title="ERP Assistant", page_icon="🤖")

# Load API key
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Simple imports
import sys
sys.path.insert(0, os.path.dirname(__file__))

from agent import ERPAgent

st.title("🤖 ERP Implementation Assistant")

# Initialize agent once
if "agent" not in st.session_state:
    st.session_state.agent = ERPAgent()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if prompt := st.chat_input("Ask a question..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response, _ = st.session_state.agent.run(prompt)
            st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
