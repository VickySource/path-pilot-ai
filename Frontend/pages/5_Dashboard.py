import streamlit as st
import plotly.graph_objects as go

st.title("📈 Analytics Dashboard")

score = 72  # later from API

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=score,
    title={'text': "Readiness Score"},
))

st.plotly_chart(fig)
