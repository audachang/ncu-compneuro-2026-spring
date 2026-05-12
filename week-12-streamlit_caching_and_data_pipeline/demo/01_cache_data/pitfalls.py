"""Demo 1b: @st.cache_data 的三種常見錯誤 — bad / good 並列示範。

對應 Week 12 slides 17–18 (Pitfall 1, 2 & 3)。

執行：
    streamlit run pitfalls.py

每個錯誤都用「先 ❌ 錯誤版」+「再 ✅ 正確版」並排展示，
讓學生看出差異。
"""

import time
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cache Pitfalls", layout="wide")
st.title("@st.cache_data 三種常見錯誤")

rng = np.random.default_rng(42)
DF = pd.DataFrame({"rt_ms": rng.normal(500, 80, 1_000)})


# ===============================================================
# Pitfall 1 — Widget 寫在 cached function 內
# ===============================================================
st.header("Pitfall 1 — Widget 寫在 cached function 內")

col1, col2 = st.columns(2)

with col1:
    st.subheader("❌ 錯誤：widget 在函式內")

    @st.cache_data
    def bad_load(_df):
        # slider 改動後 cache key 不變 → 永遠回傳同一個 sample
        n = st.slider("rows (bad)", 10, 500, 50, key="bad_n")
        return _df.sample(n, random_state=0)

    bad_sample = bad_load(DF)
    st.write(f"取樣 {len(bad_sample)} rows — slider 改動不會更新！")

with col2:
    st.subheader("✅ 正確：widget 在外面")

    @st.cache_data
    def good_load(_df, n):
        return _df.sample(n, random_state=0)

    n = st.slider("rows (good)", 10, 500, 50, key="good_n")
    good_sample = good_load(DF, n)
    st.write(f"取樣 {len(good_sample)} rows — 跟隨 slider 變化")


st.divider()

# ===============================================================
# Pitfall 2 — UnhashableParamError 與 _ underscore 救星
# ===============================================================
st.header("Pitfall 2 — UnhashableParamError")

col1, col2 = st.columns(2)

with col1:
    st.subheader("❌ 錯誤：dict 直接傳入")
    try:
        @st.cache_data
        def bad_filter(df, params):
            return df[df["rt_ms"] > params["min_rt"]]
        result = bad_filter(DF, {"min_rt": 400})
        st.write(result.head())
    except Exception as e:
        st.error(f"{type(e).__name__}: {e}")

with col2:
    st.subheader("✅ 正確：加底線跳過 hash")

    @st.cache_data
    def good_filter(df, _params):
        return df[df["rt_ms"] > _params["min_rt"]]
    result = good_filter(DF, {"min_rt": 400})
    st.write(result.head())
    st.caption("`_params` 不參與 cache key — 你必須自己保證它不影響輸出。")


st.divider()

# ===============================================================
# Pitfall 3 — Side effects 被略過
# ===============================================================
st.header("Pitfall 3 — Side effect 被略過")

@st.cache_data
def fetch_with_log(seed: int):
    print(f"DEBUG: fetch called with seed={seed} at {time.strftime('%H:%M:%S')}")
    return np.random.default_rng(seed).standard_normal(5).tolist()

seed = st.number_input("seed", 0, 100, 0)
if st.button("Call fetch_with_log()"):
    _ = fetch_with_log(seed)
    st.success(
        "點兩次同一個 seed → terminal 只會印一次。"
        " 改 seed → 才會看到第二次。"
    )
st.caption(
    "不要把 logging / 寫檔等 side effect 放在 cached function 內 — "
    "cache hit 時整個函式會被跳過。"
)
