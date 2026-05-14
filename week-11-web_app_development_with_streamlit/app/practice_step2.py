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
# 1. Selectbox — 選一個認知測驗
measure = st.selectbox("Cognitive measure",
    options=["reaction_time_ms", "moca_score", "working_memory_span"])
 
# 2. Range slider — 年齡範圍
age_min, age_max = st.slider("Age range", 20, 80, (20, 80))
 


# TODO: sex_choices = st.multiselect(...)
# 3. Multiselect — 性別
sex_choices = st.multiselect("Sex", options=["F", "M"], default=["F", "M"])
 
# 4. 用 boolean mask 篩選
mask = df_all["age"].between(age_min, age_max) & df_all["sex"].isin(sex_choices)



# --- Apply filters ---
# TODO: df = df_all[mask]
df_filtered = df_all[mask]

# --- Display ---
# TODO: st.metric("Participants", ...)
st.metric("Participants", df_filtered.shape[0])
# TODO: st.metric("Mean RT", ...)
if measure == "reaction_time_ms":
     st.metric("Mean RT", round(df_filtered["reaction_time_ms"].mean(), 1))
elif measure == "moca_score":
    st.metric("Mean MoCA", round(df_filtered["moca_score"].mean(), 1))
else:
    st.metric("Mean WM span", round(df_filtered["working_memory_span"].mean(), 1))  
# TODO: st.metric("Mean MoCA", ...)
#st.metric("Mean MoCA", round(df_filtered["moca_score"].mean(), 1))


# TODO: st.dataframe(df.head(20))
st.dataframe(df_filtered.head(20))
