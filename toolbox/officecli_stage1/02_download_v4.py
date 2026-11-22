"""Step 2 (v4): Chunked download with retries, no partial file corruption."""
import os, urllib.request, hashlib, sys, time

URL = "https://github.com/iOfficeAI/OfficeCLI/releases/download/v1.0.135/officecli-win-x64.exe"
TARGET_DIR = r"D:\OfficeCLI-test"
PART_FILE = os.path.join(TARGET_DIR, "officecli.exe.part")
TARGET_FILE = os.path.join(TARGET_DIR, "officecli.exe")
EXPECTED_SIZE = 33111928
EXPECTED_SHA256 = "937db176b585e874aa5bff48d536bce78037665cd862b5deefe56e79977e6588"
CHUNK_SIZE = 1024 * 256  # 256KB

os.makedirs(TARGET_DIR, exist_ok=True)

# Try downloading via HTTP chunked ranges to handle connection resets.
# Strategy: download entire file but with retries; on failure, get current size and resume.

def get_remote_size(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Range': 'bytes=0-0'})
        resp = urllib.request.urlopen(req, timeout=20)
        # Content-Range: bytes 0-0/TOTAL
        cr = resp.headers.get('Content-Range', '')
        if '/' in cr:
            return int(cr.split('/')[1])
        return int(resp.headers.get('Content-Length', EXPECTED_SIZE))
    except Exception as e:
        print(f"  size check err: {e}")
        return EXPECTED_SIZE

expected = get_remote_size(URL)
print(f"Remote size: {expected:,}")

downloaded = 0
attempt = 0
max_attempts = 30

while attempt < max_attempts and downloaded < expected:
    attempt += 1
    try:
        print(f"\n[Attempt {attempt}] Resuming from {downloaded:,}")
        req = urllib.request.Request(URL, headers={
            'User-Agent': 'Mozilla/5.0',
            'Range': f'bytes={downloaded}-'
        })
        resp = urllib.request.urlopen(req, timeout=60)
        mode = 'ab' if downloaded > 0 else 'wb'
        last_print = time.time()
        last_pct = -1
        with open(PART_FILE, mode) as f:
            while True:
                c = resp.read(CHUNK_SIZE)
                if not c:
                    break
                f.write(c)
                downloaded += len(c)
                now = time.time()
                pct = downloaded * 100 // expected
                if now - last_print > 0.5 or pct != last_pct:
                    print(f"  {downloaded:,}/{expected:,} ({pct}%)", flush=True)
                    last_print = now
                    last_pct = pct
        print(f"  Connection closed cleanly at {downloaded:,}")
    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}")
        time.sleep(2)

print()
print(f"Final: {downloaded:,} bytes (target {expected:,})")

if downloaded != expected:
    print(f"FAIL: size mismatch")
    sys.exit(1)

# Verify SHA256
sha = hashlib.sha256()
with open(PART_FILE, 'rb') as f:
    while True:
        c = f.read(1024 * 1024)
        if not c: break
        sha.update(c)
print(f"Computed SHA256: {sha.hexdigest()}")
print(f"Expected SHA256: {EXPECTED_SHA256}")
print(f"Match: {sha.hexdigest() == EXPECTED_SHA256}")

if sha.hexdigest() == EXPECTED_SHA256:
    os.rename(PART_FILE, TARGET_FILE)
    print(f"SUCCESS -> {TARGET_FILE}")
else:
    print("FAIL: Hash mismatch")
    if os.path.exists(PART_FILE):
        os.remove(PART_FILE)
    sys.exit(1)
