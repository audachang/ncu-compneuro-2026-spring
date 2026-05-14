# Week 02: Control Flow

> **Course:** NS5116 Computational Neuroscience — Spring 2026
> **Week:** 2 of 16 | **Date:** 2026-03-05 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Use `if / elif / else` to branch program execution based on conditions
2. Write `for` loops to iterate over ranges, lists, and other sequences
3. Write `while` loops and know when to use them instead of `for`
4. Use `break` and `continue` to control loop flow
5. Debug code using `print()` tracing

---

## In-Class Topics

### 1. Conditionals (20 min)

```python
rt = 450  # reaction time in ms

if rt < 200:
    print("Too fast — likely anticipation")
elif rt < 600:
    print("Normal response")
else:
    print("Slow response")
```

Comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
Logical operators: `and`, `or`, `not`

```python
# Combined condition
if rt > 150 and rt < 600:
    print("Valid trial")
```

#### Real Python: Truthy and Falsy Values

Python evaluates any object as either *truthy* or *falsy* in a Boolean context.
You rarely need to write `if len(rts) != 0` — just write `if rts`:

```python
rts = []
if rts:
    print("Data found")
else:
    print("No trials recorded yet")   # runs when list is empty
```

Values that are **falsy**: `None`, `0`, `0.0`, `""`, `[]`, `{}`, `()`, `set()`
Everything else is **truthy**.

#### Real Python: Conditional Expressions (Ternary)

A single-line `if/else` expression (called a *conditional expression* or *ternary operator*) assigns a value based on a condition:

```python
label = "fast" if rt < 300 else "slow"
```

Equivalent to:
```python
if rt < 300:
    label = "fast"
else:
    label = "slow"
```

Use this only when both branches are short and clear. For complex logic, stick with full `if/else` blocks.

#### Real Python: Avoiding Long `elif` Chains with Dict Dispatch

A long chain of `elif` clauses checking one variable is often better expressed as a dictionary lookup:

```python
# Long elif chain — hard to extend
def describe(condition):
    if condition == "congruent":
        return "stimulus and response match"
    elif condition == "incongruent":
        return "stimulus and response conflict"
    elif condition == "neutral":
        return "no priming"

# Dict dispatch — easy to extend, no repeated comparisons
DESCRIPTIONS = {
    "congruent":   "stimulus and response match",
    "incongruent": "stimulus and response conflict",
    "neutral":     "no priming",
}
def describe(condition):
    return DESCRIPTIONS.get(condition, "unknown condition")
```

📖 [Conditional Statements in Python](https://realpython.com/python-conditional-statements/) · [Best Practices: Conditionals](https://realpython.com/ref/best-practices/conditionals/)

---

### 2. `for` Loops (25 min)

Iterate over a range of numbers:
```python
for i in range(5):
    print(i)   # 0 1 2 3 4
```

Iterate over a list:
```python
trials = [320, 415, 280, 510]
for rt in trials:
    print(f"RT: {rt} ms")
```

`enumerate()` — get both index and value:
```python
for i, rt in enumerate(trials):
    print(f"Trial {i+1}: {rt} ms")
```

#### Real Python: `range()` in Depth

`range(start, stop, step)` — all three parameters give full control:

```python
range(10)        # 0..9
range(1, 11)     # 1..10
range(0, 100, 10)  # 0, 10, 20, ..., 90
range(10, 0, -1)   # 10, 9, ..., 1  (count down)
```

#### Real Python: `zip()` for Parallel Iteration

When you need to loop over two sequences together, use `zip()` instead of index-based access:

```python
subjects   = ["P01", "P02", "P03"]
mean_rts   = [342.1, 419.6, 378.0]

# Index-based (less Pythonic)
for i in range(len(subjects)):
    print(subjects[i], mean_rts[i])

# zip (clean and idiomatic)
for subject, mean_rt in zip(subjects, mean_rts):
    print(f"{subject}: {mean_rt:.1f} ms")
```

#### Real Python: Prefer `enumerate()` over `range(len(...))`

A common beginner mistake is `for i in range(len(trials))` just to get the index. Use `enumerate()` instead:

```python
# Avoid
for i in range(len(trials)):
    print(i, trials[i])

# Prefer
for i, rt in enumerate(trials):
    print(i, rt)
```

You can also set the start index: `enumerate(trials, start=1)`.

#### Real Python: `else` Clause on Loops

Python's `for` and `while` loops have an optional `else` block that runs only if the loop completed *without* hitting a `break`:

```python
target = 999
for rt in trials:
    if rt == target:
        print("Found target RT")
        break
else:
    print("Target RT not found in any trial")  # runs if no break
```

📖 [Python `for` Loops: The Pythonic Way](https://realpython.com/python-for-loop/) · [Python `enumerate()`](https://realpython.com/python-enumerate/) · [Python `range()`](https://realpython.com/python-range/) · [Python `zip()`](https://realpython.com/python-zip-function/)

---

### 3. `while` Loops (15 min)

```python
count = 0
while count < 5:
    print(f"Trial {count}")
    count += 1
```

`break` — exit the loop early:
```python
while True:
    response = input("Press q to quit: ")
    if response == 'q':
        break
```

`continue` — skip to the next iteration:
```python
for rt in trials:
    if rt < 0:
        continue    # skip invalid values
    print(rt)
```

#### Real Python: The Sentinel / `while True` Pattern

The `while True: ... break` pattern is idiomatic in Python for loops where the exit condition is best checked in the middle of the body — for example, collecting user input until a valid value is given:

```python
while True:
    raw = input("Enter RT (ms): ")
    if raw.isdigit():
        rt = int(raw)
        break
    print("Please enter a positive integer.")
```

This avoids duplicating the input call outside and inside the loop (the *loop-and-a-half* problem).

#### Real Python: Emulating `do-while`

Python has no `do-while` statement, but the pattern above achieves the same effect — the body runs at least once before the condition is checked:

```python
# Equivalent of: do { body } while (condition);
while True:
    body()
    if not condition():
        break
```

#### Real Python: Flag Variables vs `break`

Both styles are valid; choose the one that makes intent clearest:

```python
# Flag variable
found = False
for rt in trials:
    if rt > 1000:
        found = True
        break

# Using else on a for loop (no flag needed)
for rt in trials:
    if rt > 1000:
        break
else:
    found = False  # loop finished without break
```

📖 [Python `while` Loops](https://realpython.com/python-while-loop/) · [`break` Keyword](https://realpython.com/python-break/) · [`continue` Keyword](https://realpython.com/python-continue/) · [Emulate Do-While](https://realpython.com/python-do-while/)

---

### 4. Debugging with `print()` (10 min)

When code behaves unexpectedly, add `print()` statements to trace values:

```python
def sum_valid(rt_list, min_rt=100, max_rt=1000):
    total = 0
    for rt in rt_list:
        print(f"  checking rt={rt}")   # debug line
        if min_rt <= rt <= max_rt:
            total += rt
    print(f"  total={total}")          # debug line
    return total
```

Remove or comment out debug prints before submitting.

#### Real Python: Using `assert` to Catch Bugs Early

`assert` lets you state assumptions in code. If the assumption is false, Python raises `AssertionError` immediately, pinpointing the problem:

```python
def mean_rt(rt_list):
    assert len(rt_list) > 0, "rt_list must not be empty"
    assert all(rt > 0 for rt in rt_list), "all RTs must be positive"
    return sum(rt_list) / len(rt_list)
```

Assertions are for *developer errors* (wrong input to your own functions), not for handling user-facing errors in production.

---

## Neuroscience Connection

These concepts map directly to experiment programming:

| Programming concept  | Experiment use                                           |
| -------------------- | -------------------------------------------------------- |
| `if / else`          | Accept or reject a trial based on response time          |
| Truthy/Falsy         | Check whether a data list is non-empty before processing |
| `for` loop           | Run a fixed number of trials                             |
| `enumerate()`        | Pair trial numbers with responses                        |
| `zip()`              | Pair stimuli with correct answers for scoring            |
| `while` loop         | Wait for a key press or timeout                          |
| `while True / break` | Input validation loop — keep prompting until valid data  |

---

## Tools This Week

- Python (no additional libraries needed)
- VS Code + Jupyter (from Week 01 setup)

---

## Assignment

Work through [`lpthw_ex11-22_27-36.ipynb`](lpthw_ex11-22_27-36.ipynb) for hands-on practice.

Then create a new notebook `week-02-assignment.ipynb` and:

Key exercises:
- Classify a list of reaction times as fast / normal / slow
- Write a function `mean_rt()` and a function `remove_outliers()`
- Build a simple trial loop that counts correct responses

Submit by pushing to your GitHub repository before Week 03.

---

## Resources

### Official Documentation
- [Python Control Flow](https://docs.python.org/3/tutorial/controlflow.html)

### Real Python — Conditionals
- [Conditional Statements in Python](https://realpython.com/python-conditional-statements/)
- [Python Best Practices: Conditionals](https://realpython.com/ref/best-practices/conditionals/)

### Real Python — Loops
- [Python `for` Loops: The Pythonic Way](https://realpython.com/python-for-loop/)
- [Python `while` Loops: Repeating Tasks Conditionally](https://realpython.com/python-while-loop/)
- [How to Exit Loops Early With the Python `break` Keyword](https://realpython.com/python-break/)
- [Skip Ahead in Loops With Python's `continue` Keyword](https://realpython.com/python-continue/)
- [Python `enumerate()`: Simplify Loops That Need Counters](https://realpython.com/python-enumerate/)
- [Python `range()`: Represent Numerical Ranges](https://realpython.com/python-range/)
- [Using the Python `zip()` Function for Parallel Iteration](https://realpython.com/python-zip-function/)
- [How Can You Emulate Do-While Loops in Python?](https://realpython.com/python-do-while/)

---

## What Comes Next

| Week | Topic                                                                              |
| ---- | ---------------------------------------------------------------------------------- |
| 03   | Functions, data structures, file I/O — organizing code and storing experiment data |
| 04   | NumPy arrays — vectorized computation on large datasets                            |
| 05   | Matplotlib — plotting reaction time distributions                                  |
