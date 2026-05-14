# Week 03: Functions, Data Structures & File I/O

> **Course:** NS5116 Computational Neuroscience — Spring 2026
> **Week:** 3 of 16 | **Date:** 2026-03-12 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Define reusable functions with `def`, parameters, and `return`
2. Set default parameter values in function definitions
3. Explain the difference between local and global scope
4. Create and manipulate Python lists using indexing, slicing, and common methods
5. Build and query dictionaries to store key-value data
6. Explain when to use a tuple vs. a list
7. Use sets to find unique values and compute intersections
8. Read and write plain text files with `open()`
9. Parse and write CSV files using the `csv` module
10. Represent a single experiment trial as a dictionary

---

## Video

📺 [Week 03 Lecture](https://youtu.be/6D4scknsEJs)

---

## In-Class Topics

### 1. Functions

Defining a function:
```python
def greet(name):
    print(f"Hello, {name}!")

greet("Erik")
```

With a return value:
```python
def mean_rt(rt_list):
    return sum(rt_list) / len(rt_list)

avg = mean_rt([320, 415, 280, 510])
print(f"Mean RT: {avg:.1f} ms")
```

Default parameter values:
```python
def classify_rt(rt, threshold=500):
    if rt < threshold:
        return "fast"
    else:
        return "slow"

classify_rt(420)                    # uses default threshold=500
classify_rt(420, threshold=400)     # overrides default
```

#### Docstrings

Every function should have a *docstring* — a string literal immediately after `def` that documents what the function does, what it accepts, and what it returns:

```python
def mean_rt(rt_list):
    """Return the arithmetic mean of a list of reaction times.

    Args:
        rt_list (list[float]): Reaction times in milliseconds.

    Returns:
        float: The mean reaction time.

    Raises:
        ZeroDivisionError: If rt_list is empty.
    """
    return sum(rt_list) / len(rt_list)
```

Access it with `help(mean_rt)` or `mean_rt.__doc__`.

#### Returning Multiple Values

Python functions can return multiple values packaged as a tuple — the caller can unpack them directly:

```python
def rt_stats(rt_list):
    """Return mean, minimum, and maximum reaction time."""
    return sum(rt_list) / len(rt_list), min(rt_list), max(rt_list)

mean, lo, hi = rt_stats([320, 415, 280, 510])
print(f"Mean: {mean:.1f}, Range: {lo}–{hi} ms")
```

#### `*args` — Accept Any Number of Positional Arguments

Prefix a parameter with `*` to receive extra positional arguments as a tuple:

```python
def add_rts(*rts):
    """Sum any number of reaction times."""
    return sum(rts)

add_rts(100, 200, 300)   # rts = (100, 200, 300)
```

#### Mutable Default Argument Gotcha

**Never use a mutable object (list, dict) as a default argument.** The default is created once when `def` is executed and shared across all calls:

```python
# BUG — the list persists between calls!
def record(rt, history=[]):
    history.append(rt)
    return history

record(320)  # [320]
record(415)  # [320, 415]  ← unexpected!

# Fix — use None as the sentinel
def record(rt, history=None):
    if history is None:
        history = []
    history.append(rt)
    return history
```

📖 [Defining Your Own Python Function](https://realpython.com/defining-your-own-python-function/) · [The `return` Statement](https://realpython.com/python-return-statement/) · [Optional Arguments](https://realpython.com/python-optional-arguments/) · [`*args` and `**kwargs`](https://realpython.com/python-kwargs-and-args/) · [How to Write Docstrings](https://realpython.com/how-to-write-docstrings-in-python/)

---

### 2. Scope

```python
x = 10  # global variable

def show():
    x = 99  # local variable — does NOT change the global x
    print(x)

show()    # prints 99
print(x)  # prints 10  (global unchanged)
```

> **Rule of thumb:** Functions should receive data through parameters and
> return results with `return`. Avoid relying on global variables inside functions.

#### The LEGB Rule

Python resolves names in a specific order — **L E G B**:

| Scope         | Description                       | Example                                    |
| ------------- | --------------------------------- | ------------------------------------------ |
| **L**ocal     | Inside the current function       | Variables defined with `=` inside `def`    |
| **E**nclosing | In any enclosing `def` (closures) | Outer function's variables                 |
| **G**lobal    | At module (file) level            | Variables defined at the top of the script |
| **B**uilt-in  | Python's built-in namespace       | `len`, `print`, `range`, `sum`             |

Python searches from L → E → G → B and uses the first match it finds.

```python
value = "global"           # G

def outer():
    value = "enclosing"    # E

    def inner():
        value = "local"    # L
        print(value)       # prints "local"

    inner()
    print(value)           # prints "enclosing"

outer()
print(value)               # prints "global"
```

#### `global` and `nonlocal`

Use these sparingly — they are usually a sign that the design could be improved:

```python
count = 0

def increment():
    global count    # explicitly refer to the module-level variable
    count += 1

increment()
print(count)  # 1
```

`nonlocal` does the same for the enclosing (E) scope inside nested functions.

📖 [Python Scope and the LEGB Rule](https://realpython.com/python-scope-legb-rule/)

---

### 3. Lists

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

#### `sort()` vs `sorted()`

`list.sort()` sorts *in place* and returns `None`; `sorted()` returns a new sorted list and leaves the original unchanged:

```python
rts = [320, 415, 280, 510]

sorted_copy = sorted(rts)   # [280, 320, 415, 510] — original unchanged
rts.sort()                  # modifies rts in place

# Sort descending
sorted(rts, reverse=True)

# Sort by a custom key — e.g. absolute distance from 400 ms
rts.sort(key=lambda rt: abs(rt - 400))
```

#### List Comprehensions in Depth

A list comprehension has the form `[expression for item in iterable if condition]`. The `if` part is optional:

```python
rts = [320, -5, 415, 1200, 280, 510]

# Map: convert to seconds
rts_sec = [rt / 1000 for rt in rts]

# Filter: keep valid RTs only
valid    = [rt for rt in rts if 100 <= rt <= 1000]

# Map + filter together
valid_sec = [rt / 1000 for rt in rts if 100 <= rt <= 1000]
```

**When to prefer a regular loop over a comprehension (best practices):**

- The comprehension spans multiple lines with complex logic → use a `for` loop
- You need side effects (e.g., `print`) inside the loop → use a `for` loop
- Keep comprehensions flat: avoid deeply nested ones

```python
# Avoid — hard to read
matrix = [[row[i] for row in matrix] for i in range(4)]

# Prefer — explicit loop for complex nesting
transposed = []
for i in range(4):
    transposed.append([row[i] for row in matrix])
```

📖 [Python's `list` Data Type](https://realpython.com/python-list/) · [When to Use a List Comprehension](https://realpython.com/list-comprehension-python/) · [Comprehensions Best Practices](https://realpython.com/ref/best-practices/comprehensions/)

---

### 4. Dictionaries

📺 [Introduction to Dictionaries](https://youtu.be/A1dz_WPWO90)

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

#### `dict.get()` and `dict.setdefault()`

`dict.get(key, default)` returns a fallback value when the key is missing — no `KeyError`:

```python
trial = {"rt_ms": 412, "correct": True}

accuracy = trial.get("accuracy", None)   # None — key missing, no crash
block    = trial.get("block", 1)         # 1   — sensible default
```

`dict.setdefault(key, default)` goes one step further: it *also inserts* the default if the key is absent:

```python
trial.setdefault("notes", "")   # adds "notes": "" if not present
```

#### Dictionary Comprehensions

Like list comprehensions, but produce a dict:

```python
subjects = ["P01", "P02", "P03"]
mean_rts = [342.1, 419.6, 378.0]

# Build a lookup dict from two lists
rt_lookup = {subj: rt for subj, rt in zip(subjects, mean_rts)}
# {"P01": 342.1, "P02": 419.6, "P03": 378.0}

# Invert a dict (swap keys and values)
inverted = {v: k for k, v in rt_lookup.items()}
```

#### `collections.defaultdict` for Grouping

When grouping data (e.g., all trials per condition), `defaultdict` eliminates the boilerplate of checking whether a key exists:

```python
from collections import defaultdict

results = [
    {"condition": "congruent",   "rt": 320},
    {"condition": "incongruent", "rt": 510},
    {"condition": "congruent",   "rt": 390},
]

# Without defaultdict — requires key existence check
by_condition = {}
for r in results:
    cond = r["condition"]
    if cond not in by_condition:
        by_condition[cond] = []
    by_condition[cond].append(r["rt"])

# With defaultdict — cleaner
by_condition = defaultdict(list)
for r in results:
    by_condition[r["condition"]].append(r["rt"])
```

📖 [Dictionaries in Python](https://realpython.com/python-dicts/) · [Python Dictionary Comprehensions](https://realpython.com/python-dictionary-comprehension/) · [Using `defaultdict`](https://realpython.com/python-defaultdict/)

---

### 5. Tuples and Sets

📺 [Python 集合入門](https://youtu.be/dEqjv0PNnzM)

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

#### Lists vs Tuples — When to Choose Which

| Characteristic | `list`                                     | `tuple`                                 |
| -------------- | ------------------------------------------ | --------------------------------------- |
| Mutability     | Mutable — can add, remove, change elements | Immutable — fixed after creation        |
| Typical use    | Homogeneous sequences that grow/shrink     | Fixed records with heterogeneous fields |
| Example        | All RTs from one block                     | `(subject_id, session, rt_ms)`          |
| As dict key?   | ❌ Not allowed (unhashable)                 | ✅ Allowed (hashable)                    |

```python
# Tuple as a dict key — useful for condition x block lookups
lookup = {}
lookup[("congruent", 1)] = [320, 415, 280]
lookup[("incongruent", 1)] = [510, 488, 530]
```

#### `namedtuple` — Self-Documenting Tuples

`collections.namedtuple` gives fields readable names without the overhead of a full class:

```python
from collections import namedtuple

Trial = namedtuple("Trial", ["subject", "condition", "rt_ms", "correct"])

t = Trial("P01", "congruent", 412, True)
print(t.rt_ms)      # 412
print(t.correct)    # True
# Still works as a regular tuple:
subject, condition, rt_ms, correct = t
```

#### Set Operations and `frozenset`

```python
completed_day1 = {"P01", "P02", "P03", "P04"}
completed_day2 = {"P02", "P03", "P05"}

# Subjects who completed both sessions
both = completed_day1 & completed_day2    # {"P02", "P03"}

# Subjects who dropped out after day 1
dropped = completed_day1 - completed_day2  # {"P01", "P04"}

# Is day2 a subset of day1?
completed_day2.issubset(completed_day1)    # False — P05 not in day1
```

A `frozenset` is an immutable set — it can be used as a dictionary key or stored inside another set:

```python
# Store a combination of conditions as a frozenset key
combo_rts = {}
combo_rts[frozenset(["congruent", "high_load"])] = [340, 365, 320]
```

📖 [Python's `tuple` Data Type](https://realpython.com/python-tuple/) · [Lists vs Tuples in Python](https://realpython.com/python-lists-tuples/) · [Sets in Python](https://realpython.com/python-sets/) · [Common Python Data Structures](https://realpython.com/python-data-structures/)

---

### 6. File I/O — Reading and Writing Files in Python

📺 [Python 檔案 I/O：從概念到執行](https://youtu.be/vfmC5Ytb-Z8)

> 📖 This section is based on [Reading and Writing Files in Python (Guide)](https://realpython.com/read-write-files-python/).

#### 6.1 What Is a File?

At its core, a file is a **contiguous set of bytes** used to store data. Every file on a modern file system is composed of three parts:

| Part                  | Description                                     |
| --------------------- | ----------------------------------------------- |
| **Header**            | Metadata — file name, size, type, etc.          |
| **Data**              | The actual contents written by the creator      |
| **End of File (EOF)** | A special marker indicating the end of the file |

What the data bytes represent depends on the **format specification**, which is typically indicated by the file extension (`.txt`, `.csv`, `.png`, …).

#### 6.2 File Paths

A file path is a string that tells the operating system where to find a file. It has three parts:

1. **Folder path** — separated by `/` (Unix/macOS) or `\` (Windows)
2. **File name** — the actual name
3. **Extension** — e.g. `.txt`, `.csv`

```text
project/
│
├── data/
│   ├── raw/
│   │   └── eeg_recording.csv     ← full path: data/raw/eeg_recording.csv
│   └── processed/
│       └── summary.txt
│
└── analysis.py                   ← current working directory is project/
```

- **Absolute path:** `C:\Users\lab\project\data\raw\eeg_recording.csv`
- **Relative path:** `data/raw/eeg_recording.csv` (from the `project/` folder)
- **`..` moves up one directory:** `../other_project/config.txt`

#### 6.3 Line Endings and Character Encodings

**Line endings** differ across operating systems:

| OS           | Line ending | Escape sequence |
| ------------ | ----------- | --------------- |
| Windows      | CR+LF       | `\r\n`          |
| Unix / macOS | LF          | `\n`            |

This can cause problems when a file created on Windows is opened on Unix (extra `\r` characters). Python's text mode handles this automatically by converting all line endings to `\n` on read, but be aware of this when working with binary mode.

**Character encodings** translate byte values into human-readable characters:

| Encoding | Characters supported | Notes                                      |
| -------- | -------------------- | ------------------------------------------ |
| ASCII    | 128 characters       | English letters, digits, basic punctuation |
| UTF-8    | 1,114,112 characters | Superset of ASCII; supports all languages  |

> **Best practice:** Always specify `encoding="utf-8"` when your text might contain non-ASCII characters (accented letters, Chinese/Japanese/Korean characters, etc.):

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("反應時間: 420 ms\n")   # Chinese characters
```

#### 6.4 Opening and Closing a File

The built-in `open()` function returns a **file object**. You must always close this object when you are done.

**Method 1 — `try` / `finally` (manual close):**
```python
reader = open("log.txt")
try:
    content = reader.read()
    print(content)
finally:
    reader.close()     # guaranteed to run even if an error occurs
```

**Method 2 — `with` statement (recommended):**
```python
with open("log.txt") as reader:
    content = reader.read()
    print(content)
# file is automatically closed when the block ends
```

> **Always use `with open(...)`** — it is cleaner, safer, and automatically closes the file even if an error occurs.

#### 6.5 File Open Modes

| Mode            | Meaning                                                      |
| --------------- | ------------------------------------------------------------ |
| `"r"`           | Read text (default) — error if file missing                  |
| `"w"`           | Write text — creates file or **overwrites** existing content |
| `"a"`           | Append text — adds to end, creates if missing                |
| `"x"`           | Exclusive create — error if file already exists              |
| `"rb"` / `"wb"` | Read / Write **binary** (images, pickled data, etc.)         |

Each mode returns a different type of file object:

```python
>>> f = open("log.txt", "r")     # TextIOWrapper (text mode)
>>> f = open("log.txt", "rb")    # BufferedReader (binary mode)
>>> f = open("log.txt", "wb")    # BufferedWriter (binary mode)
```

#### 6.6 Writing a File

Use `.write()` to write a single string, or `.writelines()` to write a sequence of strings:

```python
# Write experiment log
with open("log.txt", "w") as f:
    f.write("Trial 1: RT=320ms\n")
    f.write("Trial 2: RT=415ms\n")

# Write multiple lines at once
lines = ["Trial 1: RT=320ms\n", "Trial 2: RT=415ms\n", "Trial 3: RT=390ms\n"]
with open("log.txt", "w") as f:
    f.writelines(lines)     # note: does NOT add \n automatically
```

**Appending** to an existing file (without overwriting):
```python
with open("log.txt", "a") as f:
    f.write("Trial 4: RT=450ms\n")   # added to the end
```

#### 6.7 Reading a File — Three Methods

Python offers three methods for reading from a file object:

| Method         | Returns                      | Best for                         |
| -------------- | ---------------------------- | -------------------------------- |
| `.read()`      | Entire file as one string    | Small files you need as a string |
| `.readline()`  | Next single line as a string | Processing one line at a time    |
| `.readlines()` | List of all lines            | When you need a list of lines    |

```python
# 1. Read the entire file at once
with open("log.txt") as f:
    content = f.read()
    print(content)

# 2. Read one line at a time with .readline()
with open("log.txt") as f:
    line = f.readline()
    while line != "":          # empty string signals EOF
        print(line, end="")    # end="" avoids double newlines
        line = f.readline()

# 3. Read all lines into a list
with open("log.txt") as f:
    lines = f.readlines()      # each element includes the "\n"
    print(lines)
    # ['Trial 1: RT=320ms\n', 'Trial 2: RT=415ms\n', ...]
```

#### 6.8 Iterating Over Each Line — The Pythonic Way

The **most Pythonic** (and memory-efficient) way to process a file line by line is to iterate directly over the file object — no need to call `.readlines()`:

```python
with open("experiment_data.txt") as f:
    for line in f:                 # file object is an iterator
        print(line.strip())        # strip() removes trailing \n
```

This is preferred over `.readlines()` for large files because it reads one line at a time instead of loading the entire file into memory.

```python
# Practical example — extract RTs from a log file
rts = []
with open("log.txt") as f:
    for line in f:
        # Each line: "Trial 1: RT=320ms"
        if "RT=" in line:
            rt_str = line.split("RT=")[1].replace("ms\n", "")
            rts.append(int(rt_str))

print(f"Mean RT: {sum(rts)/len(rts):.1f} ms")
```

#### 6.9 Working With Two Files at the Same Time

You can open multiple files in a single `with` statement — useful for reading from one file and writing to another:

```python
# Read raw data, write cleaned version
with open("raw_log.txt", "r") as reader, open("clean_log.txt", "w") as writer:
    for line in reader:
        cleaned = line.strip().lower()
        writer.write(cleaned + "\n")
```

```python
# Reverse the lines of a file
with open("log.txt", "r") as reader, open("log_reversed.txt", "w") as writer:
    lines = reader.readlines()
    writer.writelines(reversed(lines))
```

#### 6.10 Working with Bytes (Binary Mode)

When working with non-text files (images, audio, pickled data), open in binary mode by adding `"b"` to the mode string. All read/write methods then work with `bytes` objects instead of strings:

```python
# Read the first 8 bytes of a PNG file header
with open("brain_scan.png", "rb") as f:
    header = f.read(8)
    print(header)
    # b'\x89PNG\r\n\x1a\n'  ← standard PNG magic bytes

# Copy a binary file
with open("brain_scan.png", "rb") as src, open("backup.png", "wb") as dst:
    dst.write(src.read())
```

#### 6.11 Common Libraries for Other File Formats

Don't re-invent the wheel — Python's standard library and PyPI have modules for many formats:

| Module / Package    | File type                  |
| ------------------- | -------------------------- |
| `csv`               | CSV / TSV files            |
| `json`              | JSON files                 |
| `pathlib`           | Object-oriented file paths |
| `zipfile`           | ZIP archives               |
| `tarfile`           | Tar archives               |
| `wave`              | WAV audio                  |
| `configparser`      | INI config files           |
| `xml.etree`         | XML files                  |
| `PyPDF2` *(PyPI)*   | PDF documents              |
| `Pillow` *(PyPI)*   | Image processing           |
| `openpyxl` *(PyPI)* | Excel .xlsx files          |

📖 [Reading and Writing Files in Python](https://realpython.com/read-write-files-python/) · [Working With Files in Python](https://realpython.com/working-with-files-in-python/) · [Why Is It Important to Close Files in Python?](https://realpython.com/why-close-file-python/)

---

### 7. CSV Files

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

#### Why `newline=""` When Opening for CSV

On Windows, opening a file in text mode adds an extra `\r` to each line, causing double-blank-lines in the output. Passing `newline=""` hands newline control entirely to the `csv` module, which handles it correctly on all platforms:

```python
# Always open CSV files with newline="" on write
with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    ...
```

#### `DictReader` Key Points

- The first row of the CSV is automatically used as field names (the dict keys)
- Every subsequent row becomes an `OrderedDict` (behaves like a regular dict)
- All values are read as **strings** — convert explicitly where needed:

```python
with open("results.csv") as f:
    reader = csv.DictReader(f)
    data = []
    for row in reader:
        data.append({
            "trial":   int(row["trial"]),
            "rt_ms":   float(row["rt_ms"]),
            "correct": row["correct"] == "True",   # str → bool
        })
```

#### `DictWriter` Key Points

- `fieldnames` is **required** and sets the column order
- `writeheader()` writes the first row; call it before any data rows
- Use `extrasaction="ignore"` if your dicts have extra keys you don't want in the file:

```python
writer = csv.DictWriter(f, fieldnames=["trial", "rt_ms"], extrasaction="ignore")
```

#### Non-Standard Delimiters

`csv.reader` / `csv.writer` accept a `delimiter` argument for TSV (tab-separated) and other formats:

```python
# Read a tab-separated file
with open("data.tsv") as f:
    reader = csv.DictReader(f, delimiter="\t")
```

📖 [Reading and Writing CSV Files in Python](https://realpython.com/python-csv/) · [csv Standard Library Reference](https://realpython.com/ref/stdlib/csv/)

---

## Neuroscience Connection

| Concept              | Experiment use                                                           |
| -------------------- | ------------------------------------------------------------------------ |
| Function + docstring | Encapsulate a scoring algorithm and document its contract                |
| Default parameter    | `threshold=500` that callers can override without breaking existing code |
| List                 | Store all reaction times from a block                                    |
| List comprehension   | Filter valid trials or convert units in one line                         |
| Dictionary           | Represent one trial with labelled fields                                 |
| `defaultdict`        | Group trials by condition without boilerplate                            |
| List of dicts        | Full experiment dataset — one dict per trial                             |
| Tuple                | Fixed stimulus parameters (position, colour, duration)                   |
| `namedtuple`         | Readable trial records that unpack like tuples                           |
| Set                  | Find which subjects completed all sessions                               |
| CSV file             | Save and reload experiment results; compatible with R, MATLAB, Excel     |
| File paths           | Organise raw vs processed data in a clear directory hierarchy            |
| Line endings         | Understand cross-platform issues when collaborators use Windows vs macOS |
| Binary mode          | Read/write neuroimaging data files (`.nii`, `.edf`, `.bdf`)              |

---

## Tools This Week

- Python standard library: `csv`, `collections`, built-in `open()`
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

### Official Documentation
- [Python Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python Scope](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding)
- [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python `csv` module](https://docs.python.org/3/library/csv.html)
- [Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)

### Functions & Scope
- [Defining Your Own Python Function](https://realpython.com/defining-your-own-python-function/)
- [The Python `return` Statement: Usage and Best Practices](https://realpython.com/python-return-statement/)
- [Using Python Optional Arguments When Defining Functions](https://realpython.com/python-optional-arguments/)
- [Python `args` and `kwargs`: Demystified](https://realpython.com/python-kwargs-and-args/)
- [How to Write Docstrings in Python](https://realpython.com/how-to-write-docstrings-in-python/)
- [Python Scope and the LEGB Rule: Resolving Names in Your Code](https://realpython.com/python-scope-legb-rule/)

### Lists
- [Python's `list` Data Type: A Deep Dive With Examples](https://realpython.com/python-list/)
- [When to Use a List Comprehension in Python](https://realpython.com/list-comprehension-python/)
- [Comprehensions Best Practices](https://realpython.com/ref/best-practices/comprehensions/)
- [Python `enumerate()`: Simplify Loops That Need Counters](https://realpython.com/python-enumerate/)

### Dictionaries
- [Dictionaries in Python](https://realpython.com/python-dicts/)
- [Python Dictionary Comprehensions](https://realpython.com/python-dictionary-comprehension/)
- [Using the Python `defaultdict` Type for Handling Missing Keys](https://realpython.com/python-defaultdict/)
- [Common Python Data Structures (Guide)](https://realpython.com/python-data-structures/)

### Tuples & Sets
- [Python's `tuple` Data Type: A Deep Dive With Examples](https://realpython.com/python-tuple/)
- [Lists vs Tuples in Python](https://realpython.com/python-lists-tuples/)
- [Sets in Python](https://realpython.com/python-sets/)

### File I/O
- [Reading and Writing Files in Python (Guide)](https://realpython.com/read-write-files-python/)
- [Working With Files in Python](https://realpython.com/working-with-files-in-python/)
- [Why Is It Important to Close Files in Python?](https://realpython.com/why-close-file-python/)
- [Python `with` Statement](https://realpython.com/python-with-statement/)

### CSV
- [Reading and Writing CSV Files in Python](https://realpython.com/python-csv/)
- [Reading and Writing CSV Files (Course)](https://realpython.com/courses/reading-and-writing-csv-files/)

---

## What Comes Next

| Week | Topic                                                           |
| ---- | --------------------------------------------------------------- |
| 04   | NumPy — faster, more powerful than lists for numerical data     |
| 05   | Matplotlib — visualize your CSV data                            |
| 06   | PsychoPy — write data in CSV format directly from an experiment |
