import streamlit as st
from components.api import upload_resume

st.title("📄 Upload Resume")

file = st.file_uploader("Upload PDF Resume")

if file:
    if st.button("Analyze"):
        result = upload_resume(file)
        st.json(result)
        st.session_state["analysis"] = result