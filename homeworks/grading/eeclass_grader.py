"""
eeclass Homework Grader — Playwright Automation
================================================
Automates the full grading workflow on NCU eeclass:
  1. Logs in
  2. Navigates to the homework submit list
  3. For each student: enters score, uploads PDF, submits

Usage:
  pip install playwright
  playwright install chromium
  python eeclass_grader.py --week week07

The script reads a grading config JSON file from:
  homeworks/<week>/grading_config.json
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
except ImportError:
    print("Playwright is not installed. Run:")
    print("  pip install playwright")
    print("  playwright install chromium")
    sys.exit(1)


# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
EECLASS_BASE = "https://ncueeclass.ncu.edu.tw"
LOGIN_URL = f"{EECLASS_BASE}/sys/lib/ajax/login_submit.php"
COURSE_HW_LIST = f"{EECLASS_BASE}/course/homeworkList/38662"

ACCOUNT = os.environ.get("EECLASS_ACCOUNT", "A165741")
PASSWORD = os.environ.get("EECLASS_PASSWORD", "^%$#2wsx1qaz")

SCRIPT_DIR = Path(__file__).parent
HOMEWORKS_DIR = SCRIPT_DIR / "homeworks"


def load_grading_config(week: str, homework_id: str = None, students_json: str = None):
    """Load grading configuration from JSON file or CLI arguments."""
    config_path = HOMEWORKS_DIR / week / "grading_config.json"

    if config_path.exists():
        print(f"Loading config from {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        week_dir = HOMEWORKS_DIR / week
        for student in config["students"]:
            pdf_path = week_dir / student["pdf"]
            student["pdf_path"] = str(pdf_path.resolve())
            if not pdf_path.exists():
                print(f"  WARNING: PDF not found: {pdf_path}")
        return config

    if homework_id and students_json:
        students = json.loads(students_json)
        week_dir = HOMEWORKS_DIR / week
        for student in students:
            pdf_path = week_dir / student["pdf"]
            student["pdf_path"] = str(pdf_path.resolve())
        return {"homework_id": homework_id, "students": students}

    print(f"No config file found at {config_path}")
    sys.exit(1)


def _click_session_modal(page):
    """If the 'account already logged in elsewhere' modal is up, accept and kick other sessions."""
    for sel in [
        'button:has-text("登出所有裝置")',
        'a:has-text("登出所有裝置")',
        'button:has-text("登出其他")',
        'button:has-text("確定")',
        '.bootbox-accept',
    ]:
        btn = page.locator(sel)
        if btn.count() > 0 and btn.first.is_visible():
            print(f"  Handling session conflict modal via: {sel}")
            btn.first.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2500)
            return True
    return False


def login(page):
    """Log into eeclass and verify authentication."""
    print("Navigating to eeclass login page...")
    page.goto(EECLASS_BASE, wait_until="networkidle")
    page.wait_for_timeout(1000)

    print(f"Filling login form as {ACCOUNT}...")
    try:
        page.fill('input[name="account"]', ACCOUNT)
        page.fill('input[name="password"]', PASSWORD)
        page.locator('button:has-text("登入"), input[value="登入"]').first.click()
    except Exception:
        page.fill('input[name="account"]', ACCOUNT)
        page.fill('input[name="password"]', PASSWORD)
        page.keyboard.press("Enter")

    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Handle "account active elsewhere" modal
    _click_session_modal(page)

    # If still showing login form, try once more
    if page.locator('input[name="account"]').count() > 0:
        print("  Still on login page — resubmitting...")
        try:
            page.fill('input[name="account"]', ACCOUNT)
            page.fill('input[name="password"]', PASSWORD)
            page.locator('button:has-text("登入")').first.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2500)
            _click_session_modal(page)
        except Exception:
            pass

    # Verify: teacher's homework-list page should load and contain a logout link
    page.goto(COURSE_HW_LIST, wait_until="networkidle")
    page.wait_for_timeout(1500)
    _click_session_modal(page)

    url = page.url
    has_logout_link = page.locator('a[href*="logout"], a:has-text("登出")').count() > 0
    has_login_form = page.locator('input[name="account"]').count() > 0
    is_teacher_hw_page = "/course/homeworkList/" in url and not has_login_form
    if is_teacher_hw_page and has_logout_link:
        print(f"Login successful! (URL: {url})")
        return True
    print(f"ERROR: Could not verify login. URL={url} logout_link={has_logout_link} login_form={has_login_form}")
    return False


def grade_student(page, homework_id: str, student: dict, dry_run: bool = False):
    """Grade a single student: navigate to report → enter score → upload PDF → submit."""
    name = student["name"]
    score = student["score"]
    pdf_path = student["pdf_path"]

    print(f"\n{'='*60}")
    print(f"Grading: {name} (score: {score})")
    print(f"PDF: {pdf_path}")
    print('='*60)

    submit_list_url = f"{EECLASS_BASE}/homework/submitList/{homework_id}"
    page.goto(submit_list_url, wait_until="networkidle")
    page.wait_for_timeout(2000)
    _click_session_modal(page)

    # If session expired and redirected back to login
    if "login" in page.url or page.locator('input[name="account"]').count() > 0:
        print("  Session expired — re-logging in...")
        login(page)
        page.goto(submit_list_url, wait_until="networkidle")
        page.wait_for_timeout(2000)

    # If submitList redirected us to /course/info/ (wrong course context), try visiting
    # the course homework list first to set session, then re-goto submitList.
    if "/homework/submitList/" not in page.url:
        print(f"  submitList redirected to {page.url} — warming course session...")
        page.goto(COURSE_HW_LIST, wait_until="networkidle")
        page.wait_for_timeout(1500)
        _click_session_modal(page)
        page.goto(submit_list_url, wait_until="networkidle")
        page.wait_for_timeout(2000)

    page.screenshot(path=f"debug_submitlist_{name}.png")
    print(f"  Navigated to {submit_list_url} (current: {page.url})")

    link = None
    for sel in [
        f'a:has-text("{name}_Homework")',
        f'a:has-text("{name}")',
        f'td:has-text("{name}") a',
        f'tr:has-text("{name}") a[href*="report"]',
    ]:
        try:
            candidate = page.locator(sel)
            if candidate.count() > 0:
                link = candidate.first
                print(f"  Found link with selector: {sel}")
                break
        except Exception:
            continue

    if link is None:
        print(f"  ERROR: Could not find submission link for {name}")
        page.screenshot(path=f"error_nolink_{name}.png")
        return False

    print(f"  Clicking into {name}'s report...")
    link.first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    grade_btn = page.locator('a:has-text("批改")')
    if grade_btn.count() == 0:
        if page.locator('input[name="auditScore"]').count() > 0:
            print("  Already in grading mode.")
        else:
            print(f"  ERROR: Could not find 批改 button for {name}")
            return False
    else:
        print("  Clicking 批改...")
        grade_btn.first.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)

    score_input = page.locator('input[name="auditScore"]')
    if score_input.count() == 0:
        print(f"  ERROR: Score input field not found for {name}")
        return False
    print(f"  Entering score: {score}")
    score_input.fill(str(score))

    if os.path.exists(pdf_path):
        print(f"  Uploading PDF: {os.path.basename(pdf_path)}")
        upload_btn = page.locator('button:has-text("上傳檔案"), a:has-text("上傳檔案")')
        if upload_btn.count() > 0:
            upload_btn.first.click()
            page.wait_for_timeout(1000)

        file_input = page.locator('input[type="file"]')
        if file_input.count() > 0:
            print("  Setting file on input[type=file]...")
            file_input.first.set_input_files(pdf_path)
            page.wait_for_timeout(4000)
        else:
            print("  WARNING: No file input found.")
    else:
        print(f"  WARNING: PDF file not found at {pdf_path}, skipping upload")

    if dry_run:
        print(f"  DRY RUN — would submit grade for {name}")
        page.screenshot(path=f"dry_run_{name}.png", full_page=True)
        print(f"  Screenshot saved: dry_run_{name}.png")
        return True

    # Close upload modal if open
    close_btn = page.locator('.modal .close, button[aria-label="Close"]')
    if close_btn.count() > 0 and close_btn.first.is_visible():
        close_btn.first.click()
        page.wait_for_timeout(500)

    print("  Submitting grade...")
    submit_btn = page.locator('button:has-text("送出"), input[value="送出"]')
    if submit_btn.count() > 0:
        submit_btn.first.click()
        page.wait_for_timeout(2000)
        page.on("dialog", lambda dialog: dialog.accept())
        page.wait_for_load_state("networkidle")
        print(f"  Successfully graded {name}: {score} points")
        return True
    print(f"  ERROR: Submit button not found for {name}")
    return False


def main():
    parser = argparse.ArgumentParser(description="eeclass Homework Grader")
    parser.add_argument("--week", required=True, help="Week folder name (e.g., week07)")
    parser.add_argument("--homework-id", help="eeclass homework ID (from URL)")
    parser.add_argument("--students", help="JSON string of students array")
    parser.add_argument("--dry-run", action="store_true", help="Don't actually submit; take screenshots instead")
    parser.add_argument("--headed", action="store_true", help="Show browser window (default: headless)")
    parser.add_argument("--slow-mo", type=int, default=0, help="Slow down actions by N ms (for debugging)")
    args = parser.parse_args()

    config = load_grading_config(args.week, args.homework_id, args.students)
    homework_id = config["homework_id"]
    students = config["students"]

    print(f"\nGrading Plan:")
    print(f"  Week: {args.week}")
    print(f"  Homework ID: {homework_id}")
    print(f"  Students: {len(students)}")
    for s in students:
        print(f"    - {s['name']}: {s['score']} pts -> {s.get('pdf', 'N/A')}")
    print()
    if args.dry_run:
        print("*** DRY RUN MODE — no grades will be submitted ***\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed, slow_mo=args.slow_mo)
        context = browser.new_context(viewport={"width": 1280, "height": 800}, locale="zh-TW")
        page = context.new_page()
        page.on("dialog", lambda dialog: dialog.accept())

        if not login(page):
            print("Login failed. Exiting.")
            browser.close()
            sys.exit(1)

        results = []
        for student in students:
            try:
                ok = grade_student(page, homework_id, student, dry_run=args.dry_run)
                results.append((student["name"], ok))
            except Exception as e:
                print(f"  ERROR grading {student['name']}: {e}")
                results.append((student["name"], False))
                try:
                    page.screenshot(path=f"error_{student['name']}.png")
                except Exception:
                    pass

        print("\n" + "="*60)
        print("GRADING SUMMARY")
        print("="*60)
        for name, ok in results:
            print(f"  {name}: {'OK' if ok else 'FAILED'}")
        failed = [n for n, ok in results if not ok]
        if failed:
            print(f"\n{len(failed)} student(s) failed.")
        browser.close()
        print("\nDone!")


if __name__ == "__main__":
    main()
