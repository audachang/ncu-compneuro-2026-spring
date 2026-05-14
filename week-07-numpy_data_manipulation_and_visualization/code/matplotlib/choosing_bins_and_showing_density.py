"""Week 07 · matplotlib — Choosing Bins and Showing Density

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
rts_congruent   = np.random.normal(380, 60, 100)
rts_incongruent = np.random.normal(460, 80, 100)

fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(rts_congruent,   bins=20, density=True, alpha=0.6, label="Congruent",   color="steelblue")
ax.hist(rts_incongruent, bins=20, density=True, alpha=0.6, label="Incongruent", color="coral")
ax.set_xlabel("RT (ms)")
ax.set_ylabel("Probability density")
ax.set_title("Overlapping histograms (density=True)")
ax.legend()
plt.tight_layout()
plt.show()
