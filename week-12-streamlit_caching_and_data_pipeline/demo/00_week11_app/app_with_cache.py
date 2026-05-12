"""Cognitive Aging Dashboard — **有 cache 版**（實驗組）.

對應 Week 12 slides 11–13（rerun model + @st.cache_data）。

執行方式：
    streamlit run app_with_cache.py

與 app_no_cache.py 並排比較：
    - 第一次 rerun → load_data() 真的執行（≈ 800 ms）
    - 之後拖任何 widget → cache hit → load_data() 直接被跳過（≈ 0 ms）
    - 頁面上方顯示同樣的計時指標，差異一目了然
    - rerun history 累積在 session_state 中

關鍵：唯一的差別只是 @st.cache_data 這一行裝飾器！
"""

from pathlib import Path
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ============================================================
# 區塊 1 — Page configuration
# ============================================================
st.set_page_config(
    page_title="Cognitive Aging Dashboard (cached) | ACL@NCU",
    page_icon="⚡",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "data" / "cognitive_aging_taiwan.csv"
MEASURES = {
    "reaction_time_ms":       "Reaction Time (ms)",
    "working_memory_span":    "Working Memory Span",
    "processing_speed":       "Processing Speed",
    "moca_score":             "MoCA Score",
    "stroop_interference_ms": "Stroop Interference (ms)",
}

SIMULATED_IO_SECONDS = 0.8


# ============================================================
# 區塊 3 — Data loading（**有 @st.cache_data**）⭐
# ============================================================
# 唯一與 app_no_cache.py 的差別 ↓
# 第一次呼叫 → 真的執行；之後同樣 path 呼叫 → 跳過、回傳上次的 DataFrame deep copy。
@st.cache_data(show_spinner="第一次載入資料（之後就會被 cache）...")
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    time.sleep(SIMULATED_IO_SECONDS)        # 同樣的「慢」I/O — 但只會付一次
    df["group"] = pd.Categorical(
        df["group"], categories=["young", "middle", "older"], ordered=True
    )
    return df


# ============================================================
# 計時開始
# ============================================================
t_rerun_start = time.perf_counter()

t0 = time.perf_counter()
df_all = load_data(DATA_PATH)
t_load_ms = (time.perf_counter() - t0) * 1000


# ============================================================
# Session state — 累積每次 rerun 的計時
# ============================================================
if "rerun_count" not in st.session_state:
    st.session_state["rerun_count"] = 0
    st.session_state["history"] = []
st.session_state["rerun_count"] += 1


# ============================================================
# 區塊 4 — Sidebar
# ============================================================
with st.sidebar:
    st.header("🔬 Filters")
    age_min, age_max = st.slider(
        "Age range (years)",
        min_value=int(df_all["age"].min()),
        max_value=int(df_all["age"].max()),
        value=(20, 80), step=1,
    )
    sex_choices = st.multiselect("Sex", options=["F", "M"], default=["F", "M"])
    edu_min, edu_max = st.slider(
        "Years of education",
        min_value=int(df_all["education"].min()),
        max_value=int(df_all["education"].max()),
        value=(9, 22),
    )
    measure = st.selectbox(
        "Cognitive measure to visualize",
        options=list(MEASURES.keys()),
        format_func=lambda k: MEASURES[k],
        index=0,
    )
    show_regression = st.checkbox("Show age regression line", value=True)
    st.markdown("---")
    st.caption(f"Reruns this session: **{st.session_state['rerun_count']}**")
    cols = st.columns(2)
    if cols[0].button("Reset timing history"):
        st.session_state["rerun_count"] = 0
        st.session_state["history"] = []
        st.rerun()
    if cols[1].button("Clear cache"):
        # 把 cache 清空 → 下一次 rerun 會「第一次」付那 800 ms
        st.cache_data.clear()
        st.toast("✓ Cache cleared — 下一次 rerun 會重讀 CSV", icon="🧹")
        st.rerun()


# ============================================================
# 區塊 5 — Filter
# ============================================================
mask = (
    df_all["age"].between(age_min, age_max)
    & df_all["sex"].isin(sex_choices)
    & df_all["education"].between(edu_min, edu_max)
)
df = df_all[mask].copy()


# ============================================================
# 區塊 6 — Header + KPI + ⏱ Timing banner
# ============================================================
st.title("⚡ Cognitive Aging Dashboard — with cache")
st.markdown(
    "**實驗組**：load_data() 有 @st.cache_data 裝飾。第一次拖 widget 會付那 "
    "≈ 800 ms 的代價，但之後同樣 input → cache hit → 幾乎瞬間。"
)

t_total_ms_so_far = (time.perf_counter() - t_rerun_start) * 1000
c1, c2, c3 = st.columns(3)
# 用 cache_hit 旗標（< 50 ms 視為 hit）讓 metric delta 直接表達差異
cache_hit = t_load_ms < 50
c1.metric(
    "⏱ load_data() 耗時",
    f"{t_load_ms:.0f}  ms",
    delta="cache hit ⚡" if cache_hit else "cache miss",
    delta_color="normal" if cache_hit else "inverse",
    help="第一次 ≈ 800 ms；之後同樣 input → < 5 ms",
)
c2.metric("📊 Rerun 累計次數", f"{st.session_state['rerun_count']}",
          help="拖 widget / 切 tab 都會累加")
c3.metric("⏳ 本次 rerun 開銷",
          f"~{t_total_ms_so_far:.0f}  ms",
          help="從 script 開始執行到 KPI 卡片顯示為止")

st.markdown("---")


if df.empty:
    st.warning("No participants match the current filters.")
    st.stop()


m1, m2, m3, m4 = st.columns(4)
m1.metric("Participants", f"{len(df)}",
          delta=f"{len(df) - len(df_all):+d} vs all")
m2.metric("Mean age", f"{df['age'].mean():.1f} y")
m3.metric("Mean RT", f"{df['reaction_time_ms'].mean():.0f} ms",
          delta=f"{df['reaction_time_ms'].mean() - df_all['reaction_time_ms'].mean():+.0f}",
          delta_color="inverse")
m4.metric("Mean MoCA", f"{df['moca_score'].mean():.1f}",
          delta=f"{df['moca_score'].mean() - df_all['moca_score'].mean():+.2f}")

st.markdown("---")


# ============================================================
# 區塊 7 — Tabs
# ============================================================
tab_scatter, tab_dist, tab_group, tab_raw, tab_timing = st.tabs(
    ["📈 Age trajectory", "📊 Distributions", "👥 By age group",
     "🗃️ Raw data", "⏱ Rerun timing history"]
)

with tab_scatter:
    left, right = st.columns([2, 1])
    with left:
        st.subheader(f"Age × {MEASURES[measure]}")
        fig, ax = plt.subplots(figsize=(8, 4.5))
        colors = {"F": "#E8788C", "M": "#1F6FB4"}
        for sex_label in sex_choices:
            sub = df[df["sex"] == sex_label]
            ax.scatter(sub["age"], sub[measure], s=22, alpha=0.6,
                       c=colors[sex_label], label=sex_label,
                       edgecolors="white", linewidths=0.5)
        if show_regression and len(df) >= 3:
            slope, intercept = np.polyfit(df["age"], df[measure], 1)
            xs = np.array([df["age"].min(), df["age"].max()])
            ax.plot(xs, slope * xs + intercept, color="#212121", lw=2,
                    ls="--", label=f"slope={slope:.2f}/yr")
        ax.set_xlabel("Age (years)")
        ax.set_ylabel(MEASURES[measure])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(frameon=False, loc="best")
        plt.tight_layout()
        st.pyplot(fig)
    with right:
        st.subheader("Pearson correlation with age")
        corr_table = (
            df[list(MEASURES.keys()) + ["age"]]
            .corr(numeric_only=True)["age"].drop("age").rename("r").to_frame()
            .assign(direction=lambda x: np.where(x["r"] >= 0, "↑", "↓"))
        )
        corr_table["r"] = corr_table["r"].round(3)
        corr_table.index = [MEASURES[k] for k in corr_table.index]
        st.dataframe(corr_table, use_container_width=True)

with tab_dist:
    st.subheader(f"Distribution of {MEASURES[measure]}")
    fig, ax = plt.subplots(figsize=(9, 3.8))
    for g, color in zip(["young", "middle", "older"],
                        ["#4CAF50", "#FF9800", "#9C27B0"]):
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

with tab_group:
    st.subheader("Group means across measures")
    summary = (df.groupby("group", observed=True)[list(MEASURES.keys())]
                 .agg(["mean", "std", "count"]).round(2))
    st.dataframe(summary, use_container_width=True)

with tab_raw:
    st.subheader("Filtered participant data")
    st.dataframe(df, use_container_width=True, height=420)


# ============================================================
# Tab 5 — Rerun timing history（最重要的對照畫面）
# ============================================================
t_total_ms = (time.perf_counter() - t_rerun_start) * 1000
st.session_state["history"].append(
    (st.session_state["rerun_count"], t_load_ms, t_total_ms)
)
st.session_state["history"] = st.session_state["history"][-30:]

with tab_timing:
    st.subheader("每次 rerun 的耗時 — cache hit 的威力")
    hist = pd.DataFrame(
        st.session_state["history"],
        columns=["rerun #", "load_data (ms)", "total rerun (ms)"],
    )
    st.dataframe(hist, use_container_width=True)

    if len(hist) >= 2:
        first = hist["load_data (ms)"].iloc[0]
        cache_hits = hist[hist["load_data (ms)"] < 50]
        if len(cache_hits):
            avg_hit = cache_hits["load_data (ms)"].mean()
            saved = (first - avg_hit) * (len(hist) - 1)
            st.metric(
                "已省下的總時間",
                f"≈ {saved/1000:.1f}  s",
                help=f"第一次 {first:.0f} ms vs 之後 cache hit 平均 {avg_hit:.1f} ms × "
                     f"{len(hist) - 1} 次 reruns",
            )

    st.markdown(
        "**對照 app_no_cache.py**：每一次 rerun 都付 ≈ 800 ms。"
        " 試試按側邊欄的「Clear cache」→ 下一次 rerun 就會回到「第一次」狀態。"
    )
    st.bar_chart(hist.set_index("rerun #")[["load_data (ms)"]])
