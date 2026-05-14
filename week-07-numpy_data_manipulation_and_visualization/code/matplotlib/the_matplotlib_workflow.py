"""Week 07 · matplotlib — The Matplotlib Workflow

Extracted from: week-07-data_visualization_with_matplotlib.md
"""

import matplotlib.pyplot as plt
import numpy as np

# Quick (stateless) interface
plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Quick interface")
plt.show()

# Object-oriented interface (recommended)
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_title("Object-oriented interface")
plt.show()
