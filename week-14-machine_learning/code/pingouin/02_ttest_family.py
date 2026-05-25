"""
02_ttest_family.py
-------------------
示範 pingouin t-test 家族：paired / independent / one-sample，
以及 non-parametric 替代方案 (Wilcoxon, Mann-Whitney) 與 effect size 計算。

Course : NS5116 (Week 14 supplement)
Topic  : Behavioral statistics — t-test family
Run    : python 02_ttest_family.py
"""

import numpy as np
import pingouin as pg
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats


FIG_DIR = Path(__file__).with_name("figures")
FIG_DIR.mkdir(exist_ok=True)


def save_current_figure(filename):
    """Save the current matplotlib figure and print the output path."""
    path = FIG_DIR / filename
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    print(f"Figure saved: {path}")


def jittered_x(center, n, width=0.05):
    """Small deterministic offsets so dots do not fully overlap."""
    return center + np.linspace(-width, width, n)

np.random.seed(42)

# ---------------------------------------------------------------
# 1. 模擬資料：Stroop within-subject + baseline 對照
# ---------------------------------------------------------------
n = 30
congruent = np.random.uniform(450, 60, n)      # within-subject
incongruent = np.random.normal(520, 80, n)    # within-subject
baseline = np.random.normal(500, 30, n)       # between-group control sample

# ---------------------------------------------------------------
# 2. (a) Paired t-test — within-subject design
# ---------------------------------------------------------------
print("=" * 60)
print("(a) Paired t-test (congruent vs. incongruent):")
print(pg.ttest(congruent, incongruent, paired=True))

plt.figure(figsize=(7, 4.5))
for i in range(n):
    plt.plot([0, 1], [congruent[i], incongruent[i]],
             color='0.78', linewidth=1)
plt.errorbar(
    [0, 1],
    [congruent.mean(), incongruent.mean()],
    yerr=[
        congruent.std(ddof=1) / np.sqrt(n),
        incongruent.std(ddof=1) / np.sqrt(n),
    ],
    color='black', marker='o', linewidth=2.5, capsize=5,
)
plt.xticks([0, 1], ['congruent', 'incongruent'])
plt.ylabel('Reaction time (ms)')
plt.title('Paired t-test: within-subject Stroop effect')
save_current_figure('02a_paired_ttest_stroop.png')

# ---------------------------------------------------------------
# 2. (b) Independent t-test — between-group design
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("(b) Independent t-test (congruent vs. baseline control group):")
print(pg.ttest(congruent, baseline, paired=False))

plt.figure(figsize=(7, 4.5))
plt.scatter(jittered_x(0, n), congruent, color='0.25', alpha=0.75,
            label='congruent')
plt.scatter(jittered_x(1, n), baseline, color='0.55', alpha=0.75,
            label='baseline')
plt.errorbar(
    [0, 1],
    [congruent.mean(), baseline.mean()],
    yerr=[congruent.std(ddof=1) / np.sqrt(n), 0],
    color='black', marker='o', linewidth=0, capsize=5,
)
plt.xticks([0, 1], ['congruent', 'baseline'])
plt.ylabel('Reaction time (ms)')
plt.title('Independent t-test: observed RT vs. baseline control group')
plt.legend(frameon=False)
save_current_figure('02b_independent_ttest_congruent_baseline.png')

# ---------------------------------------------------------------
# 2. (c) One-sample t-test — 與固定值比較
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("(c) One-sample t-test (RT vs. 500ms):")
print(pg.ttest(congruent, 500))

plt.figure(figsize=(7, 4.5))
plt.hist(congruent, bins=10, color='0.80', edgecolor='white')
plt.axvline(500, color='black', linestyle='--', linewidth=2,
            label='Null value = 500 ms')
plt.axvline(congruent.mean(), color='0.15', linewidth=2,
            label=f'Sample mean = {congruent.mean():.1f} ms')
plt.xlabel('Reaction time (ms)')
plt.ylabel('Number of subjects')
plt.title('One-sample t-test: sample mean compared with 500 ms')
plt.legend(frameon=False)
save_current_figure('02c_one_sample_ttest_vs_500ms.png')

# ---------------------------------------------------------------
# 3. Non-parametric 替代方案 (違反 normality 假設時)
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("Wilcoxon signed-rank test (paired non-parametric):")
print(pg.wilcoxon(congruent, incongruent, alternative='two-sided'))

diff = incongruent - congruent
plt.figure(figsize=(7, 4.5))
plt.axvline(0, color='black', linestyle='--', linewidth=1.5,
            label='No within-subject difference')
plt.hist(diff, bins=10, color='0.80', edgecolor='white')
plt.axvline(np.median(diff), color='0.15', linewidth=2,
            label=f'Median difference = {np.median(diff):.1f} ms')
plt.xlabel('Incongruent - congruent RT (ms)')
plt.ylabel('Number of subjects')
plt.title('Wilcoxon signed-rank test: distribution of paired differences')
plt.legend(frameon=False)
save_current_figure('02d_wilcoxon_paired_differences.png')

print("\nMann-Whitney U test (independent non-parametric):")
print(pg.mwu(congruent, baseline))

plt.figure(figsize=(7, 4.5))
for values, label, color in [
    (congruent, 'congruent', '0.25'),
    (baseline, 'baseline', '0.55'),
]:
    sorted_values = np.sort(values)
    y = np.arange(1, len(sorted_values) + 1) / len(sorted_values)
    plt.step(sorted_values, y, where='post', label=label, color=color)
plt.xlabel('Reaction time (ms)')
plt.ylabel('Empirical cumulative probability')
plt.title('Mann-Whitney U test: comparing two distributions')
plt.legend(frameon=False)
save_current_figure('02e_mann_whitney_ecdf.png')

# ---------------------------------------------------------------
# 4. Effect size 計算
# ---------------------------------------------------------------
print("\n" + "=" * 60)
d_cohen = pg.compute_effsize(congruent, incongruent, paired=True, eftype='cohen')
g_hedges = pg.compute_effsize(congruent, incongruent, paired=True, eftype='hedges')
print(f"Cohen's d = {d_cohen:.3f}    (0.2 small, 0.5 medium, 0.8 large)")
print(f"Hedges' g = {g_hedges:.3f}    (small-sample bias-corrected d)")

# ---------------------------------------------------------------
# 5. 假設檢驗：normality 是否成立？
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("Shapiro-Wilk normality test:")
print(pg.normality(congruent))
print(pg.normality(incongruent))

fig, axes = plt.subplots(1, 2, figsize=(9, 4))
for ax, values, label in [
    (axes[0], congruent, 'congruent'),
    (axes[1], incongruent, 'incongruent'),
]:
    stats.probplot(values, dist='norm', plot=ax)
    ax.set_title(f'Q-Q plot: {label}')
    ax.get_lines()[0].set_markerfacecolor('0.25')
    ax.get_lines()[0].set_markeredgecolor('0.25')
    ax.get_lines()[1].set_color('black')
fig.suptitle('Shapiro-Wilk normality check: visual companion')
save_current_figure('02f_normality_qq_plots.png')
