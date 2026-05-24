import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import requests

st.set_page_config(page_title="Supplier Submission", page_icon="📥", layout="wide")
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

if st.session_state.role != "supplier":
    st.error("⛔ Access Denied: Only supplier can access this page.")
    st.stop()

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwyiN6SfHfR6b3w-hu2lhzDFE01JEwaNLzOio3tqbHmHueYlSlKw9pBIYoy-o1Z1c4f/exec"

st.title("📥 Supplier Colour Reading Submission")
st.caption("Enter actual L*a*b* values and get automatic Pass/Fail judgement with visual proof.")

master = pd.read_csv("data/master_data.csv")

def check_result(row, actual_l, actual_a, actual_b):
    l_pass = row["L_From"] <= actual_l <= row["L_To"]
    a_pass = row["A_From"] <= actual_a <= row["A_To"]
    b_pass = row["B_From"] <= actual_b <= row["B_To"]

    reasons = []
    if not l_pass:
        reasons.append("L out of range")
    if not a_pass:
        reasons.append("A out of range")
    if not b_pass:
        reasons.append("B out of range")

    judgement = "Pass" if l_pass and a_pass and b_pass else "Fail"
    reason = "All values within range" if not reasons else ", ".join(reasons)

    warnings = []
    if row["Master_B"] < 0 and actual_b > 0:
        warnings.append("Possible B sign mismatch")
    if row["Master_A"] < 0 and actual_a > 0:
        warnings.append("Possible A sign mismatch")

    warning = "Normal" if not warnings else ", ".join(warnings)

    return judgement, reason, warning

left, right = st.columns([1, 1])

with left:
    supplier = st.text_input("Supplier Name", "Supplier A")

    model = st.selectbox("Select Model", sorted(master["Model"].dropna().unique()))
    model_df = master[master["Model"] == model]

    color = st.selectbox("Select Color", sorted(model_df["Color"].dropna().unique()))
    color_df = model_df[model_df["Color"] == color]

    angle = st.selectbox("Select Angle", sorted(color_df["Angle"].dropna().unique()))
    angle_df = color_df[color_df["Angle"] == angle]

    part = st.selectbox("Select Part", sorted(angle_df["Part"].dropna().unique()))
    selected = angle_df[angle_df["Part"] == part].iloc[0]

    st.subheader("Enter Actual Reading")

    actual_l = st.number_input("Actual L Value", value=float(selected["Actual_L"]), format="%.3f")
    actual_a = st.number_input("Actual A Value", value=float(selected["Actual_A"]), format="%.3f")
    actual_b = st.number_input("Actual B Value", value=float(selected["Actual_B"]), format="%.3f")

    submit = st.button("Inspect Colour Reading", use_container_width=True)

with right:
    st.subheader("Master Standard")

    st.write(f"**Master L:** {selected['Master_L']}")
    st.write(f"**Master A:** {selected['Master_A']}")
    st.write(f"**Master B:** {selected['Master_B']}")

    st.write("---")

    st.write(f"**L Range:** {selected['L_From']} to {selected['L_To']}")
    st.write(f"**A Range:** {selected['A_From']} to {selected['A_To']}")
    st.write(f"**B Range:** {selected['B_From']} to {selected['B_To']}")

judgement, reason, warning = check_result(selected, actual_l, actual_a, actual_b)
delta_l = actual_l - float(selected["Master_L"])
delta_a = actual_a - float(selected["Master_A"])
delta_b = actual_b - float(selected["Master_B"])

delta_e = (delta_l**2 + delta_a**2 + delta_b**2) ** 0.5

if submit:
    st.divider()

    if judgement == "Pass":
        st.success(f"✅ PASS — {reason} | Validation: {warning}")
    else:
        st.error(f"❌ FAIL — {reason} | Validation: {warning}")

    submission = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Supplier": supplier,
        "Model": model,
        "Color": color,
        "Angle": angle,
        "Part": part,
        "Actual_L": actual_l,
        "Actual_A": actual_a,
        "Actual_B": actual_b,
        "AI_Judgement": judgement,
        "Reason": reason,
        "Validation_Warning": warning,
        "Delta_L": round(delta_l, 3),
        "Delta_A": round(delta_a, 3),
        "Delta_B": round(delta_b, 3),
        "Delta_E": round(delta_e, 3),
    }

    response = requests.post(GOOGLE_SCRIPT_URL, json=submission)

    if response.status_code == 200:
        st.success("Submission saved successfully to Google Sheet.")
    else:
        st.error("Submission result shown, but saving to Google Sheet failed.")

st.divider()

st.subheader("🎯 2D A-B Tolerance Zone")

master_a = float(selected["Master_A"])
master_b = float(selected["Master_B"])

min_a = float(selected["A_From"])
max_a = float(selected["A_To"])
min_b = float(selected["B_From"])
max_b = float(selected["B_To"])

actual_a = float(actual_a)
actual_b = float(actual_b)

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

fig.update_layout(
    template="plotly_dark",
    height=600,
    title="A-B Colour Tolerance Inspection",
    xaxis_title="B Value",
    yaxis_title="A Value",
    plot_bgcolor="#07111f",
    paper_bgcolor="#07111f"
)

fig.update_xaxes(
    range=[min(min_b, master_b, actual_b) - x_padding, max(max_b, master_b, actual_b) + x_padding],
    gridcolor="rgba(255,255,255,0.10)"
)

fig.update_yaxes(
    range=[min(min_a, master_a, actual_a) - y_padding, max(max_a, master_a, actual_a) + y_padding],
    gridcolor="rgba(255,255,255,0.10)"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🌈 Full 3D LAB Colour Universe")

import numpy as np

def lab_to_rgb(L, a, b):
    y = (L + 16) / 116
    x = a / 500 + y
    z = y - b / 200

    def pivot(t):
        return t ** 3 if t ** 3 > 0.008856 else (t - 16 / 116) / 7.787

    x = 95.047 * pivot(x)
    y = 100.000 * pivot(y)
    z = 108.883 * pivot(z)

    x /= 100
    y /= 100
    z /= 100

    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    blue = x * 0.0557 + y * -0.2040 + z * 1.0570

    def gamma(c):
        return 1.055 * (c ** (1 / 2.4)) - 0.055 if c > 0.0031308 else 12.92 * c

    r = max(0, min(255, gamma(r) * 255))
    g = max(0, min(255, gamma(g) * 255))
    blue = max(0, min(255, gamma(blue) * 255))

    return f"rgb({int(r)}, {int(g)}, {int(blue)})"


master_l = float(selected["Master_L"])
master_a = float(selected["Master_A"])
master_b = float(selected["Master_B"])

actual_l = float(actual_l)
actual_a = float(actual_a)
actual_b = float(actual_b)

# Wider colour universe
L_values = np.linspace(10, 95, 8)
A_values = np.linspace(-80, 80, 17)
B_values = np.linspace(-80, 80, 17)

x_vals = []
y_vals = []
z_vals = []
colors = []

for L in L_values:
    for A in A_values:
        for B in B_values:
            x_vals.append(L)
            y_vals.append(A)
            z_vals.append(B)
            colors.append(lab_to_rgb(L, A, B))

master_color = lab_to_rgb(master_l, master_a, master_b)
actual_color = lab_to_rgb(actual_l, actual_a, actual_b)

fig3d = go.Figure()

fig3d.add_trace(go.Scatter3d(
    x=x_vals,
    y=y_vals,
    z=z_vals,
    mode="markers",
    marker=dict(
        size=4,
        color=colors,
        opacity=0.75
    ),
    name="Full LAB Colour Space"
))

fig3d.add_trace(go.Scatter3d(
    x=[master_l],
    y=[master_a],
    z=[master_b],
    mode="markers+text",
    marker=dict(size=18, color=master_color, line=dict(color="white", width=5)),
    text=["MASTER"],
    textposition="top center",
    name="Master Colour"
))

fig3d.add_trace(go.Scatter3d(
    x=[actual_l],
    y=[actual_a],
    z=[actual_b],
    mode="markers+text",
    marker=dict(size=18, color=actual_color, line=dict(color="white", width=5)),
    text=["ACTUAL"],
    textposition="top center",
    name="Actual Colour"
))

fig3d.add_trace(go.Scatter3d(
    x=[master_l, actual_l],
    y=[master_a, actual_a],
    z=[master_b, actual_b],
    mode="lines",
    line=dict(color="yellow", width=8),
    name=f"ΔE Distance = {round(delta_e, 3)}"
))

fig3d.update_layout(
    template="plotly_dark",
    height=760,
    title=f"Full Coloured LAB Space | Master vs Actual | ΔE = {round(delta_e, 3)}",
    scene=dict(
        xaxis_title="L - Lightness",
        yaxis_title="A - Green ↔ Red",
        zaxis_title="B - Blue ↔ Yellow",
        bgcolor="#07111f"
    ),
    paper_bgcolor="#07111f"
)

st.plotly_chart(fig3d, use_container_width=True)

st.info("The full background cloud shows the wider LAB colour universe. Master and Actual points show where your inspected colour lies inside that space.")