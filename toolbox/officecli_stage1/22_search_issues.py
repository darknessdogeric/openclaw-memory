"""Search OfficeCLI issues for Chinese encoding bug."""
import urllib.request, json

req = urllib.request.Request(
    'https://api.github.com/search/issues?q=repo:iOfficeAI/OfficeCLI+chinese+OR+encoding+OR+utf',
    headers={'User-Agent': 'Mozilla/5.0'}
)
try:
    data = json.loads(urllib.request.urlopen(req, timeout=30).read())
    print(f"Total: {data.get('total_count', 0)}")
    for issue in data.get('items', [])[:20]:
        n = issue['number']
        t = issue['title']
        s = issue['state']
        d = issue['created_at'][:10]
        labels = ','.join([l['name'] for l in issue.get('labels', [])])
        print(f"  #{n}: [{s}] {t} ({d}) labels={labels}")
except Exception as e:
    print(f"Error: {e}")
