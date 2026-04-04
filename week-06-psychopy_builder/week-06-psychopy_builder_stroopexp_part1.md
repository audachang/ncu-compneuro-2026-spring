# Building a Stroop Experiment in PsychoPy Builder

This guide walks through creating a complete Stroop experiment from scratch using PsychoPy's graphical Builder interface — from experiment structure through data analysis.

**The Stroop Task:** A classic psychology experiment where subjects name the ink color of a word while ignoring the word's text (e.g., the word "RED" written in blue ink).

---

## Step 1: Design the Experiment Timeline

A professional experiment requires more than just the task itself. Set up four routines in the Builder's Flow panel:

| Order | Routine | Purpose |
|-------|---------|---------|
| 1 | **WelcomeScreen** | Display instructions for the participant |
| 2 | **Blank500** | A 500ms buffer so the first stimulus doesn't appear immediately |
| 3 | **StroopTrial** | The core task *(placed inside a loop)* |
| 4 | **GoodbyeScreen** | A closing message |

> **Pro Tip:** Set the **GoodbyeScreen** on a timer (e.g., 10–20 seconds). This ensures the experiment ends and saves data automatically even if the participant walks away without pressing a key.

## Step 2: Create the Stimulus File

PsychoPy reads trial conditions from an external **Excel file** (e.g., `stroop_stimuli.xlsx`). Each column becomes a variable you can reference in your experiment.

**Minimum required columns:**

| word | color |
|------|-------|
| RED | red |
| GREEN | green |
| BLUE | blue |
| YELLOW | yellow |

You will add more columns in Step 5 below.

## Step 3: Connect the Stimulus File to Builder Components

1. **Create a Loop** around the StroopTrial routine and point it to your Excel file.
2. **Add a Text Component** to the StroopTrial routine:
   * Set the **Text** field to `$word`
   * Set the **Color** field (Appearance tab) to `$color`
   * **Critical:** Change both dropdowns from "constant" to **"set every repeat"**. If left as constant, PsychoPy will crash because it tries to resolve the `$variable` before the loop starts.

## Step 4: Add Keyboard Responses

Add a **Keyboard component** (e.g., `key_stroop`) to the StroopTrial routine:

* **Allowed Keys:** Restrict to the response keys — `'r', 'g', 'b', 'y'`
* **Case Sensitivity:** Always use **lowercase** letters. If you use uppercase `'R'`, the participant would need to hold Shift to respond.
* **Force End of Routine:** Check this box so the next trial starts immediately after a key press.

## Step 5: Add Condition Labels and Automatic Scoring

Go back to your Excel file and add two more columns:

| word | color | congruent | correct_key |
|------|-------|-----------|-------------|
| RED | red | con | r |
| GREEN | blue | incon | b |
| BLUE | blue | con | b |
| ... | ... | ... | ... |

* **`congruent`** — A label to easily sort and filter trials during analysis.
* **`correct_key`** — The key that *should* be pressed for each trial.

**Enable Automatic Scoring:** In the Keyboard component's **Data tab**, check **"Store correct"** and enter `$correct_key`. PsychoPy will automatically create a `key_stroop.corr` column in your output (1 = correct, 0 = incorrect).

## Step 6: Configure Loop Repetitions

* **nReps** determines how many times PsychoPy cycles through your Excel sheet.
  * *Example:* 8 conditions × 5 nReps = 40 total trials.
* **Randomization:** By default, PsychoPy re-randomizes the conditions for each pass through the sheet. If you want all 40 trials in a single randomized pool (where the same word could appear consecutively), duplicate the rows within the Excel sheet itself and set nReps to 1.

## Step 7: Run the Experiment and Read the Data

After running, PsychoPy generates three files in the `/data` folder:

| File Type | Use |
|-----------|-----|
| `.csv` | **Primary data file** — open this for analysis |
| `.log` | Detailed event log for debugging timing issues |
| `.psydat` | PsychoPy's internal format (rarely needed) |

**Understanding the CSV structure:**

* Each **row** = one completed routine.
* Column names follow the pattern `componentName.measure` — e.g., `key_stroop.rt` (reaction time), `key_stroop.corr` (accuracy).
* **`trials.thisN`** — The trial index (starting at 0).
* If you name your keyboard component `key_welcome`, its columns will be `key_welcome.rt`, `key_welcome.keys`, etc. — making it easy to identify which routine each column belongs to.

## Step 8: Summarize Results with Pivot Tables

Pivot Tables are the fastest way to extract meaningful results from raw PsychoPy data.

**Setup:**

1. Save the CSV as an **Excel Workbook (.xlsx)** first (Pivot Tables can't be saved in .csv).
2. **Insert → Pivot Table.** Select your full data range.
3. Configure the layout:
   * **Rows:** Participant ID
   * **Columns:** `congruent` (con vs. incon)
   * **Values:** Average of `key_stroop.rt` and Average of `key_stroop.corr`

> **Filtering for Accuracy:** Add `key_stroop.corr` as a **Filter** and select only `1`. This calculates reaction times **only for correct trials** — a standard requirement in psychological research reporting.

---

**What's Next?** Part 2 covers using **Code Components** to independently randomize words and colors (so any word can appear in any color) and deploying your experiment **online via Pavlovia**.

**Reference Video:** [Your First PsychoPy Experiment (Part 1) | PsychoPy Help #3](https://www.youtube.com/watch?v=Dw8xQf20TtI)
