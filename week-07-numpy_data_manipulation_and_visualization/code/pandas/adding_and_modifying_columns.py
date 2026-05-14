"""Week 07 · pandas — Adding and Modifying Columns

Extracted from: week-07-pandas_and_dataframes.md
"""

import numpy as np
import pandas as pd

df = pd.DataFrame({
    "subject":   ["P01", "P01", "P02", "P02"],
    "condition": ["congruent", "incongruent", "congruent", "incongruent"],
    "rt_ms":     [320, 450, 340, 470],
    "correct":   [1, 1, 1, 0],
})

# Derived column — vectorized
df["rt_sec"] = df["rt_ms"] / 1000

# Label fast/slow using np.where (faster than apply for simple cases)
median_rt = df["rt_ms"].median()
df["speed"] = np.where(df["rt_ms"] < median_rt, "fast", "slow")

print(df)
print(f"\nMedian RT: {median_rt} ms")
