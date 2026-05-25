# Week 12 Grading Report — Dataset Hygiene & Caching Dashboard

> **Course**: NS5116 | **HW ID**: 69340 | **Due**: 2026-05-20 23:59
> **Graded by**: Automated run (2026-05-20) — **awaiting instructor review before upload**
> **Submissions**: 3/3 students

---

## Summary Scores

| 學生 | A.0 (10) | A.1+A.2 (5) | A.3 (15) | A.4 (20) | A.5 (5) | A.6 (10) | B.1 (10) | B.2 (5) | B.3 (10) | README (10) | Bonus (+5) | **Total** |
|------|----------|-------------|----------|----------|---------|---------|---------|---------|---------|------------|-----------|---------|
| 呂杰驛 (113825002) | 10 | 5 | 14 | 19 | 5 | 10 | 10 | 5 | 10 | 10 | +5 | **98+5** |
| 吳心圓 (113892001) | 10 | 5 | 14 | 18 | 4 | 10 | 10 | 5 | 10 | 10 | 0 | **96** |
| 何官臻 (114825002) | 10 | 5 | 15 | 20 | 5 | 10 | 10 | 5 | 10 | 10 | +2 | **100+2** |

> **Bonus cap**: Rubric allows max +5 bonus; added to base score as noted. Recommend recording as 100 (capped), 96, 100 respectively for eeclass entry.

---

## 呂杰驛 (113825002) — Recommended score: **98** (+5 bonus → cap at 100)

**Submitted**: 2026-05-19 18:21 | **GitHub**: https://github.com/Jie-Yi-Lu/HW12_Dataset-Hygiene-Caching-Dashboard | **Streamlit**: deployed ✓

### Strengths

- **A.0 (10/10)**: Excellent triangulation. Generator line numbers cited precisely. Literature citation is real and appropriate (Lamers, Roelofs, & Rabeling-Keus, 2010, *Memory & Cognition*). Schema table is complete with reasoning and tradeoff column for every field. Correctly identifies both string sentinels (`"missing"`, `"--"`) and both numeric sentinels (`-1`, `9999`) with exact generator line references. The `condition`-6-levels finding and the duplicate-row analysis are thorough.

- **A.3 (14/15)**: Six problems identified with specific numbers — loses 1pt because the A.3 markdown table lists `age` sentinel counts as `?` (placeholder text "?筆" left unfilled). All other observations have concrete numbers.

- **A.4 (19/20)**: `clean()` is a pure function with `df.copy()` at top. Every step has observation → action → cost commentary. `print` row-count logging present for each step. No bare `df.dropna()`. Only minor deduction: Step 3 (range filter) uses a slightly awkward `df.loc[~between & notna(), col] = np.nan` followed by `dropna(subset=)` — functionally correct, but less readable than a direct boolean mask; the combined sentinel+range step could be one cleaner block. Cleaning correctly linked back to A.0 schema entries.

- **A.5 (5/5)**: Clear before/after comparison with specific statistics cited.

- **A.6 (10/10)**: `analyse()` function is correct with `outlier_sd` as named parameter. Explanation for why it belongs in `analyse()` not `clean()` is precise and well-articulated (references the "cleaning vs. analysis boundary" principle). Stroop effect calculation correct; expected ~80 ms aligns with Lamers et al. (2010) range.

- **app.py (B.1 10/10, B.2 5/5, B.3 10/10)**: `load_data` uses `@st.cache_data(ttl=600, show_spinner=...)` — both non-default parameters present with rationale in comments. `clean()` also cached. Sidebar has `multiselect` (subject_id), `slider` (RT range), and `outlier_sd` slider — all three reflected via boolean mask on `df_view`. KPI metrics via `st.metric` (n, mean congruent RT, mean incongruent RT, Stroop effect), one matplotlib bar chart via `st.pyplot`, cleaned data table via `st.dataframe`. All three required B.3 elements present.

- **Bonus (+5)**: Cache timing with `time.perf_counter()` implemented and displayed in an expander. Sidebar "Clear cache" button implemented. Both bonus criteria satisfied.

- **README (10/10)**: Concise (well under 1 page). Install + run instructions clear. APA citation present. Three cleaning decisions each with explicit source annotation. `outlier_sd` rationale paragraph is well-written.

### Points deducted

- **A.3 (-1)**: Placeholder `?` left in the age sentinel counts (table shows "-1（?筆）、888（?筆）、NaN（?筆）"). Should have been filled in from running the cells.
- **A.4 (-1)**: Minor: Step 3 range-filtering logic is split across two operations when it could be cleaner; the cost commentary for the range step is weaker than the other steps.

---

## 吳心圓 (113892001) — Recommended score: **96**

**Submitted**: 2026-05-19 12:01 | **GitHub**: https://github.com/SuperCandy611/week-12-hw | **Streamlit**: deployed ✓

### Strengths

- **A.0 (10/10)**: Outstanding A.0 — among the best in the class. Generator reverse-engineering section is organized by execution order (field generation → Stroop injection → messy patterns), with every injected pattern shown as a quoted code block with line numbers. Literature citation is real (Ménétré & Laganaro, 2023, *PLOS ONE*) and used thoughtfully — critically, the student correctly notes that the SD-based upper bound from that paper (1074.5 ms) depends on *that study's* sample mean (682 ms) and **cannot be directly applied** to this dataset (mean ≈520 ms). This methodological reasoning is exemplary. The decision to use 200–3000 ms with the SD-based trimming moved to `analyse()` is well-justified.

- **A.3 (14/15)**: Comprehensive six-problem table with concrete numbers, all four required and two extra. The observation table format (with column for "觀察到的指令") is particularly clear. Loses 1pt: the A.3 markdown problem table has `?` placeholders in the `age` sentinel row ("age 含三種 missing 表示 | `value_counts(dropna=False)` | -1（?筆）、888（?筆）、NaN（?筆）") — same issue as 呂杰驛, those numbers were not filled in after running the code cell.

- **A.4 (18/20)**: `clean()` is a pure function, every step has observation/action/cost documentation, row-count prints present. Deductions: (1) Step order places `drop_duplicates` first, then condition normalization, then rt_ms cleaning — this order is defensible but the `drop_duplicates` step's cost commentary is thin ("若存在兩筆完全相同的合法 trial 也會被併掉（本資料不會）"). (2) The A.4 code cell is cut off at 2500 chars in the displayed version — full code continues after the truncation point; reviewing the file shows the complete function is present. Minor: `df = df[df["rt_ms"].between(200, 3000)]` is correct but doesn't print the before/after row count separately from the preceding `dropna` step; they're merged into one flow without individual print statements for each operation.

- **A.5 (4/5)**: Before/after comparison text is written *prospectively* in markdown ("相比 A.3，清理後：..." followed by a `?` placeholder for the final row count: "由 243 降至？列"). The text is correct in structure but the actual numbers were not filled in. Loses 1pt.

- **A.6 (10/10)**: `analyse()` correct, outlier logic per-condition is good, explanation of cleaning/analysis boundary is thorough and well-articulated.

- **app.py (B.1 10/10, B.2 5/5, B.3 10/10)**: Two cached functions: `load_data` with `ttl=600, show_spinner=` and `get_clean_data` with `max_entries=1, show_spinner=`. Both non-default parameters with reasoning in comments — excellent. Sidebar: `multiselect` (subject_id) and `slider` (RT range) correctly reflected via boolean mask. KPI `st.metric` present (4 metrics), matplotlib chart via `st.pyplot`, data table via `st.dataframe`. All B.3 elements present.

- **README (10/10)**: Clean, concise, under 1 page. APA citation. Three cleaning decisions all cite specific source (generator line numbers or literature section).

### Points deducted

- **A.3 (-1)**: Unfilled `?` placeholder in age sentinel counts.
- **A.4 (-2)**: Individual row-count prints not separated for each operation step within the rt_ms cleaning sequence; the `cost` documentation for the duplicate removal step is thinner than other steps.
- **A.5 (-1)**: Final row count left as `?` placeholder, not filled in after running.

---

## 何官臻 (114825002) — Recommended score: **100** (+2 bonus → cap at 100)

**Submitted**: 2026-05-16 23:05 (earliest of the three) | **GitHub**: https://github.com/ireneho3507/week12_hw | **Streamlit**: deployed ✓

### Strengths

- **A.0 (10/10)**: The best-organized A.0 of the three. Uses a structured approach: generator section is thorough with all 6 injected patterns quoted with line references. **Two** literature citations (Whelan 2008 + MacLeod 1991) — Whelan for the RT cutoffs, MacLeod for expected Stroop effect range. The schema table is the most polished: the `rt_ms` entry explicitly states why the SD-based upper bound from Whelan cannot be applied here (same methodological reasoning as 吳心圓, independently arrived at). The "來源 3 — 資料本身" table is exceptional: side-by-side with "對應到來源 1 / 2" column confirming each observation against the generator/literature ground truth, including the key insight "only the generator confirms `9999` is a sentinel (not just an extreme RT)". Schema table has exact counts for every sentinel (`NaN:15, -1:17, 888:12`) and a "取捨摘要" paragraph.

- **A.3 (15/15)**: Five problems documented, every one with concrete numbers and a "可能原因" trace back to the generator line. The value_counts table snippet for `condition` (showing exact counts for all 6 levels) is cited inline. Full marks — no unfilled placeholders.

- **A.4 (20/20)**: `clean()` is exemplary. Pure function with `df.copy()`. Every step has Obs reference, action, cost. Row-count prints are separated per step. Uses explicit boolean mask `df[df["rt_ms"].notna()]` instead of bare `dropna()`. Includes a validation assertion (`if bad.any(): raise ValueError`) after condition normalization — excellent defensive programming. The `age` sentinel handling correctly notes "本作業分析不依賴 age，可保留 NaN 不 drop" with reference to A.0 schema. All 6 cleaning steps mapped to their A.3 observations.

- **A.5 (5/5)**: Clear before/after comparison — actual numbers present: "243 → 240 (去3整列重複) → 最終 219 row". Statistics cited (raw mean≈709, std≈1244 → cleaned mean≈556, std≈91). NaN preservation in `age` explained.

- **A.6 (10/10)**: `analyse()` is correct. The sensitivity analysis (running outlier_sd at 2.0, 2.5, 3.0 and showing different Stroop effects) is an excellent addition that directly demonstrates *why* `outlier_sd` belongs in `analyse()` rather than being stated abstractly. Stroop effect = **77.1 ms** at 3 SD — closest to the generator's +80 ms injection of all three students (slightly less due to condition-level vs. global trimming). The explanation for the cleaning/analysis boundary is the most concrete of the three (cites specific numbers: "outlier_sd=2.0 → ~63 ms vs 3.0 → ~77 ms").

- **app.py (B.1 10/10, B.2 5/5, B.3 10/10)**: Architecture is noteworthy — `app.py` imports `clean` and `analyse` from `pipeline.py` (same module as notebook), avoiding code duplication. `@st.cache_data(ttl=600)` for load, `@st.cache_data` (default, deterministic) for clean. Cache timing displayed in sidebar as `st.metric`. Sidebar: `multiselect` (subject_id), `slider` (RT range), `slider` (outlier_sd) — all via boolean mask. The `outlier_sd` slider directly feeds `analyse()`, making the cleaning/analysis separation *interactive and visible*. KPI metrics, matplotlib chart, cleaning log expander, data table all present. Edge case handling (empty filter → `st.stop()`, missing condition → `_analyse_safe()`).

- **Bonus (+2)**: Cache timing displayed in sidebar with `time.perf_counter()` (satisfies one bonus criterion). "Clear cache" button present. Partial bonus for architectural bonus (pipeline.py import avoids drift between notebook and app). Full +5 not awarded because the cache hit/miss *comparison* (showing "first run slow, second run fast") is implemented as live metrics rather than the explicit demo shown in `app_with_cache.py`.

- **README (10/10)**: Two APA citations. Three cleaning decisions each cite source and include actual numbers (e.g., "243→219"). The `outlier_sd` paragraph includes the specific before/after numbers ("outlier_sd=2.0 → ~63 ms, 3.0 → ~77 ms"). Under 1 page.

### Points deducted

None. The submission is technically complete and methodologically rigorous throughout.

---

## Cross-Student Notes for Instructor

1. **All three students correctly identified the `9999` (not `99999`) sentinel** — this was the key differentiation from demo code, and all three caught it. Good sign of independent work.

2. **The unfilled `?` placeholder issue** (呂杰驛 in A.3, 吳心圓 in A.3 and A.5): This is a recurring pattern — students write the markdown analysis template in advance and sometimes forget to fill in actual numbers after running cells. Consider flagging this in next week's feedback as a pre-submission checklist item.

3. **Literature quality**: All three cited real, relevant papers. 何官臻 cited both Whelan (2008) and MacLeod (1991). 吳心圓 cited Ménétré & Laganaro (2023) — a more recent PLOS ONE paper, which is fine, though its SD-based upper bound required careful adaptation (which the student handled correctly). 呂杰驛 cited Lamers et al. (2010) from *Memory & Cognition*.

4. **The cleaning/analysis boundary explanation**: All three students articulated this well. 何官臻's sensitivity analysis demonstration (showing Stroop effect changes from ~63 ms at ±2 SD to ~77 ms at ±3 SD) is the most convincing pedagogical demonstration of *why* the boundary matters.

5. **app.py architecture**: 何官臻's decision to import from `pipeline.py` rather than rewriting `clean()` in `app.py` is a more advanced and correct software practice. Worth praising explicitly in feedback.

---

## Recommended eeclass Scores

| 學生 | Score |
|------|-------|
| 呂杰驛 (113825002) | **98** |
| 吳心圓 (113892001) | **96** |
| 何官臻 (114825002) | **100** |

> ⚠️ **Action required**: Instructor review needed before uploading scores to eeclass.
> Run `python eeclass_grader.py --week week12 --headed --dry-run` to verify, then `--headed` without dry-run to submit.
> Also update `homeworks/CLAUDE.md` Known Homework IDs table: `week12 | 69021 | ...`
