"""Week 07 · pandas — From Pandas to Matplotlib

Extracted from: week-07-pandas_and_dataframes.md
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "subject":   ["P01", "P01", "P02", "P02"],
    "condition": ["congruent", "incongruent", "congruent", "incongruent"],
    "rt_ms":     [320, 450, 340, 470],
    "correct":   [1, 1, 1, 0],
})

# Bar chart from groupby
#means = df[df["correct"] == 1].groupby("condition")["rt_ms"].mean()
#sems  = df[df["correct"] == 1].groupby("condition")["rt_ms"].sem()

means = df.groupby("condition")["rt_ms"].mean()
sems  = df.groupby("condition")["rt_ms"].sem()


fig, ax = plt.subplots(figsize=(5, 4))
ax.bar(means.index, means.values,
       yerr=sems.values, capsize=5,
       color=["#4C72B0", "#DD8452"], edgecolor="black", alpha=0.85)
#df.boxplot(column = df["rt_ms"], by= df["condition"])
#ax.boxplot(df.groupby('condition')["rt_ms"], labels=df['condition'].unique())
ax.set_ylabel("Mean RT (ms)")
ax.set_title("Stroop Effect")
ax.set_ylim(0, max(means) * 1.5)
plt.tight_layout()
plt.show()
