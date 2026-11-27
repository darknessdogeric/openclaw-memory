"""逆向 Kimi PPT 的【方法论规格】: 抓公开帮助文档, 抽取输入/输出/工作流
只抓公开页面 (无需登录), 不碰私有接口
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from scrapling import StealthyFetcher

URLS = [
    ("Kimi PPT 帮助", "https://www.kimi.com/help/ppt/ppt-overview"),
    ("Kimi Slides 功能页", "https://www.kimi.com/features/slides"),
    ("Kimi PPT 教程", "https://www.kimi.com/help/ppt"),
]

for name, url in URLS:
    print("=" * 78)
    print(f"【{name}】 {url}")
    print("=" * 78)
    try:
        page = StealthyFetcher.fetch(url, headless=True, network_idle=True,
                                     timeout=30000, retries=2, retry_delay=2)
        st = getattr(page, "status", "?")
        print(f"  HTTP {st}")
        text = page.get_text() if hasattr(page, "get_text") else str(page)
        # 压缩空白
        text = re.sub(r"\n{3,}", "\n\n", text)
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        # 过滤导航噪音
        skip = {"首页", "登录", "注册", "下载", "更多", "关于", "帮助", "文档", "API",
                "Kimi", "kimi", "价格", "企业版", "探索", "首页概览", "隐私", "条款"}
        kept = [l for l in lines if l not in skip and len(l) > 1]
        print(f"  有效行数: {len(kept)}")
        for l in kept[:70]:
            print("   ", l[:150])
    except Exception as e:
        print(f"  [X] {type(e).__name__}: {e}")
    print()
