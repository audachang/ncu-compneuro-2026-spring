# Week 06: NumPy & Data Manipulation

> **Course:** NS5116 Computational Neuroscience — Spring 2026
> **Week:** 6 of 16 | **Date:** 2026-04-02 | **Room:** TBA

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

#### arange vs linspace vs range

Understanding when to use each sequence-generation function is key:

- **`np.arange(start, stop, step)`**: Use when you know the **step size**. Like Python's `range()`, but for NumPy arrays. Returns integers by default; use `dtype=float` if you want floats.

  ```python
  np.arange(0, 10, 2)      # [0, 2, 4, 6, 8]
  np.arange(0, 1, 0.1)     # [0.0, 0.1, 0.2, ..., 0.9]
  ```
- **`np.linspace(start, stop, num)`**: Use when you know how many **points** you want, evenly spaced. Perfect for plotting.

  ```python
  np.linspace(0, 1, 5)     # exactly 5 points from 0 to 1
  # Output: [0.  , 0.25, 0.5 , 0.75, 1.  ]
  ```
- **Python `range()`**: Use for *integer-only* loops in `for` statements. Doesn't create a NumPy array.

  ```python
  for i in range(5):
      print(i)  # 0, 1, 2, 3, 4
  ```

In experiment code, use `np.linspace` when creating stimulus timings or axis labels, and `np.arange` for trial indexing.

#### Array dtype and Type Promotion

When you create an array, NumPy infers the **dtype** (data type):

```python
np.array([1, 2, 3])        # int64 (on most systems)
np.array([1.0, 2.0, 3.0])  # float64
np.array([1, 2.0, 3])      # float64 (mixed types promote to float)

# Explicit dtype
np.array([1, 2, 3], dtype=float)   # force float64
np.array([1, 2, 3], dtype=int32)   # force 32-bit int
```

**Why it matters:** If you mix integers and floats, NumPy silently converts everything to float, which uses more memory and might not be what you want.

#### zeros, ones, empty, and Initialization

- **`np.zeros(shape)`**: Initialize with zeros. Safe; always use if you're unsure.

  ```python
  np.zeros((3, 4))  # 3×4 matrix of zeros
  ```
- **`np.ones(shape)`**: Initialize with ones.

  ```python
  np.ones(5)        # [1., 1., 1., 1., 1.]
  ```
- **`np.empty(shape)`**: Allocate memory but don't initialize. *Faster* because it skips the initialization step, but contains garbage values. Only use when you will immediately fill every element:

  ```python
  output = np.empty(1000)
  for i in range(1000):
      output[i] = compute(i)  # fills immediately
  ```

  **Never read from `np.empty` without filling it first!**

📖 [NumPy Array Creation](https://numpy.org/doc/stable/reference/routines.array-creation.html) · [NumPy arange: How to Use np.arange()](https://realpython.com/how-to-use-numpy-arange/)

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

#### Broadcasting — Operating on Different Shapes

NumPy's **broadcasting** allows operations between arrays of different shapes, as long as they are compatible. This eliminates the need for loops:

```python
rts = np.array([[320, 415, 280],    # subject 1: 3 trials
                [390, 425, 310]])    # subject 2: 3 trials
                # shape: (2, 3)

baseline = np.array([350, 400, 290])  # per-trial baseline
                # shape: (3,)

# Broadcasting: baseline stretches to match rts rows
centered = rts - baseline
# Equivalent to:
# centered[0] = [320-350, 415-400, 280-290] = [-30, 15, -10]
# centered[1] = [390-350, 425-400, 310-290] = [40, 25, 20]
```

**Broadcasting rules** (compared from right to left):

- If arrays have different numbers of dimensions, pad the smaller with ones on the left.
- Dimensions are compatible if they are equal *or* one of them is 1 (the size-1 dimension stretches).

```python
# shape (2, 3) minus shape (3,) broadcasts as:
# (2, 3) minus (1, 3) after padding → (2, 3) minus (2, 3)
```

#### Universal Functions (ufuncs) — Vectorized Operations

NumPy's **ufuncs** (universal functions) are compiled C implementations that operate element-wise. They're *much* faster than Python loops:

```python
# Instead of:
result = []
for rt in rts:
    result.append(np.log(rt))

# Use the ufunc (compiled, fast):
result = np.log(rts)
```

Common ufuncs:

- Arithmetic: `np.add`, `np.subtract`, `np.multiply`, `np.divide`
- Math: `np.log`, `np.exp`, `np.sqrt`, `np.abs`, `np.sin`, `np.cos`
- Comparison: `np.less`, `np.greater`, `np.equal`

Ufuncs also support **output arrays** to avoid allocating new memory:

```python
output = np.empty_like(rts)
np.log(rts, out=output)  # result stored in output, no new allocation
```

📖 [NumPy Array Programming](https://realpython.com/numpy-array-programming/) · [NumPy Ufuncs](https://numpy.org/doc/stable/reference/ufuncs.html)

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

#### np.where — Vectorized if/else

`np.where(condition, value_if_true, value_if_false)` is a vectorized version of `if/else` that returns values based on a condition:

```python
rts = np.array([320, 415, 280, 510, 390])
labels = np.where(rts > 400, "slow", "fast")
# Output: array(['fast', 'slow', 'fast', 'slow', 'fast'], dtype='<U4')

# You can also use arrays as the values:
rts_categorized = np.where(rts > 400, "outlier", "normal")

# Or perform different computations:
rts_adjusted = np.where(rts > 1000, rts - 100, rts)  # subtract 100 from slow RTs
```

#### argmax, argmin — Finding Indices

`np.argmax()` and `np.argmin()` return the **index** (not the value) of the maximum or minimum:

```python
rts = np.array([320, 415, 280, 510, 390])

slowest_trial = rts.argmax()    # 3 (index of 510)
rts[slowest_trial]              # 510

fastest_trial = rts.argmin()    # 2 (index of 280)
rts[fastest_trial]              # 280

# Useful for finding the outlier:
outlier_idx = np.argmax(np.abs(rts - rts.mean()))  # furthest from mean
```

#### Fancy Indexing — Selecting by Indices

Index with an integer array to select multiple elements:

```python
indices = np.array([0, 2, 4])
rts[indices]                    # [320, 280, 390] — trials 0, 2, 4

# Useful for reordering:
sorted_indices = np.argsort(rts)  # indices that would sort the array
sorted_rts = rts[sorted_indices]
```

📖 [NumPy Boolean Indexing and Masking](https://numpy.org/doc/stable/user/basics.indexing.html#boolean-indexing-through-a-mask) · [NumPy where()](https://numpy.org/doc/stable/reference/generated/numpy.where.html)

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

#### np.random — Seeding and Modern RNG

NumPy's random number generation has two interfaces:

**Old API (still works but less thread-safe):**

```python
np.random.seed(42)
rts = np.random.normal(loc=400, scale=80, size=100)
```

**New API (recommended for reproducibility and thread-safety):**

```python
rng = np.random.default_rng(42)
rts = rng.normal(loc=400, scale=80, size=100)
```

The new API returns a **Generator** object with the same methods, so the code looks the same but is more robust.

#### percentile vs quantile

Both do the same thing but with different conventions:

- **`np.percentile(a, q)`**: `q` is in range 0–100
- **`np.quantile(a, q)`**: `q` is in range 0–1

```python
rts = np.array([320, 415, 280, 510, 390])

np.percentile(rts, 50)   # median (50th percentile)
np.quantile(rts, 0.5)    # same (0.5 quantile)

# Both are equivalent:
np.percentile(rts, [25, 50, 75])  # quartiles in percentile form
np.quantile(rts, [0.25, 0.5, 0.75])  # quartiles in quantile form
```

Use whichever mental model matches your field (psychology/neuroscience often uses percentiles, statistics often uses quantiles).

📖 [NumPy Statistics Functions](https://numpy.org/doc/stable/reference/routines.statistics.html) · [NumPy Random Number Generator](https://realpython.com/numpy-random-number-generator/)

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

| NumPy feature          | Experiment analysis use                          |
| ---------------------- | ------------------------------------------------ |
| Boolean masking        | Remove invalid trials (RT < 100 ms or > 1500 ms) |
| `mean()`, `std()`  | Summarize accuracy and RT per condition          |
| `axis=1` aggregation | Compute per-subject or per-block statistics      |
| `np.random.normal()` | Simulate data to test analysis pipelines         |
| z-score                | Normalize RTs for comparison across subjects     |

---

## Tools This Week

- `numpy` — install already done in Week 01 (`pip install numpy`)
- `pandas` — preview only; full coverage in Week 12

---

## Assignment

Review [`lpthw_ex40-45.ipynb`](lpthw_ex40-45.ipynb) for OOP background (NumPy arrays are objects too).

Then create a new notebook `week-06-assignment.ipynb` and:

Key exercises:

- Create and inspect arrays of simulated reaction time data
- Apply z-score normalization using vectorized operations
- Use boolean masking to remove outlier trials
- Compute per-condition mean and standard deviation on a 2D array

Submit by pushing to your GitHub repository before Week 07.

---

## Resources

### Official Documentation

- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy Indexing](https://numpy.org/doc/stable/user/basics.indexing.html)
- [NumPy for MATLAB users](https://numpy.org/doc/stable/user/numpy-for-matlab-users.html)

### Real Python — Array Creation & Indexing

- [NumPy arange: How to Use np.arange()](https://realpython.com/how-to-use-numpy-arange/)

### Real Python — Vectorization & Operations

- [Array Programming with NumPy](https://realpython.com/numpy-array-programming/)
- [NumPy Array Example: From Basic to Advanced](https://realpython.com/numpy-example/)

### Real Python — Random Numbers

- [NumPy Random Number Generator](https://realpython.com/numpy-random-number-generator/)

---

## What Comes Next

| Week | Topic                                                                      |
| ---- | -------------------------------------------------------------------------- |
| 07   | Matplotlib — plot the distributions and statistics you computed this week |
| 08   | **Midterm:** Deploy a full experiment to Pavlovia                    |
| 12   | pandas — tabular data with column names (builds on NumPy)                 |
