"""Week 07 · matplotlib — Publication-Quality Figures

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
conditions = ["Congruent", "Incongruent", "Neutral"]
mean_rts   = [380, 460, 400]
sem        = [12, 18, 10]
colors     = ["#4C72B0", "#DD8452", "#55A868"]

# Use a professional style sheet
plt.style.use("seaborn-v0_8-whitegrid")

# Single-column figure (3.5 inches) — journal format
fig, ax = plt.subplots(figsize=(3.5, 2.8))
ax.bar(conditions, mean_rts, color=colors, yerr=sem, capsize=5,
       width=0.5, alpha=0.85, edgecolor="black", linewidth=0.8)
ax.set_ylabel("Mean RT (ms)")
ax.set_title("Stroop Task", fontsize=10)
ax.set_ylim(0, 550)
plt.tight_layout()

# Save in vector and raster formats
fig.savefig("results.pdf", dpi=300, bbox_inches="tight")
fig.savefig("results.svg", bbox_inches="tight")
print("Saved results.pdf and results.svg")

plt.show()

# Reset to default
plt.style.use("default")
