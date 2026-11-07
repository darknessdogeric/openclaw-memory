"""用 Playwright 抓 Kimi 公开帮助文档 (等 React 渲染完再取文本)"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

URLS = [
    ("Kimi PPT 帮助总览", "https://www.kimi.com/help/ppt/ppt-overview"),
    ("Kimi PPT 教程页", "https://www.kimi.com/help/ppt"),
    ("Kimi Slides 功能页", "https://www.kimi.com/features/slides"),
]

SKIP = {"首页", "登录", "注册", "下载", "更多", "关于", "帮助", "文档", "API", "Kimi",
        "kimi", "价格", "企业版", "探索", "隐私", "条款", "设置", "退出", "新对话",
        "深度研究", "联网搜索", "写作助手", "总结", "翻译", "文档助手"}

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    for name, url in URLS:
        print("=" * 78)
        print(f"【{name}】 {url}")
        print("=" * 78)
        page = b.new_page(viewport={"width": 1440, "height": 1000},
                          user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(4500)
            # 滚动触发懒加载
            for _ in range(3):
                page.mouse.wheel(0, 1400)
                page.wait_for_timeout(900)
            page.wait_for_timeout(2000)
            text = page.inner_text("body")
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            kept, seen = [], set()
            for l in lines:
                if l in SKIP or len(l) < 2 or l in seen:
                    continue
                seen.add(l)
                kept.append(l)
            print(f"  有效行数: {len(kept)}\n")
            for l in kept[:90]:
                print("   ", l[:160])
        except Exception as e:
            print(f"  [X] {type(e).__name__}: {e}")
        finally:
            page.close()
        print()
    b.close()
print("DONE")
