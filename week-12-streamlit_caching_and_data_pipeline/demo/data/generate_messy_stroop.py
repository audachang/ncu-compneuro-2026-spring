"""Generate a deliberately messy Stroop-like dataset for Week 12 demos.

執行：
    python generate_messy_stroop.py

產出：messy_stroop.csv (n=200 trials)

故意製造的問題（讓學生用 descriptive statistics 發現）：
    1. rt_ms 欄是字串 dtype（含 "NA"）
    2. rt_ms 含 99999 sentinel outlier
    3. condition 4 個 level 但其實只有 2 個（大小寫不一致）
    4. age 含 -999 sentinel 與真正的 NaN
"""

import numpy as np
import pandas as pd

np.random.seed(99)

N = 200
df = pd.DataFrame({
    "subject_id": np.random.choice([1, 2, 3, 4, 5], N),
    "condition":  np.random.choice(
        ["congruent", "Congruent", "incongruent", "INCONG"], N),
    # 注意：產生時是 numpy float，但下面會混入字串 → 變 object dtype
    "rt_ms":      np.random.normal(500, 80, N),
    "accuracy":   np.random.choice([0, 1, 1, 1, 1], N),
    "age":        np.random.choice([25, 30, 35, 40, 45, 50, 55, 60, 65, 70,
                                    -999, np.nan], N),
})

# 注入 "NA" 字串到 rt_ms（變 object dtype）
rt_col = df["rt_ms"].astype(object)
na_idx = np.random.choice(N, 12, replace=False)
rt_col.iloc[na_idx] = "NA"

# 注入 99999 sentinel
out_idx = np.random.choice(N, 5, replace=False)
rt_col.iloc[out_idx] = 99999
df["rt_ms"] = rt_col

# 為了讓 Stroop effect 在 cleaned data 中可見，
# 把 incongruent trials 的 RT 整體加上 60ms（mean）— 在生成後注入：
incong_mask = df["condition"].str.lower().isin(["incongruent", "incong"])
# 只對非 "NA" 且非 99999 的 row 加；保留物件 dtype
add_idx = df.index[incong_mask & (df["rt_ms"] != "NA") & (df["rt_ms"] != 99999)]
df.loc[add_idx, "rt_ms"] = df.loc[add_idx, "rt_ms"].astype(float) + 60

out = "messy_stroop.csv"
df.to_csv(out, index=False)
print(f"Wrote {out}  (n={len(df)})")
print(df.head())
print(f"\ndtype of rt_ms: {df['rt_ms'].dtype}")
print(f"condition levels: {df['condition'].unique()}")
