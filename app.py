import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Health Companion", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []
if 'fast_start' not in st.session_state:
    st.session_state.fast_start = None

st.title("Health Companion")

with st.container():
    st.subheader("Physical Profile")
    col1, col2 = st.columns(2)
    weight = col1.number_input("Weight (kg)", value=70.0, step=0.1)
    height = col2.number_input("Height (cm)", value=175.0, step=1.0)
    
    bmi = weight / ((height/100)**2)
    st.write(f"Current BMI: **{bmi:.1f}**")

with st.container():
    st.subheader("Water Fasting")
    if not st.session_state.fast_start:
        if st.button("Start Timer"):
            st.session_state.fast_start = datetime.now()
    else:
        elapsed = datetime.now() - st.session_state.fast_start
        hours = elapsed.total_seconds() // 3600
        st.write(f"Active Fast: **{int(hours)} hours**")
        if st.button("End Fast"):
            st.session_state.fast_start = None

with st.container():
    st.subheader("Daily Intake & Activity")
    meal = st.text_area("What did you eat?", placeholder="Describe your meals...")
    workout = st.text_area("Workout details", placeholder="Exercises performed...")
    done = st.checkbox("Daily workout completed")
    
    if st.button("Log Daily Data"):
        entry = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Meal": meal,
            "Workout": workout,
            "Status": "Completed" if done else "Pending"
        }
        st.session_state.history.append(entry)

with st.container():
    st.subheader("AI Recommendation")
    if weight > 0:
        if "sugar" in meal.lower() or "carbs" in meal.lower():
            st.warning("High glucose detected. Suggested: 20 min HIIT session.")
        elif done:
            st.success("Target reached. Focus on protein intake and recovery.")
        else:
            st.info("Recommendation: 30 min moderate cardio based on current profile.")

if st.session_state.history:
    with st.container():
        st.subheader("Recent Logs")
        df = pd.DataFrame(st.session_state.history).tail(5)
        st.dataframe(df, use_container_width=True)
