"""测试 GitHub 镜像连通性"""
import urllib.request, socket, time

MIRRORS = [
    "https://kkgithub.com",
    "https://hub.fastgit.org", 
    "https://gitclone.com",
    "https://ghproxy.com",
    "https://gh.con.sh",
    "https://github.com.cnpmjs.org",
    "https://mirror.ghproxy.com",
    "https://gh.api.99988866.xyz",
]

for url in MIRRORS:
    try:
        t0 = time.time()
        r = urllib.request.urlopen(url, timeout=8)
        elapsed = time.time() - t0
        print(f"  ✅ {url:45s} {r.status} {elapsed:.1f}s")
    except Exception as e:
        print(f"  ❌ {url:45s} {type(e).__name__}")

# Also test Docker Hub
for url in ["https://registry-1.docker.io", "https://hub.docker.com"]:
    try:
        t0 = time.time()
        r = urllib.request.urlopen(url, timeout=8)
        elapsed = time.time() - t0
        print(f"  ✅ {url:45s} {r.status} {elapsed:.1f}s")
    except Exception as e:
        print(f"  ❌ {url:45s} {type(e).__name__}")
