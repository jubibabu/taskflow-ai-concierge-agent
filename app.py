import os
import sys
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from agent import build_agent

st.set_page_config(page_title="TaskFlow AI Concierge", page_icon="Robot")
st.title("TaskFlow AI Concierge Agent")
st.caption("Ask about Notion features, pricing, or support - or ask me to book a demo / raise a ticket.")

if "agent" not in st.session_state:
    st.session_state.agent = build_agent()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(msg)

user_input = st.chat_input("Type your question...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.agent.run(user_input)
            except Exception as e:
                response = f"Sorry, I ran into an error: {e}"
            st.write(response)

    st.session_state.chat_history.append(("assistant", response))
