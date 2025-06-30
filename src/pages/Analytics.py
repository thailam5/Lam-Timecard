import streamlit as st


from utils.analytics import weeklyData
df = weeklyData()

st.bar_chart(
    df,
    x="week_no",
    y="hours_worked",
    x_label="Week Number",
    y_label="Hours Worked"
)
