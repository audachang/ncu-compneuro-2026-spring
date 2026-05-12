"""Cognitive Aging Dashboard — Week 11 整合範例（Week 12 繁體中文註解版）.

這支檔案是 Week 11 最後交付的整合 dashboard。Week 12 的前半段（slides 7–21）
逐段拆解這支程式，本檔案在 Week 11 原版的基礎上 **加入大量繁體中文註解**，
讓學生在閱讀程式碼時能對應到投影片的講解。

執行方式：
    pip install -r requirements.txt
    streamlit run app.py

資料：n=400 的合成 lifespan cognitive battery（reaction_time、working_memory_span、
processing_speed、moca、stroop_interference）。

# ============================================================
# Streamlit app 的七大區塊（對應 slide 8）
#   1. Page config       — st.set_page_config()      ← 必須最先呼叫
#   2. Constants         — DATA_PATH、MEASURES
#   3. Data loading      — @st.cache_data + load_data()   ← Week 12 重點
#   4. Sidebar widgets   — st.slider、multiselect、selectbox、checkbox
#   5. Filtering         — boolean mask on DataFrame
#   6. Header + KPI      — st.title、st.metric × 4
#   7. Tabs              — st.tabs(...) × 4
# ============================================================
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------
# 區塊 1 — Page configuration
# ---------------------------------------------------------------
# st.set_page_config() **必須是第一個** Streamlit 呼叫；否則會 raise
# StreamlitAPIException。如果在它之前寫過任何 st.title / st.write，就會壞掉。
st.set_page_config(
    page_title="Cognitive Aging Dashboard | ACL@NCU",
    page_icon="🧠",
    layout="wide",
)

# ---------------------------------------------------------------
# 區塊 2 — Constants
# ---------------------------------------------------------------
# DATA_PATH：相對於本檔案的位置；用 Path(__file__).parent 而不是 cwd，
# 避免「我用哪個資料夾啟動 streamlit」造成 FileNotFoundError。
DATA_PATH = Path(__file__).parent / "data" / "cognitive_aging_taiwan.csv"

# 把可視化用的「程式內部 key」與「給使用者看的標籤」分開維護。
# 這個 dict 之後會餵給 st.selectbox 的 options + format_func，
# 達到「內部用英文 key，UI 顯示英文友善標籤」的分離（見 §1.1b）。
MEASURES = {
    "reaction_time_ms":       "Reaction Time (ms)",
    "working_memory_span":    "Working Memory Span",
    "processing_speed":       "Processing Speed",
    "moca_score":             "MoCA Score",
    "stroop_interference_ms": "Stroop Interference (ms)",
}


# ---------------------------------------------------------------
# 區塊 3 — Cached data loading（Week 12 重點！對應 slides 13–18）
# ---------------------------------------------------------------
# @st.cache_data 是這支 dashboard 的「肌肉」：
#   - 第一次呼叫 load_data(DATA_PATH) → 真的讀 CSV、做 Categorical 處理
#   - 第二次以後 → 跳過函式內容，直接回傳上次的 DataFrame（deep copy）
#
# 為什麼需要 cache？
#   Streamlit 的執行模型：每次使用者拖 slider、切 tab、按按鈕 ⋯⋯
#   整支 app.py 都會從頭到尾重跑一次。
#   如果 load_data() 沒有 cache，每次互動都會重讀 CSV → 慢 + 浪費 I/O。
#
# Cache key 由三件事組成：函式名、參數的 hash、函式原始碼的 hash。
# 修改函式內容 → 舊 cache 自動失效（不用手動清）。
#
# 回傳的是 **deep copy** 不是 reference：你怎麼亂改 df 都不會污染 cache。
@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """讀取 cognitive aging CSV — cache 起來避免每次 rerun 都重讀。"""
    df = pd.read_csv(path)
    # 把 'group' 設為 ordered categorical，後續 groupby 與 plot 的順序才會
    # 是 young → middle → older 而不是字母排序的 middle → older → young。
    df["group"] = pd.Categorical(
        df["group"], categories=["young", "middle", "older"], ordered=True
    )
    return df


# ---------------------------------------------------------------
# 區塊 4 — Sidebar（widget 輸入區，對應 slide 9 — 1.1b Sidebar 的角色）
# ---------------------------------------------------------------
# 重要：load_data() 必須在 sidebar 之前呼叫，
# 因為 sidebar 的 slider 範圍要用 df_all 的 min/max 來決定。
df_all = load_data(DATA_PATH)

# `with st.sidebar:` 區塊 → 所有放在這個 with 內的 widgets 都會被
# Streamlit 自動放到左側 sidebar；右邊主畫面留給結果。
# 紀律 #1：widgets 寫在 sidebar，篩選 logic 寫在主程式（不要混在一起）。
with st.sidebar:
    st.header("🔬 Filters")

    # st.slider 的 value=(a, b) → 回傳一個 tuple，自動變成 range slider。
    # 紀律 #2：value=(20, 80) 寫死合理的初始值，避免使用者開啟 app 看到空白。
    age_min, age_max = st.slider(
        "Age range (years)",
        min_value=int(df_all["age"].min()),
        max_value=int(df_all["age"].max()),
        value=(20, 80),
        step=1,
    )

    # st.multiselect 回傳一個 list；default 同樣要設合理初值（避免 empty mask）。
    sex_choices = st.multiselect(
        "Sex",
        options=["F", "M"],
        default=["F", "M"],
    )

    # 第二個 range slider — 教育年數
    edu_min, edu_max = st.slider(
        "Years of education",
        min_value=int(df_all["education"].min()),
        max_value=int(df_all["education"].max()),
        value=(9, 22),
    )

    # st.selectbox + format_func：分離「內部 key」（英文，給程式用）與
    # 「顯示標籤」（英文友善文字，給人看）。這就是紀律 #3。
    measure = st.selectbox(
        "Cognitive measure to visualize",
        options=list(MEASURES.keys()),
        format_func=lambda k: MEASURES[k],   # k 是 "reaction_time_ms"；顯示成 "Reaction Time (ms)"
        index=0,
    )

    # st.checkbox 回傳 bool；用來開關「是否畫迴歸線」的可選功能。
    show_regression = st.checkbox("Show age regression line", value=True)

    st.markdown("---")
    st.caption("Data: synthetic, n=400 (Week 11 demo)")
    st.caption("ACL@NCU · NS5116 · Spring 2026")


# ---------------------------------------------------------------
# 區塊 5 — Filtering：把 sidebar 的 widget 值組成 boolean mask
# ---------------------------------------------------------------
# 這就是 slide 9 強調的「widget → mask」pattern：
# 每個 widget 的回傳值直接用 pandas 的 vectorized comparison 組成 mask。
# 注意：element-wise 邏輯運算用 &、|、~（不是 and/or/not），
# 否則會 raise "truth value of an array is ambiguous"。
mask = (
    df_all["age"].between(age_min, age_max)
    & df_all["sex"].isin(sex_choices)
    & df_all["education"].between(edu_min, edu_max)
)
df = df_all[mask].copy()      # .copy() 避免 SettingWithCopyWarning


# ---------------------------------------------------------------
# 區塊 6 — Header + KPI metrics
# ---------------------------------------------------------------
st.title("🧠 Cognitive Aging Dashboard")
st.markdown(
    "Interactive visualization of a lifespan cognitive battery "
    "(synthetic data). Use the sidebar to filter by age, sex, and education."
)

# 早期 return：mask 把所有 row 都過濾掉的情境（empty DataFrame）。
# st.warning + st.stop() 讓 app 顯示提示後安全結束 rerun，不會 raise。
if df.empty:
    st.warning("No participants match the current filters.")
    st.stop()

# st.columns(4) → 把畫面切成 4 等寬欄；每欄塞一個 st.metric。
# st.metric(label, value, delta=...) 是 dashboard 風格的「KPI 卡片」。
# delta_color="inverse" 讓「數值變小」顯示為綠色 — 對 RT 這種「越快越好」
# 的指標特別實用。
m1, m2, m3, m4 = st.columns(4)
m1.metric("Participants", f"{len(df)}", delta=f"{len(df) - len(df_all):+d} vs all")
m2.metric("Mean age",     f"{df['age'].mean():.1f} y")
m3.metric(
    "Mean RT",
    f"{df['reaction_time_ms'].mean():.0f} ms",
    delta=f"{df['reaction_time_ms'].mean() - df_all['reaction_time_ms'].mean():+.0f}",
    delta_color="inverse",
)
m4.metric(
    "Mean MoCA",
    f"{df['moca_score'].mean():.1f}",
    delta=f"{df['moca_score'].mean() - df_all['moca_score'].mean():+.2f}",
)

st.markdown("---")


# ---------------------------------------------------------------
# 區塊 7 — Tabs：四個分析視角
# ---------------------------------------------------------------
# st.tabs(["A", "B", "C"]) 回傳對應數量的 tab 物件。
# `with tab_X:` 區塊內的所有 st.* 呼叫都會被放到該 tab 內。
tab_scatter, tab_dist, tab_group, tab_raw = st.tabs(
    ["📈 Age trajectory", "📊 Distributions", "👥 By age group", "🗃️ Raw data"]
)

# ----- Tab 1：散佈圖 + 可選迴歸線 -----
with tab_scatter:
    # 二欄版面：左大圖、右側放相關係數表
    left, right = st.columns([2, 1])

    with left:
        st.subheader(f"Age × {MEASURES[measure]}")
        # 使用 matplotlib — 注意：fig 必須傳給 st.pyplot(fig)，不能只 plt.show()
        fig, ax = plt.subplots(figsize=(8, 4.5))
        colors = {"F": "#E8788C", "M": "#1F6FB4"}
        # 分性別畫散佈圖
        for sex_label in sex_choices:
            sub = df[df["sex"] == sex_label]
            ax.scatter(
                sub["age"], sub[measure],
                s=22, alpha=0.6, c=colors[sex_label], label=sex_label,
                edgecolors="white", linewidths=0.5,
            )
        # show_regression 由 sidebar checkbox 控制 — widget → 視覺化的直接連結
        if show_regression and len(df) >= 3:
            slope, intercept = np.polyfit(df["age"], df[measure], 1)
            xs = np.array([df["age"].min(), df["age"].max()])
            ax.plot(xs, slope * xs + intercept, color="#212121", lw=2, ls="--",
                    label=f"slope={slope:.2f}/yr")
        ax.set_xlabel("Age (years)")
        ax.set_ylabel(MEASURES[measure])
        # 去掉上、右兩條軸線 — 一個小但有效的視覺潔淨化習慣
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(frameon=False, loc="best")
        plt.tight_layout()
        st.pyplot(fig)

    with right:
        st.subheader("Pearson correlation with age")
        # .corr()["age"] 取出每個 measure 與 age 的 r；
        # .assign(direction=lambda ...) 加一欄箭頭方便閱讀。
        corr_table = (
            df[list(MEASURES.keys()) + ["age"]]
            .corr(numeric_only=True)["age"]
            .drop("age")
            .rename("r")
            .to_frame()
            .assign(direction=lambda x: np.where(x["r"] >= 0, "↑", "↓"))
        )
        corr_table["r"] = corr_table["r"].round(3)
        corr_table.index = [MEASURES[k] for k in corr_table.index]
        st.dataframe(corr_table, use_container_width=True)

# ----- Tab 2：分組 histogram -----
with tab_dist:
    st.subheader(f"Distribution of {MEASURES[measure]}")
    fig, ax = plt.subplots(figsize=(9, 3.8))
    for g, color in zip(["young", "middle", "older"], ["#4CAF50", "#FF9800", "#9C27B0"]):
        sub = df[df["group"] == g][measure]
        if len(sub) > 0:
            ax.hist(sub, bins=18, alpha=0.55, label=f"{g} (n={len(sub)})",
                    color=color, edgecolor="white")
    ax.set_xlabel(MEASURES[measure])
    ax.set_ylabel("Count")
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

# ----- Tab 3：分組 means 表 + bar chart -----
with tab_group:
    st.subheader("Group means across measures")
    # observed=True：避免 categorical 的「空 group」被顯示成 NaN row
    summary = (
        df.groupby("group", observed=True)[list(MEASURES.keys())]
        .agg(["mean", "std", "count"])
        .round(2)
    )
    st.dataframe(summary, use_container_width=True)

    st.subheader(f"Bar chart — mean {MEASURES[measure]} by group")
    # Streamlit 內建 st.bar_chart() — 接受 Series 或 DataFrame；
    # 比 matplotlib 快一行，但客製化能力弱（無法調色、無法加 error bar）。
    bar_data = df.groupby("group", observed=True)[measure].mean()
    st.bar_chart(bar_data)

# ----- Tab 4：原始資料表 + 下載按鈕 -----
with tab_raw:
    st.subheader("Filtered participant data")
    st.dataframe(df, use_container_width=True, height=420)
    # st.download_button 讓使用者把目前篩選後的 DataFrame 下載成 CSV。
    # .to_csv(index=False).encode("utf-8") → bytes，正是 button 需要的格式。
    st.download_button(
        label="⬇️ Download filtered CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="cognitive_aging_filtered.csv",
        mime="text/csv",
    )
    # st.expander：可摺疊的補充說明區塊 — 預設收合，點開才顯示。
    with st.expander("📖 About this dataset"):
        st.markdown(
            """
            **Source:** Synthetic data generated for NS5116 (Spring 2026, ACL@NCU)
            following age-related patterns reported in the cognitive aging
            literature.

            **n = 400** participants, ages 20–80, drawn from a simulated
            Taiwan-based study.

            **Measures:**
            - `reaction_time_ms` — simple RT, lower is faster
            - `working_memory_span` — n-back / digit span (2–9)
            - `processing_speed` — digit-symbol substitution (items / 90 s)
            - `moca_score` — Montreal Cognitive Assessment (0–30)
            - `stroop_interference_ms` — incongruent − congruent RT
            """
        )
