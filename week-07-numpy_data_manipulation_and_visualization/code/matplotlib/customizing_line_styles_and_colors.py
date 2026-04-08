"""Week 07 · matplotlib — Customizing Line Styles and Colors

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
x = np.arange(1, 11)
y = np.random.normal(400, 60, 10)

fig, axes = plt.subplots(2, 3, figsize=(12, 6))

# Color variants
axes[0, 0].plot(x, y, color="steelblue")
axes[0, 0].set_title("color='steelblue'")

axes[0, 1].plot(x, y, color="#4C72B0")
axes[0, 1].set_title("color='#4C72B0'")

axes[0, 2].plot(x, y, color=(0.2, 0.4, 0.8))
axes[0, 2].set_title("color=(R, G, B)")

# Line style variants
axes[1, 0].plot(x, y, linestyle="--")
axes[1, 0].set_title("linestyle='--'")

axes[1, 1].plot(x, y, marker="o", markersize=5)
axes[1, 1].set_title("marker='o'")

axes[1, 2].plot(x, y, "b--o")
axes[1, 2].set_title("shorthand 'b--o'")

plt.suptitle("Line style and color options", fontsize=13)
plt.tight_layout()
plt.show()
