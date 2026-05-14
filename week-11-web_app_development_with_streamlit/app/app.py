"""Cognitive Aging Dashboard — Week 11 Streamlit demo.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py

Dataset: synthetic n=400 lifespan cognitive battery
(reaction_time, working_memory_span, processing_speed, moca, stroop_interference).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------
# Page configuration — must be the first Streamlit command
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Cognitive Aging Dashboard | ACL@NCU",
    page_icon="🧠",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "data" / "cognitive_aging_taiwan.csv"

# Cognitive measures available for plotting / filtering
MEASURES = {
    "reaction_time_ms":       "Reaction Time (ms)",
    "working_memory_span":    "Working Memory Span",
    "processing_speed":       "Processing Speed",
    "moca_score":             "MoCA Score",
    "stroop_interference_ms": "Stroop Interference (ms)",
}


# ---------------------------------------------------------------
# Cached data loading
# ---------------------------------------------------------------
@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """Load the cognitive aging CSV. Cached to avoid re-reading on every rerun."""
    df = pd.read_csv(path)
    # Ensure 'group' has a meaningful order for plots
    df["group"] = pd.Categorical(
        df["group"], categories=["young", "middle", "older"], ordered=True
    )
    return df


# ---------------------------------------------------------------
# Sidebar — filters
# ---------------------------------------------------------------
df_all = load_data(DATA_PATH)

with st.sidebar:
    st.header("🔬 Filters")

    # Age slider
    age_min, age_max = st.slider(
        "Age range (years)",
        min_value=int(df_all["age"].min()),
        max_value=int(df_all["age"].max()),
        value=(20, 80),
        step=1,
    )

    # Sex multiselect
    sex_choices = st.multiselect(
        "Sex",
        options=["F", "M"],
        default=["F", "M"],
    )

    # Education slider
    edu_min, edu_max = st.slider(
        "Years of education",
        min_value=int(df_all["education"].min()),
        max_value=int(df_all["education"].max()),
        value=(9, 22),
    )

    # Cognitive measure for plots
    measure = st.selectbox(
        "Cognitive measure to visualize",
        options=list(MEASURES.keys()),
        format_func=lambda k: MEASURES[k],
        index=0,
    )

    show_regression = st.checkbox("Show age regression line", value=True)

    st.markdown("---")
    st.caption("Data: synthetic, n=400 (Week 11 demo)")
    st.caption("ACL@NCU · NS5116 · Spring 2026")


# Apply filters
mask = (
    df_all["age"].between(age_min, age_max)
    & df_all["sex"].isin(sex_choices)
    & df_all["education"].between(edu_min, edu_max)
)
df = df_all[mask].copy()


# ---------------------------------------------------------------
# Header
# ---------------------------------------------------------------
st.title("🧠 Cognitive Aging Dashboard")
st.markdown(
    "Interactive visualization of a lifespan cognitive battery "
    "(synthetic data). Use the sidebar to filter by age, sex, and education."
)

if df.empty:
    st.warning("No participants match the current filters.")
    st.stop()


# ---------------------------------------------------------------
# Top-row KPI metrics
# ---------------------------------------------------------------
m1, m2, m3, m4 = st.columns(4)
m1.metric("Participants", f"{len(df)}", delta=f"{len(df) - len(df_all):+d} vs all")
m2.metric("Mean age",     f"{df['age'].mean():.1f} y")
m3.metric(
    "Mean RT",
    f"{df['reaction_time_ms'].mean():.0f} ms",
    delta=f"{df['reaction_time_ms'].mean() - df_all['reaction_time_ms'].mean():+.0f}",
    delta_color="inverse",  # lower RT is better
)
m4.metric(
    "Mean MoCA",
    f"{df['moca_score'].mean():.1f}",
    delta=f"{df['moca_score'].mean() - df_all['moca_score'].mean():+.2f}",
)

st.markdown("---")


# ---------------------------------------------------------------
# Tabs: Overview / Distributions / By group / Raw data
# ---------------------------------------------------------------
tab_scatter, tab_dist, tab_group, tab_raw = st.tabs(
    ["📈 Age trajectory", "📊 Distributions", "👥 By age group", "🗃️ Raw data"]
)

# ----- Tab 1: scatter + regression -----
with tab_scatter:
    left, right = st.columns([2, 1])

    with left:
        st.subheader(f"Age × {MEASURES[measure]}")
        fig, ax = plt.subplots(figsize=(8, 4.5))
        colors = {"F": "#E8788C", "M": "#1F6FB4"}
        for sex_label in sex_choices:
            sub = df[df["sex"] == sex_label]
            ax.scatter(
                sub["age"], sub[measure],
                s=22, alpha=0.6, c=colors[sex_label], label=sex_label,
                edgecolors="white", linewidths=0.5,
            )
        if show_regression and len(df) >= 3:
            slope, intercept = np.polyfit(df["age"], df[measure], 1)
            xs = np.array([df["age"].min(), df["age"].max()])
            ax.plot(xs, slope * xs + intercept, color="#212121", lw=2, ls="--",
                    label=f"slope={slope:.2f}/yr")
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
            .corr(numeric_only=True)["age"]
            .drop("age")
            .rename("r")
            .to_frame()
            .assign(direction=lambda x: np.where(x["r"] >= 0, "↑", "↓"))
        )
        corr_table["r"] = corr_table["r"].round(3)
        corr_table.index = [MEASURES[k] for k in corr_table.index]
        st.dataframe(corr_table, use_container_width=True)

# ----- Tab 2: histograms -----
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

# ----- Tab 3: group means -----
with tab_group:
    st.subheader("Group means across measures")
    summary = (
        df.groupby("group", observed=True)[list(MEASURES.keys())]
        .agg(["mean", "std", "count"])
        .round(2)
    )
    st.dataframe(summary, use_container_width=True)

    st.subheader(f"Bar chart — mean {MEASURES[measure]} by group")
    bar_data = df.groupby("group", observed=True)[measure].mean()
    st.bar_chart(bar_data)

# ----- Tab 4: raw data -----
with tab_raw:
    st.subheader("Filtered participant data")
    st.dataframe(df, use_container_width=True, height=420)
    st.download_button(
        label="⬇️ Download filtered CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="cognitive_aging_filtered.csv",
        mime="text/csv",
    )
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
