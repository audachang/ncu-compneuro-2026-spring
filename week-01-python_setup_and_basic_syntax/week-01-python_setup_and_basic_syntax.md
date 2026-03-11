# Week 01: Python Setup & Basic Syntax

> **Course:** NS5116 Computational Neuroscience — Spring 2026
> **Week:** 1 of 16 | **Date:** 2026-02-27 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Install Python 3 and set up a VS Code + Jupyter environment
2. Run Python code interactively in a Jupyter notebook
3. Use `print()` to display output with various formatting options
4. Declare variables and understand Python's dynamic typing
5. Work with strings: quotes, concatenation, `len()`, and common methods
6. Use f-strings for readable string interpolation and format specifiers
7. Perform arithmetic with integers and floats; understand operator precedence
8. Convert between types with `int()`, `float()`, `str()`
9. Collect user input with `input()` and convert it to a usable type
10. Write comments to document your code

---

## In-Class Topics

### 1. print()

The `print()` function outputs text to the console:

```python
print("Hello, world!")
print("Subject ID:", "P01")
print("RT =", 320, "ms")
print(f"Trial 1: RT = {320} ms")
```

Control formatting with keyword arguments:

```python
# sep parameter — change the separator between arguments
print("A", "B", "C", sep=", ")          # "A, B, C"
print("A", "B", "C", sep="-")           # "A-B-C"

# end parameter — change what comes at the end
print("Loading", end="...")
print("done")                           # outputs "Loading...done"
```

#### Real Python: Beyond Basic Printing

The `print()` function is more powerful than it first appears. Use it for:

- **Debugging**: Add `print()` statements to trace code flow and inspect variable values at different points
- **Output redirection**: `print(..., file=sys.stderr)` sends output to stderr instead of stdout
- **Flushing**: `print(..., flush=True)` forces immediate output (useful in real-time experiments)
- **String representation**: Objects can define `__str__()` and `__repr__()` to control what `print()` outputs

```python
# Example: printing with a file handle
import sys
print("This is an error", file=sys.stderr)

# Example: immediate output (no buffering)
print("Stimulus appeared", flush=True)
```

For large-scale data logging, consider the `logging` module, which is more flexible than `print()`.

📖 [The Python `print()` Function: Go Beyond the Basics](https://realpython.com/python-print/)

---

### 2. Variables and Assignment

A variable stores a value with a label. Python lets you assign any type to any variable name:

```python
subject_id = "P01"
age = 22
mean_rt = 342.5
is_valid = True
```

Python is **dynamically typed** — the same variable can hold different types at different times:

```python
x = 10           # x is an int
x = "now a string"  # x is now a str — this works but is poor practice
```

Multiple assignment — assign multiple variables at once:

```python
a, b, c = 1, 2, 3
x = y = 0        # x and y both get 0
```

Augmented assignment — shorthand for updating:

```python
count = 5
count += 1       # count = count + 1
count *= 2       # count = count * 2
```

#### Real Python: Naming Conventions and Best Practices

**Use `snake_case` for variable names** (lowercase, underscores between words):

```python
# Good
subject_id = "P01"
mean_reaction_time = 345.2

# Avoid
subjectId = "P01"          # camelCase (used in Java/JavaScript)
SUBJECT_ID = "P01"         # ALL_CAPS is reserved for constants (see below)
subject = "P01"            # unclear what kind of data
```

**Constants by convention** — use ALL_CAPS for values that should not change:

```python
MAX_RT_MS = 1500
MIN_RT_MS = 100
PI = 3.14159
```

Python does *not* enforce immutability on ALL_CAPS names (unlike other languages), so treat them as read-only by convention.

**Use `type()` to inspect a variable's type** (especially useful when debugging):

```python
print(type(subject_id))      # <class 'str'>
print(type(age))             # <class 'int'>
print(type(mean_rt))         # <class 'float'>
```

📖 [Python Variables: How to Define and Use Them](https://realpython.com/python-variables/)

---

### 3. Strings

A string is a sequence of characters. Create with single or double quotes:

```python
name = "Erik"
greeting = 'Hello'
```

**Concatenation and repetition:**

```python
full = greeting + ", " + name + "!"         # "Hello, Erik!"
separator = "-" * 40                        # 40 dashes
```

**Built-in string methods** (strings are objects with methods you can call):

```python
"hello".upper()              # "HELLO"
"HELLO".lower()              # "hello"
"  trim me  ".strip()        # "trim me"  (removes leading/trailing whitespace)
"a,b,c".split(",")           # ["a", "b", "c"]  (split into a list)
"hello world".replace("world", "Python")   # "hello Python"
"P01".startswith("P")        # True
"P01".endswith("01")         # True
"P" in "P01"                 # True (membership test)
```

**Length:**

```python
len("reaction time")         # 13
```

Strings are **immutable** — you cannot change a character in-place. Methods return new strings.

#### Real Python: String Methods and Manipulation

Strings have over 40 built-in methods. Common ones for data cleaning:

```python
# Clean whitespace
line = "  P01, 420.5  \n"
line = line.strip()          # "P01, 420.5"

# Case conversion
condition = "CONGRUENT"
condition = condition.lower() # "congruent"

# Check properties
"123".isdigit()              # True
"abc".isalpha()              # True
"P01".isalnum()              # True (alphanumeric)

# Find substrings
rt_str = "RT: 420 ms"
index = rt_str.find("420")   # 4 (index of substring)

# Format and pad
code = "P01"
code.ljust(10)               # "P01       " (left-justify in 10 chars)
code.rjust(10)               # "       P01" (right-justify)
```

Strings support **indexing** (like lists):

```python
word = "Python"
word[0]      # "P"
word[-1]     # "n"  (last character)
word[1:4]    # "yth"
```

📖 [Strings and Character Data in Python](https://realpython.com/python-strings/)

---

### 4. F-strings

F-strings (formatted string literals, Python 3.6+) are the most readable way to insert variables into strings:

```python
subject = "P03"
rt = 412.75
correct = True

# Basic interpolation
print(f"Subject {subject}: RT = {rt} ms")   # "Subject P03: RT = 412.75 ms"
```

**Format specifiers** — control decimal places, width, and more:

```python
# Decimal places
print(f"RT = {rt:.1f} ms")        # "RT = 412.8 ms"  (1 decimal place)
print(f"RT = {rt:.3f} ms")        # "RT = 412.750 ms"  (3 decimal places)

# Width and alignment
print(f"RT = {rt:8.1f} ms")       # "RT =    412.8 ms"  (width 8, right-aligned)
print(f"RT = {rt:<8.1f} ms")      # "RT = 412.8    ms"  (left-aligned)

# Percentage
accuracy = 0.876
print(f"Accuracy: {accuracy:.1%}")   # "Accuracy: 87.6%"

# Zero-padding
trial = 5
print(f"Trial {trial:03d}")        # "Trial 005"
```

**Expressions inside {}:**

```python
rts = [320, 415, 280]
print(f"Mean: {sum(rts)/len(rts):.1f} ms")  # "Mean: 338.3 ms"

# Even boolean expressions
print(f"Valid: {rt > 150 and rt < 1000}")
```

**Debug mode (Python 3.8+)** — the `=` specifier shows the expression and its value:

```python
print(f"{rt=}")               # "rt=412.75"
print(f"{subject=}")          # "subject='P03'"
```

#### Real Python: String Formatting: A Deep Dive

Python has three main ways to format strings. Know them all, but **prefer f-strings** for new code:

```python
# Old-style % formatting (Python 2 legacy — avoid in new code)
print("RT: %f ms" % rt)

# .format() method (Python 3.0–3.5 — still valid but verbose)
print("RT: {:.1f} ms".format(rt))

# f-strings (Python 3.6+ — fastest and most readable)
print(f"RT: {rt:.1f} ms")
```

**Multiline f-strings** — useful for complex formatting:

```python
report = f"""
Subject: {subject}
RT: {rt:.1f} ms
Correct: {correct}
"""
print(report)
```

**Nested quotes** — escape or alternate quote styles:

```python
print(f"He said 'Hello, {subject}'")     # single quotes inside f-string
print(f'She said "Hi, {subject}"')       # double quotes inside f-string
```

F-strings are evaluated at runtime and compile to optimized bytecode. They're significantly faster than `.format()` and string concatenation for loops.

📖 [Python f-Strings: The Ultimate Guide](https://realpython.com/python-f-strings/) · [String Formatting: % vs .format() vs f-strings](https://realpython.com/python-string-formatting/)

---

### 5. Numbers and Arithmetic

Python has two main numeric types: `int` and `float`.

**Integer arithmetic:**

```python
trials = 40
correct = 32
wrong = trials - correct    # 8
```

**Float arithmetic:**

```python
mean_rt = 1823.5 / 5       # 364.7  (always returns float in Python 3)
accuracy = correct / trials # 0.8
```

**Operator precedence** (PEMDAS — Parentheses, Exponents, Multiplication/Division, Addition/Subtraction):

```python
result = 2 + 3 * 4        # 14, not 20 (multiply first)
result = (2 + 3) * 4      # 20 (parentheses force addition first)
```

**Integer division (`//`) and modulo (`%`):**

```python
blocks = trials // 10      # 4 (how many complete blocks of 10?)
remainder = trials % 10    # 0 (leftover trials)

# Practical use: break trials into blocks
block_number = trial_number // 10  # which block is trial 27? block 2
position_in_block = trial_number % 10  # position within block (7)
```

**Exponentiation:**

```python
variance = 64.0
std = variance ** 0.5      # 8.0 (square root)
squared = 5 ** 2           # 25
```

#### Real Python: Working with Numbers Carefully

**Integer vs. float division:**

```python
# In Python 3, / always returns float
7 / 2         # 3.5 (float)
7 // 2        # 3 (int, floor division)
```

**Floating-point precision gotcha:**

```python
0.1 + 0.2            # 0.30000000000000004 (not exactly 0.3!)
0.1 + 0.2 == 0.3     # False (be careful with == on floats)

# Solution: use round() for display or comparisons
abs(0.1 + 0.2 - 0.3) < 1e-9  # True (check closeness within tolerance)
round(0.1 + 0.2, 1) == 0.3    # True
```

This happens because decimal numbers cannot be represented exactly in binary. For money, use the `decimal` module; for most scientific work, the tiny error is irrelevant.

**Rounding and other functions:**

```python
round(412.75, 1)     # 412.8
abs(-320)            # 320
pow(2, 3)            # 8 (same as 2 ** 3)
```

**The `math` module** for scientific functions:

```python
import math
math.sqrt(64)        # 8.0
math.log(100)        # natural log
math.exp(1)          # e^1 ≈ 2.718
math.ceil(3.2)       # 4 (round up)
math.floor(3.8)      # 3 (round down)
```

📖 [Numeric Types in Python: int, float, complex](https://realpython.com/python-numbers/) · [The `math` Module](https://docs.python.org/3/library/math.html)

---

### 6. Type Conversion

Convert between types using `int()`, `float()`, `str()`, and `bool()`:

```python
# String to number
int("42")            # 42
float("3.14")        # 3.14
bool("anything")     # True (any non-empty string is truthy)

# Number to string
str(320)             # "320"
str(3.14)            # "3.14"

# Boolean conversion
bool(0)              # False
bool(1)              # True
bool("")             # False (empty string is falsy)
bool([])             # False (empty list is falsy)
```

**Practical example — reading user input:**

```python
raw = input("Enter RT (ms): ")   # input() always returns a string
rt = int(raw)                    # convert string to int for math
```

**Error handling — what if the user enters invalid input?**

```python
try:
    rt_str = input("Enter RT (ms): ")
    rt = int(rt_str)
    print(f"RT: {rt} ms")
except ValueError:
    print("Please enter an integer")
```

#### Real Python: Safe Type Conversion and Validation

The `try/except` block prevents crashes when conversion fails:

```python
def get_rt():
    """Prompt for RT and return as int, or None if invalid."""
    try:
        return int(input("Enter RT (ms): "))
    except ValueError:
        print("Invalid input — not an integer")
        return None

rt = get_rt()
if rt is not None:
    print(f"RT: {rt} ms")
```

For more complex validation:

```python
# Check if a string is all digits
if user_input.isdigit():
    value = int(user_input)
else:
    print("Expected a number")

# Check range
if 100 <= rt <= 1500:
    print("Valid RT")
else:
    print("RT out of range")
```

This defensive approach prevents cryptic errors downstream.

📖 [Using Python's Input Function for Strings and Integers](https://realpython.com/python-input-integer-float/)

---

### 7. User Input

Collect input from the user with the `input()` function:

```python
subject_id = input("Enter subject ID: ")
age_str = input("Enter age: ")
age = int(age_str)

print(f"Hello, subject {subject_id}! Age: {age}")
```

The `input()` function always returns a **string**, even if the user types numbers. You must convert it if you need a different type.

```python
# Right-hand side of this comparison is a string, not a number!
age_str = input("Age: ")       # "25"
if age_str > "20":             # String comparison: "25" > "20" → True (alphabetical)
    print("Old")

# Correct: convert first
age = int(age_str)
if age > 20:                   # Numeric comparison: 25 > 20 → True
    print("Old")
```

#### Real Python: Input, Validation, and the Sentinel Pattern

For experiment code, always validate user input before using it:

```python
# Keep asking until valid
while True:
    try:
        subject_id = input("Subject ID (e.g., P01): ")
        if not subject_id.startswith("P"):
            print("Subject ID must start with 'P'")
            continue
        if len(subject_id) != 3:
            print("Subject ID must be 3 characters (e.g., P01)")
            continue
        break
    except KeyboardInterrupt:
        print("\nCancelled by user")
        exit()

print(f"Starting experiment for {subject_id}")
```

This **sentinel loop** pattern (`while True` with early `break`) ensures the program doesn't proceed until valid data is provided.

For automated testing and file-based input, consider reading from a file or JSON configuration instead of `input()`.

📖 [How to Accept User Input in Python](https://realpython.com/python-input-integer-float/) · [Input Validation Patterns](https://docs.python.org/3/library/exceptions.html)

---

### 8. Comments

Comments document your code. Use `#` for single-line comments:

```python
# This is a comment
subject_id = "P01"  # Store the participant identifier

# For experiment timing, always use milliseconds
rt_ms = 412.5

# For multi-line comments, use # on each line
# (not docstrings — those are for functions and classes)
# This RT was unusually slow due to network lag.
# We'll remove it in outlier detection.
```

**Docstrings** (triple-quoted strings) document functions (covered in Week 02).

---

## Neuroscience Connection

These foundational concepts map directly to experiment programming:

| Programming concept | Experiment use |
|---------------------|-----------------|
| `print()` | Log trial events and timestamps |
| Variables | Store subject ID, condition labels, RT values |
| Strings | Encode condition names, file paths, participant IDs |
| F-strings | Format results for printing or file output (e.g., `f"Accuracy: {acc:.1%}"`) |
| `int()` / `float()` | Parse RT from keyboard or file |
| `input()` | Collect subject ID or response codes before running an experiment |
| Comments | Explain parameter choices (e.g., RT thresholds, timing constants) |

---

## Tools This Week

- **Python 3** (https://www.python.org/downloads/)
- **VS Code** + Python extension (https://code.visualstudio.com/docs/python/python-tutorial)
- **Jupyter Notebook** or **JupyterLab** (installed via `pip install jupyter`)
- Text editor for writing scripts

---

## Assignment

Work through [`lpthw_ex00-10.ipynb`](lpthw_ex00-10.ipynb) for hands-on practice with basic syntax.

Then create a new notebook `week-01-assignment.ipynb` with a script that:

1. Prompts for a participant's name
2. Prompts for age (convert to int)
3. Prompts for a reaction time in milliseconds (convert to float)
4. Prints a formatted summary using f-strings:
   ```
   Subject: [name]
   Age: [age] years
   RT: [rt] ms ([rt/1000:.2f] seconds)
   ```

Submit by pushing to your GitHub repository before Week 02.

---

## Resources

### Official Documentation
- [Python 3 Tutorial: Introduction](https://docs.python.org/3/tutorial/introduction.html)
- [Python Built-in Functions](https://docs.python.org/3/library/functions.html)
- [Python String Methods](https://docs.python.org/3/library/stdtypes.html#string-methods)

### Real Python — print()
- [The Python `print()` Function: Go Beyond the Basics](https://realpython.com/python-print/)

### Real Python — Variables
- [Python Variables: How to Define and Use Them](https://realpython.com/python-variables/)

### Real Python — Strings
- [Strings and Character Data in Python](https://realpython.com/python-strings/)

### Real Python — String Formatting
- [Python f-Strings: The Ultimate Guide](https://realpython.com/python-f-strings/)
- [String Formatting in Python: %, .format(), and f-strings](https://realpython.com/python-string-formatting/)

### Real Python — Numbers
- [Numeric Types in Python: int, float, complex](https://realpython.com/python-numbers/)

### Real Python — Input
- [How to Accept User Input in Python](https://realpython.com/python-input-integer-float/)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 02 | Control flow (`if`, `for`, `while`) and functions |
| 03 | Data structures (lists, dicts, files) |
| 04 | NumPy arrays — vectorized computation on large datasets |
