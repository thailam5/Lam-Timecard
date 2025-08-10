import streamlit as st
from datetime import datetime, timedelta
import pandas as pd


dateformat = "%Y-%m-%d"
timeformat = "%H%M"

st.session_state["auth"] = False

if st.session_state["auth"] == False:
    auth = st.text_input("Password", type="password")

if auth == "avocado":
    st.session_state["auth"] = True

if st.session_state["auth"] == True:
    
    # NEW ENTRY FORM

    with st.form("New Time"):
        st.title("New Entry")
        
        timeIn, timeOut = st.columns(2)

        with timeIn:

            indateinput = st.date_input("Date In")
            intimeinput = st.time_input("Time In")

        with timeOut:
        
            outdateinput = st.date_input("Date Out")
            outtimeinput = st.time_input("Time Out")

        newSubmitted = st.form_submit_button("Submit")


    if newSubmitted:

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


    # UPDATE ENTRY FORM
    
    with st.form("Update Time"):
        st.title("Update Time")
        
        updateDate = st.date_input("Date")
        updateTime = st.time_input("Time")
        updateAction = st.selectbox("Actions", ["clock_in", "clock_out"])

        updateSubmitted = st.form_submit_button("Submit")


    if updateSubmitted:

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