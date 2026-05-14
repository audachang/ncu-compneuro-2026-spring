"""Week 07 · numpy — Array Properties

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

a = np.array([[1, 2, 3],
              [4, 5, 6]])

print("shape:", a.shape)   # (2, 3)  — 2 rows, 3 columns
print("ndim: ", a.ndim)    # 2       — number of dimensions
print("dtype:", a.dtype)   # int64   — data type
print("size: ", a.size)    # 6       — total number of elements
