# Week 07: Pandas & DataFrames

> **Course:** NS5116 Computational Neuroscience — Spring 2026
> **Week:** 7 of 16 | **Date:** 2026-04-09 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Create a pandas DataFrame from a Python dictionary
2. Select rows and columns using `.loc`, `.iloc`, and boolean filters
3. Add derived columns with vectorized expressions
4. Summarize data by group using `groupby` and aggregate functions
5. Reshape data with `pivot_table`
6. Read and write CSV files with `pd.read_csv` and `df.to_csv`
7. Pass pandas results directly to Matplotlib for publication figures

---

## Why Pandas?

NumPy is fast but indexing is positional — you must remember that column 2 is RT and column 3 is accuracy.
Pandas stores data in a **DataFrame**: a table with named columns and labeled rows, like a spreadsheet in Python.

*📄 [`why_pandas.py`](code/pandas/why_pandas.py)*
```python
import numpy as np
import pandas as pd

# NumPy — positional, easy to lose track
data = np.array([[1, 320, 1],
                 [2, 450, 0]])
rt = data[:, 1]   # what is column 1? need to remember

# Pandas — self-documenting
df = pd.DataFrame(data, columns=["trial", "rt_ms", "correct"])
rt = df["rt_ms"]  # clear immediately
```

For behavioral experiments with multiple subjects, conditions, and measures, labeled columns are far less error-prone.

---

## In-Class Topics

### 1. Creating DataFrames (15 min)

The most common way in experiment code is from a Python dictionary:

*📄 [`creating_dataframes.py`](code/pandas/creating_dataframes.py)*
```python
import pandas as pd

df = pd.DataFrame({
    "subject":   ["P01", "P01", "P02", "P02"],
    "condition": ["congruent", "incongruent", "congruent", "incongruent"],
    "rt_ms":     [320, 450, 340, 470],
    "correct":   [1, 1, 1, 0],
})

print(df)
print(df.shape)   # (4, 4)
print(df.dtypes)
```

You can also create a DataFrame row-by-row (useful when building trial lists in a loop):

*📄 [`creating_dataframes_2.py`](code/pandas/creating_dataframes_2.py)*
```python
rows = []
for trial in range(1, 5):
    rows.append({"trial": trial, "rt_ms": 300 + trial * 20})

df = pd.DataFrame(rows)
```

#### Key DataFrame Attributes

| Attribute | Description |
| --------- | ----------- |
| `df.shape` | Tuple `(rows, columns)` |
| `df.dtypes` | Data type of each column |
| `df.columns` | Column names as an Index |
| `df.index` | Row labels (integer by default) |
| `df.head(n)` | First n rows (default 5) |
| `df.tail(n)` | Last n rows |
| `df.info()` | Shape, dtypes, memory use |
| `df.describe()` | Descriptive stats for numeric columns |

---

### 2. Selecting Data (20 min)

#### Column selection

*📄 [`column_selection.py`](code/pandas/column_selection.py)*
```python
# Single column → Series (1D)
df["rt_ms"]

# Multiple columns → DataFrame (2D)
df[["subject", "rt_ms"]]
```

#### Row selection with `.loc` (label-based) and `.iloc` (position-based)

*📄 [`row_selection_with_loc_label_based_and_iloc_position_based.py`](code/pandas/row_selection_with_loc_label_based_and_iloc_position_based.py)*
```python
# loc: label-based — use with index labels or boolean arrays
df.loc[0]          # first row by index label
df.loc[0:2]        # rows with index labels 0, 1, 2 (inclusive)

# iloc: position-based — always uses integer offsets
df.iloc[0]         # first row
df.iloc[0:2]       # rows 0 and 1 (exclusive upper bound)
df.iloc[0, 2]      # row 0, column 2
```

#### Boolean filtering (most common in practice)

*📄 [`boolean_filtering_most_common_in_practice.py`](code/pandas/boolean_filtering_most_common_in_practice.py)*
```python
# Keep only correct trials
df_correct = df[df["correct"] == 1]

# Keep only fast correct trials (no explicit mask variable needed)
df_fast = df[(df["correct"] == 1) & (df["rt_ms"] < 400)]

# Keep only P01's trials
df_p01 = df[df["subject"] == "P01"]
```

Use `&` (AND) and `|` (OR) — **not** Python's `and`/`or` — when combining conditions. Wrap each condition in parentheses.

---

### 3. Adding and Modifying Columns (10 min)

*📄 [`adding_and_modifying_columns.py`](code/pandas/adding_and_modifying_columns.py)*
```python
# Derived column — vectorized, no loop required
df["rt_sec"] = df["rt_ms"] / 1000

# Label each trial as fast or slow relative to the median
median_rt = df["rt_ms"].median()
df["speed"] = df["rt_ms"].apply(lambda rt: "fast" if rt < median_rt else "slow")

# Or equivalently with np.where (faster for large DataFrames)
import numpy as np
df["speed"] = np.where(df["rt_ms"] < median_rt, "fast", "slow")
```

#### apply — execute a custom function per row or per column

*📄 [`apply_execute_a_custom_function_per_row_or_per_column.py`](code/pandas/apply_execute_a_custom_function_per_row_or_per_column.py)*
```python
# Per-element transformation using a function
def classify_rt(rt):
    if rt < 300:
        return "very fast"
    elif rt < 500:
        return "normal"
    else:
        return "slow"

df["rt_class"] = df["rt_ms"].apply(classify_rt)
```

Use `apply` when the logic is too complex for a one-liner; otherwise prefer vectorized expressions (faster).

---

### 4. Groupby and Aggregation (20 min)

`groupby` splits the DataFrame by one or more columns, then applies an aggregate function to each group.

*📄 [`groupby_and_aggregation.py`](code/pandas/groupby_and_aggregation.py)*
```python
# Mean RT per condition
df.groupby("condition")["rt_ms"].mean()

# Multiple stats at once
df.groupby("condition")["rt_ms"].agg(["mean", "std", "count"])

# Group by two variables
df.groupby(["subject", "condition"])["rt_ms"].mean()
```

#### Common aggregate functions

| Function | Meaning |
| -------- | ------- |
| `.mean()` | Average |
| `.std()` | Standard deviation |
| `.sem()` | Standard error of the mean |
| `.median()` | Median |
| `.count()` | Number of non-null rows |
| `.sum()` | Sum |
| `.min()`, `.max()` | Extremes |

#### Correct-trial accuracy pattern

*📄 [`correct_trial_accuracy_pattern.py`](code/pandas/correct_trial_accuracy_pattern.py)*
```python
# Proportion correct per condition (mean of 0/1 column = proportion)
df.groupby("condition")["correct"].mean()
```

---

### 5. Pivot Tables (10 min)

`pivot_table` reshapes long-format data (one row per trial) into wide format (conditions as columns).

*📄 [`pivot_tables.py`](code/pandas/pivot_tables.py)*
```python
# Mean RT: subjects as rows, conditions as columns
summary = pd.pivot_table(
    df,
    values="rt_ms",
    index="subject",
    columns="condition",
    aggfunc="mean",
)
print(summary)
```

The result is a standard DataFrame — you can subtract columns directly to compute interference costs:

*📄 [`pivot_tables_2.py`](code/pandas/pivot_tables_2.py)*
```python
summary["interference_cost"] = summary["incongruent"] - summary["congruent"]
```

---

### 6. Reading and Writing CSV (10 min)

*📄 [`reading_and_writing_csv.py`](code/pandas/reading_and_writing_csv.py)*
```python
# Write — index=False avoids saving the row numbers as a column
df.to_csv("stroop_results.csv", index=False)

# Read
df_loaded = pd.read_csv("stroop_results.csv")
```

#### Common `read_csv` options

| Parameter | Purpose |
| --------- | ------- |
| `sep=","` | Column separator (default comma) |
| `header=0` | Row to use as column names |
| `skiprows=n` | Skip first n rows |
| `usecols=[...]` | Load only specific columns |
| `dtype={"rt_ms": float}` | Force column dtypes |
| `na_values=["NA", "n/a"]` | Treat these strings as NaN |

After loading, always check:

*📄 [`common_read_csv_options.py`](code/pandas/common_read_csv_options.py)*
```python
df_loaded.info()        # dtypes and non-null counts
df_loaded.describe()    # numeric summaries
df_loaded.isna().sum()  # count missing values per column
```

---

### 7. From Pandas to Matplotlib (15 min)

pandas Series and numpy arrays can be passed directly to matplotlib functions.

*📄 [`from_pandas_to_matplotlib.py`](code/pandas/from_pandas_to_matplotlib.py)*
```python
import matplotlib.pyplot as plt

# Bar chart from groupby
means = df[df["correct"] == 1].groupby("condition")["rt_ms"].mean()
sems  = df[df["correct"] == 1].groupby("condition")["rt_ms"].sem()

fig, ax = plt.subplots(figsize=(5, 4))
ax.bar(means.index, means.values,
       yerr=sems.values, capsize=5,
       color=["#4C72B0", "#DD8452"], edgecolor="black", alpha=0.85)
ax.set_ylabel("Mean RT (ms)")
ax.set_title("Stroop Effect")
ax.set_ylim(0, max(means) * 1.5)
plt.tight_layout()
plt.show()
```

#### Iterating over groups to plot per-subject lines

*📄 [`iterating_over_groups_to_plot_per_subject_lines.py`](code/pandas/iterating_over_groups_to_plot_per_subject_lines.py)*
```python
fig, ax = plt.subplots(figsize=(7, 4))

for subj, group in df.groupby("subject"):
    group_sorted = group.sort_values("trial")
    ax.plot(group_sorted["trial"], group_sorted["rt_ms"], label=subj, marker="o", markersize=4)

ax.set_xlabel("Trial")
ax.set_ylabel("RT (ms)")
ax.set_title("RT over trials by subject")
ax.legend()
plt.tight_layout()
plt.show()
```

---

## Choosing the Right Tool

| Task | Tool |
| ---- | ---- |
| Fast numeric computation, z-scores, masking | **NumPy** |
| Labeled columns, groupby, CSV I/O | **Pandas** |
| Figures and plots | **Matplotlib** |
| Convert between them | `df["col"].to_numpy()` / `pd.Series(arr)` |

---

## Neuroscience Connection

| Pandas feature | Experiment analysis use |
| -------------- | ----------------------- |
| `groupby` + `mean()` | Mean RT / accuracy per condition and subject |
| `groupby` + `sem()` | Error bars for bar charts |
| `pivot_table` | Interference cost (incongruent − congruent) |
| Boolean filter | Remove incorrect trials, outlier exclusion |
| `read_csv` | Load PsychoPy output files directly |

---

## Tools This Week

- `pandas` — install if needed: `pip install pandas`
- `numpy` — covered in `week-07-numpy_and_data_manipulation.md`
- `matplotlib` — covered in `week-07-data_visualization_with_matplotlib.md`

---

## Assignment

Complete **Part 2** of `week-07-puzzles.ipynb` (Puzzles 15–18):

- Puzzle 15: Derived columns and filtering
- Puzzle 16: Pivot table of mean RT
- Puzzle 17: Interference cost with `apply` or subtraction
- Puzzle 18: Merging a metadata DataFrame

Submit by pushing to your GitHub repository before Week 08.

---

## Resources

### Official Documentation
- [pandas Getting Started](https://pandas.pydata.org/docs/getting_started/intro_tutorials/)
- [pandas User Guide — Indexing and Selecting](https://pandas.pydata.org/docs/user_guide/indexing.html)
- [pandas User Guide — GroupBy](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [pandas User Guide — IO Tools (CSV, Excel)](https://pandas.pydata.org/docs/user_guide/io.html)

### Further Reading
- [10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [pandas Cheat Sheet (PDF)](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

---

## What Comes Next

| Week | Topic                                                          |
| ---- | -------------------------------------------------------------- |
| 08   | **Midterm:** Deploy a full experiment to Pavlovia              |
| 12   | pandas advanced — REST APIs, data cleaning, merging Open Data  |
