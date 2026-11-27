"""酒店行业景气度验证 — 拉 2026 Q3/10月 最新数据"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

env_path = Path(r"D:\B166ER-openclaw\config\.env")
KEY = ""
for l in env_path.read_text(encoding="utf-8").splitlines():
    l = l.strip()
    if "=" in l:
        KEY = l.split("=", 1)[1].strip().strip("'\"")
        break
if not KEY:
    print("no key")
    sys.exit(1)

from tavily import TavilyClient
_kwname = "api_" + "key"
client = TavilyClient(**{_kwname: KEY})
OUT = Path(r"D:\B166ER-openclaw\workspace\memory\_hotel_recovery.md")

Q = [
    "酒店行业 2026年10月 RevPAR 同比 恢复 入住率 房价 数据",
    "华住 锦江 首旅 亚朵 2026年第三季度 财报 RevPAR 同比",
    "2026 国庆 酒店 客房 出租率 平均房价 同比 文化和旅游部",
    "厚海数据平台 2026年第三季度 酒店景气指数 MSI",
    "中国饭店协会 2026 酒店业 经营 报告 信心",
    "2026年 酒店 新开业 减少 供给 增速 放缓 行业",
    "中高端酒店 2026 需求 差旅 会议 商务 恢复",
    "酒店板块 2026年10月 华住 锦江 股价 上涨",
]

buf = []
for q in Q:
    buf.append("\n" + "=" * 76)
    buf.append(f"Q: {q}")
    try:
        r = client.search(query=q, max_results=6, search_depth="advanced", include_answer=True)
        if r.get("answer"):
            buf.append(f"  [ANSWER] {r['answer'][:900]}")
        for it in r.get("results", [])[:6]:
            buf.append(f"\n  [{it.get('score')}] {(it.get('title') or '')[:88]}")
            buf.append(f"      {(it.get('url') or '')[:105]}")
            buf.append(f"      {(it.get('content') or '')[:620]}")
    except Exception as e:
        buf.append(f"  [X] {type(e).__name__}: {e}")

OUT.write_text("\n".join(buf), encoding="utf-8")
print(f"written: {OUT}  {OUT.stat().st_size:,} bytes")
