"""Demo 2: @st.cache_data vs @st.cache_resource 行為對照。

對應 Week 12 slides 20–21 (cache_data vs cache_resource + decision rule)。

執行：
    streamlit run compare.py

兩個函式各被「同一 session 內」呼叫多次：
    - cache_data → 每次回傳新的 deep copy（id 不同）
    - cache_resource → 每次回傳同一個 reference（id 相同）

注意：對於 dict、list、自訂 class instance（這裡用 SimpleCounter
模擬 DB connection），差異最容易看出來。
"""

import streamlit as st


class SimpleCounter:
    """模擬一個有狀態的「資源」— 例如 DB connection / ML model。"""

    def __init__(self, name):
        self.name = name
        self.calls = 0

    def hit(self):
        self.calls += 1
        return self.calls


# ---------------------------------------------------------------
# 兩種快取
# ---------------------------------------------------------------
@st.cache_data
def get_counter_data(name: str) -> SimpleCounter:
    """每次都回傳 deep copy — 每個 session 都拿到全新物件。"""
    return SimpleCounter(name)


@st.cache_resource
def get_counter_resource(name: str) -> SimpleCounter:
    """整個 app 共用同一個物件（singleton）。"""
    return SimpleCounter(name)


# ---------------------------------------------------------------
# UI
# ---------------------------------------------------------------
st.set_page_config(page_title="cache_data vs cache_resource", layout="wide")
st.title("@st.cache_data vs @st.cache_resource")

st.markdown(
    "兩種快取對「狀態」的處理方式完全不同。下面各放一顆按鈕，按下後該"
    "計數器 +1，**重點看 `calls` 數字會不會跨 rerun 累加**。"
)

col_data, col_resource = st.columns(2)

with col_data:
    st.subheader("@st.cache_data")
    c1 = get_counter_data("data-counter")
    if st.button("Hit data-counter"):
        c1.hit()
    st.metric("calls", c1.calls)
    st.write(f"id(c1) = `{id(c1)}`")
    st.caption(
        "因為回傳的是 deep copy，每次 rerun 你拿到的都是「新生兒」— "
        "計數永遠是 0 或 1。"
    )

with col_resource:
    st.subheader("@st.cache_resource")
    c2 = get_counter_resource("resource-counter")
    if st.button("Hit resource-counter"):
        c2.hit()
    st.metric("calls", c2.calls)
    st.write(f"id(c2) = `{id(c2)}`")
    st.caption(
        "回傳同一個 reference — 每次 rerun 拿到的是同一個物件，"
        "計數會累加。"
    )

st.divider()
st.markdown(
    "**Decision rule**\n\n"
    "> 要的是「資料」？ → 用 `@st.cache_data`\n"
    "> 要的是「資源 / 連線 / 物件」？ → 用 `@st.cache_resource`\n"
)
