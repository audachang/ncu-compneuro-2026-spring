"""Week 07 · matplotlib — Scatter Plot

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
accuracy = np.random.uniform(0.6, 1.0, 20)
mean_rt  = np.random.normal(400, 80, 20)

fig, ax = plt.subplots()
ax.scatter(mean_rt, accuracy, color="coral", edgecolors="black", s=60, alpha=0.8)
ax.set_xlabel("Mean RT (ms)")
ax.set_ylabel("Accuracy")
ax.set_title("Speed–accuracy relationship")
plt.tight_layout()
plt.show()
