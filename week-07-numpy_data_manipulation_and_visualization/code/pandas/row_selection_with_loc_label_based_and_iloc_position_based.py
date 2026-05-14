"""Week 07 · pandas — Row selection with .loc and .iloc

Extracted from: week-07-pandas_and_dataframes.md
"""

import pandas as pd

df = pd.DataFrame({
    "subject":   ["P01", "P01", "P02", "P02"],
    "condition": ["congruent", "incongruent", "congruent", "incongruent"],
    "rt_ms":     [320, 450, 340, 470],
    "correct":   [1, 1, 1, 0],
})

# loc: label-based (index label)
print("df.loc[0]:")
print(df.loc[0])

print("\ndf.loc[0:2]  (rows 0, 1, 2 — inclusive):")
print(df.loc[0:2])

# iloc: position-based (integer offset)
print("\ndf.iloc[0]:")
print(df.iloc[0])

print("\ndf.iloc[0:2]  (rows 0, 1 — exclusive upper):")
print(df.iloc[0:2])

print("\ndf.iloc[0, 2]  (row 0, column 2):", df.iloc[0, 2])
