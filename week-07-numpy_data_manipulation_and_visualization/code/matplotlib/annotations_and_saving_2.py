"""Week 07 · matplotlib — Saving to multiple formats

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
mean_rt  = np.random.normal(400, 80, 20)
accuracy = np.random.uniform(0.6, 1.0, 20)

fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(mean_rt, accuracy, color="coral", edgecolors="black", s=80)
ax.set_xlabel("Mean RT (ms)")
ax.set_ylabel("Accuracy")
ax.set_title("Speed–Accuracy Relationship")
plt.tight_layout()

fig.savefig("summary_figure.png", dpi=150, bbox_inches="tight")
fig.savefig("summary_figure.pdf", bbox_inches="tight")   # vector format for papers

import os
print(f"PNG: {os.path.getsize('summary_figure.png'):,} bytes")
print(f"PDF: {os.path.getsize('summary_figure.pdf'):,} bytes")

plt.show()
