"""Week 07 · numpy — Fancy Indexing — Selecting by Indices

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

rts = np.array([320, 415, 280, 510, 390])

indices = np.array([0, 2, 4])
selected = rts[indices]    # trials 0, 2, 4
print("Selected trials:", selected)   # [320, 280, 390]

# Sort by RT using argsort
sorted_indices = np.argsort(rts)
sorted_rts = rts[sorted_indices]
print("Sort order (indices):", sorted_indices)
print("Sorted RTs          :", sorted_rts)
