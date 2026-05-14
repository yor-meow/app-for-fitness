import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Health Companion", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

    .stApp {
        background-color: #000000 !important;
    }

    h1, h2, h3, p, label, span, div {
        font-family: 'VT323', monospace !important;
        color: #ffffff !important;
    }

    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: #1a1a1a !important;
        padding: 20px;
        border: 2px solid #333333;
        border-radius: 0px;
        margin-bottom: 10px;
    }

    input, textarea {
        background-color: #000000 !important;
        color: #00ff41 !important; 
        border: 1px solid #444444 !important;
        font-family: 'VT323', monospace !important;
    }

    .stButton>button {
        width: 100%;
        border-radius: 0px !important;
        height: 3.5em;
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        font-weight: bold;
        text-transform: uppercase;
        font-family: 'VT323', monospace !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    .stButton>button:hover {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    [data-testid="stTable"] {
        background-color: #111111 !important;
        color: #ffffff !important;
    }
    
    *:focus {
        outline: none !important;
        border: 1px solid #00ff41 !important;
    }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("USER_SYSTEM_v1.0")

with st.container():
    st.subheader("I_METRICS")
    col1, col2 = st.columns(2)
    weight = col1.number_input("WEIGHT_KG", value=70.0)
    height = col2.number_input("HEIGHT_CM", value=170.0)
    bmi = weight / ((height/100)**2)
    st.write(f"BMI_INDEX: {bmi:.1f}")

with st.container():
    st.subheader("II_FASTING")
    if 'fast_start' not in st.session_state:
        st.session_state.fast_start = None
    
    if not st.session_state.fast_start:
        if st.button("START_TIMER"):
            st.session_state.fast_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        start_time = datetime.strptime(st.session_state.fast_start, "%Y-%m-%d %H:%M:%S")
        hours = (datetime.now() - start_time).total_seconds() / 3600
        st.write(f"TIME_ELAPSED: {hours:.1f} HRS")
        if st.button("END_TIMER"):
            st.session_state.fast_start = None

with st.container():
    st.subheader("III_LOGS")
    food = st.text_input("INTAKE_DESC")
    exercise = st.text_area("ACTIVITY_DESC")
    task_done = st.checkbox("WORKOUT_COMPLETE")
    
    if st.button("SYNC_TO_CLOUD"):
        try:
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
            st.success("DATA_SYNC_OK")
        except Exception as e:
            st.error("SYNC_ERROR: CHECK_PERMISSIONS")

with st.container():
    st.subheader("IV_AI_ANALYTICS")
    if weight > 0:
        if task_done:
            st.write("> STATUS: TRAINING DETECTED. UP PROTEIN.")
        elif bmi > 25:
            st.write("> STATUS: BMI OVER LIMIT. START CARDIO.")
        else:
            st.write("> STATUS: OPTIMAL.")

try:
    history = conn.read(worksheet="Sheet1")
    if not history.empty:
        with st.container():
            st.subheader("V_HISTORY")
            st.dataframe(history.tail(5), use_container_width=True)
except:
    st.write("WAITING_FOR_DATA...")
