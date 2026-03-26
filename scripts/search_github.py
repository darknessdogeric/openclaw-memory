import requests, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

keywords = [
    'hotel operations manual',
    'hotel standard operating procedure', 
    'hospitality SOP',
    'hotel training manual',
    'hotel front desk procedures'
]

for kw in keywords:
    url = f'https://api.github.com/search/repositories?q={kw.replace(" ", "+")}&sort=stars&per_page=5'
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            print(f'=== {kw} ({data.get("total_count", 0)} results) ===')
            for item in data.get('items', [])[:3]:
                print(f'  - {item["full_name"]} | Stars: {item["stargazers_count"]}')
            print()
    except Exception as e:
        print(f'Error: {e}')
