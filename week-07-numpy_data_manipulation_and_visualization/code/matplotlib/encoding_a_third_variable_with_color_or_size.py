"""Week 07 · matplotlib — Encoding a Third Variable with Color or Size

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)
mean_rt  = rng.normal(400, 80, 20)
accuracy = rng.uniform(0.6, 1.0, 20)
n_trials = rng.integers(10, 60, 20)   # 3rd variable: number of trials

fig, ax = plt.subplots(figsize=(7, 5))
sc = ax.scatter(mean_rt, accuracy,
                c=n_trials,          # color encodes trial count
                cmap="viridis",
                s=60, alpha=0.8)
fig.colorbar(sc, ax=ax, label="Number of trials")
ax.set_xlabel("Mean RT (ms)")
ax.set_ylabel("Accuracy")
ax.set_title("Speed–accuracy by trial count")
plt.tight_layout()
plt.show()
