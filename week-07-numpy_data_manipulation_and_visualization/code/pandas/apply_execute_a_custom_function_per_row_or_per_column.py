"""Week 07 · pandas — apply: execute a custom function per element

Extracted from: week-07-pandas_and_dataframes.md
"""

import pandas as pd

df = pd.DataFrame({
    "subject":   ["P01", "P01", "P02", "P02"],
    "condition": ["congruent", "incongruent", "congruent", "incongruent"],
    "rt_ms":     [320, 450, 340, 470],
    "correct":   [1, 1, 1, 0],
})

def classify_rt(rt):
    if rt < 300:
        return "very fast"
    elif rt < 400:
        return "normal"
    else:
        return "slow"

df["rt_class"] = df["rt_ms"].apply(classify_rt)
print(df[["subject", "condition", "rt_ms", "rt_class"]])
