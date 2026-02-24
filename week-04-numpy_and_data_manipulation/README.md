# Week 04: NumPy & Data Manipulation

> **Course:** NS5116 Computational Neuroscience — Spring 2026
> **Week:** 4 of 16 | **Date:** 2026-03-19 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Create NumPy arrays from lists and with built-in constructors
2. Inspect array shape, dtype, and number of dimensions
3. Index and slice 1D and 2D arrays
4. Apply vectorized arithmetic without writing explicit loops
5. Use boolean masking to filter data
6. Compute descriptive statistics (mean, std, min, max, median)
7. Load a CSV file into a NumPy array with `np.loadtxt()`

---

## Why NumPy?

Pure Python lists are flexible but slow for numerical computation.
NumPy stores data in contiguous memory blocks and applies operations
to entire arrays at once — no Python `for` loop required.

```python
import numpy as np

# Python list — slow for large data
rts_list = [320, 415, 280, 510, 390]
doubled = [rt * 2 for rt in rts_list]   # loop needed

# NumPy array — fast, no loop needed
rts = np.array([320, 415, 280, 510, 390])
doubled = rts * 2   # vectorized — operates on all elements at once
```

For 10,000 trials, NumPy is typically 50–100× faster than a Python loop.

---

## In-Class Topics

### 1. Creating Arrays (20 min)

```python
import numpy as np

# From a list
rts = np.array([320, 415, 280, 510, 390])

# Sequences
np.zeros(5)              # [0. 0. 0. 0. 0.]
np.ones((3, 4))          # 3×4 matrix of ones
np.arange(0, 10, 2)      # [0 2 4 6 8]  (start, stop, step)
np.linspace(0, 1, 5)     # [0.   0.25  0.5   0.75  1. ]  (5 evenly spaced points)

# Random data (useful for simulations)
np.random.seed(42)
rts_sim = np.random.normal(loc=400, scale=80, size=100)  # 100 simulated RTs
```

---

### 2. Array Properties (10 min)

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])

a.shape    # (2, 3)  — 2 rows, 3 columns
a.ndim     # 2       — number of dimensions
a.dtype    # int64   — data type
a.size     # 6       — total number of elements
```

---

### 3. Indexing and Slicing (20 min)

**1D arrays — same as lists:**
```python
rts = np.array([320, 415, 280, 510, 390])
rts[0]      # 320
rts[-1]     # 390
rts[1:4]    # [415, 280, 510]
```

**2D arrays — `[row, col]`:**
```python
data = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])

data[0, 1]    # 2       — row 0, col 1
data[1, :]    # [4,5,6] — entire row 1
data[:, 2]    # [3,6,9] — entire column 2
data[0:2, 1:] # [[2,3],[5,6]]  — submatrix
```

---

### 4. Vectorized Operations (15 min)

```python
rts = np.array([320, 415, 280, 510, 390])

# Arithmetic applied element-wise
rts_sec = rts / 1000          # convert ms → seconds
rts_z = (rts - rts.mean()) / rts.std()  # z-score

# Comparison (returns boolean array)
rts > 400   # [False, True, False, True, False]

# Mathematical functions
np.log(rts)
np.sqrt(rts)
np.abs(rts - 400)
```

---

### 5. Boolean Masking (20 min)

Boolean masking lets you filter data without loops:

```python
rts = np.array([320, 415, 280, 510, 390])

mask = rts > 400          # [False, True, False, True, False]
rts[mask]                 # [415, 510]  — only values where mask is True

# Shorthand — combine in one step
fast = rts[rts < 350]     # [320, 280]

# Multiple conditions
valid = rts[(rts >= 150) & (rts <= 900)]
```

**Outlier removal:**
```python
mean = rts.mean()
std  = rts.std()
clean = rts[np.abs(rts - mean) < 2.5 * std]   # remove values > 2.5 SD from mean
```

---

### 6. Descriptive Statistics (10 min)

```python
rts = np.array([320, 415, 280, 510, 390])

rts.mean()      # mean
rts.std()       # standard deviation
rts.min()       # minimum
rts.max()       # maximum
np.median(rts)  # median
np.percentile(rts, [25, 75])  # quartiles
```

**2D aggregation — compute per row or per column:**
```python
# Shape (3 subjects × 10 trials)
data = np.random.normal(400, 80, size=(3, 10))

data.mean(axis=1)   # mean RT per subject (3 values)
data.mean(axis=0)   # mean RT per trial position (10 values)
```

---

### 7. Loading Data from a File (15 min)

```python
# Load a single-column text file of reaction times
rts = np.loadtxt("rts.txt")

# Load a CSV (skip header row, use comma delimiter)
data = np.loadtxt("results.csv", delimiter=",", skiprows=1)
```

For more complex CSVs (with string columns), use pandas:
```python
import pandas as pd
df = pd.read_csv("results.csv")
rts = df["rt_ms"].to_numpy()   # extract one column as a NumPy array
```

---

## Neuroscience Connection

| NumPy feature | Experiment analysis use |
|--------------|------------------------|
| Boolean masking | Remove invalid trials (RT < 100 ms or > 1500 ms) |
| `mean()`, `std()` | Summarize accuracy and RT per condition |
| `axis=1` aggregation | Compute per-subject or per-block statistics |
| `np.random.normal()` | Simulate data to test analysis pipelines |
| z-score | Normalize RTs for comparison across subjects |

---

## Tools This Week

- `numpy` — install already done in Week 01 (`pip install numpy`)
- `pandas` — preview only; full coverage in Week 12

---

## Assignment

Complete `week-04-starter.ipynb`. Fill in every cell marked `# YOUR CODE HERE`.

Key exercises:
- Create and inspect arrays of simulated reaction time data
- Apply z-score normalization using vectorized operations
- Use boolean masking to remove outlier trials
- Compute per-condition mean and standard deviation on a 2D array

Submit by pushing to your GitHub repository before Week 05.

---

## Resources

- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy Indexing](https://numpy.org/doc/stable/user/basics.indexing.html)
- [NumPy for MATLAB users](https://numpy.org/doc/stable/user/numpy-for-matlab-users.html)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 05 | Matplotlib — plot the distributions and statistics you computed this week |
| 06 | PsychoPy — `numpy` is used internally by PsychoPy for timing |
| 12 | pandas — tabular data with column names (builds on NumPy) |
