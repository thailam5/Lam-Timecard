import os
from datetime import date, datetime, timedelta

import streamlit as st
import pandas as pd

from utils.postgres_conn import postgres_conn_tst, tableCleanUp

db = postgres_conn_tst()


def main():

    todays_date = date.today()

    start_date = todays_date + timedelta(
        days=1-todays_date.isoweekday(),
    )

    end_date = todays_date + timedelta(
        days=5-todays_date.isoweekday(),
    )
    
    pay_date = todays_date + timedelta(
        days=6-todays_date.isoweekday()-1,
    )

    QUERY = f"""
    select * 
    from daily_log
    where "Date" between '{start_date}' and '{end_date}'
    """
    df = db.query(QUERY)

    if df.shape[0] == 0:
        df_display = pd.DataFrame(
            {
                "Date": [],
                "Start": [],
                "End": [],
                "Worked (hrs)": []
            }
        )

    else:

        df_display = df.copy()
    
    st.title("TimeCard")
    st.markdown(f"""Pay Period: {start_date.strftime("%A, %B %e")} thru {end_date.strftime("%A, %B %e")}

Today's Date: {todays_date.strftime('%A, %B %d %Y')}

Pay Date: {pay_date.strftime("%A, %B %e")}
            """)
    
    try:
        pay = (df_display['Worked (hrs)'].sum()*14)
    
    except:
        pay = 0.00

    st.write(f"Current Pay Amount: ${pay:.2f}")

    time_stamp = st.button("Time Stamp")

    st.session_state["table"] = df_display
    
    if time_stamp:
        db.writeTimeStamp()
        st.session_state["table"] = db.query(QUERY)


    st.dataframe(st.session_state.table)

    
if __name__ == "__main__":
    main()
