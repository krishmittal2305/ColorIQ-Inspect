import streamlit as st

st.set_page_config(
    page_title="ColorIQ Inspect",
    page_icon="🎨",
    layout="wide"
)

# LOGIN SYSTEM
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if not st.session_state.logged_in:

    st.markdown("""
    <style>
    .stApp{
        background: linear-gradient(to right,#020617,#071a33,#020617);
        color:white;
    }

    .main-title{
        font-size:70px;
        font-weight:900;
        background: linear-gradient(to right,#38bdf8,#22c55e,#eab308);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        margin-bottom:10px;
    }

    .subtitle{
        font-size:28px;
        color:#cbd5e1;
        font-weight:600;
        margin-bottom:40px;
    }

    .login-box{
        background: rgba(15,23,42,0.9);
        padding:40px;
        border-radius:25px;
        border:1px solid rgba(255,255,255,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">ColorIQ Inspect</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="subtitle">AI Powered Automotive LAB Colour Inspection Platform</div>',
        unsafe_allow_html=True
    )

    with st.container():

        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if username == "supplier" and password == "1234":
                st.session_state.logged_in = True
                st.session_state.role = "supplier"
                st.rerun()

            elif username == "manager" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = "manager"
                st.rerun()

            else:
                st.error("Invalid username or password")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# SIDEBAR
st.sidebar.success(f"Logged in as: {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()

# HOME PAGE
st.markdown("""
<style>
.card{
    background:rgba(15,23,42,0.85);
    padding:30px;
    border-radius:25px;
    border:1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">

<h1 style="
font-size:70px;
font-weight:900;
background: linear-gradient(to right,#38bdf8,#22c55e,#eab308);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
">
ColorIQ Inspect
</h1>

<h3 style="color:#e2e8f0;">
Smart Automotive Colour Quality Inspection Platform
</h3>

<br>

<p style="font-size:22px;line-height:2;color:#cbd5e1;">
Digitizing manual Excel-based automotive colour inspection into an AI-powered intelligent platform using LAB colour space analysis, Delta E deviation measurement, automatic Pass/Fail judgement and interactive 2D/3D visual inspection.
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("## 🚀 Platform Highlights")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("🎯 Automatic Pass/Fail Judgement")

with c2:
    st.info("📊 2D & 3D LAB Visualizations")

with c3:
    st.info("🌐 Supplier + Manager Workflow")

with c4:
    st.info("📄 Inspection Reports & Analytics")