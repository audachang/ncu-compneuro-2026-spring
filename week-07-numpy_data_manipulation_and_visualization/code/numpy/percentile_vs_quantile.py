"""Week 07 · numpy — percentile vs quantile

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

rts = np.array([320, 415, 280, 510, 390])

print("percentile(50) :", np.percentile(rts, 50))    # median
print("quantile(0.5)  :", np.quantile(rts, 0.5))     # same

print("quartiles (percentile):", np.percentile(rts, [25, 50, 75]))
print("quartiles (quantile)  :", np.quantile(rts, [0.25, 0.5, 0.75]))
