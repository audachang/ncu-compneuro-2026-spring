import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_csv("data/moe_higher_ed.csv")

# 一個 px.bar 呼叫 = 一張完整 bar chart
fig = px.bar(df, x="city_name", y="男生計",
             color="sector", barmode="group")

# 把這個 figure 物件直接交給 streamlit
st.plotly_chart(fig, use_container_width=True)


# streamlit run .\test_plotly.py
