# eeclass Homework Grading Upload — Playwright Automation

## Problem

Grading homework on NCU eeclass (https://ncueeclass.ncu.edu.tw) requires repetitive manual steps for each student: navigating to their submission, entering a score, uploading a feedback PDF, and submitting. When attempted via the Chrome DevTools Protocol (Claude in Chrome extension), the native file picker dialog could not be automated — CDP's `DOM.setFileInputFiles` returned `-32000 "Not allowed"` on the blueimp jQuery File Upload widget used by eeclass.

## Solution

A Playwright Python script (`eeclass_grader.py`) that automates the full workflow. Playwright's `set_input_files()` bypasses the native file picker entirely, setting files directly on `<input type="file">` elements at a higher abstraction level than CDP.

## Setup

```bash
pip install playwright
playwright install chromium
```

## File Structure

```
2026_Spring_CompBigData/
├── eeclass_grader.py              # Main automation script
├── homeworks/
│   ├── week05/
│   │   ├── grading_config.json    # Scores + PDF mapping
│   │   ├── 呂杰驛.pdf
│   │   ├── 吳心圓.pdf
│   │   └── 何官臻.pdf
│   ├── week06/
│   │   ├── grading_config.json
│   │   ├── 呂杰驛.pdf
│   │   ├── 吳心圓.pdf
│   │   └── 何官臻.pdf
│   └── weekNN/
│       ├── grading_config.json    # Create this for each new week
│       └── *.pdf                  # Feedback PDFs
```

## grading_config.json Format

Each week folder needs a `grading_config.json`:

```json
{
  "homework_id": "67474",
  "students": [
    {"name": "呂杰驛", "student_id": "113825002", "score": 94, "pdf": "呂杰驛.pdf"},
    {"name": "吳心圓", "student_id": "113892001", "score": 0,  "pdf": "吳心圓.pdf"},
    {"name": "何官臻", "student_id": "114825002", "score": 92, "pdf": "何官臻.pdf"}
  ]
}
```

- `homework_id`: The numeric ID from the eeclass URL (`/homework/submitList/{homework_id}`)
- `name`: Student's Chinese name (must match exactly what appears in eeclass)
- `student_id`: Student number
- `score`: Integer score
- `pdf`: Filename of the feedback PDF in the same week folder

## Usage

```bash
# Dry run (fills forms + takes screenshots, does NOT submit)
python eeclass_grader.py --week week07 --headed --dry-run

# Actually submit grades
python eeclass_grader.py --week week07 --headed

# Headless (no visible browser)
python eeclass_grader.py --week week07

# Slow motion for debugging (500ms between actions)
python eeclass_grader.py --week week07 --headed --slow-mo 500
```

## Credentials

The script uses these defaults (from `test_login_requests.py`):

- Account: `A165741`
- Password: `^%$#2wsx1qaz`

Override via environment variables:

```bash
set EECLASS_ACCOUNT=A165741
set EECLASS_PASSWORD=your_password
python eeclass_grader.py --week week07
```

## eeclass Grading Flow (What the Script Automates)

1. **Login**: POST to `/sys/lib/ajax/login_submit.php` with account/password
2. **Navigate**: Go to `/homework/submitList/{homework_id}`
3. **For each student**:
   - Click the link `{name}_Homework-week-NN` to open their report
   - Click the `批改` button to enter grading mode
   - Fill `input[name="auditScore"]` with the score
   - Click `上傳檔案` to open the upload modal
   - Use `set_input_files()` on `input[type="file"]` to attach the PDF
   - Click `送出` to submit

## Course Info

- Course: 電腦硬體與程式語言在行為科學實驗與大數據分析之應用
- Course homework list: https://ncueeclass.ncu.edu.tw/course/homeworkList/38662
- Students: 呂杰驛 (113825002), 吳心圓 (113892001), 何官臻 (114825002)

## Typical Workflow for a New Week

1. Generate feedback PDFs (from LaTeX or other source) into `homeworks/weekNN/`
2. Create `homeworks/weekNN/grading_config.json` with homework ID and scores
3. Run `python eeclass_grader.py --week weekNN --headed --dry-run` to verify
4. Run `python eeclass_grader.py --week weekNN --headed` to submit
