"""Week 07 · numpy — np.random — Legacy seeding (old API)

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

np.random.seed(42)
rts = np.random.normal(loc=400, scale=80, size=100)
print("First 5 RTs:", rts[:5].round(1))
print(f"Mean: {rts.mean():.1f}  Std: {rts.std():.1f}")
