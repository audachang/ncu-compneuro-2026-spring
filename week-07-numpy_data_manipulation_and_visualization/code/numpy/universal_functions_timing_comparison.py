"""Week 07 · numpy — Ufunc Speed Comparison vs Python Loop

Extracted from: week-07-numpy_and_data_manipulation.md

Demonstrates the speedup of np.log (ufunc) over a Python list comprehension
using timeit for a fair, repeated measurement.
"""

import numpy as np
import timeit

rng = np.random.default_rng(42)
rts = rng.normal(400, 80, size=100_000)

# Python list comprehension — calls np.log one element at a time
loop_time  = timeit.timeit(lambda: [np.log(rt) for rt in rts], number=10) / 10

# NumPy ufunc — operates on the whole array in compiled C
ufunc_time = timeit.timeit(lambda: np.log(rts), number=10) / 10

print(f"Array size : {len(rts):,} elements")
print(f"Loop       : {loop_time * 1000:.1f} ms")
print(f"Ufunc      : {ufunc_time * 1000:.2f} ms")
print(f"Speedup    : {loop_time / ufunc_time:.0f}×")
# Typical output on a modern laptop:
#   Loop       : ~90 ms
#   Ufunc      : ~0.4 ms
#   Speedup    : ~200×
