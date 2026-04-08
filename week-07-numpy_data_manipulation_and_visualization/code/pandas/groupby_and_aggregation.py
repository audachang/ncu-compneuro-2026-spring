"""Week 07 · pandas — Groupby and Aggregation

Extracted from: week-07-pandas_and_dataframes.md
"""

import pandas as pd

df = pd.DataFrame({
    "subject":   ["P01", "P01", "P02", "P02"],
    "condition": ["congruent", "incongruent", "congruent", "incongruent"],
    "rt_ms":     [320, 450, 340, 470],
    "correct":   [1, 1, 1, 0],
})

# Mean RT per condition
print("Mean RT per condition:")
print(df.groupby("condition")["rt_ms"].mean())

# Multiple stats at once
print("\nMultiple stats per condition:")
print(df.groupby("condition")["rt_ms"].agg(["mean", "std", "count"]))

# Group by two variables
print("\nMean RT per subject × condition:")
print(df.groupby(["subject", "condition"])["rt_ms"].mean())
