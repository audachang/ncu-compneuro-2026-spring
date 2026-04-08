"""Week 07 · matplotlib — Line Plot

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
trials = np.arange(1, 51)
rts = np.random.normal(loc=400, scale=60, size=50)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(trials, rts, color="steelblue", linewidth=1.5, label="RT")
ax.axhline(rts.mean(), color="red", linestyle="--", label="Mean RT")
ax.set_xlabel("Trial number")
ax.set_ylabel("Reaction time (ms)")
ax.set_title("RT across trials")
ax.legend()
plt.tight_layout()
plt.show()
