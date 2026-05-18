import streamlit as st
from components.api import chat_with_ai

st.title("💬 AI Career Mentor")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Ask anything about career...")

if st.button("Send"):
    response = chat_with_ai(user_input)

    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("AI", response["reply"]))

for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")