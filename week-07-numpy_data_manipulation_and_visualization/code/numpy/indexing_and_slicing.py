"""Week 07 · numpy — Indexing and Slicing (1D)

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

rts = np.array([320, 415, 280, 510, 390])
print("rts[0]  :", rts[0])     # 320
print("rts[-1] :", rts[-1])    # 390
print("rts[1:4]:", rts[1:4])   # [415, 280, 510]
