import streamlit as st
import os

st.set_page_config(page_title="PathPilot AI", layout="wide")

def load_css():
    css_path = os.path.join(
        os.path.dirname(__file__),
        "assets",
        "style.css"
    )

    if not os.path.exists(css_path):
        st.error(f"CSS file not found: {css_path}")
        return

    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------- CENTER LOGIN UI ----------------

if not st.session_state.get("logged_in", False):

    st.markdown(
        """
        <style>
        .login-box {
            text-align: center;
            box-shadow: 0px 0px 20px rgba(0,255,213,0.2);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    st.title("🚀 PathPilot AI Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            st.session_state.logged_in = True
            st.session_state.user_id = email
            st.rerun()
        else:
            st.error("Enter credentials")

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# ---------- SIDEBAR NAV ----------
st.sidebar.title("🚀 PathPilot AI")

menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Upload Resume", "Skill Gap", "Roadmap", "Dashboard", "Chat"]
)

# ---------- HOME ----------
if menu == "Home":
    st.title("🏠 Welcome to PathPilot AI")

    st.markdown("""
    AI Career Platform:
    - Upload Resume 📄  
    - Skill Analysis 📊  
    - Career Roadmap 🧭  
    - AI Chat 💬  
    """)

# ---------- UPLOAD ----------
elif menu == "Upload Resume":
    st.title("📄 Resume Upload")

    from components.api import upload_resume

    file = st.file_uploader("Upload your resume (PDF)")

    if file and st.button("Analyze"):
        result = upload_resume(file)
        st.json(result)

# ---------- SKILL GAP ----------
elif menu == "Skill Gap":
    st.title("📊 Skill Gap Analysis")

    from components.api import get_skill_gap

    user_id = st.session_state.user_id
    data = get_skill_gap(user_id)

    st.write(data)

# ---------- ROADMAP ----------
elif menu == "Roadmap":
    st.title("🧭 Career Roadmap")

    from components.api import get_roadmap

    user_id = st.session_state.user_id
    roadmap = get_roadmap(user_id)

    if roadmap:
        for step in roadmap.get("steps", []):
            st.success(step)

# ---------- DASHBOARD ----------
elif menu == "Dashboard":
    st.title("📈 Dashboard")

    import plotly.graph_objects as go

    score = 70

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Readiness Score"}
    ))

    st.plotly_chart(fig)

# ---------- CHAT ----------
elif menu == "Chat":
    st.title("💬 AI Mentor Chat")

    from components.api import chat_with_ai

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("Ask something")

    if st.button("Send"):
        if user_input:
            reply = chat_with_ai(user_input)
            st.session_state.messages.append(("You", user_input))
            st.session_state.messages.append(("AI", reply.get("reply", "")))

    for role, msg in st.session_state.messages:
        st.write(f"**{role}:** {msg}")