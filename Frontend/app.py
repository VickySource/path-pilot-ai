import streamlit as st

st.set_page_config(page_title="PathPilot AI", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3 {
    color: #00ffd5;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.sidebar.title("🔐 Login")

    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if email and password:
            st.session_state.logged_in = True
            st.session_state.user_id = email
        else:
            st.sidebar.error("Enter details")

if not st.session_state.logged_in:
    login()
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