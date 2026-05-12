"""Demo 1: 觀察 @st.cache_data 的行為差異。

對應 Week 12 slides 13–19 (Caching 深入解析 + Hands-on 2)。

執行：
    streamlit run cache_demo.py

操作步驟：
    1. 預設啟動：DECORATED=True → terminal 只印一次 "DEBUG: reading CSV"，
       拖 sidebar slider 不會再印。
    2. 把 DECORATED 改成 False → 每次拖 slider 都會印。
    3. 把 DECORATED 改回 True，並把 ttl=None 改成 ttl=10 → 10 秒後再拖
       slider 會觸發一次重讀。
"""

from pathlib import Path
import time
import numpy as np
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------
# 切換點：改這兩個常數來觀察 cache 行為
# ---------------------------------------------------------------
DECORATED = True      # False = 完全不 cache
#DECORATED = False      # False = 完全不 cache
#TTL       = None      # None = 永久；改 10 = 10 秒 TTL
TTL       = 5      # None = 永久；改 10 = 10 秒 TTL

# ---------------------------------------------------------------
# 製造一筆「重」的合成資料（夠慢以看出差異）
# ---------------------------------------------------------------
DATA = Path(__file__).parent / "synthetic_rt.csv"
if not DATA.exists():
    rng = np.random.default_rng(42)
    pd.DataFrame({
        "subject":   rng.integers(1, 50, 200_000),
        "condition": rng.choice(["congruent", "incongruent"], 200_000),
        "rt_ms":     rng.normal(500, 80, 200_000),
    }).to_csv(DATA, index=False)


def _maybe_cached(ttl):
    """根據 DECORATED 與 TTL 選擇是否套裝飾器。"""
    if not DECORATED:
        return lambda f: f
    return st.cache_data(ttl=ttl, show_spinner="Loading CSV...")


@_maybe_cached(TTL)
def load_data(path: Path) -> pd.DataFrame:
    """讀 CSV — 第二次（cache hit）時應該被跳過。"""
    print(f"DEBUG: reading CSV at {time.strftime('%H:%M:%S')}")
    time.sleep(0.5)        # 故意慢一點，方便觀察 spinner
    return pd.read_csv(path)


# ---------------------------------------------------------------
# UI
# ---------------------------------------------------------------
st.set_page_config(page_title="Cache Demo", layout="wide")
st.title("@st.cache_data 行為觀察")

st.caption(
    f"設定：DECORATED={DECORATED} · TTL={TTL!r}  ·  "
    "觀察 terminal 是否印出 'DEBUG: reading CSV'"
)

df = load_data(DATA)

with st.sidebar:
    st.header("Filters")
    n = st.slider("Show first N rows", 5, 200, 20)
    cond = st.multiselect("Condition",
                          ["congruent", "incongruent"],
                          default=["congruent", "incongruent"])

sub = df[df["condition"].isin(cond)].head(n)
st.dataframe(sub, use_container_width=True)

st.write(
    f"**總 row 數**：{len(df):,}  ·  **顯示**：{len(sub)} rows"
)
