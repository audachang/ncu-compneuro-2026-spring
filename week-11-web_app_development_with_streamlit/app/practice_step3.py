"""Hands-on Practice 3 — 完整 Cognitive Aging Dashboard.

Run with:
    streamlit run practice_step3.py

Goal: 整合 widgets、charts、layout、caching 為一個完整 dashboard。

Tasks:
1. 用 @st.cache_data 包住 load_data() 函式
2. 把所有 filters 移到 st.sidebar
3. 加一個 measure selectbox 讓使用者選擇要視覺化的認知測驗
4. 主畫面用 st.tabs(["Scatter", "Distribution", "Raw data"]) 分三頁
5. Scatter 頁：散佈圖 + 線性迴歸線
6. Distribution 頁：young / middle / older 三組 histogram (overlay)
7. Raw data 頁：篩選後 dataframe + st.download_button

對照解答：app.py（先嘗試自己寫，再對照）
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cognitive Aging Dashboard", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "cognitive_aging_taiwan.csv"

MEASURES = {
    "reaction_time_ms":       "Reaction Time (ms)",
    "working_memory_span":    "Working Memory Span",
    "processing_speed":       "Processing Speed",
    "moca_score":             "MoCA Score",
    "stroop_interference_ms": "Stroop Interference (ms)",
}


# ----------------------------------------------------
# TODO 1: cached data loader
# ----------------------------------------------------
# @st.cache_data
# def load_data(path):
#     ...
#     return df


# df_all = load_data(DATA_PATH)


# ----------------------------------------------------
# TODO 2: sidebar filters
# ----------------------------------------------------
# with st.sidebar:
#     st.header("Filters")
#     age_min, age_max = st.slider(...)
#     sex_choices      = st.multiselect(...)
#     measure          = st.selectbox(...)


# ----------------------------------------------------
# TODO: apply filters → df
# ----------------------------------------------------


# ----------------------------------------------------
# Main layout
# ----------------------------------------------------
st.title("🧠 Cognitive Aging Dashboard")

# TODO: top-row metrics (st.columns(4) → 4 個 metric)


# TODO 4: tabs
# tab_scatter, tab_dist, tab_raw = st.tabs(["...", "...", "..."])

# with tab_scatter:
#     # TODO 5: scatter + regression
#     ...

# with tab_dist:
#     # TODO 6: histogram by group
#     ...

# with tab_raw:
#     # TODO 7: raw dataframe + download_button
#     ...
