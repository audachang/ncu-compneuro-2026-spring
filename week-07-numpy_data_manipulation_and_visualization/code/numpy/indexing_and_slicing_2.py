"""Week 07 · numpy — Indexing and Slicing (2D)

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

data = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])

print("data[0, 1]   :", data[0, 1])     # 2       — row 0, col 1
print("data[1, :]   :", data[1, :])     # [4,5,6] — entire row 1
print("data[:, 2]   :", data[:, 2])     # [3,6,9] — entire column 2
print("data[0:2, 1:]:\n", data[0:2, 1:])  # [[2,3],[5,6]] — submatrix
