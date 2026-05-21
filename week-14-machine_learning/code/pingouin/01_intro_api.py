"""
01_intro_api.py
----------------
比較 scipy.stats 與 pingouin 的 paired t-test API 與輸出格式。

Course : NS5116 (Week 14 supplement)
Topic  : Pingouin API philosophy — one test = one DataFrame
Run    : python 01_intro_api.py
"""

import numpy as np
import pandas as pd
from scipy import stats
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

# ---------------------------------------------------------------
# 1. 模擬 Stroop 任務的 within-subject 資料
# ---------------------------------------------------------------
np.random.seed(42)
n_subjects = 30
congruent = np.random.normal(450, 60, n_subjects)        # ms
incongruent = np.random.normal(520, 80, n_subjects)      # ms
stroop_df = pd.DataFrame({
    'subject': np.arange(n_subjects),
    'congruent': congruent,
    'incongruent': incongruent,
})

# ---------------------------------------------------------------
# 2. scipy.stats: 只回傳 (T, p)
# ---------------------------------------------------------------
t_scipy, p_scipy = stats.ttest_rel(congruent, incongruent)
print("=" * 60)
print("scipy.stats.ttest_rel:")
print(f"  t = {t_scipy:.3f},  p = {p_scipy:.4f}")
print(f"  type = {type(stats.ttest_rel(congruent, incongruent)).__name__}")
print()

# ---------------------------------------------------------------
# 3. pingouin: 一行 → 完整 DataFrame
# ---------------------------------------------------------------
result = pg.ttest(congruent, incongruent, paired=True)
print("=" * 60)
print("pg.ttest (paired=True):")
print(result)
print()
print("Columns:", list(result.columns))
print(f"type = {type(result).__name__}")

# ---------------------------------------------------------------
# 3b. 對應圖：paired t-test 的 within-subject 變化
# ---------------------------------------------------------------
plt.figure(figsize=(7, 4.5))
x = [0, 1]
for _, row in stroop_df.iterrows():
    plt.plot(x, [row['congruent'], row['incongruent']],
             color='0.78', linewidth=1, zorder=1)
means = [congruent.mean(), incongruent.mean()]
ses = [congruent.std(ddof=1) / np.sqrt(n_subjects),
       incongruent.std(ddof=1) / np.sqrt(n_subjects)]
plt.errorbar(x, means, yerr=ses, color='black', marker='o',
             linewidth=2.5, capsize=5, zorder=3, label='Mean ± SE')
plt.xticks(x, ['congruent', 'incongruent'])
plt.ylabel('Reaction time (ms)')
plt.title('Paired t-test: Stroop condition change within each subject')
plt.legend(frameon=False)
save_current_figure('01_paired_ttest_stroop.png')

# ---------------------------------------------------------------
# 4. 直接抽欄位寫 APA-style 報告
# ---------------------------------------------------------------
r = result.iloc[0]
print()
print("=" * 60)
print("APA-style writeup:")
print(
    f"  Paired-samples t-test revealed a significant Stroop effect, "
    f"t({int(r['dof'])}) = {r['T']:.2f}, p = {r['p_val']:.3f}, "
    f"Cohen's d = {r['cohen_d']:.2f}, 95% CI {r['CI95']}, "
    f"BF10 = {r['BF10']}."
)
