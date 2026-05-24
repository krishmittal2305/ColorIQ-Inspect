import streamlit as st
import pandas as pd




st.set_page_config(
    page_title="ColorIQ Inspect",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 ColorIQ Inspect Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "supplier" and password == "1591":
            st.session_state.logged_in = True
            st.session_state.role = "supplier"

        elif username == "manager" and password == "admin1191":
            st.session_state.logged_in = True
            st.session_state.role = "manager"

        else:
            st.error("Invalid Login")

    st.stop()

st.sidebar.success(f"Logged in as: {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()

master = pd.read_csv("data/master_data.csv")

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}

.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #000000);
    color: white;
}

[data-testid="stSidebar"] {
    background: #020617;
}

.block-container {
    padding-top: 2rem;
}

.hero-box {
    padding: 45px;
    border-radius: 28px;
    background: linear-gradient(135deg, #0f172a, #111827);
    border: 1px solid rgba(56,189,248,0.35);
    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
}

.title-text {
    font-size: 64px;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #22c55e, #facc15);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle-text {
    font-size: 26px;
    font-weight: 700;
    color: #f8fafc;
}

.desc-text {
    font-size: 18px;
    line-height: 1.7;
    color: #cbd5e1;
}

.card {
    padding: 24px;
    border-radius: 22px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(148,163,184,0.20);
    box-shadow: 0 12px 35px rgba(0,0,0,0.35);
    min-height: 160px;
}

.card h3 {
    color: #38bdf8;
}

.kpi {
    padding: 24px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(56,189,248,0.14), rgba(34,197,94,0.10));
    border: 1px solid rgba(56,189,248,0.25);
    text-align: center;
}

.kpi h2 {
    color: #38bdf8;
    font-size: 38px;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <div class="title-text">ColorIQ Inspect</div>
    <br>
    <div class="subtitle-text">Smart Automotive Colour Quality Inspection Platform</div>
    <br>
    <div class="desc-text">
    Digitizing manual Excel-based colour checking into a professional inspection platform.
    The system compares supplier-entered actual L*a*b* readings with master panel values,
    tolerance limits and operating ranges to generate automatic Pass/Fail judgement
    with 2D and 3D visual proof.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f'<div class="kpi"><h2>{len(master)}</h2><p>Master Records</p></div>', unsafe_allow_html=True)

with k2:
    st.markdown(f'<div class="kpi"><h2>{master["Model"].nunique()}</h2><p>Active Models</p></div>', unsafe_allow_html=True)

with k3:
    st.markdown(f'<div class="kpi"><h2>{master["Angle"].nunique()}</h2><p>Angles Covered</p></div>', unsafe_allow_html=True)

with k4:
    st.markdown(f'<div class="kpi"><h2>{master["Color"].nunique()}</h2><p>Colours Available</p></div>', unsafe_allow_html=True)

st.write("")
st.subheader("Platform Highlights")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
        <h3>🎯 Automatic Judgement</h3>
        <p>Checks L, A and B values against tolerance ranges and gives accurate Pass/Fail result.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <h3>📊 2D & 3D Analysis</h3>
        <p>Visualizes actual colour position against master range for easier manager review.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
        <h3>🏭 Supplier Workflow</h3>
        <p>Supplier enters readings remotely and manager can review judgement and graphs instantly.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.subheader("How It Works")

w1, w2, w3 = st.columns(3)

with w1:
    st.markdown("""
    <div class="card">
        <h3>1. Select Standard</h3>
        <p>Select model, colour, angle and part from master data.</p>
    </div>
    """, unsafe_allow_html=True)

with w2:
    st.markdown("""
    <div class="card">
        <h3>2. Enter Reading</h3>
        <p>Enter actual measured L, A and B values.</p>
    </div>
    """, unsafe_allow_html=True)

with w3:
    st.markdown("""
    <div class="card">
        <h3>3. Get Result</h3>
        <p>System shows Pass/Fail result with reason and visual proof.</p>
    </div>
    """, unsafe_allow_html=True)

st.success("Open Supplier Submission from the sidebar to start inspection.")