"""
03_anova.py
------------
ANOVA 家族：one-way / repeated-measures / mixed (2 × 2 factorial)。

Course : NS5116 (Week 14 supplement)
Topic  : ANOVA for behavioral / cognitive experiments
Run    : python 03_anova.py
"""

import numpy as np
import pandas as pd
import pingouin as pg
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path


FIG_DIR = Path(__file__).with_name("figures")
FIG_DIR.mkdir(exist_ok=True)


def save_current_figure(filename):
    """Save the current matplotlib figure and print the output path."""
    path = FIG_DIR / filename
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    print(f"Figure saved: {path}")


def mean_sem(values):
    """Return mean and standard error for one numeric vector."""
    values = np.asarray(values)
    return values.mean(), values.std(ddof=1) / np.sqrt(len(values))

np.random.seed(42)

# ---------------------------------------------------------------
# 1. 模擬 N-back 任務：3 個 working memory load
# ---------------------------------------------------------------
def simulate_nback(n_subjects=30):
    """每位受試者跑 1-back, 2-back, 3-back，回傳 long-format DataFrame."""
    rows = []
    for sid in range(n_subjects):
        for load, base_rt in [('1-back', 500), ('2-back', 580), ('3-back', 680)]:
            rt = np.random.normal(base_rt, 70)
            rows.append({'subject': sid, 'load': load, 'rt': rt})
    return pd.DataFrame(rows)


df = simulate_nback()
print("=" * 60)
print("Long-format data (first 6 rows):")
print(df.head(6))

# ---------------------------------------------------------------
# 2. One-way ANOVA (假設 load 是 between-subject)
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("One-way ANOVA (between-subject view):")
print(pg.anova(data=df, dv='rt', between='load', detailed=True))

load_order = ['1-back', '2-back', '3-back']
plt.figure(figsize=(7, 4.5))
for x, load in enumerate(load_order):
    values = df.loc[df['load'] == load, 'rt'].to_numpy()
    jitter = np.linspace(-0.08, 0.08, len(values))
    plt.scatter(x + jitter, values, color='0.55', alpha=0.55, s=22)
    m, se = mean_sem(values)
    plt.errorbar(x, m, yerr=se, color='black', marker='o',
                 linewidth=0, capsize=5)
plt.xticks(range(len(load_order)), load_order)
plt.ylabel('Reaction time (ms)')
plt.title('One-way ANOVA: RT distribution across N-back load')
save_current_figure('03a_oneway_anova_load.png')

# ---------------------------------------------------------------
# 3. Repeated-measures ANOVA (load 是 within-subject)
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("Repeated-measures ANOVA:")
rm = pg.rm_anova(
    data=df, dv='rt', within='load', subject='subject', detailed=True
)
print(rm)
# eps = Greenhouse-Geisser ε；若 < 0.75 需引用 GG 校正版本

wide = df.pivot(index='subject', columns='load', values='rt')[load_order]
plt.figure(figsize=(7, 4.5))
for _, row in wide.iterrows():
    plt.plot(range(len(load_order)), row.values, color='0.80', linewidth=1)
means = wide.mean(axis=0).to_numpy()
ses = wide.sem(axis=0).to_numpy()
plt.errorbar(range(len(load_order)), means, yerr=ses, color='black',
             marker='o', linewidth=2.5, capsize=5)
plt.xticks(range(len(load_order)), load_order)
plt.ylabel('Reaction time (ms)')
plt.title('Repeated-measures ANOVA: each subject across load')
save_current_figure('03b_rm_anova_subject_trajectories.png')

# ---------------------------------------------------------------
# 4. Post-hoc pairwise tests with Bonferroni 校正
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("Post-hoc pairwise t-tests (Bonferroni):")
posthoc = pg.pairwise_tests(
    data=df, dv='rt', within='load', subject='subject', padjust='bonf'
)
print(posthoc[['A', 'B', 'T', 'p_unc', 'p_corr', 'p_adjust', 'hedges']])

posthoc_plot = posthoc.copy()
posthoc_plot['contrast'] = posthoc_plot['A'] + ' vs. ' + posthoc_plot['B']
plt.figure(figsize=(7, 4.5))
plt.axvline(0, color='black', linewidth=1)
plt.barh(posthoc_plot['contrast'], posthoc_plot['hedges'], color='0.60')
for y, row in enumerate(posthoc_plot.itertuples()):
    plt.text(row.hedges, y, f"  p_corr={row.p_corr:.3f}", va='center')
plt.xlabel("Hedges' g")
plt.title('Post-hoc pairwise tests: effect size by contrast')
save_current_figure('03c_posthoc_pairwise_effect_sizes.png')

# ---------------------------------------------------------------
# 5. Mixed ANOVA: 2 × 2 factorial (age × condition)
# ---------------------------------------------------------------
np.random.seed(1)
rows = []
for sid in range(40):
    age = 'young' if sid < 20 else 'old'
    for cond in ['congruent', 'incongruent']:
        base = 450 if cond == 'congruent' else 520
        if age == 'old':
            base += 80
        rt = np.random.normal(base, 60)
        rows.append({'subject': sid, 'age': age, 'cond': cond, 'rt': rt})
mixed_df = pd.DataFrame(rows)

print("\n" + "=" * 60)
print("Mixed ANOVA (age between × cond within):")
print(pg.mixed_anova(
    data=mixed_df, dv='rt', within='cond', between='age', subject='subject'
))


cond_order = ['congruent', 'incongruent']
age_order = ['young', 'old']
plt.figure(figsize=(7, 4.5))
for age in age_order:
    means = []
    ses = []
    for cond in cond_order:
        values = mixed_df.loc[
            (mixed_df['age'] == age) & (mixed_df['cond'] == cond), 'rt'
        ].to_numpy()
        m, se = mean_sem(values)
        means.append(m)
        ses.append(se)
    plt.errorbar(cond_order, means, yerr=ses, marker='o',
                 linewidth=2.5, capsize=5, label=age)
plt.ylabel('Reaction time (ms)')
plt.title('Mixed ANOVA: age group × condition interaction')
plt.legend(title='age group', frameon=False)
save_current_figure('03d_mixed_anova_interaction.png')
