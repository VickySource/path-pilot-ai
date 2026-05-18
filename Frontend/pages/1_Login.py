import streamlit as st

st.title("🔐 Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if email and password:
        st.success("Login successful (mock)")
        st.session_state["user_id"] = "123"
    else:
        st.error("Enter credentials")