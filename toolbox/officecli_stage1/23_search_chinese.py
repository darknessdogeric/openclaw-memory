"""Search OfficeCLI issues for Chinese encoding bugs."""
import urllib.request, json

queries = [
    'chinese',
    'encoding',
    'utf-8',
    'unicode',
    'cjk',
    'chinese characters',
    'mojibake',
]

all_issues = set()
for q in queries:
    url = f'https://api.github.com/search/issues?q=repo:iOfficeAI/OfficeCLI+{q}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=20).read())
        for issue in data.get('items', []):
            all_issues.add((issue['number'], issue['title'], issue['state'], issue['html_url']))
    except Exception as e:
        print(f"Error searching {q}: {e}")

# Filter to relevant ones (Chinese-related)
print(f"Total unique issues found: {len(all_issues)}")
for n, t, s, url in sorted(all_issues):
    relevant = any(kw in t.lower() for kw in ['chinese', 'encoding', 'utf', 'unicode', 'cjk', 'mojibake', '中文', '编码'])
    marker = '***' if relevant else '   '
    safe_t = t.encode('ascii', errors='replace').decode('ascii')
    print(f"{marker} #{n}: [{s}] {safe_t}")
    if relevant:
        print(f"    {url}")
