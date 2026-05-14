import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Health Companion", layout="centered")

# --- RETRO PIXEL / NOTHING PHONE STYLE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

    /* Background and Global Text */
    .main { 
        background-color: #000000; 
    }
    
    html, body, [class*="st-"] {
        font-family: 'VT323', monospace !important;
        color: #ffffff !important;
        font-size: 1.15rem;
    }

    /* Modern Glass/Retro Card Style */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: #111111;
        padding: 25px;
        border-radius: 0px; /* Square edges for retro look */
        border: 2px solid #333333;
        margin-bottom: 20px;
    }

    /* Input Fields */
    input, textarea {
        background-color: #000000 !important;
        color: #ff0000 !important; /* Red accent for inputs */
        border: 1px solid #333333 !important;
        font-family: 'VT323', monospace !important;
    }

    /* Buttons - Dot Matrix Style */
    .stButton>button {
        width: 100%;
        border-radius: 0px;
        height: 3.5em;
        background-color: #ffffff;
        color: #000000 !important;
        border: 2px solid #ffffff;
        font-weight: bold;
        letter-spacing: 2px;
        text-transform: uppercase;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #000000;
        color: #ffffff !important;
    }

    /* Header Styling */
    h1, h2, h3 {
        text-transform: uppercase;
        letter-spacing: 4px;
        color: #ffffff !important;
    }

    /* BMI Info Box */
    .stAlert {
        background-color: #000000;
        border: 1px dashed #ffffff;
        color: #ffffff !important;
        border-radius: 0px;
    }
    
    /* Fix for DataFrame visibility */
    .stDataFrame {
        border: 1px solid #333333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP LOGIC ---
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("SYS_HEALTH_v1.0")

with st.container():
    st.subheader("User Profile")
    col1, col2 = st.columns(2)
    weight = col1.number_input("WEIGHT_KG", value=70.0)
    height = col2.number_input("HEIGHT_CM", value=170.0)
    bmi = weight / ((height/100)**2)
    st.info(f"STATUS_BMI: {bmi:.1f}")

with st.container():
    st.subheader("Water Fasting")
    if 'fast_start' not in st.session_state:
        st.session_state.fast_start = None
    
    if not st.session_state.fast_start:
        if st.button("Initialize Fast"):
            st.session_state.fast_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        start_time = datetime.strptime(st.session_state.fast_start, "%Y-%m-%d %H:%M:%S")
        hours = (datetime.now() - start_time).total_seconds() / 3600
        st.write(f"TIMER_ACTIVE: {hours:.1f} HRS")
        if st.button("Terminate Fast"):
            st.session_state.fast_start = None

with st.container():
    st.subheader("Data Entry")
    food = st.text_input("INTAKE_LOG")
    exercise = st.text_area("ACTIVITY_LOG")
    task_done = st.checkbox("WORKOUT_COMPLETE")
    
    if st.button("Sync Data"):
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
        st.success("SYNC_SUCCESSFUL")

with st.container():
    st.subheader("AI Coach Output")
    if weight > 0:
        if task_done:
            st.write("> Analysis: Workout detected. Priority: Protein intake.")
        elif bmi > 25:
            st.write("> Analysis: BMI elevated. Priority: 30m Cardio.")
        else:
            st.write("> Analysis: System steady. Maintain routine.")

try:
    history = conn.read(worksheet="Sheet1")
    if not history.empty:
        with st.container():
            st.subheader("History Log")
            st.dataframe(history.tail(5), use_container_width=True)
except:
    st.write("NO_RECORDS_FOUND")
