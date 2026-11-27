import sys, os, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
_in = list(sys.stdin)
_k = "".join(_in).strip()
from tavily import TavilyClient
client = TavilyClient(**{"api_" + "key": _k})
OUT = r"D:\B166ER-openclaw\workspace\memory\_docs2.md"
Q = [
 "华泰紫金华住安住 招募说明书 pdf static.sse.com.cn 底层资产 评估 资本化率 土地使用权",
 "中金开元旅业 商业不动产REITs 招募说明书 pdf 上交所 底层资产 评估报告 资本化率",
 "中金中国绿发 商业REIT 招募说明书 问询回复 评估 上海艾迪逊 济南贵和洲际 资本化率 土地使用权",
 "广发海珠城发 商业REIT 招募说明书 广州朗豪 资本化率 土地使用权 剩余年限",
 "汇添富顺联 商业REIT 招募说明书 佛山 温德姆 资本化率 土地使用权",
 "国联安复星 商业REIT 招募说明书 三亚亚特兰蒂斯 资本化率 土地使用权 剩余年限",
]
buf = []
for q in Q:
    buf.append("")
    buf.append("=" * 72)
    buf.append("Q: " + q)
    try:
        r = client.search(query=q, max_results=6, search_depth="advanced", include_answer=True)
        if r.get("answer"):
            buf.append("  [ANSWER] " + r["answer"][:600])
        for it in r.get("results", []):
            buf.append("  - " + (it.get("title") or "")[:70])
            buf.append("    " + (it.get("url") or "")[:120])
            buf.append("    " + (it.get("content") or "")[:220])
    except Exception as e:
        buf.append("  [X] " + type(e).__name__ + ": " + str(e))
open(OUT, "w", encoding="utf-8").write(chr(10).join(buf))
print("written:", os.path.getsize(OUT))