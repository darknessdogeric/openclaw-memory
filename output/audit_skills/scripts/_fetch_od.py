"""用 GitHub API 精准拉取 open-design 的 design-systems (只取 DESIGN.md, 不搬 3.5GB)"""
import json
import os
import sys
import time
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = "nexu-io/open-design"
API = f"https://api.github.com/repos/{REPO}/contents"
RAW = f"https://raw.githubusercontent.com/{REPO}/main"
ROOT = Path.home() / ".open-design-skill" / "repo"
SESSION = requests.Session()
SESSION.headers.update({"Accept": "application/vnd.github+json",
                         "User-Agent": "B166ER-skill-bootstrap"})


def api_get(path):
    for attempt in range(4):
        try:
            r = SESSION.get(f"{API}/{path}", timeout=30)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 404:
                return None
            time.sleep(1.5 * (attempt + 1))
        except Exception:
            time.sleep(2)
    return None


# 1. 顶层结构
print("=== 仓库顶层结构 ===")
top = api_get("")
if top:
    for it in top:
        print(f"  {it['type']:5} {it['name']}")

# 2. design-systems 全量拉取
print("\n=== 拉取 design-systems/*/DESIGN.md ===")
ds = api_get("design-systems")
if not ds:
    print("  ❌ 无法列出 design-systems")
    sys.exit(1)

slugs = [it["name"] for it in ds if it["type"] == "dir"]
print(f"  发现 {len(slugs)} 个品牌设计系统")

ds_dir = ROOT / "design-systems"
ds_dir.mkdir(parents=True, exist_ok=True)

ok = fail = 0
for i, slug in enumerate(slugs, 1):
    dest = ds_dir / slug / "DESIGN.md"
    if dest.exists() and dest.stat().st_size > 100:
        ok += 1
        continue
    url = f"{RAW}/design-systems/{slug}/DESIGN.md"
    try:
        r = SESSION.get(url, timeout=30)
        if r.status_code == 200 and len(r.text) > 100:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(r.text, encoding="utf-8")
            ok += 1
        else:
            fail += 1
    except Exception:
        fail += 1
    if i % 25 == 0:
        print(f"    ... {i}/{len(slugs)}  ok={ok} fail={fail}")

print(f"\n  ✅ 成功 {ok} / 失败 {fail}")

# 3. 统计体积
total = 0
cnt = 0
for f in ds_dir.rglob("DESIGN.md"):
    total += f.stat().st_size
    cnt += 1
print(f"  落盘: {cnt} 个 DESIGN.md, {total/1024:.0f} KB")

# 4. 其他目录清单 (只列不拉)
for sub in ["templates", "skills", "craft"]:
    items = api_get(sub)
    if items:
        dirs = [it["name"] for it in items if it["type"] == "dir"]
        files = [it["name"] for it in items if it["type"] == "file"]
        print(f"\n  {sub}/: {len(dirs)} 目录 + {len(files)} 文件")
        if dirs:
            print(f"     目录样例: {', '.join(dirs[:12])}")
        if files:
            print(f"     文件样例: {', '.join(files[:8])}")

print("\nROOT:", ROOT)
