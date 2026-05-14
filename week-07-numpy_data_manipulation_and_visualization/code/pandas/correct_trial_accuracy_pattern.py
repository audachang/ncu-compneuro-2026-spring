"""Week 07 · pandas — Correct-trial accuracy pattern

Extracted from: week-07-pandas_and_dataframes.md
"""

import pandas as pd

df = pd.DataFrame({
    "subject":   ["P01", "P01", "P02", "P02"],
    "condition": ["congruent", "incongruent", "congruent", "incongruent"],
    "rt_ms":     [320, 450, 340, 470],
    "correct":   [1, 1, 1, 0],
})

# Proportion correct per condition (mean of 0/1 column = proportion)
accuracy = df.groupby("condition")["correct"].mean()
print("Accuracy per condition:")
print(accuracy)
