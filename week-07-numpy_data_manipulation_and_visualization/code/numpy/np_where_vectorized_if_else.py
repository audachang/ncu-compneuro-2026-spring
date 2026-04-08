"""Week 07 · numpy — np.where — Vectorized if/else

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

rts = np.array([320, 415, 280, 510, 390])

labels = np.where(rts > 400, "slow", "fast")
print("RTs   :", rts)
print("Labels:", labels)   # ['fast', 'slow', 'fast', 'slow', 'fast']

# You can also use arrays as the values:
rts_categorized = np.where(rts > 400, "outlier", "normal")
print("Categories:", rts_categorized)

# Or perform computations:
rts_adjusted = np.where(rts > 1000, rts - 100, rts)
print("Adjusted  :", rts_adjusted)
