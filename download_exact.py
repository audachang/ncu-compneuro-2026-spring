import requests
import os

urls = {
    "66154": "https://ncueeclass.ncu.edu.tw/homework/package/66154/?ajaxAuth=132e5fc01fb8f336727da02eb6bc9cce&file=2f182a69976fe0ba6816d579831fa16e",
    "66745": "https://ncueeclass.ncu.edu.tw/homework/package/66745/?ajaxAuth=9538e235b4644e77f036bf8a47724a72&file=baff3ee8551bd11261d94a09ba41d48d"
}

cookies = {
    "PHPSESSID": "u8hq18ivkqa4av2ijkrfk9rgfn",
    "accesstoken": "643914289",
    "timezone": "%2B0800"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://ncueeclass.ncu.edu.tw/course/homeworkList/38662"
}

save_dir = os.path.join(os.getcwd(), 'homeworks')
os.makedirs(save_dir, exist_ok=True)

for hw_id, url in urls.items():
    print(f"Downloading HW {hw_id}...")
    res = requests.get(url, cookies=cookies, headers=headers)
    if res.status_code == 200:
        filepath = os.path.join(save_dir, f"hw_{hw_id}.zip")
        with open(filepath, 'wb') as f:
            f.write(res.content)
        print(f"Saved {filepath} ({len(res.content)} bytes)")
    else:
        print(f"Failed to download HW {hw_id}. Status: {res.status_code}")
