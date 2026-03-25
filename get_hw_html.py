from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    print("Navigating to login...")
    page.goto('https://ncueeclass.ncu.edu.tw')
    print("Pre-login Title:", page.title())
    
    page.fill('input[name="account"]', 'A165741')
    page.fill('input[name="password"]', '^%$#2wsx1qaz')
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")
    print("Post-login Title:", page.title())

    print("Navigating to homework list...")
    page.goto('https://ncueeclass.ncu.edu.tw/course/homeworkList/38662')
    page.wait_for_load_state("networkidle")
    
    html = page.content()
    with open("hw_list.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved hw_list.html")
    browser.close()

with sync_playwright() as p:
    run(p)
