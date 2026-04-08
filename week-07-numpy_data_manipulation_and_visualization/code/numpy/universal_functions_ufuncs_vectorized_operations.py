"""Week 07 · numpy — Universal Functions (ufuncs) — Vectorized Operations

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

rts = np.array([320, 415, 280, 510, 390])

# Instead of a loop:
result_loop = []
for rt in rts:
    result_loop.append(np.log(rt))

# Use the ufunc (compiled, fast):
result_ufunc = np.log(rts)

print("Loop result :", [round(x, 3) for x in result_loop])
print("Ufunc result:", result_ufunc.round(3))
print("Equal:", np.allclose(result_loop, result_ufunc))
