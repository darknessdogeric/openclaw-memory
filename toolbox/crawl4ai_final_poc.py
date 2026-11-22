"""crawl4ai + DeepSeek LLM extraction 最终验证
输出写到 JSON 文件，避免 PowerShell GBK 编码问题
"""
import sys
import os
import json

sys.path.insert(0, r"D:\B166ER-OpenClaw\workspace\toolbox")
from crawl4ai_wrapper import crawl_llm_ready

# 1. GitHub crawl4ai README → LLM 提取
print("[1/2] GitHub crawl4ai README - LLM extraction...")
r1 = crawl_llm_ready(
    "https://github.com/unclecode/crawl4ai",
    extraction_schema={
        "project_name": "项目名称",
        "stars": "GitHub stars (integer)",
        "primary_purpose": "一句话描述项目主要功能",
        "key_features": ["3-5 条核心特性"],
        "tech_stack": ["使用的核心技术"],
        "license": "许可证",
        "latest_version": "最新版本号",
    },
    extraction_instruction="""从 GitHub 项目 README 提取：
- project_name: 项目名称
- stars: 数字形式 stars（去掉 'k' 后乘 1000）
- primary_purpose: 一句话说明项目做什么
- key_features: 3-5 条最重要的功能
- tech_stack: 使用的核心技术（如 Python/Playwright/Docker）
- license: 许可证
- latest_version: 最新版本号""",
)
print(f"  Success: {r1.success} | Elapsed: {r1.elapsed:.1f}s | MD: {len(r1.markdown)} chars")

# 2. python.org → LLM 提取
print("\n[2/2] python.org - LLM extraction...")
r2 = crawl_llm_ready(
    "https://www.python.org/",
    extraction_schema={
        "site_name": "网站名称",
        "main_topics": ["3-5 个主要话题"],
        "latest_news": ["最新新闻标题"],
        "tagline": "网站标语",
    },
    extraction_instruction="""从网页提取：
- site_name: 网站名称
- main_topics: 3-5 个主要话题
- latest_news: 最新新闻标题列表
- tagline: 网站标语或口号""",
)
print(f"  Success: {r2.success} | Elapsed: {r2.elapsed:.1f}s | MD: {len(r2.markdown)} chars")

# 写到 JSON 文件（避免 PowerShell GBK 编码）
out = {
    "test_1_github": {
        "success": r1.success,
        "elapsed_seconds": round(r1.elapsed, 2),
        "markdown_length": len(r1.markdown),
        "extracted": r1.extracted_json,
        "error": r1.error if not r1.success else None,
    },
    "test_2_python_org": {
        "success": r2.success,
        "elapsed_seconds": round(r2.elapsed, 2),
        "markdown_length": len(r2.markdown),
        "extracted": r2.extracted_json,
        "error": r2.error if not r2.success else None,
    },
}

out_path = r"D:\B166ER-OpenClaw\workspace\toolbox\crawl4ai_poc_result.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"\nResults written to: {out_path}")