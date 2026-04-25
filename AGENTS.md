# Project: 2026 Spring — Computational Big Data (NCU eeclass)

## Course

- Name: 電腦硬體與程式語言在行為科學實驗與大數據分析之應用 (The Applications of Computer Hardware and Programming Languages in Behavioral Experiments and Big-Data)
- Platform: NCU eeclass — https://ncueeclass.ncu.edu.tw
- Course homework list URL: https://ncueeclass.ncu.edu.tw/course/homeworkList/38662
- Instructor account: A165741 / password: ^%$#2wsx1qaz
- Login endpoint: POST https://ncueeclass.ncu.edu.tw/sys/lib/ajax/login_submit.php (fields: account, password)

## Students

| Name   | Student ID | PDF name  |
|--------|-----------|-----------|
| 呂杰驛 | 113825002 | 呂杰驛.pdf |
| 吳心圓 | 113892001 | 吳心圓.pdf |
| 何官臻 | 114825002 | 何官臻.pdf |

## End-to-End Homework Grading Workflow

The full cycle for each week has three phases: **Download → Grade → Upload**. All automation scripts use Playwright and are in the project root.

### Phase 1: Download Student Submissions

**Script:** `download_hw.py` (Playwright-based batch downloader)

How it works:
1. Logs into eeclass via the login form
2. Navigates to `/course/homework/submissionList/{hw_id}` for each homework ID
3. Clicks "全選" (select all) then "打包下載" (package download)
4. Saves ZIP files to `homeworks/` as `hw_{hw_id}.zip`

Usage:
- Edit `hw_ids` list in the script to include the target homework IDs
- Run: `python download_hw.py`
- Downloaded ZIPs land in `homeworks/`

Alternative (if session cookies are already available): `download_exact.py` — uses `requests` with known download URLs + PHPSESSID cookie. Faster but requires manually grabbing the download URL from eeclass.

After downloading, unzip into `homeworks/weekNN/` — each student's submission goes into a subfolder named `{student_id} ({name})/`.

### Phase 2: Grade & Generate Feedback PDFs

**Rubric file:** Each week has a rubric spreadsheet, e.g. `homeworks/weekNN/weekNN_rubric.xlsx`

**Feedback generation pipeline:**
1. Read student submissions from `homeworks/weekNN/{student_id} ({name})/`
2. Apply rubric criteria and produce per-student feedback markdown: `homeworks/weekNN/feedback_{student_id}.md`
3. Compile markdown → LaTeX → PDF using `compile_feedback_pdfs.py`

**Script:** `homeworks/weekNN/compile_feedback_pdfs.py`

Each week's compile script maps student IDs to Chinese names and runs:
```
pandoc feedback_{id}.md → {name}.tex → xelatex → {name}.pdf
```

Key settings (from week05 template):
- Font: Times New Roman (main), Microsoft JhengHei (CJK)
- Font size: 14pt, margin: 1in, document class: extarticle
- Patch: replaces `\rule{0.5\linewidth}{\linethickness}` with `\rule{0.5\linewidth}{0.4pt}` to fix a pandoc/xelatex bug
- Requires: pandoc, xelatex (e.g. MiKTeX on Windows)

Output: `homeworks/weekNN/{name}.pdf` for each student (e.g. `呂杰驛.pdf`, `吳心圓.pdf`, `何官臻.pdf`)

**Scores:** Recorded in `homeworks/weekNN/grading_config.json` alongside PDF filenames.

### Phase 3: Upload Scores & Feedback PDFs to eeclass

**Script:** `eeclass_grader.py` (Playwright automation — the main automation tool)

Prerequisites:
```bash
pip install playwright
playwright install chromium
```

**Config file:** `homeworks/weekNN/grading_config.json`
```json
{
  "homework_id": "67474",
  "students": [
    {"name": "呂杰驛", "student_id": "113825002", "score": 94, "pdf": "呂杰驛.pdf"},
    {"name": "吳心圓", "student_id": "113892001", "score": 97, "pdf": "吳心圓.pdf"},
    {"name": "何官臻", "student_id": "114825002", "score": 92, "pdf": "何官臻.pdf"}
  ]
}
```

- `homework_id`: numeric ID from eeclass URL `/homework/submitList/{id}` (find it on the course homework list page)
- `score`: integer, 0–100
- `pdf`: filename in the same weekNN folder

**Commands:**
```bash
# Dry run — fills forms, takes screenshots, does NOT submit
python eeclass_grader.py --week weekNN --headed --dry-run

# Submit for real
python eeclass_grader.py --week weekNN --headed

# Headless (no browser window)
python eeclass_grader.py --week weekNN

# Debug with slow motion
python eeclass_grader.py --week weekNN --headed --slow-mo 500
```

**What the script does per student:**
1. Navigates to `/homework/submitList/{homework_id}`
2. Clicks `{name}_Homework-week-NN` link → student's report page
3. Clicks `批改` (grade) button → opens grading form
4. Fills `input[name="auditScore"]` with the score
5. Clicks `上傳檔案` → opens upload modal
6. Uses Playwright `set_input_files()` on `input[type="file"]` to attach PDF (bypasses native file picker)
7. Clicks `送出` (submit)

**Why Playwright (not Chrome DevTools Protocol):** CDP's `DOM.setFileInputFiles` returns `-32000 "Not allowed"` on the blueimp jQuery File Upload widget used by eeclass. Playwright's `set_input_files()` works at a higher abstraction level and bypasses this restriction.

## eeclass URL Patterns

| Page | URL |
|------|-----|
| Course homework list | `/course/homeworkList/38662` |
| Homework submit list | `/homework/submitList/{homework_id}` |
| Student report | `/homework/report/{report_id}/?ajaxAuth={token}` |
| Grading mode | `/homework/report/{report_id}/?exerciseAction=auditReport&_lock=exerciseAction&ajaxAuth={token}` |
| Package download | `/homework/package/{homework_id}/?ajaxAuth={token}&file={hash}` |
| Login AJAX | `/sys/lib/ajax/login_submit.php` |

## eeclass Grading Form Details

- Form ID: `homework-audit-setting-form`
- Score field: `input[name="auditScore"]`
- Comment field: rich text editor (评語)
- File upload: blueimp jQuery File Upload widget with `input[type="file"]` inside a modal triggered by `上傳檔案` button
- Submit button: `送出`
- CSRF token: `input[name="anticsrf"]` (auto-populated)
- Keep audit flag: `input[name="keepAudit"]`
- Report ID: `input[name="reportId"]`

## File Structure

```
2026_Spring_CompBigData/
├── AGENTS.md                          # This file — project knowledge
├── EECLASS_GRADER_README.md           # Detailed grader script docs
├── eeclass_grader.py                  # Upload scores + PDFs to eeclass
├── download_hw.py                     # Download student submissions (Playwright)
├── download_exact.py                  # Download via direct URL + cookies
├── test_login_requests.py             # Login test script (has credentials)
├── homeworks/
│   ├── weekNN/
│   │   ├── grading_config.json        # homework_id + student scores + PDF filenames
│   │   ├── weekNN_rubric.xlsx         # Grading rubric
│   │   ├── feedback_{student_id}.md   # Per-student feedback (generated)
│   │   ├── compile_feedback_pdfs.py   # MD → TeX → PDF compiler
│   │   ├── {name}.tex                 # Intermediate LaTeX (generated)
│   │   ├── {name}.pdf                 # Final feedback PDF (generated)
│   │   └── {student_id} ({name})/     # Student submission folder (from ZIP)
│   ├── week05/
│   │   └── grading_config.json        # homework_id: 67120
│   ├── week06/
│   │   └── grading_config.json        # homework_id: 67474
│   └── ...
├── Context/                           # Course materials
├── Instructions/                      # Assignment instructions
└── general/                           # General resources
```

## Quick Reference: Grading a New Week

```bash
# 1. Download submissions
#    Edit hw_ids in download_hw.py, then:
python download_hw.py
#    Unzip into homeworks/weekNN/

# 2. Grade: read submissions, create rubric, write feedback
#    Create: homeworks/weekNN/weekNN_rubric.xlsx
#    Create: homeworks/weekNN/feedback_{student_id}.md for each student
#    Create: homeworks/weekNN/compile_feedback_pdfs.py
python homeworks/weekNN/compile_feedback_pdfs.py

# 3. Create grading config
#    Create: homeworks/weekNN/grading_config.json
#    (homework_id from eeclass URL, scores from rubric)

# 4. Upload to eeclass
python eeclass_grader.py --week weekNN --headed --dry-run   # verify first
python eeclass_grader.py --week weekNN --headed              # submit
```

## Known Homework IDs

| Week   | homework_id | Notes |
|--------|------------|-------|
| week05 | 67120      | Completed |
| week06 | 67474      | Completed |

## Notes

- The eeclass session can expire mid-grading. The `eeclass_grader.py` script detects this and re-logs in automatically.
- A "session conflict" modal may appear if the account is logged in elsewhere. The script handles this by clicking 確定.
- Debug screenshots are saved as `debug_submitlist_{name}.png` and `error_{name}.png` in the project root.
- Credentials can be overridden via environment variables: `EECLASS_ACCOUNT`, `EECLASS_PASSWORD`.
