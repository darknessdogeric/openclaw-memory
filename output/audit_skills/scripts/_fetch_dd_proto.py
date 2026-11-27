"""拉取 diagram-design 的协议文件 (本地读, 便于按其规范执行)"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import requests

BASE = "https://raw.githubusercontent.com/cathrynlavery/diagram-design/HEAD/skills/diagram-design"
DEST = Path(r"D:\B166ER-openclaw\workspace\memory\_dd_proto")
DEST.mkdir(parents=True, exist_ok=True)

FILES = [
    "SKILL.md",
    "references/style-guide.md",
    "references/output-spec.md",
    "references/semantic-patterns.md",
    "references/type-architecture.md",
    "references/type-high-level.md",
    "references/type-layers.md",
    "references/onboarding.md",
    "references/profiles.md",
]
S = requests.Session()
S.headers.update({"User-Agent": "B166ER-test"})
for f in FILES:
    try:
        r = S.get(f"{BASE}/{f}", timeout=30)
        if r.status_code == 200:
            p = DEST / f.replace("/", "_")
            p.write_text(r.text, encoding="utf-8")
            print(f"  OK {f:<34} {len(r.text):>7,} bytes")
        else:
            print(f"  -- {f:<34} HTTP {r.status_code}")
    except Exception as e:
        print(f"  XX {f:<34} {type(e).__name__}")
print(f"\n-> {DEST}")
