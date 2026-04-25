"""Midterm grader — skips PDF upload (already uploaded). Uses original timing."""
from playwright.sync_api import sync_playwright
import os, sys

BASE = "https://ncueeclass.ncu.edu.tw"
ACCOUNT = os.environ.get("EECLASS_ACCOUNT", "A165741")
PASSWORD = os.environ.get("EECLASS_PASSWORD", "^%$#2wsx1qaz")
HW_ID = "67993"
STUDENTS = [{"name": "呂杰驛", "score": 95}, {"name": "何官臻", "score": 70}]

def click_modal(page):
    for sel in ['button:has-text("登出所有裝置")', 'a:has-text("登出所有裝置")',
                'button:has-text("登出其他")', 'button:has-text("確定")', '.bootbox-accept']:
        btn = page.locator(sel)
        if btn.count() > 0 and btn.first.is_visible():
            print(f"  Modal: {sel}")
            btn.first.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2500)
            return True
    return False

def login(page):
    page.goto(BASE, wait_until="networkidle")
    page.wait_for_timeout(1000)
    page.fill('input[name="account"]', ACCOUNT)
    page.fill('input[name="password"]', PASSWORD)
    try:
        page.locator('button:has-text("登入"), input[value="登入"]').first.click()
    except Exception:
        page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    click_modal(page)
    if page.locator('input[name="account"]').count() > 0:
        page.fill('input[name="account"]', ACCOUNT)
        page.fill('input[name="password"]', PASSWORD)
        page.locator('button:has-text("登入")').first.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        click_modal(page)
    page.goto(f"{BASE}/course/homeworkList/38662", wait_until="networkidle")
    page.wait_for_timeout(1500)
    click_modal(page)
    ok = "/course/homeworkList/" in page.url
    print(f"Login {'OK' if ok else 'FAILED'}: {page.url}")
    return ok

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width":1280,"height":900}, locale="zh-TW")
    page = ctx.new_page()
    page.on("dialog", lambda d: d.accept())
    page.set_default_timeout(20000)

    print("Logging in...")
    if not login(page):
        print("Login failed!"); browser.close(); sys.exit(1)

    results = []
    for s in STUDENTS:
        name, score = s["name"], s["score"]
        print(f"\n=== {name} ({score} pts) ===")
        submit_url = f"{BASE}/homework/submitList/{HW_ID}"
        page.goto(submit_url, wait_until="networkidle")
        page.wait_for_timeout(2000)
        click_modal(page)
        if "login" in page.url or page.locator('input[name="account"]').count() > 0:
            print("  Session expired, re-login..."); login(page)
            page.goto(submit_url, wait_until="networkidle"); page.wait_for_timeout(2000)
        page.screenshot(path=f"midterm_list_{name}.png")

        link = None
        for sel in [f'a:has-text("{name}_期中")', f'a:has-text("{name}_")', f'a:has-text("{name}")']:
            c = page.locator(sel)
            if c.count() > 0:
                link = c.first; print(f"  Link: {sel}"); break
        if not link:
            print(f"  No link for {name}"); results.append((name, False, "no link")); continue

        link.click(); page.wait_for_load_state("networkidle"); page.wait_for_timeout(1000)

        body = page.inner_text("body")
        if "已批改" in body:
            print("  Already graded!"); results.append((name, True, "already done")); continue

        grade_btn = page.locator('a:has-text("批改")')
        if grade_btn.count() == 0:
            print("  No 批改 button"); page.screenshot(path=f"midterm_err_{name}.png"); results.append((name, False, "no grade btn")); continue
        grade_btn.first.click(); page.wait_for_load_state("networkidle"); page.wait_for_timeout(1000)

        si = page.locator('input[name="auditScore"]')
        if si.count() == 0:
            print("  No score input"); page.screenshot(path=f"midterm_err_{name}.png"); results.append((name, False, "no score input")); continue
        si.fill(str(score)); print(f"  Score filled: {score}")
        
        # Skip PDF upload — PDFs already uploaded from previous run
        
        sb = page.locator('button:has-text("送出"), input[value="送出"]')
        if sb.count() == 0:
            print("  No 送出 button"); results.append((name, False, "no submit btn")); continue
        sb.first.click()
        page.wait_for_timeout(2000); page.wait_for_load_state("networkidle")
        page.screenshot(path=f"midterm_done_{name}.png")
        print("  Submitted!")
        results.append((name, True, "submitted"))

    browser.close()
    print("\n=== RESULTS ===")
    for n, ok, note in results:
        print(f"  {n}: {'OK' if ok else 'FAILED'} ({note})")
