import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Health Companion", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        background-color: #000000;
        color: white;
        border: none;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("Health Companion")

with st.container():
    st.subheader("Profile")
    col1, col2 = st.columns(2)
    weight = col1.number_input("Weight (kg)", value=70.0)
    height = col2.number_input("Height (cm)", value=170.0)
    bmi = weight / ((height/100)**2)
    st.info(f"BMI: {bmi:.1f}")

with st.container():
    st.subheader("Water Fasting")
    if 'fast_start' not in st.session_state:
        st.session_state.fast_start = None
    if not st.session_state.fast_start:
        if st.button("Start Timer"):
            st.session_state.fast_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        start_time = datetime.strptime(st.session_state.fast_start, "%Y-%m-%d %H:%M:%S")
        hours = (datetime.now() - start_time).total_seconds() / 3600
        st.write(f"Fast Duration: {hours:.1f} hours")
        if st.button("Stop Timer"):
            st.session_state.fast_start = None

with st.container():
    st.subheader("Daily Logs")
    food = st.text_input("Meal description")
    exercise = st.text_area("Exercise details")
    task_done = st.checkbox("Workout completed")
    
    if st.button("Save Daily Entry"):
        data = conn.read(worksheet="Sheet1")
        new_row = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Food": food,
            "Exercise": exercise,
            "Done": str(task_done),
            "Weight": weight
        }])
        updated_df = pd.concat([data, new_row], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        st.success("Saved to Google Sheets!")

with st.container():
    st.subheader("AI Coach")
    if weight > 0:
        if task_done:
            st.write("Workout detected. Suggested: High protein meal.")
        elif bmi > 25:
            st.write("Recommendation: 30 mins walking. Limit carbs.")
        else:
            st.write("Maintain current routine.")

try:
    history = conn.read(worksheet="Sheet1")
    if not history.empty:
        with st.container():
            st.subheader("History")
            st.dataframe(history.tail(5), use_container_width=True)
except:
    st.write("No history found yet.")
