import streamlit as st
from datetime import datetime, timedelta
import pandas as pd


dateformat = "%Y-%m-%d"
timeformat = "%H%M"


with st.form("New Time", ):
    
    timeIn, timeOut = st.columns(2)

    with timeIn:

        indateinput = st.date_input("Date In")
        intimeinput = st.time_input("Time In")

    with timeOut:
    
        outdateinput = st.date_input("Date Out")
        outtimeinput = st.time_input("Time Out")

    submitted = st.form_submit_button("Submit")


if submitted:

    df = pd.DataFrame(
        {
            "date": [
                indateinput,
                outdateinput
            ],
            "action": [
                "clock_in",
                "clock_out"
            ],
            "time": [
                datetime.combine(indateinput, intimeinput),
                datetime.combine(outdateinput, outtimeinput)
            ]
        }
    )

    st.dataframe(df)