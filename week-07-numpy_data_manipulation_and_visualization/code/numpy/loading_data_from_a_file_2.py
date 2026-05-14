"""Week 07 · numpy — Loading Data via pandas then converting to NumPy

Extracted from: week-07-numpy_and_data_manipulation.md

Note: Uses io.StringIO to simulate a CSV file so this script runs
without any external files on disk.
"""

import io
import numpy as np
import pandas as pd

csv_data = "trial,rt_ms,correct\n1,320,1\n2,415,1\n3,280,1\n4,510,0\n5,390,1\n"

df = pd.read_csv(io.StringIO(csv_data))
rts = df["rt_ms"].to_numpy()   # extract one column as a NumPy array

print("DataFrame:\n", df)
print("\nrt_ms as NumPy array:", rts)
print("Mean RT:", rts.mean())
