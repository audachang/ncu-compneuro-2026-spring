"""Week 07 · numpy — Creating Arrays

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

# From a list
rts = np.array([320, 415, 280, 510, 390])
print("From list:", rts)

# Sequences
print("zeros:", np.zeros(5))
print("ones:", np.ones((3, 4)))
print("arange:", np.arange(0, 10, 2))
print("linspace:", np.linspace(0, 1, 5))

# Random data (useful for simulations)
rng = np.random.default_rng(42)
rts_sim = rng.normal(loc=400, scale=80, size=100)
print("Simulated RTs (first 5):", rts_sim[:5].round(1))
