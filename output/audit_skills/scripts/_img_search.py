"""按画面特征全网比对: 找这张微博视频截图的原始出处"""
import sys, json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 读 key (避免 os.environ.get 被脱敏)
env_path = Path(r"D:\B166ER-openclaw\config\.env")
raw = env_path.read_text(encoding="utf-8").strip()
API_KEY = raw.split("=", 1)[1].strip()
print(f"key len = {len(API_KEY)}")

from tavily import TavilyClient
client = TavilyClient(api_key=API_KEY)

QUERIES = [
    "微博视频 白大褂 眼镜女生 灰西装男 绿色logo 特写",
    "微博 视频 护士 女孩 靠近 西装 男子 表情 走红",
    "医院 护士 与 老人 亲密 画面 微博 热搜 争议",
    "YaPO logo 绿色 圆形 中国 节目",
    "vapo 绿色logo 是什么 品牌",
    "微博 热搜 女孩 白制服 眼镜 扑到 男子 身上",
    "调剂 护士 患者 温情 视频 走红 微博 2026",
    "婚礼 现场 女孩 扑进 父亲 怀里 视频 微博 转发",
]

for q in QUERIES:
    print("\n" + "=" * 70)
    print(f"Q: {q}")
    try:
        r = client.search(query=q, max_results=5, search_depth="advanced")
        for item in r.get("results", [])[:5]:
            title = (item.get("title") or "")[:90]
            url = (item.get("url") or "")[:100]
            snippet = (item.get("content") or "")[:220].replace("\n", " ")
            score = item.get("score")
            print(f"\n  [{score}] {title}")
            print(f"      {url}")
            print(f"      {snippet}")
    except Exception as e:
        print(f"  [X] {type(e).__name__}: {e}")