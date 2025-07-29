import streamlit as st
from datetime import datetime, timedelta

dateformat = "%Y-%m-%d"
timeformat = "%H%M"


with st.form("New Time", ):
    

    dateinput = st.text_input("Date")
    timeinput = st.text_input("Time")

    submitted = st.form_submit_button("Submit")

# datetime.striptime(st.text_input("Time"), timeformat)




if submitted:
    # st.write(dateinput)
    date = datetime.strptime(dateinput, dateformat)
    time = datetime.strptime(timeinput, timeformat)
    st.write(f"TimeStamp: {date} {time}")

    st.write(date + timedelta(time))
    # st.write(date.strftime("%m-%d-%Y"))