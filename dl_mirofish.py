import urllib.request, zipfile, os

MIRRORS = [
    "https://ghproxy.com/https://github.com/666ghj/MiroFish/archive/refs/heads/main.zip",
    "https://gitclone.com/github.com/666ghj/MiroFish/archive/main.zip",
    "https://hub.fastgit.xyz/666ghj/MiroFish/archive/main.zip",
    "https://gh.api.99988866.xyz/https://github.com/666ghj/MiroFish/archive/refs/heads/main.zip",
]

OUT = r"C:\Users\Administrator\.openclaw\workspace\MiroFish.zip"
DEST = r"C:\Users\Administrator\.openclaw\workspace\MiroFish"

for url in MIRRORS:
    try:
        print(f"Trying: {url[:80]}...")
        r = urllib.request.urlopen(url, timeout=60)
        size = r.headers.get("Content-Length", "?")
        print(f"  Status: {r.status}, Size: {size}")
        if r.status == 200:
            data = r.read()
            with open(OUT, 'wb') as f:
                f.write(data)
            print(f"  Downloaded {len(data):,} bytes!")
            
            # Extract
            with zipfile.ZipFile(OUT) as z:
                names = z.namelist()
                root = names[0].split('/')[0]
                z.extractall(r"C:\Users\Administrator\.openclaw\workspace")
            if os.path.exists(DEST):
                import shutil
                shutil.rmtree(DEST)
            os.rename(os.path.join(r"C:\Users\Administrator\.openclaw\workspace", root), DEST)
            print(f"  Extracted to {DEST}")
            break
    except Exception as e:
        print(f"  Failed: {type(e).__name__}: {str(e)[:60]}")

if not os.path.exists(DEST):
    print("\nALL MIRRORS FAILED")
else:
    print(f"\nDONE: {DEST}")
