"""Week 07 · matplotlib — Annotations and Saving

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
trials = np.arange(1, 51)
rts = np.random.normal(loc=400, scale=60, size=50)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(trials, rts, color="steelblue", linewidth=1.5)

# Annotate the slowest trial
ax.annotate(
    "Slowest trial",
    xy=(trials[rts.argmax()], rts.max()),
    xytext=(trials[rts.argmax()] - 10, rts.max() + 40),
    arrowprops=dict(arrowstyle="->", color="red", lw=1.5),
    fontsize=10, color="red", fontweight="bold",
)

ax.set_xlabel("Trial number")
ax.set_ylabel("RT (ms)")
ax.set_title("RT with annotation")
plt.tight_layout()

fig.savefig("summary_figure.png", dpi=150, bbox_inches="tight")
print("Saved summary_figure.png")

plt.show()
