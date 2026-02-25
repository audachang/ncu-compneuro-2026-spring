# Week 09: Intro to Vibe Coding & Claude Code

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Week:** 9 of 16 | **Date:** 2026-04-23 | **Room:** TBA

---

## Overview

Part 1 of this course focused on writing Python by hand — understanding every line before it ran. Part 2 shifts the model: you will use Claude Code, an AI coding agent, to build applications that would take much longer to write manually.

"Vibe coding" is the practice of directing an AI to produce code by describing what you want in natural language, then iterating until it works. The programmer's role shifts from syntax writer to system designer, quality arbiter, and critical reviewer. This week introduces the mindset, the tool, and the habits that make agentic programming productive.

---

## Learning Objectives

By the end of this week you will be able to:

1. Explain the difference between autocomplete AI (GitHub Copilot) and agentic AI (Claude Code)
2. Install and authenticate Claude Code CLI on your machine
3. Write an effective task description that produces useful code on the first attempt
4. Apply the describe → generate → test → revise loop to a real problem
5. Scaffold a new project directory with Claude Code
6. Verify that AI-generated code is correct and does not introduce hidden bugs
7. Identify the limits of current AI coding tools and when to fall back to manual code

---

## In-Class Topics

### 1. Vibe Coding vs. Autocomplete AI (20 min)

Two different AI programming tools are in common use:

| Feature | Autocomplete (Copilot, Cursor) | Agentic (Claude Code) |
|---------|-------------------------------|----------------------|
| Interaction | Inline, suggestion-by-suggestion | Conversational, multi-step tasks |
| File scope | Current file | Entire project |
| Can run code | No | Yes |
| Can run tests | No | Yes |
| Can use git | No | Yes |
| Best for | Completing known patterns fast | Building features from a description |

Claude Code can read your entire repository, write code, run it, read error messages, and fix itself — without you typing a single line. Your job is to describe the goal clearly, review the output, and guide it when it drifts.

---

### 2. Installing Claude Code CLI (20 min)

Claude Code runs in your terminal as a Node.js application.

```bash
# Prerequisites: Node.js 18+ and npm
node --version    # should be v18 or higher

# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Verify
claude --version
```

**Authentication:**

```bash
claude
# Claude Code will open a browser window for OAuth authentication
# Sign in with your Anthropic account (or use an API key)
```

If your organization uses an API key:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
claude
```

> On Windows, run these commands in Git Bash or WSL2.

---

### 3. Your First Conversation with Claude Code (15 min)

Start Claude Code in an empty directory and ask it to create something:

```bash
mkdir taiwan-weather-app
cd taiwan-weather-app
claude
```

Inside the Claude Code session:

```
> Create a Python script called hello.py that prints "Hello from Taiwan!"
  and then prints today's date in YYYY-MM-DD format.
```

Claude Code will write the file, show you the code, and you can ask it to run it:

```
> Run it and show me the output.
```

Then inspect the file yourself to verify it looks correct:

```bash
cat hello.py
python hello.py
```

**Rule:** Always read what Claude Code writes. Never run code you have not reviewed.

---

### 4. Effective Prompting Strategies (25 min)

The quality of AI output depends heavily on how clearly you specify the task.

**Weak prompt:**
```
Make a data app.
```

**Strong prompt:**
```
Create a Streamlit app called app.py that:
1. Reads a CSV file called "data/air_quality.csv" with columns: date, station, pm25
2. Shows a selectbox to filter by station name
3. Displays a line chart of PM2.5 values over time for the selected station
4. Prints the mean PM2.5 value below the chart
Use @st.cache_data on the data loading function.
```

**Prompting principles:**

| Principle | Example |
|-----------|---------|
| State the output file name | "Create `app.py`" not "make an app" |
| List input/output format explicitly | "CSV with columns: date, station, pm25" |
| Specify libraries to use | "Use Streamlit and Plotly Express" |
| State what must NOT happen | "Do not hardcode any file paths" |
| Ask for one thing at a time | Break large tasks into sequential steps |

---

### 5. The Describe → Generate → Test → Revise Loop (20 min)

No AI produces correct code on the first try for complex tasks. The productive workflow is iterative:

```
1. DESCRIBE   — write a clear, specific task in Claude Code
2. GENERATE   — Claude Code writes the code
3. TEST       — run it yourself; does it do what you asked?
4. REVISE     — if not, give Claude Code a specific error or correction
               ("The chart shows all stations at once; filter it by the selectbox value")
5. REPEAT     — loop until the feature is working and you understand the code
```

Example revision prompt:

```
> The app runs but the line chart ignores the selectbox.
  The filtered_df variable is not being used in the chart call. Fix it.
```

Claude Code can read the error and apply the fix. You do not need to point it at the specific line — but being specific is faster.

---

### 6. Project Scaffolding (15 min)

Ask Claude Code to create the skeleton of a new project in one step:

```
> Scaffold a new Streamlit project for a Taiwan air quality dashboard.
  Create this structure:
    taiwan-aq/
      app.py              (main Streamlit app, placeholder content)
      data/               (empty folder with a .gitkeep)
      utils/
        __init__.py
        fetch_data.py     (stub: fetch_data() returns an empty DataFrame)
      requirements.txt    (streamlit, pandas, plotly, requests)
      README.md           (project title and one-sentence description)
      .gitignore          (Python, VS Code, .env)
```

This gives you a clean starting point with no boilerplate to write manually.

---

### 7. Verifying AI Output (15 min)

AI-generated code can be wrong in subtle ways:

- Correct syntax, wrong logic (filters applied in the wrong order)
- Uses a deprecated API (old pandas `.append()` instead of `pd.concat()`)
- Hard-codes a value that should be a parameter
- Silently swallows exceptions with a bare `except: pass`

**Review checklist for any AI-generated function:**

```
[ ] Does it do what I described?
[ ] Does it handle the empty/missing data case?
[ ] Are all file paths relative or configurable?
[ ] Is there any bare except: or silent error suppression?
[ ] Would it break if the input columns are renamed?
[ ] Does it import everything it uses?
```

---

## Supplementary Background: `lpthw_ex46-52.ipynb`

The notebook `lpthw_ex46-52.ipynb` in this folder covers project skeleton organization, `unittest` basics, and a minimal Flask app — topics from *Learn Python the Hard Way* exercises 46–52. These are not required for the assignment but provide helpful background on:

- How to organize a Python project into modules and packages
- How to write unit tests and run them with `python -m unittest`
- How the request/response model of a web server works (Flask preview before Streamlit)

Read through it if you want deeper context for how Claude Code structures the projects it generates.

---

## Course Connection

| Part 1 (manual coding) | Part 2 (vibe coding) |
|------------------------|----------------------|
| Write every line yourself | Describe goals; review AI output |
| Debug by reading tracebacks | Paste tracebacks into Claude Code |
| Learn syntax and patterns | Learn to prompt and evaluate quality |
| Build one experiment | Build a full web application |
| Output: Pavlovia URL | Output: Streamlit Cloud URL |

---

## Tools This Week

| Tool | Purpose | Install |
|------|---------|---------|
| Claude Code CLI | Agentic AI coding in the terminal | `npm install -g @anthropic-ai/claude-code` |
| Node.js 18+ | Runtime for Claude Code | [nodejs.org](https://nodejs.org) |
| git | Version control; required for Claude Code projects | [git-scm.com](https://git-scm.com) |
| GitHub | Remote repository; Claude Code pushes here | [github.com](https://github.com) |

---

## Assignment

Use Claude Code to scaffold your final project directory and write an initial working Streamlit app.

**Steps:**

1. Choose a Taiwan open data topic for your final project (suggestions: air quality, earthquake records, public health statistics, transit ridership, water quality).
2. Find the dataset on [data.gov.tw](https://data.gov.tw/en) or [EPA open data portal](https://data.epa.gov.tw/en/). Download a sample CSV.
3. Open a terminal in a new folder and start Claude Code. Prompt it to:
   - Scaffold the project directory structure (app.py, data/, utils/, requirements.txt, README.md, .gitignore)
   - Write a `utils/fetch_data.py` that loads your sample CSV with pandas
   - Write a minimal `app.py` that displays the dataset title, a dataframe preview, and one chart
4. Run `streamlit run app.py` and confirm the app launches without errors.
5. Initialize a git repository, make an initial commit, and push to a new GitHub repository.

Submit the GitHub repository URL on the course portal before Week 10.

---

## Resources

- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Anthropic prompt engineering guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [Karpathy (2025) — "Vibe Coding" concept](https://x.com/karpathy/status/1886192184808149383)
- [Karpathy's Claude Coding Notes (2026)](Karpathy_2026_Claude_Coding_Notes.qmd) — supplementary reading in this folder
- [data.gov.tw — Taiwan Open Data Portal](https://data.gov.tw/en)
- [Node.js download](https://nodejs.org/en/download)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 10 | Agentic workflows — multi-step tasks, git branching, GitHub Actions CI |
| 11 | Streamlit — widgets, layout, caching, deployment |
| 12 | Taiwan open data APIs — fetching and cleaning real datasets |
| 16 | **Final milestone:** Present your completed web app |
