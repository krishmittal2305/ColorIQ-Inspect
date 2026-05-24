import streamlit as st
import pandas as pd
import os
import requests

st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

if st.session_state.role != "manager":
    st.error("⛔ Access Denied: Only manager can access this page.")
    st.stop()
st.title("📄 Inspection Reports")
st.caption("Filter, review and download supplier colour inspection reports.")

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwyiN6SfHfR6b3w-hu2lhzDFE01JEwaNLzOio3tqbHmHueYlSlKw9pBIYoy-o1Z1c4f/exec"

response = requests.get(GOOGLE_SCRIPT_URL)

if response.status_code != 200:
    st.error("Unable to load report data from Google Sheet.")
    st.stop()

df = pd.DataFrame(response.json())

if df.empty:
    st.warning("No inspection reports found yet.")
    st.stop()

c1, c2, c3 = st.columns(3)

with c1:
    supplier_filter = st.selectbox(
        "Filter by Supplier",
        ["All"] + sorted(df["Supplier"].dropna().unique())
    )

with c2:
    judgement_filter = st.selectbox(
        "Filter by Judgement",
        ["All", "Pass", "Fail"]
    )

with c3:
    warning_filter = st.selectbox(
        "Filter by Warning",
        ["All", "Normal", "Warnings Only"]
    )

filtered = df.copy()

if supplier_filter != "All":
    filtered = filtered[filtered["Supplier"] == supplier_filter]

if judgement_filter != "All":
    filtered = filtered[filtered["AI_Judgement"] == judgement_filter]

if warning_filter == "Normal":
    filtered = filtered[filtered["Validation_Warning"] == "Normal"]

elif warning_filter == "Warnings Only":
    filtered = filtered[filtered["Validation_Warning"] != "Normal"]

st.divider()

st.subheader("Filtered Report Data")

st.dataframe(
    filtered.sort_values(by="Timestamp", ascending=False),
    use_container_width=True
)

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Report CSV",
    csv,
    "filtered_inspection_report.csv",
    "text/csv",
    use_container_width=True
)

st.divider()

st.subheader("Report Summary")

total = len(filtered)
passed = len(filtered[filtered["AI_Judgement"] == "Pass"])
failed = len(filtered[filtered["AI_Judgement"] == "Fail"])
warnings = len(filtered[filtered["Validation_Warning"] != "Normal"])

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric("Total Records", total)

with s2:
    st.metric("Passed", passed)

with s3:
    st.metric("Failed", failed)

with s4:
    st.metric("Warnings", warnings)