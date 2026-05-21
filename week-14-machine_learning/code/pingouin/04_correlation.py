"""
04_correlation.py
------------------
相關分析：Pearson / Spearman / Partial correlation / Correlation matrix。
情境：individual differences 研究 — working memory (WM) 與 fluid
intelligence (Gf) 的關係，控制 age / education 等 covariates。

Course : NS5116 (Week 14 supplement)
Topic  : Correlation and partial correlation with pingouin
Run    : python 04_correlation.py
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


def add_regression_line(x, y, color='black'):
    """Add a simple least-squares line to the active axes."""
    slope, intercept = np.polyfit(x, y, deg=1)
    xs = np.linspace(np.min(x), np.max(x), 100)
    plt.plot(xs, intercept + slope * xs, color=color, linewidth=2)


def residualize(y, covariates):
    """Return residuals after removing linear effects of covariates."""
    y = np.asarray(y)
    covariates = np.asarray(covariates)
    if covariates.ndim == 1:
        covariates = covariates[:, None]
    design = np.column_stack([np.ones(len(y)), covariates])
    beta, *_ = np.linalg.lstsq(design, y, rcond=None)
    return y - design @ beta

np.random.seed(42)

# ---------------------------------------------------------------
# 1. 模擬資料：WM、Gf、Age (Age 是潛在混淆變項)
# ---------------------------------------------------------------
n = 100
wm = np.random.normal(50, 10, n)
gf = 0.5 * wm + np.random.normal(0, 8, n)
age = np.random.uniform(20, 70, n)

df = pd.DataFrame({'wm': wm, 'gf': gf, 'age': age})

# ---------------------------------------------------------------
# 2. Pearson 與 Spearman correlation
# ---------------------------------------------------------------
print("=" * 60)
print("Pearson correlation (wm × gf):")
print(pg.corr(df['wm'], df['gf'], method='pearson'))

plt.figure(figsize=(6, 5))
plt.scatter(df['wm'], df['gf'], color='0.35', alpha=0.75)
add_regression_line(df['wm'], df['gf'])
plt.xlabel('Working memory score')
plt.ylabel('Fluid intelligence score')
plt.title('Pearson correlation: linear WM-Gf association')
save_current_figure('04a_pearson_scatter_wm_gf.png')

print("\nSpearman correlation (rank-based, robust to outliers):")
print(pg.corr(df['wm'], df['gf'], method='spearman'))

wm_rank = df['wm'].rank()
gf_rank = df['gf'].rank()
plt.figure(figsize=(6, 5))
plt.scatter(wm_rank, gf_rank, color='0.35', alpha=0.75)
add_regression_line(wm_rank, gf_rank)
plt.xlabel('Rank of working memory')
plt.ylabel('Rank of fluid intelligence')
plt.title('Spearman correlation: association between ranks')
save_current_figure('04b_spearman_rank_scatter.png')

# ---------------------------------------------------------------
# 3. Partial correlation：控制 age
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("Partial correlation (wm × gf, controlling for age):")
print(pg.partial_corr(data=df, x='wm', y='gf', covar='age'))

wm_resid_age = residualize(df['wm'], df['age'])
gf_resid_age = residualize(df['gf'], df['age'])
plt.figure(figsize=(6, 5))
plt.scatter(wm_resid_age, gf_resid_age, color='0.35', alpha=0.75)
add_regression_line(wm_resid_age, gf_resid_age)
plt.axhline(0, color='0.75', linewidth=1)
plt.axvline(0, color='0.75', linewidth=1)
plt.xlabel('WM residual after controlling age')
plt.ylabel('Gf residual after controlling age')
plt.title('Partial correlation: residualized WM-Gf relationship')
save_current_figure('04c_partial_corr_age_residuals.png')

# ---------------------------------------------------------------
# 4. Correlation matrix with FDR 校正
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("Correlation matrix (rcorr, FDR-corrected):")
print(df.rcorr(padjust='fdr_bh', stars=True))

corr = df[['wm', 'gf', 'age']].corr()
fig, ax = plt.subplots(figsize=(5.5, 4.8))
im = ax.imshow(corr, vmin=-1, vmax=1, cmap='coolwarm')
ax.set_xticks(range(len(corr.columns)), corr.columns)
ax.set_yticks(range(len(corr.columns)), corr.columns)
for i, row in enumerate(corr.index):
    for j, col in enumerate(corr.columns):
        ax.text(j, i, f"{corr.loc[row, col]:.2f}",
                ha='center', va='center', color='black')
fig.colorbar(im, ax=ax, label='Pearson r')
ax.set_title('Correlation matrix: WM, Gf, and age')
save_current_figure('04d_correlation_matrix_heatmap.png')

# ---------------------------------------------------------------
# 5. 進階：同時控制多個 covariates (age + 額外 noise variable)
# ---------------------------------------------------------------
np.random.seed(0)
df['edu'] = 0.2 * age + np.random.normal(14, 3, n)   # 教育年數

print("\n" + "=" * 60)
print("Partial correlation controlling age + education:")
print(pg.partial_corr(data=df, x='wm', y='gf', covar=['age', 'edu']))

covars = df[['age', 'edu']]
wm_resid_covars = residualize(df['wm'], covars)
gf_resid_covars = residualize(df['gf'], covars)
plt.figure(figsize=(6, 5))
plt.scatter(wm_resid_covars, gf_resid_covars, color='0.35', alpha=0.75)
add_regression_line(wm_resid_covars, gf_resid_covars)
plt.axhline(0, color='0.75', linewidth=1)
plt.axvline(0, color='0.75', linewidth=1)
plt.xlabel('WM residual after controlling age + education')
plt.ylabel('Gf residual after controlling age + education')
plt.title('Partial correlation: controlling multiple covariates')
save_current_figure('04e_partial_corr_age_education_residuals.png')
