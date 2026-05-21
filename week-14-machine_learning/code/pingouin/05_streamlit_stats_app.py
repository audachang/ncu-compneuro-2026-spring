"""
05_streamlit_stats_app.py
--------------------------
互動式行為實驗統計報告 dashboard。

整合 pingouin (統計) + Plotly (視覺化) + Streamlit (部署)。
使用者可上傳 trial-level CSV 或使用內建模擬資料，
透過 sidebar 過濾 RT / accuracy，並在 tabs 切換不同統計分析。

Course : NS5116 (Week 14 supplement)
Run    : streamlit run 05_streamlit_stats_app.py
Deploy : 把本檔 + requirements.txt push 到 GitHub，再到 share.streamlit.io
"""

import numpy as np
import pandas as pd
import pingouin as pg
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------
# Page config
# ---------------------------------------------------------------
st.set_page_config(page_title="Behavioral Stats Dashboard", layout="wide")
st.title("行為實驗統計報告 Dashboard")
st.caption("Pingouin + Plotly + Streamlit · NS5116 2026 Spring Week 14")


# ---------------------------------------------------------------
# 1. 資料來源：上傳 CSV 或使用模擬資料
# ---------------------------------------------------------------
@st.cache_data
def simulate_data(n_subj: int = 30, seed: int = 42) -> pd.DataFrame:
    """生成 trial-level Stroop 模擬資料 (within: condition, between: group)."""
    rng = np.random.default_rng(seed)
    rows = []
    for sid in range(n_subj):
        group = 'young' if sid < n_subj // 2 else 'old'
        age_offset = 0 if group == 'young' else 80
        for cond, mu in [('congruent', 450), ('incongruent', 520)]:
            for trial in range(20):
                rt = rng.normal(mu + age_offset, 60)
                acc = rng.binomial(1, 0.9 if cond == 'congruent' else 0.82)
                rows.append({
                    'subject': sid, 'group': group, 'condition': cond,
                    'trial': trial, 'rt': rt, 'accuracy': acc,
                })
    return pd.DataFrame(rows)


with st.sidebar:
    st.header("資料來源")
    uploaded = st.file_uploader("上傳 trial CSV", type=['csv'])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        st.info("使用模擬資料（30 受試者 × 2 condition × 20 trials）")
        df = simulate_data()

    st.header("分析參數")
    rt_lower = st.slider("RT lower bound (ms)", 100, 400, 200)
    rt_upper = st.slider("RT upper bound (ms)", 800, 2000, 1500)
    only_correct = st.checkbox("只分析 correct trials", value=True)

# ---------------------------------------------------------------
# 2. Cleaning
# ---------------------------------------------------------------
df_clean = df[(df['rt'] >= rt_lower) & (df['rt'] <= rt_upper)]
if only_correct and 'accuracy' in df.columns:
    df_clean = df_clean[df_clean['accuracy'] == 1]

st.subheader("資料概覽")
c1, c2, c3 = st.columns(3)
c1.metric("受試者數", df_clean['subject'].nunique())
c2.metric("總 trial 數", len(df_clean))
c3.metric("Conditions", df_clean['condition'].nunique())

# ---------------------------------------------------------------
# 3. Subject-level aggregation
# ---------------------------------------------------------------
subj_mean = (
    df_clean.groupby(['subject', 'group', 'condition'])['rt']
    .mean()
    .reset_index()
)

# ---------------------------------------------------------------
# 4. Visualisation (Plotly)
# ---------------------------------------------------------------
st.subheader("RT 分布")
fig = px.box(
    subj_mean, x='condition', y='rt', color='group',
    points='all', title="Subject-level mean RT by condition × group",
)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------
# 5. 統計分析 — Tabs
# ---------------------------------------------------------------
st.subheader("統計分析")
tab1, tab2, tab3 = st.tabs(["Paired t-test", "Mixed ANOVA", "Correlation"])

with tab1:
    st.markdown("**Stroop effect — paired t-test (congruent vs. incongruent)**")
    wide = (
        subj_mean.pivot(index='subject', columns='condition', values='rt')
        .dropna()
    )
    paired_plot_df = (
        wide.reset_index()
        .melt(id_vars='subject', value_vars=['congruent', 'incongruent'],
              var_name='condition', value_name='rt')
    )
    fig_t = px.line(
        paired_plot_df, x='condition', y='rt', color='subject',
        markers=True, title="Paired t-test companion plot: each subject",
    )
    fig_t.update_traces(showlegend=False, opacity=0.35)
    st.plotly_chart(fig_t, use_container_width=True)

    t_res = pg.ttest(wide['congruent'], wide['incongruent'], paired=True)
    st.dataframe(t_res.round(4))
    st.download_button(
        "下載 t-test 結果 CSV",
        t_res.to_csv(index=False).encode('utf-8'),
        file_name="ttest_result.csv",
    )

with tab2:
    st.markdown("**Mixed ANOVA — condition (within) × group (between)**")
    interaction = (
        subj_mean.groupby(['group', 'condition'])['rt']
        .agg(['mean', 'sem'])
        .reset_index()
    )
    fig_aov = px.line(
        interaction, x='condition', y='mean', color='group',
        error_y='sem', markers=True,
        title="Mixed ANOVA companion plot: group × condition interaction",
        labels={'mean': 'Mean RT (ms)', 'sem': 'SE'},
    )
    st.plotly_chart(fig_aov, use_container_width=True)

    aov = pg.mixed_anova(
        data=subj_mean, dv='rt', within='condition',
        between='group', subject='subject',
    )
    st.dataframe(aov.round(4))

    st.markdown("**Post-hoc pairwise tests (Bonferroni)**")
    posthoc = pg.pairwise_tests(
        data=subj_mean, dv='rt', within='condition',
        between='group', subject='subject', padjust='bonf',
    )
    st.dataframe(posthoc.round(4))

with tab3:
    st.markdown("**Correlation matrix（每位受試者層級）**")
    wide_corr = (
        subj_mean.pivot(index='subject', columns='condition', values='rt')
    )
    wide_corr['stroop_effect'] = (
        wide_corr['incongruent'] - wide_corr['congruent']
    )
    corr_matrix = wide_corr.corr(numeric_only=True)
    fig_corr = px.imshow(
        corr_matrix, text_auto='.2f', zmin=-1, zmax=1,
        color_continuous_scale='RdBu_r',
        title="Correlation companion plot: subject-level RT features",
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    st.dataframe(wide_corr.rcorr(stars=True))

st.markdown("---")
st.caption("Built with pingouin · plotly · streamlit")
