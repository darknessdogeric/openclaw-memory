"""Step 1: Find latest OfficeCLI release."""
import urllib.request, json

req = urllib.request.Request(
    'https://api.github.com/repos/iOfficeAI/OfficeCLI/releases/latest',
    headers={'User-Agent': 'Mozilla/5.0'}
)
data = json.loads(urllib.request.urlopen(req, timeout=30).read())

print('Tag:', data.get('tag_name'))
print('Name:', data.get('name'))
print('Published:', data.get('published_at'))
print('--- Assets ---')
for a in data.get('assets', []):
    name = a['name']
    size = a['size']
    url = a['browser_download_url']
    print('  ' + name.ljust(50) + ' | ' + str(size).rjust(10) + ' bytes | ' + url)

# Save URL for next step
windows_assets = [a for a in data.get('assets', []) if 'windows' in a['name'].lower() or 'win' in a['name'].lower()]
print('--- Windows candidates ---')
for a in windows_assets:
    print('  ' + a['name'] + ' -> ' + a['browser_download_url'])
