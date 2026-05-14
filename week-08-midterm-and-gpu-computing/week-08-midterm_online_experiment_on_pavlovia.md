# Week 08: MILESTONE — Midterm: Online Experiment on Pavlovia

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Week:** 8 of 16 | **Date:** 2026-04-16 | **Room:** TBA

---

## Overview

This is the midterm milestone for Part 1 of the course. There is no new programming content this week. Instead, you will deploy your Posner spatial-cueing experiment to Pavlovia, collect data from classmates, and give a five-minute presentation of your results.

By the end of class, you will have produced and publicly demonstrated a working, browser-based cognitive experiment — the same standard used in published online behavioural studies.

---

## Learning Objectives

By the end of this week you will be able to:

1. Deploy a PsychoPy experiment to Pavlovia and set it to "Running" status
2. Share a Pavlovia experiment URL and collect data from remote participants
3. Download a data CSV from the Pavlovia data dashboard
4. Produce a minimal analysis: mean RT and accuracy by condition with error bars
5. Present a 5-minute experiment demo and results summary to the class
6. Identify and fix at least one PsychoJS compatibility issue

---

## Pavlovia Upload Checklist

Complete every item before class. Experiments that do not pass this checklist cannot be presented.

```
TECHNICAL CHECKLIST
-------------------
[ ] Experiment runs locally without errors in PsychoPy Coder
[ ] All file paths are relative (no /Users/name/... absolute paths)
[ ] No pandas or other non-PsychoJS imports in the main script
[ ] Data saved with psychopy.data.ExperimentHandler (not manually with csv module)
[ ] All images, audio, or resource files are inside the experiment folder
[ ] A GitLab repository has been created on the Pavlovia dashboard
[ ] Experiment folder pushed to the GitLab repo (git push)
[ ] Experiment status set to "Running" on the Pavlovia dashboard
[ ] Pilot URL tested in both Chrome and Firefox
[ ] CSV data file appears in Pavlovia data folder after a complete pilot run
[ ] Escape key is handled gracefully (experiment exits cleanly, partial data saved)

CONTENT CHECKLIST
-----------------
[ ] Participant info dialog collects Subject ID and Session number
[ ] Instructions screen clearly describes the task
[ ] At least 20 trials with both valid and invalid cue conditions
[ ] Fixation cross present on every trial
[ ] Inter-trial interval between trials
[ ] End-of-experiment thank-you screen
```

---

## Switching to `ExperimentHandler`

Pavlovia requires `psychopy.data.ExperimentHandler` for data saving. Replace the pandas `save_data()` function from Week 07 with this pattern:

```python
from psychopy import data

# Create the handler at the start of the experiment
exp = data.ExperimentHandler(
    name="PosnerTask",
    version="1.0",
    extraInfo=info,           # the dict from gui.DlgFromDict
    dataFileName=f"data/{info['Participant ID']}_session{info['Session']}",
)

# Inside your trial loop, after collecting the response:
exp.addData("trial_num",  trial["trial_num"])
exp.addData("validity",   trial["validity"])
exp.addData("cue",        trial["cue"])
exp.addData("target",     trial["target"])
exp.addData("response",   response)
exp.addData("rt",         rt)
exp.addData("correct",    correct)
exp.nextEntry()   # advance to the next row

# At the very end:
exp.saveAsWideText(exp.dataFileName + ".csv")
```

`ExperimentHandler` is compatible with both local runs and Pavlovia's cloud data storage.

---

## Presentation Format

Each student gives a **5-minute presentation** structured as follows:

| Section | Time | Content |
|---------|------|---------|
| Task overview | 1 min | What is the Posner spatial-cueing task? What is the prediction? |
| Live demo | 1 min | Open the Pavlovia URL and show a classmate completing 4–6 trials |
| Data summary | 2 min | Show 2–3 figures: RT by validity, accuracy by validity, RT distribution |
| Reflection | 1 min | What worked? What would you change for a real study? |

Slides are optional. A Jupyter notebook or a printed figure is sufficient for the data summary section.

---

## Minimum Analysis

Produce the following analysis from your downloaded Pavlovia data CSV:

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/posner_combined.csv")

# Exclude non-responses and RT outliers
df = df.dropna(subset=["rt"])
df = df[(df["rt"] > 100) & (df["rt"] < 1500)]

# Mean RT and accuracy by validity condition
summary = df.groupby("validity").agg(
    mean_rt   = ("rt",      "mean"),
    sem_rt    = ("rt",      lambda x: x.std() / len(x)**0.5),
    accuracy  = ("correct", "mean"),
    n_trials  = ("rt",      "count"),
).reset_index()

print(summary.round(2))

# Bar chart: mean RT by validity
fig, axes = plt.subplots(1, 2, figsize=(9, 4))

axes[0].bar(summary["validity"], summary["mean_rt"],
            yerr=summary["sem_rt"], capsize=5,
            color=["#4C72B0", "#DD8452"])
axes[0].set_ylabel("Mean RT (ms)")
axes[0].set_title("Reaction Time by Cue Validity")

axes[1].bar(summary["validity"], summary["accuracy"],
            color=["#4C72B0", "#DD8452"])
axes[1].set_ylabel("Proportion correct")
axes[1].set_ylim(0, 1.05)
axes[1].set_title("Accuracy by Cue Validity")

plt.tight_layout()
plt.savefig("midterm_results.png", dpi=150)
plt.show()
```

You should observe faster RTs on valid trials than invalid trials — the classic Posner cueing effect (typically 20–80 ms advantage).

---

## Grading Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| Experiment runs online | 35 | Pavlovia URL is accessible; experiment runs to completion without errors |
| Data collected correctly | 25 | CSV file contains correct columns; at least 5 complete participant runs |
| Analysis with 2+ figures | 25 | Bar charts for RT and accuracy by validity; axes labelled; error bars shown |
| Presentation clarity | 15 | Task explained clearly; data figures shown; live demo performed |
| **Total** | **100** | |

**Deductions:** −10 if experiment requires Escape to exit rather than finishing naturally; −10 if absolute file paths cause the experiment to fail on a different machine.

---

## Common PsychoJS Compatibility Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| `import pandas` | Experiment fails to load | Use `ExperimentHandler` instead |
| `import os` | Runtime error in browser | Use `psychopy.data` for paths |
| Absolute file paths | Images/audio not found | Use relative paths: `"images/stim.png"` |
| `f-strings` (older PsychoJS) | Syntax error | Test with Pavlovia's PsychoJS version |
| `core.wait()` inside a long loop | Timing drift online | Use frame-based timing for short intervals |

---

## Resources

- [Pavlovia documentation](https://pavlovia.org/docs/home)
- [PsychoPy → Pavlovia guide](https://psychopy.org/online/fromBuilder.html)
- [PsychoJS compatibility table](https://psychopy.org/online/psycojsCode.html)
- [psychopy.data.ExperimentHandler](https://www.psychopy.org/api/data.html#psychopy.data.ExperimentHandler)
- [Posner (1980) — original cueing paper](https://doi.org/10.1080/00335558008248231)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 09 | **Part 2 begins:** Vibe Coding & Claude Code — AI-assisted application development |
| 10 | Agentic workflows, git branching, GitHub Actions CI |
| 11 | Building interactive web apps with Streamlit |
| 16 | **Final milestone:** Live web app presentation using Taiwan open data |
