"""通过 gitclone.com 代理下载 GitHub tar.gz"""
import urllib.request, tarfile, io, os, shutil

# codeload.github.com 是 GitHub 的 archive CDN，路由可能不同
URLS = [
    "https://gitclone.com/github.com/666ghj/MiroFish/archive/refs/heads/main.tar.gz",
    "https://codeload.github.com/666ghj/MiroFish/tar.gz/refs/heads/main",
]

DEST = r"C:\Users\Administrator\.openclaw\workspace\MiroFish"
if os.path.exists(DEST):
    shutil.rmtree(DEST, ignore_errors=True)

for url in URLS:
    try:
        print(f"Trying: {url[:80]}...")
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/octet-stream"
        })
        
        # Stream download
        CHUNK = 65536
        data = bytearray()
        with urllib.request.urlopen(req, timeout=120) as resp:
            print(f"  Status: {resp.status}, Content-Length: {resp.headers.get('Content-Length','?')}")
            total = 0
            while True:
                chunk = resp.read(CHUNK)
                if not chunk:
                    break
                data.extend(chunk)
                total += len(chunk)
                if total % (CHUNK * 100) == 0:
                    print(f"  ... {total:,} bytes")
        
        print(f"  Downloaded {len(data):,} bytes")
        
        if len(data) < 10000:
            print(f"  Too small ({len(data)} bytes), not a valid tarball")
            continue
        
        # Extract
        print("  Extracting...")
        with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as tar:
            root = tar.getnames()[0].split('/')[0]
            tar.extractall(path=r"C:\Users\Administrator\.openclaw\workspace")
        
        extracted = os.path.join(r"C:\Users\Administrator\.openclaw\workspace", root)
        if os.path.exists(extracted):
            os.rename(extracted, DEST)
        
        # Verify
        files = len(list(os.scandir(DEST)))
        print(f"  ✅ SUCCESS! {files} files in {DEST}")
        break
        
    except Exception as e:
        print(f"  ❌ {type(e).__name__}: {str(e)[:80]}")

if not os.path.exists(DEST):
    print("\n❌ ALL METHODS FAILED")
    print("Network IS working for DNS and basic HTTP, but GitHub's data servers are blocked.")
    print("This is a typical Great Firewall pattern - GitHub.com resolves but data transfer is throttled/blocked.")
else:
    print(f"\n✅ Repo ready at: {DEST}")
