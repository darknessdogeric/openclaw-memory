"""完整审计 tavily + scrapling 元信息, 规避编码/语法问题"""
import requests, json, sys

def get_pypi(name):
    r = requests.get(f"https://pypi.org/pypi/{name}/json", timeout=15)
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}"}
    d = r.json()
    i = d["info"]
    rels = list(d.get("releases", {}).keys())
    return {
        "name": i["name"],
        "version": i["version"],
        "summary": i["summary"][:200],
        "author": i["author"],
        "home": i["home_page"],
        "requires_python": i["requires_python"],
        "deps": (i.get("requires_dist") or [])[:6],
        "releases_count": len(rels),
        "last_5": rels[-5:],
    }

def get_github(repo):
    r = requests.get(f"https://api.github.com/repos/{repo}", timeout=15)
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}"}
    d = r.json()
    return {
        "full_name": d.get("full_name"),
        "description": (d.get("description") or "")[:200],
        "stars": d.get("stargazers_count"),
        "forks": d.get("forks_count"),
        "language": d.get("language"),
        "created": d.get("created_at"),
        "updated": d.get("updated_at"),
        "license": (d.get("license") or {}).get("name"),
        "topics": d.get("topics"),
        "homepage": d.get("homepage"),
    }

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

print("=== tavily-python (PyPI) ===")
t = get_pypi("tavily-python")
for k, v in t.items():
    print(f"  {k}: {v}")

print("\n=== scrapling (PyPI) ===")
s = get_pypi("scrapling")
for k, v in s.items():
    print(f"  {k}: {v}")

print("\n=== D4Vinci/Scrapling (GitHub) ===")
g = get_github("D4Vinci/Scrapling")
for k, v in g.items():
    print(f"  {k}: {v}")

print("\n=== tavily 残留检查 ===")
import subprocess
r1 = subprocess.run(["pip", "show", "tavily-python"], capture_output=True, text=True)
print("  pip show tavily-python:", "FOUND" if "Name:" in r1.stdout else "NOT INSTALLED")
r2 = subprocess.run(["pip", "show", "tavily"], capture_output=True, text=True)
print("  pip show tavily:        ", "FOUND" if "Name:" in r2.stdout else "NOT INSTALLED")