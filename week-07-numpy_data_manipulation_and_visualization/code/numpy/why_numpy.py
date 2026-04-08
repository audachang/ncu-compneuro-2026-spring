"""Week 07 · numpy — Why NumPy?

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

# Python list — slow for large data
rts_list = [320, 415, 280, 510, 390]
doubled_list = [rt * 2 for rt in rts_list]   # loop needed
print("List doubled:", doubled_list)

# NumPy array — fast, no loop needed
rts = np.array([320, 415, 280, 510, 390])
doubled = rts * 2   # vectorized — operates on all elements at once
print("Array doubled:", doubled)
