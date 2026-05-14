"""Week 07 · numpy — Ufuncs with output arrays (out= parameter)

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

rts = np.array([320, 415, 280, 510, 390], dtype=float)

output = np.empty_like(rts)
np.log(rts, out=output)   # result stored in output, no new allocation
print("log(rts):", output.round(3))
