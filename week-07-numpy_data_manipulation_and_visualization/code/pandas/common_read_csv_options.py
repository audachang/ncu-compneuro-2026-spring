"""Week 07 · pandas — Inspecting a loaded DataFrame

Extracted from: week-07-pandas_and_dataframes.md
"""

import pandas as pd

df = pd.DataFrame({
    "subject":   ["P01", "P01", "P02", "P02"],
    "condition": ["congruent", "incongruent", "congruent", "incongruent"],
    "rt_ms":     [320, 450, 340, 470],
    "correct":   [1, 1, 1, 0],
})

# After loading a CSV these three calls give you an immediate health check
print("--- info ---")
df.info()

print("\n--- describe ---")
print(df.describe())

print("\n--- missing values ---")
print(df.isna().sum())
