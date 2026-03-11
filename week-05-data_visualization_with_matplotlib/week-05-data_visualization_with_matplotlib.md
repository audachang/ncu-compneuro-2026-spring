# Week 05: Data Visualization with Matplotlib

> **Course:** NS5116 Computational Neuroscience — Spring 2026
> **Week:** 5 of 16 | **Date:** 2026-03-26 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Create line, scatter, bar, and histogram plots with Matplotlib
2. Customize axes labels, titles, and legends
3. Arrange multiple plots in a grid using `plt.subplots()`
4. Add reference lines and text annotations
5. Save figures to PNG or PDF with `plt.savefig()`
6. Choose the right plot type for a given type of data

---

## In-Class Topics

### 1. The Matplotlib Workflow (10 min)

Matplotlib follows a two-level model:

- **`plt` functions** — quick, stateless interface (fine for single plots)
- **`fig` and `ax` objects** — explicit control (use this for anything more than one panel)

```python
import matplotlib.pyplot as plt
import numpy as np

# Quick interface
plt.plot([1, 2, 3], [4, 5, 6])
plt.show()

# Object-oriented interface (recommended)
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
plt.show()
```

Always use the object-oriented interface when making multi-panel figures.

#### Real Python: Figure and Axes Architecture

A `Figure` is the entire canvas. An `Axes` is one individual plot within the canvas. A `Figure` can have one or many `Axes`.

The **object-oriented (OO) approach** is preferred for anything beyond a single quick plot. It makes multi-panel figures, loop-based figure generation, and saving to files much cleaner.

`plt.subplots()` is the recommended entry point — it creates a `Figure` and one or more `Axes` in one call:

```python
fig, ax = plt.subplots()              # 1 panel
fig, axes = plt.subplots(2, 3)        # 2 rows × 3 cols → axes[row, col]
fig, (ax1, ax2) = plt.subplots(1, 2)  # unpack directly
```

The stateful `plt.plot()` approach works for simple one-off plots in a notebook, but avoid it in scripts and functions — it is harder to predict which figure is "active".

📖 [Python Plotting With Matplotlib (Guide)](https://realpython.com/python-matplotlib-guide/)

---

### 2. Line Plot (15 min)

Useful for time series (e.g., RT across trials, EEG signal):

```python
import numpy as np
import matplotlib.pyplot as plt

trials = np.arange(1, 51)
rts = np.random.normal(loc=400, scale=60, size=50)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(trials, rts, color="steelblue", linewidth=1.5, label="RT")
ax.axhline(rts.mean(), color="red", linestyle="--", label="Mean RT")
ax.set_xlabel("Trial number")
ax.set_ylabel("Reaction time (ms)")
ax.set_title("RT across trials")
ax.legend()
plt.tight_layout()
plt.show()
```

#### Real Python: Customizing Line Styles and Colors

```python
# Color: named, hex, RGB tuple, grayscale string
ax.plot(x, y, color="steelblue")
ax.plot(x, y, color="#4C72B0")
ax.plot(x, y, color=(0.2, 0.4, 0.8))
ax.plot(x, y, color="0.5")   # 50% grey

# Line style
ax.plot(x, y, linestyle="--")   # dashed
ax.plot(x, y, linestyle=":")    # dotted
ax.plot(x, y, linestyle="-.")   # dash-dot

# Markers
ax.plot(x, y, marker="o", markersize=5)   # circles at each data point
ax.plot(x, y, marker="s")                 # squares

# Combined shorthand
ax.plot(x, y, "b--o")   # blue, dashed, with circle markers
```

📖 [Python Plotting With Matplotlib (Guide)](https://realpython.com/python-matplotlib-guide/)

---

### 3. Scatter Plot (15 min)

Useful for showing relationships between two variables:

```python
accuracy = np.random.uniform(0.6, 1.0, 20)
mean_rt  = np.random.normal(400, 80, 20)

fig, ax = plt.subplots()
ax.scatter(mean_rt, accuracy, color="coral", edgecolors="black", s=60, alpha=0.8)
ax.set_xlabel("Mean RT (ms)")
ax.set_ylabel("Accuracy")
ax.set_title("Speed–accuracy relationship")
plt.tight_layout()
plt.show()
```

`s` controls marker size; `alpha` controls transparency (0 = invisible, 1 = opaque).

#### Real Python: Encoding a Third Variable with Color or Size

Use the `c` parameter to color points by a third variable, making scatter plots show three dimensions at once:

```python
rng = np.random.default_rng(0)
mean_rt  = rng.normal(400, 80, 20)
accuracy = rng.uniform(0.6, 1.0, 20)
n_trials = rng.integers(10, 60, 20)   # 3rd variable: number of trials

sc = ax.scatter(mean_rt, accuracy,
                c=n_trials,          # color encodes trial count
                cmap="viridis",      # perceptually uniform colormap
                s=60, alpha=0.8)
fig.colorbar(sc, ax=ax, label="Number of trials")
```

Avoid using both `c` and `s` simultaneously to encode two variables — the figure becomes unreadable.

---

### 4. Bar Plot (15 min)

Useful for comparing means across conditions:

```python
conditions = ["Congruent", "Incongruent"]
mean_rts   = [380, 460]
sem        = [15, 22]   # standard error of the mean

fig, ax = plt.subplots(figsize=(5, 4))
bars = ax.bar(conditions, mean_rts, color=["#4C72B0", "#DD8452"],
              yerr=sem, capsize=5, width=0.5)
ax.set_ylabel("Mean RT (ms)")
ax.set_title("RT by condition")
ax.set_ylim(0, 550)
plt.tight_layout()
plt.show()
```

Error bars (`yerr`) show variability — always include them in scientific figures.

---

### 5. Histogram (15 min)

Useful for showing the distribution of a single variable:

```python
rts = np.random.normal(loc=400, scale=80, size=200)

fig, ax = plt.subplots()
ax.hist(rts, bins=20, color="steelblue", edgecolor="white", alpha=0.8)
ax.axvline(rts.mean(), color="red", linestyle="--", label=f"Mean = {rts.mean():.0f} ms")
ax.set_xlabel("RT (ms)")
ax.set_ylabel("Count")
ax.set_title("RT distribution")
ax.legend()
plt.tight_layout()
plt.show()
```

Choose `bins` based on your data size — typically 15–30 bins for 100–500 data points.

#### Real Python: Choosing Bins and Showing Density

- **Too few bins** → hides the shape of the distribution. **Too many bins** → noisy, shows sampling artifacts.
- `bins="auto"` lets matplotlib choose (uses Sturges' or Freedman-Diaconis rule). `bins=np.arange(100, 1000, 50)` gives exact bin edges.
- To compare two distributions on the same plot, use `alpha` and `density=True` (normalizes area to 1):

```python
fig, ax = plt.subplots()
ax.hist(rts_congruent,   bins=20, density=True, alpha=0.6, label="Congruent",   color="steelblue")
ax.hist(rts_incongruent, bins=20, density=True, alpha=0.6, label="Incongruent", color="coral")
ax.set_xlabel("RT (ms)")
ax.set_ylabel("Probability density")
ax.legend()
```

---

### 6. Multi-panel Figures with `subplots()` (20 min)

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Top-left — line
axes[0, 0].plot(trials, rts, color="steelblue")
axes[0, 0].set_title("RT over trials")

# Top-right — histogram
axes[0, 1].hist(rts, bins=15, color="steelblue", edgecolor="white")
axes[0, 1].set_title("RT distribution")

# Bottom-left — bar
axes[1, 0].bar(conditions, mean_rts, color=["#4C72B0", "#DD8452"])
axes[1, 0].set_title("Mean RT by condition")

# Bottom-right — scatter
axes[1, 1].scatter(mean_rt, accuracy, color="coral", edgecolors="black")
axes[1, 1].set_title("Speed–accuracy")

plt.suptitle("Experiment Summary", fontsize=14, fontweight="bold", y=1.01)
plt.tight_layout()
plt.show()
```

#### Real Python: Shared Axes and Figure-Level Labels

```python
# Share y-axis across columns so comparison is fair
fig, axes = plt.subplots(1, 2, figsize=(9, 4), sharey=True)

# Add a figure-level title above all panels
fig.suptitle("Posner Task Summary", fontsize=14, fontweight="bold")

# Add a single x-label spanning both panels
fig.supxlabel("Reaction time (ms)")

plt.tight_layout()
```

- `sharex=True` / `sharey=True` links axis limits across panels — essential for fair comparisons.
- `plt.tight_layout()` adjusts spacing automatically. If suptitle gets clipped, add `rect=[0, 0, 1, 0.95]`.

---

### 7. Annotations and Saving (10 min)

**Annotating a point:**
```python
ax.annotate(
    "Slowest trial",
    xy=(trials[rts.argmax()], rts.max()),
    xytext=(30, 550),
    arrowprops=dict(arrowstyle="->", color="black")
)
```

**Saving the figure:**
```python
fig.savefig("summary_figure.png", dpi=150, bbox_inches="tight")
fig.savefig("summary_figure.pdf", bbox_inches="tight")   # vector format for papers
```

Use `bbox_inches="tight"` to prevent labels from being cut off.

#### Real Python: Publication-Quality Figures

```python
# Use a style sheet for a cleaner look
plt.style.use("seaborn-v0_8-whitegrid")

# Vector format (PDF/SVG) for papers; PNG for slides
fig.savefig("results.pdf", dpi=300, bbox_inches="tight")
fig.savefig("results.svg", bbox_inches="tight")   # editable in Inkscape

# Set figure dimensions for a specific journal column width (e.g., 3.5 inches)
fig, ax = plt.subplots(figsize=(3.5, 2.8))   # single-column figure
```

- Always use `bbox_inches="tight"` to prevent labels from being cut off.
- Call `fig.savefig()` on the **Figure object**, not `plt.savefig()` — this guarantees you save the right figure.

📖 [Python Plotting With Matplotlib (Guide)](https://realpython.com/python-matplotlib-guide/)

---

## Choosing the Right Plot

| Data type | Recommended plot |
|-----------|-----------------|
| Variable over time / trials | Line plot |
| Relationship between two variables | Scatter plot |
| Mean comparison across groups | Bar plot with error bars |
| Distribution of one variable | Histogram |
| Multiple comparisons at once | Multi-panel figure |

---

## Neuroscience Connection

| Plot | Typical use in neuroscience |
|------|-----------------------------|
| Line | EEG/ERP time series, learning curves |
| Scatter | RT vs. accuracy, neural firing rate vs. stimulus intensity |
| Bar | Mean RT or accuracy by condition with SEM |
| Histogram | RT or signal amplitude distributions |
| Multi-panel | Publication figure summarizing an experiment |

---

## Tools This Week

- `matplotlib` — already installed (`pip install matplotlib` in Week 01)
- `numpy` — from Week 04

---

## Assignment

Create a new notebook `week-05-assignment.ipynb` and:

Key exercises:
- Plot RT over trials with a mean reference line
- Build a histogram of RT for each condition separately
- Create a 2×2 summary figure (line, histogram, bar, scatter) using `subplots()`
- Save the figure to PNG

Submit by pushing to your GitHub repository before Week 06.

---

## Resources

### Official Documentation
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)
- [Matplotlib Cheat Sheet](https://matplotlib.org/cheatsheets/)
- [Choosing a chart type](https://matplotlib.org/stable/gallery/index.html)
- [Scientific visualization best practices](https://www.nature.com/articles/s41551-021-00779-8)

### Real Python — Matplotlib Fundamentals
- [Python Plotting With Matplotlib (Guide)](https://realpython.com/python-matplotlib-guide/)

### Real Python — Plot Types & Customization
- [Matplotlib Scatter Plots: How to Visualize Relationships](https://realpython.com/mpl-scatter/)
- [Matplotlib Bar Charts: How to Visualize Categorical Data](https://realpython.com/mpl-bar-chart/)

### Real Python — Visualization Best Practices
- [Effective Data Visualization in Python](https://realpython.com/python-matplotlib-guide/)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 06 | PsychoPy basics — display stimuli in a window |
| 07 | PsychoPy experiment design — trial loops, data saving |
| 08 | **Midterm:** Deploy a full experiment to Pavlovia |
