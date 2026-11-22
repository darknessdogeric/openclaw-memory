"""Check Edge process state and CDP port."""
import psutil
import urllib.request
import urllib.error

# Check Edge processes
print("=" * 60)
print("Edge processes:")
print("=" * 60)
for p in psutil.process_iter(['name', 'pid', 'cmdline']):
    n = (p.info.get('name') or '').lower()
    if 'msedge' in n and 'webview2' not in n:
        cmdline = ' '.join(p.info.get('cmdline') or [])[:200]
        print(f"PID={p.info['pid']:6} NAME={p.info['name']}")
        print(f"  CMD: {cmdline}")

# Check CDP port 9222
print()
print("=" * 60)
print("CDP port 9222:")
print("=" * 60)
try:
    r = urllib.request.urlopen('http://127.0.0.1:9222/json/version', timeout=3)
    print(f"CDP OPEN status={r.status}")
    print(r.read().decode()[:500])
except urllib.error.URLError as e:
    print(f"CDP NOT OPEN: {e}")