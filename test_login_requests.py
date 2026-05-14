import requests

session = requests.Session()
print("Logging in...")
res = session.post("https://ncueeclass.ncu.edu.tw/sys/lib/ajax/login_submit.php",
                   data={"account": "A165741", "password": "^%$#2wsx1qaz"},
                   headers={"Referer": "https://ncueeclass.ncu.edu.tw/"})
print("Login status:", res.status_code)
print("Response text:", res.text[:200])

print("Getting homework list...")
res = session.get("https://ncueeclass.ncu.edu.tw/course/homeworkList/38662")
if "登出" in res.text or "Logout" in res.text or "A165741" in res.text:
    print("Successfully authenticated and fetched homework list.")
    with open("hw_list.html", "w", encoding="utf-8") as f:
        f.write(res.text)
else:
    print("Authentication check failed. Did not see logout button.")
