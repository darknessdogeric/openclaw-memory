import urllib.request, re, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://datachart.500.com/dlt/history/newinc/history.php?start=26030&end=26037'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
req = urllib.request.Request(url, headers=headers)
try:
    resp = urllib.request.urlopen(req, timeout=15)
    content = resp.read().decode('gbk', errors='replace')

    # Find table rows with lottery data
    pattern = r'<tr[^>]*>\s*<td[^>]*>(\d+)</td>\s*<td[^>]*>(\d+)</td>\s*<td[^>]*>([\d\s,]+)</td>\s*<td[^>]*>([\d\s]+)</td>'
    matches = re.findall(pattern, content)
    for m in matches:
        print(f"Issue: {m[0]}, Red: {m[2].strip()}, Blue: {m[3].strip()}")
except Exception as e:
    print(f'Error: {e}')
