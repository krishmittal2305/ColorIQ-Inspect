import streamlit as st
import pandas as pd
import plotly.express as px
import os
import requests

st.set_page_config(
    page_title="Manager Dashboard",
    page_icon="📊",
    layout="wide"
)
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

if st.session_state.role != "manager":
    st.error("⛔ Access Denied: Only manager can access this page.")
    st.stop()

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #000000);
    color: white;
}

.kpi {
    padding: 24px;
    border-radius: 22px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(148,163,184,0.20);
    text-align: center;
}

.kpi h2 {
    color: #38bdf8;
    font-size: 36px;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Manager Quality Dashboard")
st.caption("Review supplier submissions, failures, warnings and inspection summary.")

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwyiN6SfHfR6b3w-hu2lhzDFE01JEwaNLzOio3tqbHmHueYlSlKw9pBIYoy-o1Z1c4f/exec"

response = requests.get(GOOGLE_SCRIPT_URL)

if response.status_code != 200:
    st.error("Unable to load data from Google Sheet.")
    st.stop()

df = pd.DataFrame(response.json())

if df.empty:
    st.warning("No supplier submissions available yet.")
    st.stop()

total = len(df)
passed = len(df[df["AI_Judgement"] == "Pass"])
failed = len(df[df["AI_Judgement"] == "Fail"])
warnings = len(df[df["Validation_Warning"] != "Normal"])

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f'<div class="kpi"><h2>{total}</h2><p>Total Submissions</p></div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="kpi"><h2>{passed}</h2><p>Passed</p></div>', unsafe_allow_html=True)

with c3:
    st.markdown(f'<div class="kpi"><h2>{failed}</h2><p>Failed</p></div>', unsafe_allow_html=True)

with c4:
    st.markdown(f'<div class="kpi"><h2>{warnings}</h2><p>Validation Warnings</p></div>', unsafe_allow_html=True)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Pass vs Fail Summary")
    fig = px.pie(
        df,
        names="AI_Judgement",
        template="plotly_dark",
        hole=0.45,
        color="AI_Judgement",
        color_discrete_map={
            "Pass": "#22c55e",
            "Fail": "#ef4444"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Failure Reasons")
    fail_df = df[df["AI_Judgement"] == "Fail"]

    if not fail_df.empty:
        reason_count = fail_df["Reason"].value_counts().reset_index()
        reason_count.columns = ["Reason", "Count"]

        fig = px.bar(
            reason_count,
            x="Reason",
            y="Count",
            template="plotly_dark",
            color="Count",
            color_continuous_scale="Reds"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No failed submissions found.")

st.divider()

st.subheader("Supplier-wise Submission Summary")

supplier_summary = (
    df.groupby(["Supplier", "AI_Judgement"])
    .size()
    .reset_index(name="Count")
)

fig = px.bar(
    supplier_summary,
    x="Supplier",
    y="Count",
    color="AI_Judgement",
    barmode="group",
    template="plotly_dark",
    color_discrete_map={
        "Pass": "#22c55e",
        "Fail": "#ef4444"
    }
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Latest Supplier Submissions")

st.dataframe(
    df.sort_values(by="Timestamp", ascending=False),
    use_container_width=True
)

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Full Inspection Report",
    csv,
    "inspection_report.csv",
    "text/csv",
    use_container_width=True
)