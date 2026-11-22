"""Step 2 (v3): Use Python with no append, write to .part then rename. Verify SHA256 against official."""
import os, urllib.request, hashlib, sys, time

URL = "https://github.com/iOfficeAI/OfficeCLI/releases/download/v1.0.135/officecli-win-x64.exe"
TARGET_DIR = r"D:\OfficeCLI-test"
TARGET_FILE = os.path.join(TARGET_DIR, "officecli.exe")
PART_FILE = TARGET_FILE + ".part"
EXPECTED_SIZE = 33111928
EXPECTED_SHA256 = "937db176b585e874aa5bff48d536bce78037665cd862b5deefe56e79977e6588"

# Remove any partial file
if os.path.exists(PART_FILE):
    os.remove(PART_FILE)

print(f"URL: {URL}")
print(f"Target: {TARGET_FILE}")
print(f"Expected size: {EXPECTED_SIZE:,}")
print(f"Expected SHA256: {EXPECTED_SHA256}")
print()
print("Starting fresh download...")
sys.stdout.flush()

req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req, timeout=120)
total = int(response.headers.get('Content-Length', EXPECTED_SIZE))
downloaded = 0
sha = hashlib.sha256()
last_print = time.time()
chunk = 1024 * 1024  # 1MB
with open(PART_FILE, 'wb') as f:
    while True:
        c = response.read(chunk)
        if not c:
            break
        f.write(c)
        sha.update(c)
        downloaded += len(c)
        now = time.time()
        if now - last_print > 1:
            pct = downloaded * 100 / total
            print(f"  {downloaded:,}/{total:,} ({pct:.1f}%)", flush=True)
            last_print = now

print()
print(f"Downloaded: {downloaded:,} bytes")
print(f"Computed SHA256: {sha.hexdigest()}")
print(f"Expected SHA256: {EXPECTED_SHA256}")
print(f"Match: {sha.hexdigest() == EXPECTED_SHA256}")

if sha.hexdigest() == EXPECTED_SHA256 and downloaded == EXPECTED_SIZE:
    os.rename(PART_FILE, TARGET_FILE)
    print(f"SUCCESS: Renamed to {TARGET_FILE}")
else:
    print("FAIL: Hash mismatch. Will need to retry.")
    if os.path.exists(PART_FILE):
        os.remove(PART_FILE)
