"""Week 07 · pandas — Column selection

Extracted from: week-07-pandas_and_dataframes.md
"""

import pandas as pd

df = pd.DataFrame({
    "subject":   ["P01", "P01", "P02", "P02"],
    "condition": ["congruent", "incongruent", "congruent", "incongruent"],
    "rt_ms":     [320, 450, 340, 470],
    "correct":   [1, 1, 1, 0],
})

# Single column → Series (1D)
print("Single column (Series):")
print(df["rt_ms"])

print("\nMultiple columns (DataFrame):")
print(df[["subject", "rt_ms"]])
