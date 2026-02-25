# Week 01: Orientation — Environment Setup & Python Basics

> **Course:** NS5116 Computational Neuroscience — Spring 2026
> **Week:** 1 of 16 | **Date:** 2026-02-26 | **Room:** TBA

---

## Welcome

This is the first week of a 16-week hands-on coding course for graduate students. No prior programming experience is assumed.

The course is split into two parts:

- **Weeks 1–8 — Manual Python:** Write code from scratch. Build an online cognitive experiment by Week 8.
- **Weeks 9–16 — Vibe Coding & Agentic Programming:** Use AI tools (Claude Code) to build real applications. Present a web app using Taiwan open data at Week 16.

This week is about getting your environment ready and writing your first Python code.

---

## Before Class Checklist

Complete these steps before arriving on Thursday:

- [ ] Install [Anaconda](https://www.anaconda.com/download) or [Miniforge](https://github.com/conda-forge/miniforge) (Miniforge recommended — lighter, better compatibility)
- [ ] Install [VS Code](https://code.visualstudio.com/)
- [ ] Install the **Python** and **Jupyter** extensions in VS Code
- [ ] Create a [GitHub](https://github.com/) account (free)
- [ ] Create a [Pavlovia](https://pavlovia.org/) account (free for students)
- [ ] Create a [Streamlit Cloud](https://streamlit.io/cloud) account (free)

See the step-by-step guide (in Chinese): [environment_setup_zh.md](environment_setup_zh.md)

---

## Learning Objectives

By the end of this week you will be able to:

1. Set up a working Python environment using conda
2. Launch JupyterLab from VS Code
3. Understand how Jupyter notebooks work (cells, kernel, execution order)
4. Declare variables and assign values in Python
5. Identify and use the basic data types: `int`, `float`, `str`, `bool`
6. Apply arithmetic and comparison operators
7. Print output using `print()` and f-strings
8. Run an `.ipynb` notebook from start to finish without errors

---

## In-Class Topics

### 1. Environment Setup (30 min)
Create and activate a conda environment for the course:

```bash
conda create -n compneuro python=3.10
conda activate compneuro
pip install notebook jupyterlab matplotlib numpy
```

Launch JupyterLab:

```bash
jupyter lab
```

Or open VS Code, select the `compneuro` kernel, and open `lpthw_ex00-10.ipynb` or `week-01-environment_setup_guide.ipynb`.

### 2. Jupyter Notebook Orientation (15 min)
- Code cells vs. Markdown cells
- Running a cell: `Shift + Enter`
- Restarting the kernel
- Execution order — why it matters
- Saving your work

### 3. Python Basics Walkthrough (60 min)

**Variables and data types:**
```python
name = "Erik"          # str
age = 30               # int
height = 1.75          # float
is_student = True      # bool
```

**Arithmetic operators:**
```python
x = 10
y = 3
print(x + y)   # 13
print(x ** y)  # 1000  (exponentiation)
print(x % y)   # 1     (remainder)
```

**Comparison operators:**
```python
print(10 > 5)    # True
print(10 == 10)  # True
print(10 != 5)   # True
```

**Formatted output with f-strings:**
```python
score = 95.5
print(f"Your score is {score:.1f}")
```

### 4. Easter Egg (5 min)
```python
import antigravity
```

---

## Tools This Week

| Tool | Purpose | Install |
|------|---------|---------|
| Anaconda / Miniforge | Python environment manager | [anaconda.com](https://www.anaconda.com/download) / [miniforge](https://github.com/conda-forge/miniforge) |
| VS Code | Code editor | [code.visualstudio.com](https://code.visualstudio.com/) |
| JupyterLab | Interactive notebook interface | via `pip install jupyterlab` |

---

## Assignment

Work through [`lpthw_ex00-10.ipynb`](lpthw_ex00-10.ipynb) — type every code cell by hand and complete all Study Drills.

Then create a new notebook `week-01-assignment.ipynb` and write a script that:

Submit by pushing to your own GitHub repository (instructions will be given in class).

---

## Resources

- **Setup guide (中文):** [environment_setup_zh.md](environment_setup_zh.md)
- **Karpathy's Claude Coding Notes (2026):** [Karpathy_2026_Claude_Coding_Notes.qmd](Karpathy_2026_Claude_Coding_Notes.qmd)
- [Official Python Tutorial — Introduction](https://docs.python.org/3/tutorial/introduction.html)
- [Anaconda Installation Guide](https://docs.anaconda.com/anaconda/install/)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [Jupyter Notebook Beginner Guide](https://jupyter-notebook-beginner-guide.readthedocs.io/)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 02 | if/else, loops, functions |
| 03 | Lists, dictionaries, file I/O |
| 04 | NumPy arrays |
| 05 | Data visualization with Matplotlib |
| 06–07 | PsychoPy experiments |
| 08 | **Midterm:** Deploy experiment to Pavlovia |