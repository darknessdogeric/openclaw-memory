"""Step 2 (v2): Resilient download with retries and resume support."""
import os, urllib.request, hashlib, time

URL = "https://github.com/iOfficeAI/OfficeCLI/releases/download/v1.0.135/officecli-win-x64.exe"
TARGET_DIR = r"D:\OfficeCLI-test"
TARGET_FILE = os.path.join(TARGET_DIR, "officecli.exe")
EXPECTED_SIZE = 33111928

os.makedirs(TARGET_DIR, exist_ok=True)

def download_with_resume(url, target, expected_size, max_retries=5):
    downloaded = 0
    if os.path.exists(target):
        downloaded = os.path.getsize(target)
        print(f"Resuming from {downloaded:,} bytes")

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0',
                'Range': f'bytes={downloaded}-' if downloaded > 0 else 'bytes=0-'
            })
            response = urllib.request.urlopen(req, timeout=60)
            mode = 'ab' if downloaded > 0 else 'wb'
            chunk_size = 1024 * 512  # 512KB chunks
            last_print = time.time()
            with open(target, mode) as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    now = time.time()
                    if now - last_print > 2:
                        pct = downloaded * 100 / expected_size
                        print(f"  [{attempt}] {downloaded:,}/{expected_size:,} ({pct:.1f}%)", flush=True)
                        last_print = now
            if downloaded >= expected_size:
                return downloaded
            print(f"Attempt {attempt}: got {downloaded:,} bytes (incomplete), retrying...")
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(3)
    return downloaded

print(f"Downloading {URL}")
print(f"Target: {TARGET_FILE}")
print(f"Expected: {EXPECTED_SIZE:,} bytes ({EXPECTED_SIZE/1024/1024:.1f} MB)")

final_size = download_with_resume(URL, TARGET_FILE, EXPECTED_SIZE)
actual = os.path.getsize(TARGET_FILE)
print(f"\nFinal: {actual:,} bytes ({actual/1024/1024:.2f} MB)")
print(f"Match: {actual == EXPECTED_SIZE}")

# SHA256 of full file
sha = hashlib.sha256()
with open(TARGET_FILE, 'rb') as f:
    while True:
        c = f.read(1024*1024)
        if not c: break
        sha.update(c)
print(f"SHA256: {sha.hexdigest()}")
