"""Week 07 · matplotlib — Bar Plot

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import matplotlib.pyplot as plt

conditions = ["Congruent", "Incongruent"]
mean_rts   = [380, 460]
sem        = [15, 22]   # standard error of the mean

fig, ax = plt.subplots(figsize=(5, 4))
ax.bar(conditions, mean_rts, color=["#4C72B0", "#DD8452"],
       yerr=sem, capsize=5, width=0.5)
ax.set_ylabel("Mean RT (ms)")
ax.set_title("RT by condition")
ax.set_ylim(0, 550)
plt.tight_layout()
plt.show()
