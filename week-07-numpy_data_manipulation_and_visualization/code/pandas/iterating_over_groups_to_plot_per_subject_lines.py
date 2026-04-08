"""Week 07 · pandas — Iterating over groups to plot per-subject lines

Extracted from: week-07-pandas_and_dataframes.md
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "subject":   ["P01", "P01", "P01", "P02", "P02", "P02"],
    "trial":     [1, 2, 3, 1, 2, 3],
    "condition": ["congruent", "incongruent", "congruent"] * 2,
    "rt_ms":     [320, 450, 360, 340, 470, 390],
    "correct":   [1, 1, 1, 1, 0, 1],
})

fig, ax = plt.subplots(figsize=(7, 4))

for subj, group in df.groupby("subject"):
    group_sorted = group.sort_values("trial")
    ax.plot(group_sorted["trial"], group_sorted["rt_ms"],
            label=subj, marker="o", markersize=4)

ax.set_xlabel("Trial")
ax.set_ylabel("RT (ms)")
ax.set_title("RT over trials by subject")
ax.legend()
plt.tight_layout()
plt.show()
