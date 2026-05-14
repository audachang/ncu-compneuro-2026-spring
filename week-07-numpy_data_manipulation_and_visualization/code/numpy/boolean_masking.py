"""Week 07 · numpy — Boolean Masking

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

rts = np.array([320, 415, 280, 510, 390])

mask = rts > 400
print("mask (rts > 400):", mask)
print("rts[mask]        :", rts[mask])    # [415, 510]

# Shorthand — combine in one step
fast = rts[rts < 350]
print("fast (< 350 ms)  :", fast)         # [320, 280]

# Multiple conditions
valid = rts[(rts >= 150) & (rts <= 900)]
print("valid (150–900)  :", valid)
