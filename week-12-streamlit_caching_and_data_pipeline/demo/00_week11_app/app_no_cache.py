"""Cognitive Aging Dashboard — **無 cache 版**（對照組）.

對應 Week 12 slides 11–13（rerun model + @st.cache_data）。

執行方式：
    streamlit run app_no_cache.py

與 app_with_cache.py 並排比較：
    - 拖任何 sidebar widget → load_data() 都會被完整呼叫
    - 加了一個刻意的 0.8 s sleep（模擬實際 data loading / 網路 I/O）
    - 頁面上方會顯示「本次 rerun 的 load_data() 耗時」與「總 rerun 時間」
    - rerun history 累積在 session_state 中，學生可以拖 slider 10 次後
      看到所有 reruns 都付了同樣的代價
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
    page_title="Cognitive Aging Dashboard (NO cache) | ACL@NCU",
    page_icon="🐢",
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

# 模擬「真實資料載入」的延遲（網路 I/O / 大型 parquet / fMRI volume）
SIMULATED_IO_SECONDS = 0.8


# ============================================================
# 區塊 3 — Data loading（注意：這裡 **沒有** @st.cache_data！）
# ============================================================
# 對照組：每次 rerun 都重新讀檔 + 等 0.8 s。
# Week 12 slides 11–13 強調的「rerun-on-interaction → expensive call
# 反覆執行」就是這個現象。
def load_data(path: Path) -> pd.DataFrame:
    """每次 rerun 都會被完整執行 — 因為沒有 @st.cache_data。"""
    df = pd.read_csv(path)
    time.sleep(SIMULATED_IO_SECONDS)        # 模擬慢 I/O
    df["group"] = pd.Categorical(
        df["group"], categories=["young", "middle", "older"], ordered=True
    )
    return df


# ============================================================
# 計時開始 — 紀錄整個 rerun 的開始時間
# ============================================================
t_rerun_start = time.perf_counter()

# 量測 load_data 的耗時
t0 = time.perf_counter()
df_all = load_data(DATA_PATH)
t_load_ms = (time.perf_counter() - t0) * 1000


# ============================================================
# Session state — 累積每次 rerun 的計時，讓學生看見差異
# ============================================================
if "rerun_count" not in st.session_state:
    st.session_state["rerun_count"] = 0
    st.session_state["history"] = []     # list of (rerun#, load_ms, total_ms)
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
    if st.button("Reset timing history"):
        st.session_state["rerun_count"] = 0
        st.session_state["history"] = []
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
st.title("🐢 Cognitive Aging Dashboard — NO cache")
st.markdown(
    "**對照組**：load_data() 沒有 @st.cache_data 裝飾器。拖任何 widget，"
    "整支 app.py 重新執行，CSV 被重新讀取一次。"
)

# ---- Timing banner ----
# 這裡先計算「截至目前」的總 rerun 時間（還沒結束，但已經是主要的時間花費）
t_total_ms_so_far = (time.perf_counter() - t_rerun_start) * 1000
c1, c2, c3 = st.columns(3)
c1.metric("⏱ load_data() 耗時", f"{t_load_ms:.0f}  ms",
          help="本次 rerun 中真的執行了多久？沒有 cache → 永遠 ≈ 800 ms")
c2.metric("📊 Rerun 累計次數", f"{st.session_state['rerun_count']}",
          help="拖 widget / 切 tab 都會累加")
c3.metric("⏳ 本次 rerun 開銷",
          f"~{t_total_ms_so_far:.0f}  ms",
          help="從 script 開始執行到 KPI 卡片顯示為止")

st.markdown("---")


if df.empty:
    st.warning("No participants match the current filters.")
    st.stop()


# KPI metrics（與 app.py 相同）
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
# Tab 5 — Rerun timing history（這支 app 最重要的對照）
# ============================================================
# 計算 rerun 全部完成的時間 — 用 placeholder 之後寫入，避免影響量測。
t_total_ms = (time.perf_counter() - t_rerun_start) * 1000
st.session_state["history"].append(
    (st.session_state["rerun_count"], t_load_ms, t_total_ms)
)
# 只保留最近 30 次
st.session_state["history"] = st.session_state["history"][-30:]

with tab_timing:
    st.subheader("每次 rerun 的耗時 — 沒有 cache 的代價")
    hist = pd.DataFrame(
        st.session_state["history"],
        columns=["rerun #", "load_data (ms)", "total rerun (ms)"],
    )
    st.dataframe(hist, use_container_width=True)

    if len(hist) >= 2:
        avg = hist["load_data (ms)"].mean()
        st.metric("平均 load_data 耗時", f"{avg:.0f}  ms",
                  help="每一次 rerun 都付這個代價 — 因為 load_data() 沒有 cache。")

    st.markdown(
        f"**對照 app_with_cache.py**：第一次 rerun 也是約 "
        f"{SIMULATED_IO_SECONDS*1000:.0f} ms，但之後 cache hit → 接近 0 ms。"
    )
    st.bar_chart(hist.set_index("rerun #")[["load_data (ms)"]])
