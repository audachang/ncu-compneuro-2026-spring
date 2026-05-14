"""Week 07 · pandas — Pivot Tables: Computing interference cost

Extracted from: week-07-pandas_and_dataframes.md
"""

import pandas as pd

df = pd.DataFrame({
    "subject":   ["P01", "P01", "P02", "P02"],
    "condition": ["congruent", "incongruent", "congruent", "incongruent"],
    "rt_ms":     [320, 450, 340, 470],
    "correct":   [1, 1, 1, 0],
})

summary = pd.pivot_table(
    df, values="rt_ms", index="subject", columns="condition", aggfunc="mean"
)

# Interference cost = incongruent − congruent
summary["interference_cost"] = summary["incongruent"] - summary["congruent"]
print(summary)
