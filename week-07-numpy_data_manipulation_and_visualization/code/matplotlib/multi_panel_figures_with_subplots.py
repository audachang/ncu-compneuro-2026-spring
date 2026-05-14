"""Week 07 · matplotlib — Multi-panel Figures with subplots()

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
trials     = np.arange(1, 51)
rts        = np.random.normal(loc=400, scale=60, size=50)
mean_rt    = np.random.normal(400, 80, 20)
accuracy   = np.random.uniform(0.6, 1.0, 20)
conditions = ["Congruent", "Incongruent"]
mean_rts   = [380, 460]

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Top-left — line
axes[0, 0].plot(trials, rts, color="steelblue")
axes[0, 0].set_title("RT over trials")
axes[0, 0].set_xlabel("Trial")
axes[0, 0].set_ylabel("RT (ms)")

# Top-right — histogram
axes[0, 1].hist(rts, bins=15, color="steelblue", edgecolor="white")
axes[0, 1].set_title("RT distribution")
axes[0, 1].set_xlabel("RT (ms)")

# Bottom-left — bar
axes[1, 0].bar(conditions, mean_rts, color=["#4C72B0", "#DD8452"])
axes[1, 0].set_title("Mean RT by condition")
axes[1, 0].set_ylabel("Mean RT (ms)")

# Bottom-right — scatter
axes[1, 1].scatter(mean_rt, accuracy, color="coral", edgecolors="black")
axes[1, 1].set_title("Speed–accuracy")
axes[1, 1].set_xlabel("Mean RT (ms)")
axes[1, 1].set_ylabel("Accuracy")

plt.suptitle("Experiment Summary", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
