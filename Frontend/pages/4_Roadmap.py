import streamlit as st
from components.api import get_roadmap

st.title("🧭 Career Roadmap")

user_id = st.session_state.get("user_id", "123")

roadmap = get_roadmap(user_id)

if roadmap:
    for step in roadmap["steps"]:
        st.markdown(f"✅ {step}")