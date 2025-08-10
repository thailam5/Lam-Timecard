import streamlit as st


from utils.analytics import weeklyData

df = weeklyData()

st.bar_chart(df, x="week_no", y="Pay", x_label="Week Number", y_label="Pay")
