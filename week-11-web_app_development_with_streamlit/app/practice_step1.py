"""Hands-on Practice 1 — Hello, Streamlit.

Run with:
    streamlit run practice_step1.py

Goal: 建立第一個 Streamlit app，顯示 cognitive aging dataset 的基本資訊。

Tasks (照順序完成):
1. 顯示一個 title「🧠 Cognitive Aging Dashboard」
2. 用 st.write 加上一行說明文字
3. 用 pd.read_csv 載入 data/cognitive_aging_taiwan.csv
4. 用 st.metric 顯示總受試者數與平均年齡
5. 用 st.dataframe 顯示前 10 列資料
"""

import streamlit as st
import pandas as pd

# 1. Title
# TODO: 用 st.title(...) 顯示 "🧠 Cognitive Aging Dashboard"


# 2. Description
# TODO: 用 st.write(...) 加一段介紹文字


# 3. Load data
# TODO: df = pd.read_csv("data/cognitive_aging_taiwan.csv")


# 4. Metrics
# TODO: st.metric("Participants", ...)
# TODO: st.metric("Mean age", ...)


# 5. Show first 10 rows
# TODO: st.dataframe(df.head(10))
