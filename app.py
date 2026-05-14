import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="AI Health Companion", layout="wide")

# --- APP STATE MANAGEMENT ---
if 'workout_log' not in st.session_state:
    st.session_state.workout_log = []
if 'fasting_start' not in st.session_state:
    st.session_state.fasting_start = None

# --- HEADER & AI ADVISOR ---
st.title("🛡️ AI Health Companion")
st.subheader("Your Personalized Bio-Assistant")

# --- SECTION 1: PHYSICAL STATS ---
with st.sidebar:
    st.header("Profile Metrics")
    weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0)
    height = st.number_input("Height (cm)", min_value=1.0, value=170.0)
    
    bmi = weight / ((height/100) ** 2)
    st.metric("Your BMI", f"{bmi:.1f}")
    
    if bmi < 18.5: status = "Underweight"
    elif 18.5 <= bmi < 25: status = "Healthy"
    else: status = "Overweight"
    st.info(f"Status: {status}")

# --- SECTION 2: WATER FASTING TIMER ---
st.header("💧 Water Fasting Tracker")
col1, col2 = st.columns(2)

with col1:
    if st.button("Start New Fast"):
        st.session_state.fasting_start = datetime.now()
    
    if st.session_state.fasting_start:
        duration = datetime.now() - st.session_state.fasting_start
        days = duration.days
        hours = duration.seconds // 3600
        st.success(f"Current Fast: {days} Days, {hours} Hours")
    else:
        st.write("No active fast.")

# --- SECTION 3: DAILY WORKOUT & MEAL LOG ---
st.header("🏋️ Daily Tasks & Logs")

date_today = datetime.now().strftime("%Y-%m-%d")
meal = st.text_input("What did you eat today?", placeholder="e.g. Grilled chicken, salad")
workout_done = st.checkbox("Finished daily workout?")

if st.button("Log Day"):
    entry = {"Date": date_today, "Meal": meal, "Workout": workout_done}
    st.session_state.workout_log.append(entry)
    st.toast("Day Logged Successfully!")

# --- SECTION 4: DYNAMIC AI RECOMMENDATION ---
st.divider()
st.header("🤖 AI Recommendation")

def get_ai_advice(bmi_status, is_fasting, meal_input):
    if is_fasting:
        return "You are currently fasting. Stick to light stretching or walking. Avoid heavy lifting."
    elif "sugar" in meal_input.lower() or "pizza" in meal_input.lower():
        return "High calorie intake detected. Recommendation: 30 mins of High-Intensity Interval Training (HIIT)."
    elif bmi_status == "Healthy":
        return "Maintain current form: 4 sets of Push-ups, Squats, and 5km Run."
    else:
        return "Focus on steady-state cardio (brisk walking) and high-protein meals."

advice = get_ai_advice(status, st.session_state.fasting_start is not None, meal)
st.write(advice)

# --- DISPLAY HISTORY ---
if st.session_state.workout_log:
    st.table(pd.DataFrame(st.session_state.workout_log))