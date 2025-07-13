import streamlit as st

from loguru import logger

from utils.postgres_conn import postgres_conn_tst
from utils.timecardFunctions import getDateRange, dataPrep, calcPay

db = postgres_conn_tst()

logger.add("timecard.log")


def main():

    todays_date, start_date, end_date, pay_date = getDateRange()

    QUERY = (
        open("src/utils/daily_log.sql")
        .read()
        .format(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
        )
    )

    df = db.query(QUERY)

    df_display = dataPrep(df)

    pay = calcPay(df_display)

    st.title("TimeCard")
    st.markdown(
        f"""Pay Period: {start_date.strftime("%A, %B %e")} thru {end_date.strftime("%A, %B %e")}

Today's Date: {todays_date.strftime('%A, %B %d %Y')}

Pay Date: {pay_date.strftime("%A, %B %e")}
            """
    )

    st.write(f"Current Pay Amount: ${pay:.2f}")

    time_stamp = st.button("Time Stamp")

    st.session_state["table"] = df_display

    if time_stamp:
        db.writeTimeStamp()
        st.session_state["table"] = dataPrep(db.query(QUERY))

    st.dataframe(st.session_state.table)


if __name__ == "__main__":
    main()
