"""Debug: test HTML parsing against 500.com"""
import urllib.request, re, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://datachart.500.com/dlt/history/newinc/history.php?start=26075&end=26076'
headers = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'zh-CN,zh;q=0.9'}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('gbk', errors='replace')

print(f"HTML length: {len(html)}")
print(f"Contains tdata: {'tdata' in html}")
print(f"Contains tbody: {'tbody' in html}")

# Find tbody with id=tdata
idx = html.find('id="tdata"')
if idx < 0:
    idx = html.find("id='tdata'")
print(f"id=tdata at position: {idx}")

# Try multiple regex patterns
patterns = [
    r'<tbody\s+id="tdata">(.*?)</tbody>',
    r"<tbody\s+id='tdata'>(.*?)</tbody>",
    r'<tbody[^>]*id="tdata"[^>]*>(.*?)</tbody>',
    r'<tbody[^>]*id=\'tdata\'[^>]*>(.*?)</tbody>',
    r'<tbody[^>]*id=.tdata.[^>]*>(.*?)</tbody>',
]

for i, pat in enumerate(patterns):
    m = re.search(pat, html, re.DOTALL | re.IGNORECASE)
    if m:
        body = m.group(1)
        print(f"Pattern {i} matched! Body length: {len(body)}")
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', body, re.DOTALL)
        print(f"  Found {len(rows)} tr rows")
        
        # Try to parse data rows
        for j, row in enumerate(rows):
            tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            tds_clean = [re.sub(r'<[^>]*>', '', t).strip() for t in tds]
            if len(tds_clean) >= 10:
                print(f"  Row {j}: {len(tds_clean)} tds")
                for k in range(min(15, len(tds_clean))):
                    print(f"    td[{k}]: [{tds_clean[k]}]")
                break
        break
else:
    print("No pattern matched tbody#tdata")
    # Show snippet
    if idx > 0:
        print(f"\nContext around tdata:")
        print(html[max(0,idx-80):idx+300])
