"""用 Scrapling 抓 GitHub tree 页, 绕过 API 限流, 拿到 skills/ 全量 slug"""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path.home() / ".open-design-skill" / "repo"
RAW = "https://raw.githubusercontent.com/nexu-io/open-design/main"

try:
    # Scrapling 0.5: from scrapling import Fetcher / StealthyFetcher
    # 注意: Fetcher.get() 不接受 stealth 参数 (0.5 拆成了独立类)
    from scrapling import StealthyFetcher
except Exception as e:
    print("scrapling import failed:", e)
    sys.exit(1)

url = "https://github.com/nexu-io/open-design/tree/main/skills"
print(f"抓取 {url} ...")
try:
    page = StealthyFetcher.fetch(url, headless=True, network_idle=True,
                                 timeout=30000, retries=3, retry_delay=2)
except Exception as e:
    print("stealth 抓取失败, 退回普通 Fetcher:", type(e).__name__, e)
    try:
        from scrapling import Fetcher
        page = Fetcher.get(url, timeout=30000, retries=3)
    except Exception as e2:
        print("普通抓取也失败:", type(e2).__name__, e2)
        sys.exit(1)

html = page.html_content if hasattr(page, "html_content") else str(page)
print(f"HTML {len(html)} bytes")

# GitHub tree 页把数据放在 react-app.embeddedData
slugs = set()
m = re.search(r'<script type="application/json" data-target="react-app\.embeddedData">(.*?)</script>',
              html, re.S)
if m:
    try:
        data = json.loads(m.group(1))
        txt = json.dumps(data)
        for mm in re.finditer(r'"name":"([^"]+)","path":"skills/([^"/]+)"', txt):
            slugs.add(mm.group(2))
    except Exception as e:
        print("JSON parse failed:", e)

if not slugs:
    # 兜底: 直接抓路径片段
    for mm in re.finditer(r'/nexu-io/open-design/tree/main/skills/([A-Za-z0-9._-]+)', html):
        slugs.add(mm.group(1))

print(f"解析到 {len(slugs)} 个 slug")
if not slugs:
    print("❌ 未解析到, 放弃")
    sys.exit(2)

sk_dir = ROOT / "skills"
sk_dir.mkdir(parents=True, exist_ok=True)

import requests
S = requests.Session()
S.headers.update({"User-Agent": "B166ER-skill-bootstrap"})


def grab(slug):
    dest = sk_dir / slug / "SKILL.md"
    if dest.exists() and dest.stat().st_size > 100:
        return "skip"
    try:
        r = S.get(f"{RAW}/skills/{slug}/SKILL.md", timeout=25)
        if r.status_code == 200 and len(r.text) > 100:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(r.text, encoding="utf-8")
            return "ok"
        return "miss"
    except Exception:
        return "err"


with ThreadPoolExecutor(max_workers=16) as ex:
    res = list(ex.map(grab, sorted(slugs)))

from collections import Counter
print("拉取结果:", dict(Counter(res)))
fs = [f for f in sk_dir.rglob("SKILL.md")]
print(f"落盘 {len(fs)} 个 SKILL.md, {sum(f.stat().st_size for f in fs)/1024:.0f} KB")
