"""Week 07 · numpy — Descriptive Statistics

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

rts = np.array([320, 415, 280, 510, 390])

print("mean    :", rts.mean())
print("std     :", rts.std().round(2))
print("min     :", rts.min())
print("max     :", rts.max())
print("median  :", np.median(rts))
print("quartiles:", np.percentile(rts, [25, 75]))
