"""
MediaCrawler xhs 干跑测试 - 无登录模式
Eric 2026-07-05 决策点 B：用备用账号前先验证 xhs 在无登录下的反应
"""
import asyncio
import sys

# Force UTF-8 output
if sys.stdout and hasattr(sys.stdout, 'buffer'):
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Override config BEFORE main.py loads it
import config
config.HEADLESS = True  # 不弹浏览器窗口
config.ENABLE_CDP_MODE = False  # 用 Playwright 独立实例
config.CDP_CONNECT_EXISTING = False
config.CRAWLER_MAX_NOTES_COUNT = 3  # 极小数据量
config.CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 2
config.KEYWORDS = "成都酒店"  # 测试词
config.LOGIN_TYPE = "cookie"  # 试 cookie 模式（不会真的去 login）
config.COOKIES = ""  # 空 cookies = 等同无登录
config.SAVE_DATA_OPTION = "jsonl"
config.ENABLE_GET_MEIDAS = False  # 不下载图片/视频
config.ENABLE_GET_COMMENTS = False  # 暂时不抓评论

print(f"=== Config Override Applied ===")
print(f"HEADLESS: {config.HEADLESS}")
print(f"ENABLE_CDP_MODE: {config.ENABLE_CDP_MODE}")
print(f"KEYWORDS: {config.KEYWORDS}")
print(f"CRAWLER_MAX_NOTES_COUNT: {config.CRAWLER_MAX_NOTES_COUNT}")
print(f"LOGIN_TYPE: {config.LOGIN_TYPE}")
print(f"---")

# Now run main
try:
    import main
    asyncio.run(main.main())
except Exception as e:
    print(f"\n=== Test ended with exception ===")
    print(f"Type: {type(e).__name__}")
    print(f"Msg: {str(e)[:800]}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print("\n=== Test completed ===")