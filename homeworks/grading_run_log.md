# Automated Grading Run Log

## 2026-05-14 (Weekly Grading Run)

### Status: COMPLETED

Uploaded scores and feedback PDFs for week10 and week11.

**Week 10 (hw_id: 68714)**
| Student | Score | PDF |
|---------|-------|-----|
| 呂杰驛 | 100 | 呂杰驛.pdf ✓ |
| 吳心圓 | 91 | 吳心圓.pdf ✓ |
| 何官臻 | 93 | 何官臻.pdf ✓ |

**Week 11 (hw_id: 69021)**
| Student | Score | PDF |
|---------|-------|-----|
| 呂杰驛 | 100 | 呂杰驛.pdf ✓ |
| 吳心圓 | 97 | 吳心圓.pdf ✓ |
| 何官臻 | 100 | 何官臻.pdf ✓ |

Verified on eeclass submit list: all scores confirmed live.
Method: `grade_one.py` — one student per bash call (44s timeout constraint).
Login: `button[data-role="form-submit"]` + `a.kickOtherBtn` for session conflict.
Next: Week 12 due 2026-05-20.

---

## 2026-05-13 (Weekly Grading Run)

### Status: BLOCKED — eeclass login temporarily locked

**Cause:** Multiple rapid login attempts during automated debugging triggered eeclass's brute-force lockout.  
**Error from eeclass:** `此輸入值已被鎖定無法登入，將於 27 分鐘後解鎖` ("This input has been locked and cannot log in; will unlock in 27 minutes")  
**Approximate unlock time:** ~27 minutes after the run started (~15 minutes from now at time of writing)

### What was determined before the lockout:

- **Last graded:** Week 09 (homework_id: 68433) — scores uploaded 2026-05-06
- **Next to grade:** Week 10 (homework due before Week 11, i.e., 2026-05-07)
- **Week 10 homework ID:** Not yet found (eeclass login blocked before we could retrieve it)
- **Student submissions:** No week10 folder exists yet in `homeworks/` — submissions not yet downloaded

### Next steps (manual or next scheduled run):

1. Wait for lockout to expire (~27 min from now)
2. Log in to eeclass: https://ncueeclass.ncu.edu.tw with A165741
3. Go to course homework list: https://ncueeclass.ncu.edu.tw/course/homeworkList/38662
4. Find the Week 10 homework entry and note its `homework_id` from the URL
5. Download student submissions → unzip to `homeworks/week10/`
6. Grade per rubric (see `homeworks/week10/week-10-homework.md`)
7. Generate feedback PDFs and `grading_config.json`
8. Run `python eeclass_grader.py --week week10 --headed` to upload

### Note on lockout avoidance:

The lockout was triggered by repeated Playwright login attempts during script debugging. To avoid in the future, test login logic with a single attempt only — do not loop or retry more than 2–3 times in a short window.
