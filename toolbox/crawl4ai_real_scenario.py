"""crawl4ai 实战场景：通过 scrape_matrix 抓行业新闻 + LLM 提取结构化"""
import sys
import json

sys.path.insert(0, r"D:\B166ER-OpenClaw\workspace\toolbox")
from scrape_matrix import scrape, matrix_report

# 测试 1：通用网站（GitHub README）—— Markdown 抓取
print("=" * 70)
print("[Test 1] GitHub README - Markdown 抓取")
print("=" * 70)
r1 = scrape(
    "https://github.com/unclecode/crawl4ai",
    task_type="llm-ready"
)
print(f"Status: {r1.status.value}")
print(f"Tool: {r1.tool_used}")
print(f"Content length: {len(r1.content)}")
print(f"\n--- Markdown preview (first 1500 chars) ---")
print(r1.content[:1500])

# 测试 2：另一个网站（避免 GitHub 限速）—— LLM extraction
print("\n" + "=" * 70)
print("[Test 2] Python.org - LLM extraction (DeepSeek)")
print("=" * 70)
schema = {
    "site_name": "网站名称",
    "main_topics": ["3-5 个主要话题"],
    "latest_news": ["最新资讯标题"],
    "download_count": "下载量描述",
}
instruction = """从网页提取：
- site_name: 网站名称
- main_topics: 3-5 个主要话题
- latest_news: 最新资讯标题列表
- download_count: 关于下载量的描述
"""

r2 = scrape(
    "https://www.python.org/",
    task_type="llm-ready",
    extraction_schema=schema,
    extraction_instruction=instruction,
)
print(f"Status: {r2.status.value}")
print(f"Tool: {r2.tool_used}")
# 找 Extracted JSON 部分
if "Extracted JSON" in r2.content:
    json_start = r2.content.find("```json") + len("```json")
    json_end = r2.content.find("```", json_start)
    extracted = r2.content[json_start:json_end].strip()
    print(f"\n--- Extracted JSON ---")
    try:
        parsed = json.loads(extracted)
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Parse error: {e}")
        print(extracted)
else:
    print(f"No extracted JSON in content. Last 500 chars:")
    print(r2.content[-500:])

# 测试 3：matrix 报告
print("\n" + "=" * 70)
print("[Test 3] scrape_matrix 状态报告")
print("=" * 70)
print(json.dumps(matrix_report(), indent=2, ensure_ascii=False))

print("\n" + "=" * 70)
print("[DONE] All tests complete")
print("=" * 70)