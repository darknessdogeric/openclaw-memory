"""skills/ 直连 raw 拉取 — 目录名获取加兜底 (Contents API 限流时改用 Trees API)"""
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = "nexu-io/open-design"
API = f"https://api.github.com/repos/{REPO}"
RAW = f"https://raw.githubusercontent.com/{REPO}/main"
ROOT = Path.home() / ".open-design-skill" / "repo"

S = requests.Session()
S.headers.update({"User-Agent": "B166ER-skill-bootstrap",
                  "Accept": "application/vnd.github+json"})


def get_slugs():
    # 方案1: Contents API
    try:
        r = S.get(f"{API}/contents/skills", timeout=30)
        if r.status_code == 200:
            j = r.json()
            if isinstance(j, list):
                slugs = [i["name"] for i in j if i.get("type") == "dir"]
                if slugs:
                    print(f"  [Contents API] {len(slugs)} 个目录")
                    return slugs
            else:
                print(f"  [Contents API 非列表] {str(j)[:150]}")
        else:
            print(f"  [Contents API HTTP {r.status_code}] {r.text[:120]}")
    except Exception as e:
        print(f"  [Contents API 异常] {e}")

    # 方案2: Trees API 兜底
    try:
        r = S.get(f"{API}/git/trees/main?recursive=1", timeout=90)
        if r.status_code == 200:
            j = r.json()
            paths = j.get("tree", [])
            slugs = set()
            for it in paths:
                p = it.get("path", "")
                if p.startswith("skills/") and "/SKILL.md" in p:
                    slugs.add(p.split("/")[1])
            print(f"  [Trees API 兜底] {len(slugs)} 个目录 (tree {len(paths)} 条)")
            return sorted(slugs)
        print(f"  [Trees API HTTP {r.status_code}]")
    except Exception as e:
        print(f"  [Trees API 异常] {e}")
    return []


slugs = get_slugs()
if not slugs:
    print("❌ 无法获取 skills 目录名")
    sys.exit(1)

sk_dir = ROOT / "skills"
sk_dir.mkdir(parents=True, exist_ok=True)


def grab(slug):
    dest = sk_dir / slug / "SKILL.md"
    if dest.exists() and dest.stat().st_size > 100:
        return "skip"
    for _ in range(2):
        try:
            rr = S.get(f"{RAW}/skills/{slug}/SKILL.md", timeout=25)
            if rr.status_code == 200 and len(rr.text) > 100:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(rr.text, encoding="utf-8")
                return "ok"
            if rr.status_code == 404:
                return "miss"
        except Exception:
            time.sleep(1)
    return "err"


t0 = time.time()
with ThreadPoolExecutor(max_workers=16) as ex:
    res = list(ex.map(grab, slugs))
print(f"  拉取结果: {dict(Counter(res))}  耗时 {time.time()-t0:.0f}s")

print("\n=== 落盘统计 ===")
for sub in ["design-systems", "design-templates", "skills", "craft"]:
    d = ROOT / sub
    if d.exists():
        fs = [f for f in d.rglob("*") if f.is_file()]
        size = sum(f.stat().st_size for f in fs)
        print(f"  {sub:20} {len(fs):>5} files  {size/1024:>8.0f} KB")

print("\n=== skills 名单 ===")
names = sorted(slugs)
for i in range(0, len(names), 5):
    print("  " + " | ".join(n[:24].ljust(24) for n in names[i:i + 5]))
