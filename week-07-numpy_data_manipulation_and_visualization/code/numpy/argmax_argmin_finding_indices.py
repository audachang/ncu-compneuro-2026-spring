"""Week 07 · numpy — argmax, argmin — Finding Indices

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

rts = np.array([320, 415, 280, 510, 390])

slowest_trial = rts.argmax()    # index of 510
print(f"Slowest: trial {slowest_trial}, RT = {rts[slowest_trial]} ms")

fastest_trial = rts.argmin()    # index of 280
print(f"Fastest: trial {fastest_trial}, RT = {rts[fastest_trial]} ms")

# Useful for finding the outlier:
outlier_idx = np.argmax(np.abs(rts - rts.mean()))
print(f"Furthest from mean: trial {outlier_idx}, RT = {rts[outlier_idx]} ms")
