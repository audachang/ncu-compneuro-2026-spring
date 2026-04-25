"""
Fast midterm grader using requests (no browser needed).
PDFs are already uploaded to eeclass for both students.
Just need to enter scores and submit.
"""

import requests
from bs4 import BeautifulSoup
import json, os, re, sys, time

BASE = "https://ncueeclass.ncu.edu.tw"
ACCOUNT = os.environ.get("EECLASS_ACCOUNT", "A165741")
PASSWORD = os.environ.get("EECLASS_PASSWORD", "^%$#2wsx1qaz")

def login(session):
    """Login and return True if successful."""
    # First visit the main page to get cookies
    r = session.get(BASE, timeout=15)
    print(f"  Initial GET: {r.status_code}")
    
    # POST to login AJAX
    r = session.post(
        f"{BASE}/sys/lib/ajax/login_submit.php",
        data={"account": ACCOUNT, "password": PASSWORD},
        headers={"X-Requested-With": "XMLHttpRequest", "Referer": BASE},
        timeout=15
    )
    print(f"  Login AJAX: {r.status_code}, response: {r.text[:200]}")
    
    # Verify by visiting course page
    time.sleep(1)
    r = session.get(f"{BASE}/course/homeworkList/38662", timeout=15)
    print(f"  Course page: {r.status_code}, URL: {r.url}")
    logged_in = "homeworkList" in r.url or r.status_code == 200
    
    # Check for session conflict - look for redirect
    soup = BeautifulSoup(r.text, 'html.parser')
    conflict = soup.find(text=re.compile("已在其他裝置|登出所有|session"))
    if conflict:
        print(f"  Session conflict detected: {str(conflict)[:100]}")
    
    return r.status_code == 200

def get_submit_list(session, hw_id):
    """Get the submission list and return list of (name, report_url) tuples."""
    r = session.get(f"{BASE}/homework/submitList/{hw_id}", timeout=15)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    students = []
    for a in soup.find_all('a', href=re.compile(r'/homework/report/')):
        text = a.get_text(strip=True)
        href = a.get('href', '')
        if text and '期中' in text or text.endswith('_期中作品') or any(name in text for name in ['呂杰驛','吳心圓','何官臻']):
            students.append((text, href))
    
    print(f"  Found {len(students)} student links: {[(t, h[:60]) for t, h in students]}")
    return students

def get_audit_form(session, report_relative_url):
    """Navigate to report page and return the grading form data."""
    report_url = f"{BASE}{report_relative_url}"
    r = session.get(report_url, timeout=15)
    print(f"  Report page: {r.status_code}")
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Check if already graded
    page_text = soup.get_text()
    if "已批改" in page_text:
        print("  Already graded!")
        # Extract current score
        score_m = re.search(r'分數.*?(\d+)\s*分', page_text, re.DOTALL)
        if score_m:
            print(f"  Current score: {score_m.group(1)}")
        return None, "already_graded"
    
    # Find the 批改 link/button
    audit_link = None
    for a in soup.find_all('a'):
        if '批改' in a.get_text() and 'exerciseAction=auditReport' in a.get('href', ''):
            audit_link = a['href']
            break
    if not audit_link:
        # Try constructing from URL
        match = re.search(r'/homework/report/(\d+)/\?ajaxAuth=(\w+)', report_relative_url)
        if match:
            rid, token = match.groups()
            audit_link = f"/homework/report/{rid}/?exerciseAction=auditReport&_lock=exerciseAction&ajaxAuth={token}"
    
    if not audit_link:
        print("  Could not find audit link")
        return None, "no_audit_link"
    
    print(f"  Navigating to audit form: {audit_link[:80]}")
    r = session.get(f"{BASE}{audit_link}", timeout=15)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Extract form
    form = soup.find('form', {'id': 'homework-audit-setting-form'})
    if not form:
        form = soup.find('form')
    
    if not form:
        print("  No form found on audit page")
        return None, "no_form"
    
    # Get form action
    action = form.get('action', audit_link)
    
    # Get all form fields
    form_data = {}
    for inp in form.find_all(['input', 'textarea', 'select']):
        name = inp.get('name')
        if not name:
            continue
        val = inp.get('value', '')
        form_data[name] = val
    
    print(f"  Form fields: {list(form_data.keys())}")
    print(f"  Form action: {action}")
    return action, form_data

def submit_grade(session, form_action, form_data, score):
    """Submit the grade."""
    form_data['auditScore'] = str(score)
    
    post_url = f"{BASE}{form_action}" if form_action.startswith('/') else form_action
    print(f"  Submitting to: {post_url}")
    print(f"  Score: {score}")
    
    r = session.post(post_url, data=form_data, 
                     headers={"Referer": f"{BASE}/homework/submitList/67993", 
                              "X-Requested-With": "XMLHttpRequest"},
                     timeout=15)
    print(f"  Submit response: {r.status_code}")
    print(f"  Response text: {r.text[:300]}")
    return r.status_code == 200 or r.status_code == 302


if __name__ == "__main__":
    # Load config
    config_path = "/sessions/kind-wizardly-darwin/mnt/2026_Spring_CompBigData/homeworks/midterm/grading_config.json"
    with open(config_path) as f:
        config = json.load(f)
    
    hw_id = config["homework_id"]
    students = config["students"]
    
    print(f"Midterm grading — hw_id: {hw_id}")
    print(f"Students: {[(s['name'], s['score']) for s in students]}")
    
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    
    print("\n=== Logging in ===")
    if not login(session):
        print("Login may have failed, continuing anyway...")
    
    print("\n=== Getting submit list ===")
    submit_entries = get_submit_list(session, hw_id)
    
    # Map name -> report URL
    name_to_url = {}
    for text, href in submit_entries:
        for s in students:
            if s['name'] in text:
                name_to_url[s['name']] = href
                break
    
    print(f"\nFound URLs for: {list(name_to_url.keys())}")
    
    results = []
    for student in students:
        name = student['name']
        score = student['score']
        print(f"\n{'='*50}")
        print(f"Grading: {name} (target score: {score})")
        
        if name not in name_to_url:
            print(f"  No submission found for {name}")
            results.append((name, False, "no submission"))
            continue
        
        report_url = name_to_url[name]
        action, form_data = get_audit_form(session, report_url)
        
        if form_data == "already_graded":
            results.append((name, True, "already graded"))
            continue
        if form_data in ("no_audit_link", "no_form") or form_data is None:
            results.append((name, False, str(form_data)))
            continue
        
        ok = submit_grade(session, action, form_data, score)
        results.append((name, ok, "submitted" if ok else "failed"))
        time.sleep(2)
    
    print(f"\n{'='*50}")
    print("RESULTS:")
    for name, ok, note in results:
        print(f"  {name}: {'OK' if ok else 'FAILED'} ({note})")
