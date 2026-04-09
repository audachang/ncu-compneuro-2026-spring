# Week 07 Homework: Stroop 實驗資料分析 — NumPy, Pandas & Matplotlib

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Due:** Before Week 08 (2026-04-16) | **Submit via:** eeclass

---

## Overview

This week you learned the three core data-science libraries for behavioral research: **NumPy** (fast numerical computation), **Pandas** (tabular data with labels), and **Matplotlib** (publication-quality figures). In this homework, you will integrate all three to perform a complete data analysis pipeline — from raw data simulation to a polished multi-panel summary figure — mirroring what you would do after running a real Stroop experiment.

---

## Scenario: Stroop Color-Word Task

You are analyzing data from a Stroop color-word interference experiment. The experiment has:

- **20 participants** (P01–P20)
- **2 conditions**: `congruent` and `incongruent`
- **40 trials per condition per participant** (80 total trials each)
- Measured variables: `rt_ms` (reaction time in milliseconds), `correct` (1 = correct, 0 = error)

---

## 題目一：Data Simulation with NumPy (25 pts)

使用 NumPy 模擬 20 位受試者的 Stroop 實驗資料。

### Requirements / 要求：

1. **Set a random seed** (`np.random.default_rng(2026)`) for reproducibility.
2. For each participant, simulate 80 trials (40 congruent + 40 incongruent):
   - **Congruent RT**: Draw from `Normal(μ=520, σ=80)` ms
   - **Incongruent RT**: Draw from `Normal(μ=620, σ=100)` ms
   - **Accuracy**: Congruent = 95% correct, Incongruent = 85% correct (use `rng.binomial(1, p, size=n)`)
3. **Store the data** as a Pandas DataFrame with columns:
   `subject`, `trial`, `condition`, `rt_ms`, `correct`
4. **Print**:
   - Total DataFrame shape (should be 1600 rows × 5 columns)
   - First 10 rows (`df.head(10)`)
   - Data types (`df.dtypes`)

### Hints / 提示：

- Use a `for` loop over subjects and conditions, appending rows to a list, then create the DataFrame at the end.
- Subject IDs should be formatted as `"P01"`, `"P02"`, ..., `"P20"`.
- Trial numbers should be 1–40 within each condition per subject.

---

## 題目二：Data Cleaning with Boolean Masking (20 pts)

清理資料：移除錯誤試次和異常反應時間。

### Requirements / 要求：

1. **Remove error trials**: Keep only rows where `correct == 1`.
2. **Remove RT outliers**: Within each participant, remove RTs that are more than **2.5 standard deviations** from that participant's mean RT. Use a loop over subjects or `groupby` + `transform`.
3. **Remove physiologically implausible RTs**: Remove any RT < 150 ms or > 1500 ms.
4. **Print a cleaning summary**:
   - Original trial count
   - Trials removed by each step
   - Final clean trial count
   - Percentage of data retained
5. **Save the cleaned DataFrame** to `stroop_clean.csv` (no index column).

### Hints / 提示：

- Apply the three filters in sequence: errors → outliers → implausible RTs.
- For per-subject outlier removal, you can use:
  ```python
  # Method using groupby + transform
  mean_by_subj = df_correct.groupby("subject")["rt_ms"].transform("mean")
  std_by_subj  = df_correct.groupby("subject")["rt_ms"].transform("std")
  mask = np.abs(df_correct["rt_ms"] - mean_by_subj) <= 2.5 * std_by_subj
  ```

---

## 題目三：Descriptive Statistics with Pandas groupby (20 pts)

使用 Pandas 的 groupby 功能計算描述統計量。

### Requirements / 要求：

Using the **cleaned** DataFrame from 題目二:

1. **Compute per-subject, per-condition summary**: Create a summary table with `mean`, `std`, `median`, and `count` of RT for each subject × condition combination. Print the first 10 rows.

2. **Compute the Stroop interference cost** for each subject:
   ```
   interference_cost = mean_RT(incongruent) − mean_RT(congruent)
   ```
   Use `pivot_table` to reshape the data, then subtract columns. Print all 20 subjects' costs.

3. **Overall condition means**: Compute the grand mean and SEM (standard error of the mean) of RT for each condition across all subjects (use the per-subject means as data points, not individual trials — this is the correct between-subjects analysis).

4. **Print a summary** that includes:
   - Mean RT ± SEM for congruent and incongruent conditions
   - Mean interference cost ± SD across subjects
   - Range of interference costs (min–max)

---

## 題目四：Multi-Panel Summary Figure with Matplotlib (35 pts)

使用 Matplotlib 繪製一個包含四個子圖的完整實驗摘要圖表。

### Requirements / 要求：

Create a **2 × 2** figure (`figsize=(12, 10)`) with the following panels:

#### Panel A (top-left): RT Distribution Comparison
- Overlapping histograms of RT for congruent (blue) and incongruent (orange) conditions.
- Use `density=True` and `alpha=0.6` so both distributions are visible.
- Add vertical dashed lines for each condition's mean (same colors).
- Include axis labels, title, and legend.

#### Panel B (top-right): Mean RT Bar Chart
- Bar chart comparing mean RT for congruent vs. incongruent conditions.
- Include **SEM error bars** with `capsize=5`.
- Use distinct colors and set y-axis starting from 0.
- Add the mean value as text above each bar.

#### Panel C (bottom-left): Per-Subject Interference Cost
- Horizontal bar chart (`ax.barh()`) showing the interference cost for each of the 20 subjects (sorted from largest to smallest).
- Draw a vertical dashed red line at the group mean.
- Label the y-axis with subject IDs.

#### Panel D (bottom-right): Speed–Accuracy Trade-off
- Scatter plot with mean RT (x-axis) vs. accuracy (y-axis) for each subject.
- Color the dots by condition (use congruent and incongruent means separately, or average across conditions — your choice).
- Add axis labels and title.

#### Figure-level requirements:
- Add a **figure-level title**: `"Stroop Task: Experiment Summary"` using `fig.suptitle()`.
- Label each panel as **(A)**, **(B)**, **(C)**, **(D)** using `ax.text()` or `ax.set_title("(A) ...")`.
- Call `plt.tight_layout()`.
- **Save the figure** as both `stroop_summary.png` (dpi=150) and `stroop_summary.pdf`.

---

## Deliverables / 繳交內容

Submit a **single ZIP file** to eeclass containing:

| File | Description |
|------|-------------|
| `week07_analysis.ipynb` or `week07_analysis.py` | Your complete analysis code (Jupyter notebook preferred) |
| `stroop_clean.csv` | Cleaned data output from 題目二 |
| `stroop_summary.png` | Multi-panel summary figure |
| `stroop_summary.pdf` | Same figure in vector format |

> **Note:** If using a Jupyter notebook, ensure all cells are executed and output is visible. If using a `.py` script, include printed output in a separate `output.txt` file.

---

## Grading Rubric (100 pts)

| Criterion | Points | Details |
|-----------|--------|---------|
| **題目一：Data Simulation** | 25 | Correct use of `default_rng`; correct distribution parameters; DataFrame has correct shape and column names; properly formatted subject IDs |
| **題目二：Data Cleaning** | 20 | Three filtering steps applied in sequence; per-subject outlier removal (not global); cleaning summary printed; CSV saved correctly |
| **題目三：Descriptive Stats** | 20 | Per-subject per-condition summary; interference cost via pivot_table; between-subjects grand means with SEM (not within-trial SEM); clear printed summary |
| **題目四：Summary Figure** | 35 | All 4 panels present and correct; appropriate plot types; axis labels and titles; error bars on bar chart; figure saved in both PNG and PDF formats |

### Bonus (up to 10 pts)

- **(+5 pts)** Add a **panel E** to the figure: a line plot showing RT across trial positions (1–40) averaged over subjects, with separate lines for congruent and incongruent, to visualize practice/fatigue effects.
- **(+5 pts)** Add a **paired-samples t-test** (or Wilcoxon signed-rank test) comparing congruent vs. incongruent mean RTs across subjects. Print the test statistic and p-value. You may use `scipy.stats.ttest_rel()`.

---

## Tips / 提示

- **Start with 題目一**, since all later questions depend on the simulated data.
- **Run each section in order** — the cleaning in 題目二 produces the DataFrame used in 題目三 and 題目四.
- **Between-subjects SEM**: When reporting the SEM for a bar chart, use per-subject means (20 values), not per-trial values (hundreds of values). The formula is `std / sqrt(n)` where `n` is the number of subjects (20), not the number of trials.
- **`plt.tight_layout(rect=[0, 0, 1, 0.96])`** — if `suptitle` overlaps with panel titles, use the `rect` parameter.
- Check that your CSV file can be re-loaded with `pd.read_csv()` without errors.

---

## Resources / 參考資料

- Week 07 lecture notes:
  - `week-07-numpy_and_data_manipulation.md`
  - `week-07-pandas_and_dataframes.md`
  - `week-07-data_visualization_with_matplotlib.md`
- Week 07 puzzle notebook: `week-07-puzzles.ipynb` (especially Puzzles 1–10 for worked examples)
- [NumPy Random Generator](https://numpy.org/doc/stable/reference/random/generator.html)
- [Pandas GroupBy](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [Matplotlib Subplots](https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html)
