# Week 03: Data Structures & File I/O

> **Course:** NS5116 Computational Neuroscience — Spring 2026
> **Week:** 3 of 16 | **Date:** 2026-03-12 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Create and manipulate Python lists using indexing, slicing, and common methods
2. Build and query dictionaries to store key-value data
3. Explain when to use a tuple vs. a list
4. Use sets to find unique values and compute intersections
5. Read and write plain text files with `open()`
6. Parse and write CSV files using the `csv` module
7. Represent a single experiment trial as a dictionary

---

## In-Class Topics

### 1. Lists (25 min)

A list holds an ordered sequence of values:
```python
rts = [320, 415, 280, 510, 390]
```

**Indexing and slicing:**
```python
rts[0]      # 320  (first element)
rts[-1]     # 390  (last element)
rts[1:3]    # [415, 280]  (index 1 up to but not including 3)
```

**Common methods:**
```python
rts.append(450)         # add to the end
rts.sort()              # sort in place
rts.pop()               # remove and return the last element
len(rts)                # number of elements
min(rts), max(rts)      # minimum and maximum
sum(rts) / len(rts)     # mean
```

**List comprehension — a compact `for` loop:**
```python
# Keep only RTs within the valid range
valid = [rt for rt in rts if 100 <= rt <= 1000]
```

---

### 2. Dictionaries (25 min)

A dictionary maps keys to values — ideal for labelled data:
```python
trial = {
    "subject_id": "P01",
    "condition": "congruent",
    "rt_ms": 412,
    "correct": True,
}
```

**Accessing values:**
```python
trial["rt_ms"]              # 412
trial.get("accuracy", None) # None (key doesn't exist — no error)
```

**Adding and updating:**
```python
trial["block"] = 2          # add new key
trial["rt_ms"] = 398        # update existing key
```

**Iterating:**
```python
for key, value in trial.items():
    print(f"{key}: {value}")
```

**List of dicts — standard format for experiment data:**
```python
results = [
    {"trial": 1, "rt": 320, "correct": True},
    {"trial": 2, "rt": 510, "correct": False},
    {"trial": 3, "rt": 390, "correct": True},
]

# Mean RT across correct trials only
correct_rts = [r["rt"] for r in results if r["correct"]]
mean_rt = sum(correct_rts) / len(correct_rts)
```

---

### 3. Tuples and Sets (15 min)

**Tuples** — like lists but immutable (cannot be changed after creation):
```python
coords = (1920, 1080)   # screen resolution — should not change
x, y = coords           # unpacking
```

Use tuples for fixed structured data (coordinates, RGB colours, etc.).

**Sets** — unordered collections with no duplicates:
```python
subjects_a = {"P01", "P02", "P03"}
subjects_b = {"P02", "P03", "P04"}

subjects_a & subjects_b   # intersection: {"P02", "P03"}
subjects_a | subjects_b   # union: {"P01", "P02", "P03", "P04"}
subjects_a - subjects_b   # difference: {"P01"}

# Remove duplicates from a list
conditions = ["cong", "incong", "cong", "cong", "incong"]
unique = list(set(conditions))  # ["cong", "incong"]
```

---

### 4. File I/O — Text Files (15 min)

**Writing a text file:**
```python
with open("log.txt", "w") as f:
    f.write("Trial 1: RT=320ms\n")
    f.write("Trial 2: RT=415ms\n")
```

**Reading a text file:**
```python
with open("log.txt", "r") as f:
    for line in f:
        print(line.strip())   # strip() removes trailing newline
```

> **Always use `with open(...)`** — it automatically closes the file even if an error occurs.

---

### 5. CSV Files (20 min)

CSV (comma-separated values) is the standard format for behavioural data.

**Writing CSV:**
```python
import csv

fieldnames = ["trial", "condition", "rt_ms", "correct"]
rows = [
    {"trial": 1, "condition": "congruent",   "rt_ms": 320, "correct": True},
    {"trial": 2, "condition": "incongruent", "rt_ms": 510, "correct": False},
]

with open("results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
```

**Reading CSV:**
```python
with open("results.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["condition"], row["rt_ms"])
```

---

## Neuroscience Connection

| Data structure | Experiment use |
|---------------|----------------|
| List | Store all reaction times from a block |
| Dictionary | Represent one trial with labelled fields |
| List of dicts | Full experiment dataset — one dict per trial |
| CSV file | Save and reload experiment results |
| Set | Find which subjects completed all sessions |

---

## Tools This Week

- Python standard library: `csv`, built-in `open()`
- No additional packages needed beyond Week 01 setup

---

## Assignment

Work through [`lpthw_ex15-17_37-39.ipynb`](lpthw_ex15-17_37-39.ipynb) for hands-on file and data structure practice.

Then create a new notebook `week-03-assignment.ipynb` and:

Key exercises:
- Build a list-of-dicts from raw trial data
- Compute accuracy and mean RT per condition using loops and list comprehensions
- Write the results to a CSV file, then read it back and verify the values

Submit by pushing to your GitHub repository before Week 04.

---

## Resources

- [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python `csv` module](https://docs.python.org/3/library/csv.html)
- [Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 04 | NumPy — faster, more powerful than lists for numerical data |
| 05 | Matplotlib — visualize your CSV data |
| 06 | PsychoPy — write data in CSV format directly from an experiment |
