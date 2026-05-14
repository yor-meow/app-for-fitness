import streamlit as st
import pandas as pd
from datetime import datetime
import json

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
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    if 'health_logs' not in st.session_state:
        st.session_state.health_logs = []

def save_data():
    pass 

load_data()

st.title("Health Companion")

with st.container():
    st.subheader("Profile")
    col1, col2 = st.columns(2)
    weight = col1.number_input("Weight (kg)", value=70.0)
    height = col2.number_input("Height (cm)", value=170.0)
    
    bmi = weight / ((height/100)**2)
    status = "Normal"
    if bmi < 18.5: status = "Underweight"
    elif bmi >= 25: status = "Overweight"
    
    st.info(f"BMI: {bmi:.1f} ({status})")

with st.container():
    st.subheader("Water Fasting")
    if 'fast_start' not in st.session_state:
        st.session_state.fast_start = None

    if not st.session_state.fast_start:
        if st.button("Start Timer"):
            st.session_state.fast_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        start_time = datetime.strptime(st.session_state.fast_start, "%Y-%m-%d %H:%M:%S")
        diff = datetime.now() - start_time
        hours = diff.total_seconds() / 3600
        st.write(f"Fast Duration: {hours:.1f} hours")
        if st.button("Stop Timer"):
            st.session_state.fast_start = None

with st.container():
    st.subheader("Daily Logs")
    food = st.text_input("Meal description")
    exercise = st.text_area("Exercise details")
    task_done = st.checkbox("Workout completed")
    
    if st.button("Save Daily Entry"):
        new_entry = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Food": food,
            "Exercise": exercise,
            "Done": task_done,
            "Weight": weight
        }
        st.session_state.health_logs.append(new_entry)
        st.success("Entry saved to session")

with st.container():
    st.subheader("AI Coach")
    if weight > 0:
        if "water" in food.lower() and not food:
            st.write("Current focus: Hydration maintenance.")
        elif task_done:
            st.write("Workout detected. Suggested: High protein meal for muscle recovery.")
        elif bmi > 25:
            st.write("Recommendation: 30 mins brisk walking. Limit carb intake tonight.")
        else:
            st.write("Profile steady. Maintain current movement routine.")

if st.session_state.health_logs:
    with st.container():
        st.subheader("History")
        history_df = pd.DataFrame(st.session_state.health_logs)
        st.dataframe(history_df, use_container_width=True)
