"""同程收购万达酒管 —— 事实核查, 结果写 UTF-8 文件 (控制台是 GBK 乱码)"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = Path(r"D:\B166ER-openclaw\workspace\memory\_tongcheng_wanda_facts.md")

env_path = Path(r"D:\B166ER-openclaw\config\.env")
API_KEY = ""
for raw in env_path.read_text(encoding="utf-8").splitlines():
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
    "同程旅行 24.9亿 收购 万达酒店管理 100%股权 公告 详情",
    "万达酒店管理 估值 19.8倍 EV/EBITDA 可比公司 增值率 业绩承诺",
    "万达酒店管理 2017年 融创 出售 2022年 回购 5.5亿 估值历史",
    "万达酒店管理 门店数 客房数 2025 在管酒店 规模",
    "同程旅行 收购万达酒管 协同 酒店预订 量 转化 点评 分析",
    "同程旅行 2025年 全年业绩 酒店业务 收入 利润",
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
            buf.append(f"      {(item.get('content') or '')[:700]}")
    except Exception as e:
        buf.append(f"  [X] {type(e).__name__}: {e}")

OUT.write_text("\n".join(buf), encoding="utf-8")
print(f"written: {OUT} ({OUT.stat().st_size} bytes)")
