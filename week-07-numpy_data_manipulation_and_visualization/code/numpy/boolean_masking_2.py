"""Week 07 · numpy — Boolean Masking: Outlier Removal

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

rts = np.array([320, 415, 280, 510, 390, 50, 2000, 450, 370])

mean = rts.mean()
std  = rts.std()
clean = rts[np.abs(rts - mean) < 2.5 * std]   # remove values > 2.5 SD from mean

print("Original:", rts)
print("Cleaned :", clean)
print(f"Removed : {len(rts) - len(clean)} trial(s)")
