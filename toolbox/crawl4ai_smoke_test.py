"""crawl4ai 最小可行性测试"""
import asyncio
from crawl4ai import AsyncWebCrawler

async def test():
    print("[1/3] 初始化 AsyncWebCrawler ...")
    async with AsyncWebCrawler() as crawler:
        print("[2/3] 抓取 https://example.com ...")
        result = await crawler.arun(
            url="https://example.com",
            bypass_cache=True
        )
        print(f"[3/3] success={result.success}, markdown_length={len(result.markdown or '')}")
        if result.markdown:
            print("=" * 60)
            print("MARKDOWN OUTPUT (前 800 字):")
            print("=" * 60)
            print(result.markdown[:800])
        if not result.success:
            print(f"ERROR: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(test())