"""Week 07 · pandas — Why Pandas?

Extracted from: week-07-pandas_and_dataframes.md
"""

import numpy as np
import pandas as pd

# NumPy — positional, easy to lose track
data = np.array([[1, 320, 1],
                 [2, 450, 0]])
rt_np = data[:, 1]   # need to remember which column is RT
print("NumPy (positional):", rt_np)

# Pandas — self-documenting
df = pd.DataFrame(data, columns=["trial", "rt_ms", "correct"])
rt_pd = df["rt_ms"]  # column name makes intent obvious
print("Pandas (named):\n", rt_pd.to_string())
