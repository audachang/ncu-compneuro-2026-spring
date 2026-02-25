# Week 02: Control Flow & Functions

> **Course:** NS5116 Computational Neuroscience — Spring 2026
> **Week:** 2 of 16 | **Date:** 2026-03-05 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Use `if / elif / else` to branch program execution based on conditions
2. Write `for` loops to iterate over ranges, lists, and other sequences
3. Write `while` loops and know when to use them instead of `for`
4. Use `break` and `continue` to control loop flow
5. Define reusable functions with `def`, parameters, and `return`
6. Set default parameter values in function definitions
7. Explain the difference between local and global scope
8. Debug code using `print()` tracing

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

---

### 4. Functions (30 min)

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

classify_rt(420)          # uses default threshold=500
classify_rt(420, threshold=400)   # overrides default
```

---

### 5. Scope (10 min)

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

---

### 6. Debugging with `print()` (10 min)

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

---

## Neuroscience Connection

These concepts map directly to experiment programming:

| Programming concept | Experiment use |
|--------------------|----------------|
| `if / else` | Accept or reject a trial based on response time |
| `for` loop | Run a fixed number of trials |
| `while` loop | Wait for a key press or timeout |
| Function | Encapsulate a trial sequence, scoring logic, or stimulus presentation |

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

- [Python Control Flow](https://docs.python.org/3/tutorial/controlflow.html)
- [Python Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python Scope](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 03 | Lists, dictionaries, file I/O — storing and loading experiment data |
| 04 | NumPy arrays — vectorized computation on large datasets |
| 05 | Matplotlib — plotting reaction time distributions |
