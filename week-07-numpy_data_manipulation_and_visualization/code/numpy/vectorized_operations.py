"""Week 07 · numpy — Vectorized Operations

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

rts = np.array([320, 415, 280, 510, 390])

# Arithmetic applied element-wise
rts_sec = rts / 1000          # convert ms → seconds
rts_z   = (rts - rts.mean()) / rts.std()  # z-score

print("RTs (ms)     :", rts)
print("RTs (sec)    :", rts_sec)
print("Z-scored RTs :", rts_z.round(2))

# Comparison (returns boolean array)
print("rts > 400    :", rts > 400)   # [False, True, False, True, False]

# Mathematical functions
print("log(rts)     :", np.log(rts).round(2))
print("sqrt(rts)    :", np.sqrt(rts).round(2))
print("|rts - 400|  :", np.abs(rts - 400))
