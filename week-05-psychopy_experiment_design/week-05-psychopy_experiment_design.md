# Week 05: PsychoPy Experiment Design

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Week:** 5 of 16 | **Date:** 2026-03-26 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Structure a PsychoPy experiment into well-defined functions (setup, run trial, save, quit)
2. Generate and shuffle a condition list with `random.shuffle`
3. Present a participant information dialog with `gui.DlgFromDict`
4. Record reaction time by resetting `core.Clock` at stimulus onset
5. Store trial data as a list of dicts and save to CSV with pandas
6. Implement block structure with rest screens between blocks
7. Generate full factorial trial conditions procedurally using `itertools` in Python

---

## In-Class Topics

### 1. Experiment Structure (10 min)

A well-structured experiment separates concerns into distinct functions. This makes code easier to read, test, and reuse.

```
posner_task.py
├── show_instructions(win)         — display text, wait for key
├── run_trial(win, clock, params)  — one trial, returns result dict
├── run_block(win, clock, trials)  — loop over trials, collect results
├── show_rest(win, block, n)       — rest screen between blocks
└── save_data(results, subject_id) — write CSV
```

Keeping each function short (under ~30 lines) makes debugging much faster and each piece independently testable.

---

### 2. Participant Information Dialog (15 min)

```python
from psychopy import gui, core
import datetime

info = {
    "Participant ID": "",
    "Age": "",
    "Session": 1,
    "Date": datetime.date.today().isoformat(),
}

# Show the dialog — execution blocks until the participant clicks OK or Cancel
dlg = gui.DlgFromDict(info, title="Posner Task", fixed=["Date"])

if not dlg.OK:
    core.quit()   # user pressed Cancel

subject_id = info["Participant ID"]
session    = info["Session"]
```

The `fixed` list specifies fields that are shown but cannot be edited. Always include the date as a fixed field so data files are easy to sort by run order.

---

### 3. Building the Trial List (20 min)

Define all unique conditions explicitly, then replicate and shuffle.

```python
import random

# All unique conditions (one dict per unique combination)
conditions = [
    {"cue": "left",  "target": "left",  "validity": "valid"},
    {"cue": "right", "target": "right", "validity": "valid"},
    {"cue": "left",  "target": "right", "validity": "invalid"},
    {"cue": "right", "target": "left",  "validity": "invalid"},
]

# 5 reps of each → 20 trials total (80% valid, 20% invalid)
n_reps     = 5
trial_list = conditions * n_reps

random.shuffle(trial_list)

# Add sequential trial numbers after shuffling
for i, trial in enumerate(trial_list):
    trial["trial_num"] = i + 1
```

Using a list-of-dicts means each trial carries its own condition metadata. No need to track indices separately.

---

### 4. Running a Single Trial (25 min)

```python
from psychopy import visual, core, event

def run_trial(win, clock, params):
    """
    Present one trial. Returns a dict with response, RT, and accuracy.

    params keys expected: "cue", "target", "validity", "trial_num"
    """
    cue_x   = -0.5 if params["cue"]    == "left" else 0.5
    tgt_x   = -0.5 if params["target"] == "left" else 0.5

    fixation = visual.TextStim(win, text="+", color="white", height=0.10)
    cue_box  = visual.Rect(win, width=0.06, height=0.06,
                           pos=(cue_x, 0), lineColor="yellow", fillColor=None)
    target   = visual.TextStim(win, text="*", color="white",
                               height=0.12, pos=(tgt_x, -0.20))

    # Fixation: 500 ms
    fixation.draw()
    win.flip()
    core.wait(0.5)

    # Cue: 100 ms
    fixation.draw()
    cue_box.draw()
    win.flip()
    core.wait(0.1)

    # SOA blank: 400 ms
    fixation.draw()
    win.flip()
    core.wait(0.4)

    # Target: collect response within 1500 ms
    target.draw()
    win.flip()
    clock.reset()   # anchor RT to target onset

    keys = event.waitKeys(
        maxWait=1.5,
        keyList=["left", "right", "escape"],
        timeStamped=clock,
    )

    # Inter-trial interval: 500 ms blank
    win.flip()
    core.wait(0.5)

    # Handle escape
    if keys and keys[0][0] == "escape":
        win.close()
        core.quit()

    if not keys:
        return {**params, "response": None, "rt": None, "correct": False}

    key, rt = keys[0]
    correct = (key == params["target"])
    return {**params, "response": key, "rt": round(rt * 1000, 2), "correct": correct}
```

`{**params, "response": ..., "rt": ...}` merges the condition dict with the response fields in a single expression.

---

### 5. Block Structure and Rest Screens (15 min)

```python
def show_rest(win, block_num, n_blocks):
    msg = visual.TextStim(
        win,
        text=(f"Block {block_num} of {n_blocks} complete.\n\n"
              "Take a short break.\nPress SPACE when ready."),
        color="white",
        height=0.07,
        wrapWidth=1.6,
    )
    msg.draw()
    win.flip()
    event.waitKeys(keyList=["space"])


def run_experiment(win, all_trials, n_blocks=2):
    clock             = core.Clock()
    results           = []
    trials_per_block  = len(all_trials) // n_blocks

    for b in range(n_blocks):
        block_trials = all_trials[b * trials_per_block : (b + 1) * trials_per_block]

        for params in block_trials:
            result          = run_trial(win, clock, params)
            result["block"] = b + 1
            results.append(result)

        if b < n_blocks - 1:
            show_rest(win, b + 1, n_blocks)

    return results
```

---

### 6. Saving Data with pandas (15 min)

```python
import pandas as pd
import os

def save_data(results, subject_id, session):
    df = pd.DataFrame(results)

    os.makedirs("data", exist_ok=True)
    filename = f"data/{subject_id}_session{session}.csv"
    df.to_csv(filename, index=False)

    print(f"\nData saved to: {filename}")
    summary = df.groupby("validity")["rt"].agg(["mean", "count"])
    print(summary.round(1))
```

Always save to a dedicated `data/` subdirectory. Never write data files to the root of the experiment folder, and never commit data files to version control — add `data/` to `.gitignore`.

---

### 7. Advanced Sequence Generation and Counterbalancing (20 min)

When designing complex experiments in Coder, hardcoding every condition becomes impractical. Instead, we can procedurally generate full factorial designs using Python's `itertools` module. This allows you to scale up variables easily without making copy-paste errors.

```python
import itertools
import random

# Define independent variables
cues = ["left", "right"]
targets = ["left", "right"]
soas = [0.1, 0.3, 0.5]  # Stimulus onset asynchronies in seconds

# Generate all 2 x 2 x 3 = 12 unique combinations
all_combinations = list(itertools.product(cues, targets, soas))

# Build a list of condition dictionaries
conditions = []
for cue, target, soa in all_combinations:
    # Programmatically determine validity
    validity = "valid" if cue == target else "invalid"
    
    conditions.append({
        "cue": cue,
        "target": target,
        "soa": soa,
        "validity": validity
    })

# If we want unequal probing (e.g., 80% valid, 20% invalid), we can filter or duplicate certain dicts here.
# For a raw uniform distribution:
n_reps = 5
trial_list = conditions * n_reps
random.shuffle(trial_list)
```

By generating the structural matrix programmatically, we unlock the full power of Coder over Builder. We can instantly add a third cue type simply by adding a string to the `cues` list, and the entire design expands dynamically.

---

## Neuroscience Connection

| Design element | Scientific rationale |
|---------------|---------------------|
| Participant info dialog | Records demographic metadata; required for IRB-approved studies |
| Randomized trial order | Controls for order effects and learning across trials |
| Fixed SOA cue-target structure | Controls temporal expectancy; produces clean RT separation |
| Block structure with rest | Reduces fatigue effects; enables practice and fatigue analysis |
| CSV with condition columns | Enables per-condition RT and accuracy analysis in Python or R |

---

## Tools This Week

| Tool | Purpose | Install |
|------|---------|---------|
| PsychoPy | Experiment presentation | `pip install psychopy` (from Week 04) |
| `psychopy.gui` | Participant info dialog | included with psychopy |
| pandas | Save results to CSV | `pip install pandas` |
| `itertools` | Structural matrix generation | Built-in Python library |

---

## Assignment

Extend your Week 04 script into a complete Posner spatial-cueing experiment (`week-05-posner-task.py`):

1. Show a participant info dialog collecting Subject ID, Age, and Session number.
2. Display a written instructions screen and wait for SPACE.
3. Run 2 blocks of 20 trials each (40 trials total):
   - 80% valid cues, 20% invalid cues, randomized within each block.
   - Cue-target SOA of 500 ms (100 ms cue + 400 ms blank).
   - Response window of 1500 ms; collect left/right arrow key responses.
   - Show a rest screen between blocks.
4. Save all trial data to `data/<subject_id>_session<N>.csv` with pandas.
   - Required columns: `subject_id`, `session`, `block`, `trial_num`, `cue`, `target`, `validity`, `response`, `rt`, `correct`
5. Print mean RT and accuracy per validity condition (valid vs. invalid) to the terminal.

Submit `week-05-posner-task.py` and one example CSV file from `data/` before Week 06.

---

## Resources

- [PsychoPy gui module](https://www.psychopy.org/api/gui.html)
- [PsychoPy data module](https://www.psychopy.org/api/data.html)
- [Python itertools module](https://docs.python.org/3/library/itertools.html)
- [Posner (1980) — original spatial cueing paradigm](https://doi.org/10.1080/00335558008248231)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 06 | NumPy arrays, indexing, vectorized operations |
| 07 | Data Visualization with Matplotlib |
| 08 | **Midterm:** Upload experiment to Pavlovia, run an online pilot, present results |
