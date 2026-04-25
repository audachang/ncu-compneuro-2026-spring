"""Week 07 · numpy — Why NumPy?

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np
import time

# Python list — slow for large data
rts_list = [320, 415, 280, 510, 390]*10000000
start = time.time()
doubled_list = [rt * 10000000 for rt in rts_list]  
end = time.time()
print(f"{end-start:.24f}")
 # loop needed
#print("List doubled:", doubled_list)

# NumPy array — fast, no loop needed
rts = np.array([320, 415, 280, 510, 390])
rts = np.repeat(rts, 10000000)
start = time.time()
#doubled = np.repeat(rts, 10000000)   
doubled = rts * 10000000
end = time.time()
print(f"{end-start:.24f}")
# vectorized — operates on all elements at once
#print("Array doubled:", doubled)
