import os
import time
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    print("Logging in...")
    page.goto('https://ncueeclass.ncu.edu.tw')
    page.fill('input[name="account"]', 'A165741')
    page.fill('input[name="password"]', '^%$#2wsx1qaz')
    
    # Try different login buttons
    try:
        page.locator('button:has-text("登入")').click(timeout=3000)
    except:
        page.keyboard.press("Enter")
        
    page.wait_for_load_state("networkidle")
    print("Login completed.")

    save_dir = os.path.join(os.getcwd(), 'homeworks')
    os.makedirs(save_dir, exist_ok=True)
    hw_ids = ['66154', '66745']

    for hw_id in hw_ids:
        print(f"Processing HW {hw_id}...")
        # Direct URL to submission list on eeclass
        page.goto(f'https://ncueeclass.ncu.edu.tw/course/homework/submissionList/{hw_id}')
        page.wait_for_load_state("networkidle")
        
        # In case the direct URL didn't work and routed to main HW page
        if "/course/homework/" in page.url and "submissionList" not in page.url:
            try:
                page.locator('a:has-text("繳交狀況")').click(timeout=3000)
            except:
                try:
                    page.locator('a:has-text("批改作業")').click(timeout=3000)
                except:
                    pass
            page.wait_for_load_state("networkidle")

        try:
            # Check 'select all' checkbox
            page.locator('th input[type="checkbox"], input[aria-label="全選"], .select-all').first.click(timeout=3000)
            print("Selected all submissions.")
        except Exception as e:
            print("Failed to select all:", e)

        try:
            # Click package download
            page.locator('button:has-text("打包下載"), a:has-text("打包下載"), button:has-text("下載"), a:has-text("批次下載")').first.click(timeout=3000)
            print("Clicked package download button.")
            
            time.sleep(3) # Wait for modal/generation
            
            with page.expect_download(timeout=15000) as download_info:
                # Click the generated link
                page.locator('.modal a, .bootbox a, a[href*=".zip"], a:has-text("下載")').first.click(timeout=5000)
                
            download = download_info.value
            filepath = os.path.join(save_dir, f"hw_{hw_id}.zip")
            download.save_as(filepath)
            print(f"Successfully downloaded: {filepath}")
        except Exception as e:
            print(f"Failed during download flow for {hw_id}: {e}")

    browser.close()

with sync_playwright() as p:
    run(p)
