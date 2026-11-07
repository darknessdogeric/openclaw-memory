"""补事实: 2017注入规模 / 并表后表现 / 万达物业管道"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = Path(r"D:\B166ER-openclaw\workspace\memory\_tongcheng_wanda_facts2.md")

env = Path(r"D:\B166ER-openclaw\config\.env").read_text(encoding="utf-8")
API_KEY = ""
for raw in env.splitlines():
    line = raw.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    if k.strip().upper() == "TAVILY_API_KEY":
        API_KEY = v.strip().strip('"').strip("'")
        break

from tavily import TavilyClient
client = TavilyClient(api_key=API_KEY)

QUERIES = [
    "万达酒店发展 2017年 注入 万达酒管 7.5亿 当时 在管酒店数量 家",
    "同程旅行 2026年 中期业绩 万达酒管 并表 贡献 酒店",
    "万达集团 出售 酒店物业 2025 2026 数量 酒店物业 出售 清单",
    "中国酒店管理行业 2026 存量 加盟 RevPAR 下滑 高端酒店 影响",
    "同程旅行 收购万达酒管 协同 会员 导流 直销 分析 质疑",
    "万达酒店发展 特别股息 46.2港仙 去杠杆 债务 出售原因",
]

buf = []
for q in QUERIES:
    buf.append("\n" + "=" * 78)
    buf.append(f"Q: {q}")
    try:
        r = client.search(query=q, max_results=6, search_depth="advanced")
        for item in r.get("results", [])[:6]:
            buf.append(f"\n  [{item.get('score')}] {(item.get('title') or '')[:90]}")
            buf.append(f"      {(item.get('url') or '')[:110]}")
            buf.append(f"      {(item.get('content') or '')[:800]}")
    except Exception as e:
        buf.append(f"  [X] {type(e).__name__}: {e}")

OUT.write_text("\n".join(buf), encoding="utf-8")
print(f"written: {OUT} ({OUT.stat().st_size} bytes)")
