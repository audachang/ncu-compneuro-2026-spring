"""Week 07 · pandas — Creating DataFrames (row-by-row in a loop)

Extracted from: week-07-pandas_and_dataframes.md
"""

import pandas as pd

rows = []
for trial in range(1, 5):
    rows.append({"trial": trial, "rt_ms": 300 + trial * 20})

df = pd.DataFrame(rows)
print(df)
