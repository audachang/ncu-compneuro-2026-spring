# Week 06: PsychoPy Basics — Stimuli & Windows

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Week:** 6 of 16 | **Date:** 2026-04-02 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Install PsychoPy and create a `visual.Window` with the correct screen units
2. Draw text, rectangle, and grating stimuli using the draw-flip loop
3. Control experiment timing with `core.Clock` and `core.wait()`
4. Capture keyboard responses with `event.getKeys()` and `event.waitKeys()`
5. Explain the difference between `norm`, `pix`, and `deg` coordinate systems
6. Measure frame duration and identify timing errors using flip timestamps
7. Build a minimal attention-cue + target display as a working PsychoPy script

---

## In-Class Topics

### 1. Installing PsychoPy (15 min)

The recommended installation for coding is the `psychopy` pip package inside a dedicated conda environment. The standalone installer includes a Builder GUI but is harder to automate.

```bash
conda create -n psychopy python=3.10
conda activate psychopy
pip install psychopy
```

Verify the installation:

```python
import psychopy
print(psychopy.__version__)
```

> On macOS you may also need `pip install pyobjc`. On Linux, `pip install psychopy[all]` installs audio and hardware drivers.

---

### 2. Creating a Window (15 min)

```python
from psychopy import visual, core

# Open a window (use fullscr=True for real experiments)
win = visual.Window(
    size=(1280, 720),
    color=(0, 0, 0),       # background: mid-grey in -1 to +1 range
    units="norm",          # coordinate system
    fullscr=False,
)

core.wait(2.0)   # keep the window open for 2 seconds
win.close()
core.quit()
```

**Screen units comparison:**

| Unit | Range | When to use |
|------|--------|-------------|
| `norm` | −1 to +1 on each axis | Quick demos, layout |
| `pix` | Pixels from screen centre | Precise pixel control |
| `deg` | Visual degrees from screen centre | Psychophysics experiments (requires monitor calibration) |

---

### 3. Drawing Stimuli (25 min)

All stimuli follow the same pattern: create once, update attributes as needed, then call `.draw()` before `win.flip()`.

**TextStim:**
```python
from psychopy import visual

win = visual.Window(size=(800, 600), color="grey", units="norm")

message = visual.TextStim(
    win,
    text="Press SPACE to begin",
    color="white",
    height=0.08,       # height in norm units
    pos=(0, 0),        # centre of screen
)

message.draw()
win.flip()
```

**Rect (fixation cross built from two rectangles):**
```python
fix_h = visual.Rect(win, width=0.02, height=0.12, fillColor="white", lineColor=None)
fix_v = visual.Rect(win, width=0.12, height=0.02, fillColor="white", lineColor=None)

fix_h.draw()
fix_v.draw()
win.flip()
```

**GratingStim (gratings and Gabor patches):**
```python
gabor = visual.GratingStim(
    win,
    tex="sin",           # sinusoidal grating
    mask="gauss",        # Gaussian envelope
    sf=4.0,              # spatial frequency (cycles per degree)
    size=3.0,            # size in degrees
    ori=45,              # orientation in degrees
    pos=(0, 0),
)

gabor.draw()
win.flip()
```

---

### 4. The Draw-Flip Loop (20 min)

PsychoPy renders to a back buffer. Nothing appears on screen until you call `win.flip()`, which swaps the back buffer to the front in sync with the monitor refresh.

```python
from psychopy import visual, core, event

win = visual.Window(size=(800, 600), color="grey", units="norm", fullscr=False)

fixation = visual.TextStim(win, text="+", color="white", height=0.1)
target   = visual.TextStim(win, text="X", color="yellow", height=0.12, pos=(0.4, 0))

# --- Fixation period: 500 ms ---
fixation.draw()
win.flip()
core.wait(0.5)

# --- Target: 200 ms ---
target.draw()
flip_time = win.flip()   # win.flip() returns the timestamp of the flip
core.wait(0.2)

# --- Blank: 300 ms ---
win.flip()
core.wait(0.3)

win.close()
core.quit()
```

`win.flip()` returns the time (in seconds since experiment start) at which the frame appeared. Store this value to compute precise stimulus onset times.

---

### 5. Timing with `core.Clock` (15 min)

```python
from psychopy import visual, core, event

win    = visual.Window(size=(800, 600), color="grey", units="norm", fullscr=False)
target = visual.TextStim(win, text="X", color="white", height=0.12)
clock  = core.Clock()

target.draw()
win.flip()
clock.reset()   # start timing from this flip

# Wait for any key, record RT
keys = event.waitKeys(maxWait=2.0, keyList=["space", "escape"], timeStamped=clock)

if keys:
    key, rt = keys[0]
    print(f"Key: {key}  RT: {rt*1000:.1f} ms")
else:
    print("No response within 2 s")

win.close()
core.quit()
```

`timeStamped=clock` tells `waitKeys` to record the time of each key press relative to the clock object. Use `clock.reset()` immediately after the stimulus flip to anchor RT to stimulus onset.

---

### 6. Non-blocking Key Checking with `event.getKeys()` (10 min)

Use `event.getKeys()` inside a loop when you need to check for responses while updating the display each frame.

```python
from psychopy import visual, core, event

win   = visual.Window(size=(800, 600), color="grey", fullscr=False)
stim  = visual.TextStim(win, text="Press LEFT or RIGHT", color="white", height=0.08)
clock = core.Clock()

clock.reset()
while clock.getTime() < 3.0:
    stim.draw()
    win.flip()

    keys = event.getKeys(keyList=["left", "right", "escape"])
    if "escape" in keys:
        break
    if "left" in keys or "right" in keys:
        rt = clock.getTime()
        print(f"Response: {keys[0]}  RT: {rt*1000:.1f} ms")
        break

win.close()
core.quit()
```

---

### 7. Frame Timing Check (10 min)

Real experiments require reliable frame timing. Always verify that flips are happening on schedule:

```python
durations = []
for _ in range(60):
    t = win.flip()
    durations.append(t)

frame_diffs = [durations[i+1] - durations[i] for i in range(len(durations)-1)]
mean_frame  = sum(frame_diffs) / len(frame_diffs)
print(f"Mean frame duration: {mean_frame*1000:.2f} ms")
print(f"Expected at 60 Hz: 16.67 ms")
```

Dropped frames (duration > 1.5× expected) indicate that the GPU or CPU cannot keep up. Common causes: running fullscreen video in the background, anti-virus scans, Python garbage collection.

---

## Neuroscience Connection

| PsychoPy feature | Experiment use |
|-----------------|----------------|
| `visual.GratingStim` | Contrast sensitivity, orientation selectivity paradigms |
| `core.Clock` + `timeStamped` | Millisecond-accurate RT measurement |
| `event.waitKeys(maxWait=...)` | Response window with automatic timeout |
| `win.flip()` timestamp | Verify actual stimulus onset time against intended time |
| `units="deg"` | Controlled visual angle for psychophysics |

---

## Tools This Week

| Tool | Purpose | Install |
|------|---------|---------|
| PsychoPy | Stimulus presentation and response collection | `pip install psychopy` |
| `psychopy.visual` | Stimuli: text, shapes, gratings, images | included |
| `psychopy.core` | Timing: Clock, wait | included |
| `psychopy.event` | Keyboard input | included |

---

## Assignment

Write a standalone PsychoPy script (`week-06-attention-cue.py`) that implements the following sequence:

1. Show a welcome message; wait for SPACE to begin.
2. Run 10 trials. On each trial:
   - Show a fixation cross for 500 ms.
   - Show a spatial cue (a small rectangle on the left or right) for 100 ms.
   - Show a blank screen for 400 ms (SOA = 500 ms).
   - Show a target (`"*"`) at a random location (left or right) for 200 ms.
   - Collect a left/right arrow key response with a 1500 ms deadline; record RT.
   - Show a blank inter-trial interval of 500 ms.
3. After all trials, print mean RT and accuracy to the terminal.

Cue validity should be 80% (cue correctly predicts target side 8 of 10 trials). Randomize trial order with `random.shuffle()`.

Submit `week-06-attention-cue.py` by pushing to your GitHub repository before Week 07.

---

## Resources

- [PsychoPy Documentation](https://www.psychopy.org/documentation.html)
- [PsychoPy Coder Tutorial](https://www.psychopy.org/gettingStarted/tutorial1.html)
- [PsychoPy visual stimuli reference](https://www.psychopy.org/api/visual/index.html)
- [Timing in PsychoPy (Peirce & MacAskill, 2018)](https://doi.org/10.3758/s13428-018-01193-y)
- [Screen units explained](https://www.psychopy.org/general/units.html)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 07 | PsychoPy experiment design — trial loops, dialogs, saving CSV data |
| 08 | **Midterm:** Upload complete experiment to Pavlovia and run it online |
| 09 | Vibe Coding — use Claude Code to build applications |
