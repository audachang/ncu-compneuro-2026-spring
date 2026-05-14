"""Week 07 · numpy — Loading Data from a File

Extracted from: week-07-numpy_and_data_manipulation.md

Note: Uses io.StringIO to simulate a file so this script runs without
any external files on disk.
"""

import io
import numpy as np

# Simulate a text file of reaction times
txt_data = "320\n415\n280\n510\n390\n"
rts = np.loadtxt(io.StringIO(txt_data))
print("Loaded RTs:", rts)

# Simulate a CSV with a header row
csv_data = "trial,rt_ms\n1,320\n2,415\n3,280\n4,510\n5,390\n"
data = np.loadtxt(io.StringIO(csv_data), delimiter=",", skiprows=1)
print("CSV rt_ms column:", data[:, 1])
