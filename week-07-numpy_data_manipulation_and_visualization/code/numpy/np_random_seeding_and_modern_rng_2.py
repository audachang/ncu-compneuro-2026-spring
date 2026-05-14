"""Week 07 · numpy — np.random — Modern RNG API (recommended)

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

rng = np.random.default_rng(42)
rts = rng.normal(loc=400, scale=80, size=100)
print("First 5 RTs:", rts[:5].round(1))
print(f"Mean: {rts.mean():.1f}  Std: {rts.std():.1f}")
