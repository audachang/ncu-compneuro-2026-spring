"""Week 07 · matplotlib — Shared Axes and Figure-Level Labels

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
rts_congruent   = np.random.normal(380, 60, 100)
rts_incongruent = np.random.normal(460, 80, 100)

# sharey=True links y-axis limits so comparison is fair
fig, axes = plt.subplots(1, 2, figsize=(9, 4), sharey=True)

axes[0].hist(rts_congruent, bins=20, color="steelblue", edgecolor="white")
axes[0].set_xlabel("Reaction time (ms)")
axes[0].set_ylabel("Count")
axes[0].set_title("Congruent")

axes[1].hist(rts_incongruent, bins=20, color="coral", edgecolor="white")
axes[1].set_xlabel("Reaction time (ms)")
axes[1].set_title("Incongruent")

# Figure-level title and shared x-label
fig.suptitle("Posner Task Summary", fontsize=14, fontweight="bold")
fig.supxlabel("Reaction time (ms)")

plt.tight_layout()
plt.show()
