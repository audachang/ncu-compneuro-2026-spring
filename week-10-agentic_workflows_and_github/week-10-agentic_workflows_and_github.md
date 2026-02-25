# Week 10: Agentic Workflows & GitHub

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Week:** 10 of 16 | **Date:** 2026-04-30 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Assign multi-step coding tasks to Claude Code and review the results
2. Use a feature-branch git workflow: `branch → commit → pull request`
3. Write a minimal pytest test suite for a data utility function
4. Create a GitHub Actions workflow that runs tests automatically on every push
5. Use Claude Code to perform a structured code review of a repository
6. Identify when to break a large task into smaller sequential Claude Code prompts

---

## In-Class Topics

### 1. Multi-Step Agentic Tasks (20 min)

Single-step prompts work well for small functions. Larger features require breaking the task into a sequence, where each step builds on the last.

**Example: add a new data source to an existing app**

```
Step 1:
> In utils/fetch_data.py, add a function called fetch_earthquake_data()
  that calls the CWA open data API at https://opendata.cwa.gov.tw/api/...
  and returns a pandas DataFrame with columns: time, magnitude, depth, lat, lon.
  Handle HTTP errors by raising a ValueError with the status code.

Step 2 (after reviewing Step 1 output):
> Now write a pytest test for fetch_earthquake_data() in tests/test_fetch_data.py.
  Mock the requests.get call so the test does not make a real network request.
  Test that the function returns a DataFrame with the correct columns.

Step 3 (after reviewing Step 2 output):
> Add a GitHub Actions workflow at .github/workflows/test.yml that installs
  requirements and runs pytest on every push to any branch.
```

Breaking the task this way gives you a review point between each step. If Step 1 is wrong, you correct it before Step 2 makes incorrect assumptions.

---

### 2. Git Feature-Branch Workflow (25 min)

Work on new features in a separate branch. Never commit directly to `main`.

```bash
# Create and switch to a new branch
git checkout -b feature/earthquake-tab

# Make changes (with Claude Code or manually)
# Then stage and commit
git add utils/fetch_data.py tests/test_fetch_data.py
git commit -m "Add earthquake data fetcher and tests"

# Push the branch to GitHub
git push -u origin feature/earthquake-tab
```

**Opening a Pull Request on GitHub:**

```bash
# Using the GitHub CLI (gh)
gh pr create \
  --title "Add earthquake data tab" \
  --body "Fetches CWA earthquake records, adds bar chart, includes pytest tests."
```

Or open the PR on the GitHub website by clicking the banner that appears after pushing.

**Merging:**
```bash
# After review, merge and delete the branch
gh pr merge --squash --delete-branch
git checkout main
git pull
```

Keep commits small and focused. One feature = one branch = one PR.

---

### 3. Writing Tests with pytest (20 min)

Tests verify that your code does what it claims. They also act as a safety net when you refactor.

**A simple data utility:**
```python
# utils/clean.py

import pandas as pd

def remove_outliers(df: pd.DataFrame, column: str, n_std: float = 3.0) -> pd.DataFrame:
    """Remove rows where `column` is more than n_std standard deviations from the mean."""
    mean = df[column].mean()
    std  = df[column].std()
    mask = (df[column] - mean).abs() <= n_std * std
    return df[mask].reset_index(drop=True)
```

**The test file:**
```python
# tests/test_clean.py

import pandas as pd
import pytest
from utils.clean import remove_outliers

def test_removes_high_outlier():
    df = pd.DataFrame({"value": [10, 11, 12, 10, 100]})  # 100 is an outlier
    result = remove_outliers(df, "value", n_std=2.0)
    assert 100 not in result["value"].values

def test_keeps_normal_values():
    df = pd.DataFrame({"value": [10, 11, 12, 10, 11]})
    result = remove_outliers(df, "value", n_std=2.0)
    assert len(result) == 5   # no rows should be removed

def test_empty_dataframe():
    df = pd.DataFrame({"value": []})
    result = remove_outliers(df, "value")
    assert len(result) == 0
```

Run tests locally:
```bash
pytest tests/ -v
```

Output:
```
tests/test_clean.py::test_removes_high_outlier PASSED
tests/test_clean.py::test_keeps_normal_values  PASSED
tests/test_clean.py::test_empty_dataframe      PASSED

3 passed in 0.12s
```

---

### 4. GitHub Actions CI (25 min)

A CI (Continuous Integration) workflow runs your tests automatically every time you push to GitHub. It catches bugs before they reach `main`.

Create `.github/workflows/test.yml`:

```yaml
name: Run tests

on:
  push:
    branches: ["**"]
  pull_request:
    branches: ["main"]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Check out code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run pytest
        run: pytest tests/ -v
```

After pushing this file, go to your GitHub repository → **Actions** tab. You will see the workflow run and a green checkmark if all tests pass.

If a test fails, GitHub shows you the exact error output — and you can paste it directly into Claude Code to fix it:

```
> The GitHub Actions test failed with this output:
  [paste the error here]
  Fix the test or the function, whichever is wrong.
```

---

### 5. Code Review with Claude Code (15 min)

Ask Claude Code to review your repository the same way a senior developer would:

```
> Review the code in utils/fetch_data.py and app.py.
  Look for: missing error handling, hardcoded values that should be configurable,
  functions that are too long, and any security issues (e.g. API keys in source code).
  List each issue with a suggested fix.
```

Claude Code will read both files and produce a prioritized list of issues. Work through them one by one.

**Common issues Claude Code finds in student projects:**
- API key stored in `app.py` instead of `.env` or `st.secrets`
- `except Exception: pass` silencing real errors
- DataFrame operations inside a loop (should be vectorized)
- No check for empty API responses before accessing `.json()`

---

## Course Connection

| Manual workflow (Weeks 1–8) | Agentic workflow (Weeks 9–16) |
|-----------------------------|-------------------------------|
| Write code → run → fix manually | Prompt Claude Code → review → test → iterate |
| Debug by reading tracebacks | Paste tracebacks into Claude Code |
| Single file scripts | Multi-file projects with modules |
| No automated tests | pytest + GitHub Actions CI |
| Commit to main | Feature branches + pull requests |

---

## Tools This Week

| Tool | Purpose | Install / Link |
|------|---------|----------------|
| Claude Code CLI | Agentic task execution | `npm install -g @anthropic-ai/claude-code` |
| git | Version control | [git-scm.com](https://git-scm.com) |
| GitHub CLI (`gh`) | Create PRs from terminal | `brew install gh` / [cli.github.com](https://cli.github.com) |
| pytest | Python test runner | `pip install pytest` |
| GitHub Actions | Automated CI | Built into GitHub — no install needed |

---

## Assignment

Add tests and CI to your Week 09 project:

1. Write at least two pytest tests for a utility function in your `utils/` folder. Good candidates:
   - A function that cleans missing values from your dataset
   - A function that computes a summary statistic per group
   - A function that parses a date column
2. Create `.github/workflows/test.yml` using the template from Section 4. Confirm the workflow passes (green checkmark) on GitHub.
3. Create a new feature branch called `feature/add-tests`, commit your test file and workflow, and open a pull request to `main`.
4. Ask Claude Code to review `app.py` and `utils/fetch_data.py` for the issues listed in Section 5. Fix at least two of the issues it identifies.
5. Merge the PR after the CI check passes.

Submit the GitHub repository URL (showing the merged PR and passing Actions run) on the course portal before Week 11.

---

## Resources

- [GitHub Actions quickstart](https://docs.github.com/en/actions/quickstart)
- [pytest documentation](https://docs.pytest.org/)
- [GitHub CLI documentation](https://cli.github.com/manual/)
- [Git branching model (Atlassian)](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)
- [Python unittest.mock — for mocking HTTP calls in tests](https://docs.python.org/3/library/unittest.mock.html)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 11 | Streamlit — widgets, layout, caching, deploy to Streamlit Cloud |
| 12 | Taiwan open data APIs — fetching, parsing, and cleaning real data |
| 13 | Interactive dashboards with Plotly Express |
| 16 | **Final milestone:** Live web app presentation |
