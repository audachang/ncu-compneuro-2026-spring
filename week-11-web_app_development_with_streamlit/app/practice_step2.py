"""Hands-on Practice 2 — 加入篩選器 widgets.

Run with:
    streamlit run practice_step2.py

Goal: 在 step 1 的基礎上加入互動式 widgets，讓使用者可以即時篩選資料。

Tasks:
1. 加入 age slider (range)：年齡範圍 20–80，預設 (20, 80)
2. 加入 sex multiselect：選 F 與 M，預設兩者都選
3. 用 boolean mask 篩選 DataFrame
4. 篩選後重新計算並顯示 metric (n, mean RT, mean MoCA)
5. 顯示篩選後的 dataframe (前 20 列)

提示：
- st.slider("...", min_value=20, max_value=80, value=(20, 80)) 會回傳 tuple
- st.multiselect("...", options=[...], default=[...]) 會回傳 list
- df["age"].between(lo, hi) 與 df["sex"].isin([...]) 可用 & 串接
"""

import streamlit as st
import pandas as pd

st.title("🧠 Cognitive Aging Dashboard")

df_all = pd.read_csv("data/cognitive_aging_taiwan.csv")

# --- Filters ---
# TODO: age_min, age_max = st.slider(...)


# TODO: sex_choices = st.multiselect(...)


# --- Apply filters ---
# TODO: df = df_all[mask]


# --- Display ---
# TODO: st.metric("Participants", ...)
# TODO: st.metric("Mean RT", ...)
# TODO: st.metric("Mean MoCA", ...)


# TODO: st.dataframe(df.head(20))
