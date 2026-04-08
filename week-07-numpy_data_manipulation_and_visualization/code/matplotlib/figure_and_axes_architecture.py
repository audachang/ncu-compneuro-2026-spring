"""Week 07 · matplotlib — Figure and Axes Architecture

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)
x = np.arange(1, 6)
y = rng.normal(400, 60, 5)

# 1 panel
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("1 panel")
plt.tight_layout()
plt.show()

# 2 rows × 3 cols → axes[row, col]
fig, axes = plt.subplots(2, 3, figsize=(9, 5))
for i, ax in enumerate(axes.flat):
    ax.set_title(f"Panel {i}")
fig.suptitle("2×3 grid")
plt.tight_layout()
plt.show()

# Unpack directly into two named axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
ax1.set_title("ax1")
ax2.set_title("ax2")
plt.tight_layout()
plt.show()
