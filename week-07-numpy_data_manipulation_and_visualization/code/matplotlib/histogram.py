"""Week 07 · matplotlib — Histogram

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
rts = np.random.normal(loc=400, scale=80, size=200)

fig, ax = plt.subplots()
ax.hist(rts, bins=20, color="steelblue", edgecolor="white", alpha=0.8)
ax.axvline(rts.mean(), color="red", linestyle="--", label=f"Mean = {rts.mean():.0f} ms")
ax.set_xlabel("RT (ms)")
ax.set_ylabel("Count")
ax.set_title("RT distribution")
ax.legend()
plt.tight_layout()
plt.show()
