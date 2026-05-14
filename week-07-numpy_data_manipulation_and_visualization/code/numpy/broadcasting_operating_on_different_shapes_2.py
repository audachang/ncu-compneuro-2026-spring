"""Week 07 · numpy — Broadcasting Shape Rules

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

# shape (2, 3) minus shape (3,):
# NumPy pads (3,) → (1, 3) → stretches to (2, 3)
a = np.ones((2, 3))
b = np.array([10, 20, 30])   # shape (3,)
result = a + b
print("a shape:", a.shape)
print("b shape:", b.shape)
print("(a + b) shape:", result.shape)
print("result:\n", result)
