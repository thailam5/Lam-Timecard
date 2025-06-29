import os
from datetime import date, datetime, timedelta

import streamlit as st
import pandas as pd

from postgres_conn import postgres_conn_tst, tableCleanUp
db = postgres_conn_tst()


def main():

    todays_date = date.today()

    start_date = todays_date + timedelta(
        days=1-todays_date.isoweekday(),
    )

    end_date = todays_date + timedelta(
        days=6-todays_date.isoweekday()-1,
    )
    
    pay_date = todays_date + timedelta(
        days=6-todays_date.isoweekday()-1,
    )

    st.title("Lam Timecard")
    st.markdown(f"""Pay Period: {start_date.strftime("%A, %B %e")} thru {end_date.strftime("%A, %B %e")}

Today's Date: {todays_date.strftime('%A, %B %d %Y')}

Pay Date: {pay_date.strftime("%A, %B %e")}
            """)
    
    time_stamp = st.button("Time Stamp")

    QUERY = f"""
    select * 
    from daily_log 
    -- where "date" between '{start_date}' and '{end_date}'
    """

    df = tableCleanUp(db.query(QUERY))

    st.write(df)

    if time_stamp:
        db.writeTimeStamp()
        st.rerun()


if __name__ == "__main__":
    main()
