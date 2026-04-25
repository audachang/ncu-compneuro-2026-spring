# Week 06 Homework: Posner Spatial Cueing Task in PsychoPy Builder

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Due:** Before Week 07 (2026-04-09) | **Submit via:** eeclass

---

## Overview

In Week 05 you built a Posner spatial-cueing experiment using **PsychoPy Coder** (pure Python). This week you will **rebuild the same paradigm in PsychoPy Builder** and **deploy it online via Pavlovia**. This exercise demonstrates the power of Builder for rapid prototyping and highlights the differences between Coder and Builder workflows.

---

## Task: Posner Spatial Cueing Task in Builder

Recreate the Posner task from your Week 05 homework using PsychoPy Builder's graphical interface. The experiment should be functionally equivalent to your Coder version.

### 1. Stimulus File (`posner_conditions.xlsx`)

Create an Excel file with all trial conditions. Required columns:

| cue_side | target_side | validity | soa | correct_key |
|----------|-------------|----------|-----|-------------|
| left | left | valid | 0.5 | left |
| left | right | invalid | 0.5 | right |
| right | right | valid | 0.5 | left |
| right | left | invalid | 0.5 | right |

- **Validity ratio**: Include enough rows to achieve approximately **80% valid / 20% invalid** trials (e.g., 4 valid rows + 1 invalid row per side, then set `nReps` accordingly).
- **`correct_key`**: The arrow key matching the target side.

### 2. Experiment Structure (Routines)

Build the following routines in the Flow panel:

| Order | Routine | Duration | Requirements |
|-------|---------|----------|-------------|
| 1 | **Instructions** | Key press | Display task instructions (Chinese or English): explain that a cue will flash on one side and they should press the arrow key matching the target location as quickly as possible. Wait for SPACE. |
| 2 | **Fixation** | 500 ms | Display a fixation cross (`+`) at screen center. |
| 3 | **Cue** | 100 ms | Display the fixation cross AND a cue stimulus (e.g., a highlighted box or arrow) on either the left or right side. Position determined by `$cue_side`. |
| 4 | **SOA_Blank** | 400 ms | Fixation cross only (cue disappears, target not yet shown). |
| 5 | **Target** | Until response (max 1500 ms) | Display the target (e.g., `*` or `●`) on the left or right side as specified by `$target_side`. Collect keyboard response. |
| 6 | **ITI** | 500 ms | Blank inter-trial interval. |
| 7 | **Rest** | Key press | "Take a break" screen. Shown between blocks. |
| 8 | **Goodbye** | 10 s (auto-end) | Thank-you message with duration timer. |

> **Note:** Routines 2–6 should be placed inside the trial loop. You may combine Fixation + Cue + SOA_Blank into fewer routines if you prefer (e.g., using different components with different start/stop times within a single routine).

### 3. Loop Configuration

- **Trial Loop**: Wrap routines 2–6. Link to `posner_conditions.xlsx`. Set `nReps` to produce **at least 40 trials** total.
- **Block Loop** (optional but recommended): Wrap the trial loop + rest screen to create 2 blocks of 20 trials. Use an outer loop with `nReps=2`.
- **Randomization**: Set loop type to `random`.

### 4. Keyboard Response

In the Target routine, add a **Keyboard component**:

- **Allowed keys**: `'left', 'right'`
- **Force end of routine**: ✅ Checked
- **Store correct**: ✅ Checked, with correct answer set to `$correct_key`
- **Maximum duration**: 1.5 seconds

### 5. Dynamic Stimulus Positioning

Use `$cue_side` and `$target_side` from the Excel file to control stimulus positions. You have two approaches:

**Approach A — Direct coordinate mapping in Excel:**
Add `cue_x` and `target_x` columns to your Excel file (e.g., `-0.5` for left, `0.5` for right). Reference them directly in component Position fields.

**Approach B — Code Component (recommended for learning):**
Add a Code Component at the top of the trial routine. In **Begin Routine**:

```python
# Python side
if cue_side == 'left':
    cue_pos = [-0.5, 0]
else:
    cue_pos = [0.5, 0]

if target_side == 'left':
    target_pos = [-0.5, 0]
else:
    target_pos = [0.5, 0]
```

```javascript
// JavaScript side (for Pavlovia)
if (cue_side === 'left') {
    cue_pos = [-0.5, 0];
} else {
    cue_pos = [0.5, 0];
}

if (target_side === 'left') {
    target_pos = [-0.5, 0];
} else {
    target_pos = [0.5, 0];
}
```

Then set the cue component's Position to `$cue_pos` and the target's Position to `$target_pos` (both **set every repeat**).

---

## Pavlovia Deployment

1. **Sync to Pavlovia**: Click the globe icon (🌐) in Builder and sync to a new Pavlovia project.
2. **Code Type**: If you used Code Components, set the code type to **"Both"** and provide JavaScript equivalents (see above).
3. **Pilot Online**: Set the project to **Piloting** mode. Run the full experiment in your browser and confirm it completes without errors.
4. **Collect Data**: Complete at least **1 full run** online and download the CSV from the Pavlovia dashboard.

> **Debugging tip:** If the experiment fails online, press `Ctrl+Shift+I` to open the browser Developer Console and check the Console tab for JavaScript error messages.

---

## Deliverables

Submit a **single ZIP file** to eeclass containing:

| File | Description |
|------|-------------|
| `*.psyexp` | Your PsychoPy Builder experiment file |
| `posner_conditions.xlsx` | Your conditions Excel file |
| `data/*.csv` | At least 1 complete pilot data CSV (from Pavlovia or local run) |
| `pavlovia_link.txt` | A text file containing your Pavlovia experiment URL |
| `README.md` or `content.html` | Brief description explaining your design choices and any Code Components used |

---

## Grading Rubric (100 pts)

| Criterion | Points | Details |
|-----------|--------|---------|
| **Experiment Structure** | 20 | All required routines present (instructions, fixation, cue, target, ITI, goodbye) |
| **Conditions File** | 15 | Properly formatted Excel with cue_side, target_side, validity, correct_key; 80/20 valid/invalid ratio |
| **Loop & Randomization** | 10 | Loop linked to Excel; ≥ 40 trials; randomization enabled |
| **Cue & Target Positioning** | 15 | Stimuli appear on correct side based on condition; positions update every repeat |
| **Keyboard Response & Scoring** | 10 | Allowed keys restricted; force end of routine; Store correct enabled |
| **Pavlovia Deployment** | 15 | Experiment synced and runnable online; Pavlovia link submitted |
| **Pilot Data** | 10 | At least 1 complete CSV with all expected columns (RT, accuracy, condition labels) |
| **Documentation** | 5 | Clear description of design and Code Components |

---

## Tips

- **"set every repeat"**: Any component field referencing a `$variable` from your Excel file must have its dropdown changed from "constant" to **"set every repeat"**. Forgetting this will crash the experiment.
- **Execution order**: If you use Code Components, drag them to the **top** of the routine panel so variables are defined before other components reference them.
- **Reuse your Week 05 logic**: Your Coder script already has the correct timing, trial structure, and response logic — use it as a blueprint for setting up the Builder routines.
- **Test locally first**: Always run the experiment locally before syncing to Pavlovia. Fix all local errors before attempting online deployment.

---

## Resources

- [PsychoPy Builder Tutorial](https://www.psychopy.org/builder/index.html)
- [Pavlovia Documentation](https://pavlovia.org/docs/home)
- [Your First PsychoPy Experiment (Part 1)](https://www.youtube.com/watch?v=Dw8xQf20TtI)
- [Getting Started with PsychoPy (Part 2) — Loops, Variables, and Pavlovia](https://www.youtube.com/watch?v=xkQ6HRoBMR8)
- Week 05 class materials: `week-05-psychopy_experiment_design.md`
- Week 06 class materials: `week-06-psychopy_builder_stroopexp_part1.md` and `part2.md`
