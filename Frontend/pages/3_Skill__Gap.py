import streamlit as st
import plotly.express as px
from components.api import get_skill_gap

st.title("📊 Skill Gap Analysis")

user_id = st.session_state.get("user_id", "123")

data = get_skill_gap(user_id)

if data:
    st.write("Missing Skills:")
    st.write(data["missing_skills"])

    fig = px.bar(
        x=data["skills"],
        y=data["scores"],
        title="Skill Strength Chart"
    )
    st.plotly_chart(fig)