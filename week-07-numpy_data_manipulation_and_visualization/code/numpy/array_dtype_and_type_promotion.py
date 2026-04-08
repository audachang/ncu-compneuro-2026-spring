"""Week 07 · numpy — Array dtype and Type Promotion

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

a = np.array([1, 2, 3])
b = np.array([1.0, 2.0, 3.0])
c = np.array([1, 2.0, 3])   # mixed types promote to float

print("int list  →", a.dtype)    # int64
print("float list→", b.dtype)    # float64
print("mixed list→", c.dtype)    # float64 (type promotion)

# Explicit dtype
d = np.array([1, 2, 3], dtype=float)
e = np.array([1, 2, 3], dtype=np.int32)
print("forced float →", d.dtype)
print("forced int32 →", e.dtype)
