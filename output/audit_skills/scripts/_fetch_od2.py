"""按脚本期望路径补拉 design-templates / craft / skills"""
import sys
import time
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = "nexu-io/open-design"
API = f"https://api.github.com/repos/{REPO}/contents"
RAW = f"https://raw.githubusercontent.com/{REPO}/main"
ROOT = Path.home() / ".open-design-skill" / "repo"
S = requests.Session()
S.headers.update({"Accept": "application/vnd.github+json",
                  "User-Agent": "B166ER-skill-bootstrap"})


def api_get(path):
    for a in range(4):
        try:
            r = S.get(f"{API}/{path}", timeout=30)
            if r.status_code in (200, 404):
                return r.json() if r.status_code == 200 else None
            time.sleep(1.5 * (a + 1))
        except Exception:
            time.sleep(2)
    return None


def fetch_tree(sub, exts=None, max_files=400):
    """递归拉取一个目录, 只下指定扩展名"""
    items = api_get(sub)
    if not items:
        print(f"  ❌ {sub} 无法列出")
        return 0
    n = 0
    for it in items:
        if it["type"] == "file":
            path = f"{sub}/{it['name']}"
            if exts and not any(path.endswith(e) for e in exts):
                continue
            dest = ROOT / path
            if dest.exists() and dest.stat().st_size > 0:
                n += 1
                continue
            try:
                r = S.get(it["download_url"], timeout=30)
                if r.status_code == 200:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_text(r.text, encoding="utf-8")
                    n += 1
            except Exception:
                pass
        elif it["type"] == "dir":
            n += fetch_tree(f"{sub}/{it['name']}", exts, max_files - n)
        if n >= max_files:
            break
    return n


print("=== craft/ (13 个方法论参考) ===")
n = fetch_tree("craft", exts=[".md"])
print(f"  拉取 {n} 个文件")

print("\n=== design-templates/ (渲染模板) ===")
items = api_get("design-templates")
if items:
    dirs = [i["name"] for i in items if i["type"] == "dir"]
    print(f"  {len(dirs)} 个模板目录: {', '.join(dirs[:14])}")
n = fetch_tree("design-templates", exts=[".md", ".html", ".css", ".js", ".json", ".txt"], max_files=220)
print(f"  拉取 {n} 个文件")

print("\n=== skills/ (169 个功能 skill, 只取 SKILL.md) ===")
n = fetch_tree("skills", exts=["SKILL.md"], max_files=220)
print(f"  拉取 {n} 个 SKILL.md")

print("\n=== 落盘统计 ===")
for sub in ["design-systems", "design-templates", "skills", "craft"]:
    d = ROOT / sub
    if d.exists():
        files = list(d.rglob("*"))
        fs = [f for f in files if f.is_file()]
        size = sum(f.stat().st_size for f in fs)
        print(f"  {sub:20} {len(fs):>5} files  {size/1024:>8.0f} KB")
