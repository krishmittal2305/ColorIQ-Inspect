import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Master Data",
    page_icon="⚙️",
    layout="wide"
)
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

if st.session_state.role != "manager":
    st.error("⛔ Access Denied: Only manager can access this page.")
    st.stop()

st.title("⚙️ Master Data Management")
st.caption("Add new model, colour, angle, part, master values and tolerance ranges.")

MASTER_FILE = "data/master_data.csv"

master = pd.read_csv(MASTER_FILE)

st.subheader("Existing Master Data")
st.dataframe(master, use_container_width=True)

st.divider()

st.subheader("Add New Master Standard")

c1, c2, c3, c4 = st.columns(4)

with c1:
    model = st.text_input("Model", "T11S")

with c2:
    color = st.text_input("Colour", "New Colour")

with c3:
    angle = st.text_input("Angle", "25°")

with c4:
    part = st.text_input("Part", "Part 1")

st.subheader("Master L*a*b* Values")

m1, m2, m3 = st.columns(3)

with m1:
    master_l = st.number_input("Master L", format="%.3f")

with m2:
    master_a = st.number_input("Master A", format="%.3f")

with m3:
    master_b = st.number_input("Master B", format="%.3f")

st.subheader("Operating Range")

r1, r2, r3 = st.columns(3)

with r1:
    l_from = st.number_input("L From", format="%.3f")
    l_to = st.number_input("L To", format="%.3f")

with r2:
    a_from = st.number_input("A From", format="%.3f")
    a_to = st.number_input("A To", format="%.3f")

with r3:
    b_from = st.number_input("B From", format="%.3f")
    b_to = st.number_input("B To", format="%.3f")

if st.button("Add Master Standard", use_container_width=True):

    new_row = {
        "Model": model,
        "Color": color,
        "Angle": angle,
        "Master_L": master_l,
        "Master_A": master_a,
        "Master_B": master_b,
        "L_From": l_from,
        "L_To": l_to,
        "A_From": a_from,
        "A_To": a_to,
        "B_From": b_from,
        "B_To": b_to,
        "Part": part,
        "Actual_L": master_l,
        "Actual_A": master_a,
        "Actual_B": master_b,
        "AI_Judgement": "Pass",
        "Reason": "Master standard entry",
        "Validation_Warning": "Normal"
    }

    master = pd.concat(
        [master, pd.DataFrame([new_row])],
        ignore_index=True
    )

    master.to_csv(MASTER_FILE, index=False)

    st.success("New master standard added successfully. Refresh the page to see updated dropdowns.")