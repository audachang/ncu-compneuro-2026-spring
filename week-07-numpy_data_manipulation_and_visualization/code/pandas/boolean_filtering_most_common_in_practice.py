"""Week 07 · pandas — Boolean filtering (most common in practice)

Extracted from: week-07-pandas_and_dataframes.md
"""

import pandas as pd

df = pd.DataFrame({
    "subject":   ["P01", "P01", "P02", "P02"],
    "condition": ["congruent", "incongruent", "congruent", "incongruent"],
    "rt_ms":     [320, 450, 340, 470],
    "correct":   [1, 1, 1, 0],
})

# Keep only correct trials
df_correct = df[df["correct"] == 1]
print("Correct trials:\n", df_correct)

# Keep only fast correct trials
df_fast = df[(df["correct"] == 1) & (df["rt_ms"] < 400)]
print("\nFast correct trials (RT < 400 ms):\n", df_fast)

# Keep only P01's trials
df_p01 = df[df["subject"] == "P01"]
print("\nP01 trials:\n", df_p01)
