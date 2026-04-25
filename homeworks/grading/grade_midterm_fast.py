"""
Fast midterm grader - skips PDF upload (already uploaded), minimal waits.
"""
from playwright.sync_api import sync_playwright
import os, time

BASE = "https://ncueeclass.ncu.edu.tw"
ACCOUNT = os.environ.get("EECLASS_ACCOUNT", "A165741")
PASSWORD = os.environ.get("EECLASS_PASSWORD", "^%$#2wsx1qaz")
HW_ID = "67993"

STUDENTS = [
    {"name": "呂杰驛", "score": 95},
    {"name": "何官臻", "score": 70},
]

def click_session_modal(page):
    for sel in ['button:has-text("登出所有裝置")', 'a:has-text("登出所有裝置")', 'button:has-text("確定")', '.bootbox-accept']:
        btn = page.locator(sel)
        if btn.count() > 0 and btn.first.is_visible():
            btn.first.click()
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(1500)
            return True
    return False

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 900}, locale="zh-TW")
    page = ctx.new_page()
    page.on("dialog", lambda d: d.accept())
    page.set_default_timeout(20000)

    # --- LOGIN ---
    print("Logging in...")
    page.goto(BASE, wait_until="domcontentloaded")
    page.wait_for_timeout(800)
    try:
        page.fill('input[name="account"]', ACCOUNT)
        page.fill('input[name="password"]', PASSWORD)
        page.locator('button:has-text("登入"), input[value="登入"]').first.click()
    except Exception:
        page.keyboard.press("Enter")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1500)
    click_session_modal(page)

    # Warm course session
    page.goto(f"{BASE}/course/homeworkList/38662", wait_until="domcontentloaded")
    page.wait_for_timeout(1000)
    click_session_modal(page)
    print(f"  URL: {page.url}")

    results = []
    for student in STUDENTS:
        name = student["name"]
        score = student["score"]
        print(f"\n--- {name} (score: {score}) ---")

        # Navigate to submit list
        page.goto(f"{BASE}/homework/submitList/{HW_ID}", wait_until="domcontentloaded")
        page.wait_for_timeout(1200)

        # Find student link
        link = None
        for sel in [f'a:has-text("{name}_")', f'a:has-text("{name}")']:
            c = page.locator(sel)
            if c.count() > 0:
                link = c.first
                print(f"  Found: {sel}")
                break
        if link is None:
            print(f"  ERROR: No link for {name}")
            results.append((name, False))
            continue

        link.click()
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(1000)

        # Check if already graded
        if "已批改" in page.inner_text("body"):
            print(f"  Already graded!")
            results.append((name, True))
            continue

        # Click 批改
        grade_btn = page.locator('a:has-text("批改")')
        if grade_btn.count() == 0:
            print(f"  ERROR: No 批改 button")
            page.screenshot(path=f"midterm_error_{name}.png")
            results.append((name, False))
            continue
        grade_btn.first.click()
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(800)

        # Enter score
        score_input = page.locator('input[name="auditScore"]')
        if score_input.count() == 0:
            print(f"  ERROR: No score input")
            page.screenshot(path=f"midterm_error_{name}.png")
            results.append((name, False))
            continue
        score_input.fill(str(score))
        print(f"  Filled score: {score}")

        # Skip PDF upload (already uploaded from previous run)
        # Submit
        submit_btn = page.locator('button:has-text("送出"), input[value="送出"]')
        if submit_btn.count() == 0:
            print(f"  ERROR: No 送出 button")
            page.screenshot(path=f"midterm_error_{name}.png")
            results.append((name, False))
            continue
        submit_btn.first.click()
        page.wait_for_timeout(2000)
        page.wait_for_load_state("domcontentloaded")
        print(f"  Submitted!")
        page.screenshot(path=f"midterm_after_{name}.png")
        results.append((name, True))

    browser.close()
    print("\n=== RESULTS ===")
    for name, ok in results:
        print(f"  {name}: {'OK' if ok else 'FAILED'}")
