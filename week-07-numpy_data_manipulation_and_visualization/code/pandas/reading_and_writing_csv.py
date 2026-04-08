"""Week 07 · pandas — Reading and Writing CSV

Extracted from: week-07-pandas_and_dataframes.md
"""

import pandas as pd

df = pd.DataFrame({
    "subject":   ["P01", "P01", "P02", "P02"],
    "condition": ["congruent", "incongruent", "congruent", "incongruent"],
    "rt_ms":     [320, 450, 340, 470],
    "correct":   [1, 1, 1, 0],
})

# Write — index=False avoids saving the row numbers as a column
df.to_csv("stroop_results.csv", index=False)
print("Saved stroop_results.csv")

# Read back
df_loaded = pd.read_csv("stroop_results.csv")
print("\nLoaded:")
print(df_loaded)
