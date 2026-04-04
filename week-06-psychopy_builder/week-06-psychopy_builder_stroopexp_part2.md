# Advanced PsychoPy: Code Components & Online Experiments

This guide builds on the basic Stroop experiment from Part 1. It covers two key advances: **using Code Components** for flexible stimulus control, and **deploying your experiment online** via Pavlovia.

---

## Part A: Code Components for Flexible Stimulus Control

### The Problem with Spreadsheet-Only Designs

Traditional PsychoPy loops randomize entire rows. If you have a "Word" column and a "Color" column, they stay locked together. The goal is to use code to randomize words and colors **separately**, programmatically determine congruency, and derive correct keys — all without hard-coding them into a spreadsheet.

### Stimulus Sets and Loader Loops

* **The "Simple" Stimulus File:** Create an Excel sheet with just the basic building blocks (e.g., four words and four colors) rather than every possible combination.
* **The Loader Loop:**
    * Create a routine (e.g., `stimulus_loader`) before the actual experiment starts.
    * Wrap it in a loop that pulls from your Excel file.
    * **Crucial Setting:** Uncheck **"Is trials"** in the loop properties. This prevents PsychoPy from recording these "loading" steps as actual data points.
    * **Selection:** Can be set to "sequential" since we will randomize the order ourselves via code later.

### Code Components Interface

* Code components have a **Python** side (left) for local experiments and a **JavaScript** side (right) for online experiments via Pavlovia.
* **Code Modes:**
    * **Auto->JS:** Automatically translates Python to JavaScript. Great for beginners, but not always perfect.
    * **Both:** Allows you to edit both sides independently. Essential for fixing functions that don't translate directly.
* **The Tabs (Execution Timing):**
    * **Before Experiment:** For universal variables or custom functions.
    * **Begin Experiment:** For initial setup (e.g., creating empty lists).
    * **Begin Routine:** Runs at the start of the specific routine containing the code.
    * **Each Frame:** Runs every screen refresh (e.g., for timing-based triggers).
    * **End Routine:** Runs once the routine finishes.

### Loading Stimuli with Code

1. At **Begin Experiment**, initialize empty lists: `word_list = []` and `color_list = []`.
2. At **Begin Routine** (inside the Loader Loop), use `.append()` to add the current row's variables: `word_list.append(word)`.

This effectively "imports" your spreadsheet into Python memory so you can manipulate it.

### Randomizing Stimuli

Use the Python function `shuffle()`. By calling `shuffle(word_list)` and `shuffle(color_list)` independently, you create a unique, randomized arrangement of trials where word-color pairings are no longer tied to the original spreadsheet rows.

### Cycling Stimuli with Counters

Since we aren't using a "Conditions" file in our actual trial loop, we need a counter to index into the lists:

1. Set `current_item = -1` at the start of the experiment.
2. Inside the Stroop trial routine, at **Begin Routine**, increment it: `current_item += 1`.
3. Define variables for the trial: `trial_word = word_list[current_item]` and `trial_color = color_list[current_item]`.

### Deriving Correct Keys Programmatically

Instead of writing the correct key in Excel, derive it from the color:

```python
correct_key = trial_color[0]  # "red" → "r"
```

This makes your experiment more robust; if you add the color "purple" later, the code handles the key assignment automatically.

### Determining Congruency On-the-Fly

Since pairings are random, check if they match during each trial:

```python
if trial_word.upper() == trial_color.upper():
    congruency = 'congruent'
else:
    congruency = 'incongruent'
```

> **Tip:** Use `.upper()` or `.lower()` when comparing strings to avoid bugs caused by case sensitivity (e.g., "Red" vs "red").

### Builder Tips

* **Execution Order:** PsychoPy executes objects in a routine from top to bottom. Always move your Code Component to the **top** of the routine list, or the text component may try to use a variable before the code has defined it.
* **Dynamic Repetitions:** In the trial loop properties, set a variable like `list_length = len(word_list)` instead of hard-coding repeats. This adjusts automatically if you add words to your Excel file.
* **Duplicating Items:** If you only have 4 items but want 20 trials, use a nested `for` loop in the Loader routine to append the same item multiple times before shuffling.
* **Direct List References:** In Builder components (like a Text stim), you can reference the list directly using the dollar sign: `$word_list[current_item]`.

---

## Part B: Taking Your Experiment Online (Pavlovia)

### Uploading to Pavlovia

Syncing your experiment to **Pavlovia** converts it to HTML/JavaScript. This is where "Auto→JS" translation errors usually appear, since Python and JavaScript are fundamentally different languages.

### Python → JavaScript Translation Reference

When using Code Components for online experiments, you must ensure your code works in **both** Python and JavaScript. Set the Code Component mode to **"Both"** so you can edit each side independently.

| Task | Python | JavaScript |
|------|--------|------------|
| Append to list | `my_list.append(item)` | `my_list.push(item)` |
| Shuffle a list | `shuffle(my_list)` | `shuffle = util.shuffle;`* then `shuffle(my_list)` |
| Uppercase string | `my_str.upper()` | `my_str.toUpperCase()` |
| Lowercase string | `my_str.lower()` | `my_str.toLowerCase()` |
| Log custom data | `thisExperiment.addData('col', val)` | `psychojs.experiment.addData('col', val)` |

> \* Define `shuffle = util.shuffle;` once in the **Begin Experiment** tab on the JavaScript side. JavaScript has no native `shuffle` function.

### Logging Custom Variables to Data Files

Variables created in Code Components are **not** saved to your `.csv` file automatically. You must explicitly log them:

**Python side:**
```python
thisExperiment.addData('word', trial_word)
thisExperiment.addData('color', trial_color)
thisExperiment.addData('congruency', congruency)
```

**JavaScript side:**
```javascript
psychojs.experiment.addData('word', trial_word);
psychojs.experiment.addData('color', trial_color);
psychojs.experiment.addData('congruency', congruency);
```

> **Important:** Without these calls, your congruency calculations and custom labels will **not** appear in your final data file.

### Debugging Online Experiments

When your experiment fails online:

1. Open the browser's **Developer Console** with `Ctrl+Shift+I` (Chrome).
2. Go to the **Console** tab to see JavaScript error messages.
3. The error message will point to the line where the JS code is breaking — cross-reference it with your Code Component.
4. Common culprits: untranslated Python functions (`.append()`, `.upper()`, `shuffle()`).

---

**Reference Video:**

* [Getting Started with PsychoPy (Part 2) | Loops, Variables, and Pavlovia](https://www.youtube.com/watch?v=xkQ6HRoBMR8)