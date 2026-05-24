import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import requests

st.set_page_config(
    page_title="LAB Analysis",
    page_icon="🧪",
    layout="wide"
)
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

if st.session_state.role != "manager":
    st.error("⛔ Access Denied: Only manager can access this page.")
    st.stop()

st.title("🧪 LAB Colour Analysis")
st.caption("Visual inspection of actual colour reading against master tolerance range.")

master = pd.read_csv("data/master_data.csv")
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwyiN6SfHfR6b3w-hu2lhzDFE01JEwaNLzOio3tqbHmHueYlSlKw9pBIYoy-o1Z1c4f/exec"

response = requests.get(GOOGLE_SCRIPT_URL)

if response.status_code != 200:
    st.error("Unable to load submissions from Google Sheet.")
    st.stop()

submissions = pd.DataFrame(response.json())

if submissions.empty:
    st.warning("No submissions available yet.")
    st.stop()

submissions["Record"] = (
    submissions["Timestamp"].astype(str) + " | " +
    submissions["Supplier"].astype(str) + " | " +
    submissions["Color"].astype(str) + " | " +
    submissions["Angle"].astype(str) + " | " +
    submissions["Part"].astype(str)
)

record = st.selectbox("Select Submission Record", submissions["Record"])

row = submissions[submissions["Record"] == record].iloc[0]

selected = master[
    (master["Model"] == row["Model"]) &
    (master["Color"] == row["Color"]) &
    (master["Angle"] == row["Angle"]) &
    (master["Part"] == row["Part"])
].iloc[0]

actual_l = float(row["Actual_L"])
actual_a = float(row["Actual_A"])
actual_b = float(row["Actual_B"])

judgement = row["AI_Judgement"]
reason = row["Reason"]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Judgement", judgement)

with c2:
    st.metric("Model", row["Model"])

with c3:
    st.metric("Angle", row["Angle"])

with c4:
    st.metric("Part", row["Part"])

st.info(f"Reason: {reason}")

st.divider()

st.subheader("🎯 2D A-B Tolerance Zone")

master_a = float(selected["Master_A"])
master_b = float(selected["Master_B"])

min_a = float(selected["A_From"])
max_a = float(selected["A_To"])
min_b = float(selected["B_From"])
max_b = float(selected["B_To"])

fig = go.Figure()

fig.add_shape(
    type="rect",
    x0=min_b,
    x1=max_b,
    y0=min_a,
    y1=max_a,
    line=dict(color="#22c55e", width=3, dash="dash"),
    fillcolor="rgba(34,197,94,0.12)",
    layer="below"
)

fig.add_trace(go.Scatter(
    x=[master_b, actual_b],
    y=[master_a, actual_a],
    mode="lines",
    line=dict(color="#facc15", width=3, dash="dot"),
    name="Deviation Line"
))

fig.add_trace(go.Scatter(
    x=[master_b],
    y=[master_a],
    mode="markers+text",
    marker=dict(size=18, color="#38bdf8", line=dict(color="white", width=2)),
    text=[f"MASTER<br>A={master_a:.2f}, B={master_b:.2f}"],
    textposition="bottom center",
    name="Master"
))

fig.add_trace(go.Scatter(
    x=[actual_b],
    y=[actual_a],
    mode="markers+text",
    marker=dict(
        size=20,
        color="#22c55e" if judgement == "Pass" else "#ef4444",
        line=dict(color="white", width=2)
    ),
    text=[f"ACTUAL<br>A={actual_a:.2f}, B={actual_b:.2f}"],
    textposition="top center",
    name="Actual"
))

b_span = max_b - min_b
a_span = max_a - min_a

x_padding = max(b_span * 0.35, 0.6)
y_padding = max(a_span * 0.35, 0.4)

x_min = min(min_b, master_b, actual_b) - x_padding
x_max = max(max_b, master_b, actual_b) + x_padding

y_min = min(min_a, master_a, actual_a) - y_padding
y_max = max(max_a, master_a, actual_a) + y_padding

fig.update_layout(
    template="plotly_dark",
    height=600,
    title="A-B Colour Tolerance Inspection",
    xaxis_title="B Value",
    yaxis_title="A Value",
    plot_bgcolor="#07111f",
    paper_bgcolor="#07111f",
    font=dict(color="#f8fafc")
)

fig.update_xaxes(range=[x_min, x_max], gridcolor="rgba(255,255,255,0.10)")
fig.update_yaxes(range=[y_min, y_max], gridcolor="rgba(255,255,255,0.10)")

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("🧊 3D L-A-B Master vs Actual")

fig3d = go.Figure()

fig3d.add_trace(go.Scatter3d(
    x=[float(selected["Master_L"])],
    y=[float(selected["Master_A"])],
    z=[float(selected["Master_B"])],
    mode="markers+text",
    marker=dict(size=8, color="#38bdf8"),
    text=["Master"],
    name="Master"
))

fig3d.add_trace(go.Scatter3d(
    x=[actual_l],
    y=[actual_a],
    z=[actual_b],
    mode="markers+text",
    marker=dict(size=8, color="#22c55e" if judgement == "Pass" else "#ef4444"),
    text=["Actual"],
    name="Actual"
))

fig3d.add_trace(go.Scatter3d(
    x=[float(selected["Master_L"]), actual_l],
    y=[float(selected["Master_A"]), actual_a],
    z=[float(selected["Master_B"]), actual_b],
    mode="lines",
    line=dict(color="#facc15", width=6),
    name="Deviation"
))

fig3d.update_layout(
    template="plotly_dark",
    height=650,
    scene=dict(
        xaxis_title="L",
        yaxis_title="A",
        zaxis_title="B"
    ),
    title="3D LAB Colour Difference Visualization"
)

st.plotly_chart(fig3d, use_container_width=True)