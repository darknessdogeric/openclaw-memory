# -*- coding: utf-8 -*-
"""
tavily_search.py - 兼容垫片 (shim)
历史：TOOLS.md 误描述为独立脚本，实际 Tavily 集成在 scrape_matrix.py 的 TavilyAdapter。
本文件保留以保证旧 import 路径不破。
"""
from __future__ import annotations
import sys, os
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

try:
    from toolbox.scrape_matrix import TavilyAdapter, ScrapeResult  # type: ignore
    _ADAPTER = TavilyAdapter()

    def search(query: str, max_results: int = 5, include_answer: bool = True):
        """
        用法: tavily_search.search("你的 query")
        内部走 scrape_matrix.TavilyAdapter
        """
        return _ADAPTER.scrape("__search__", query=query, max_results=max_results, include_answer=include_answer)

    def is_available() -> bool:
        return _ADAPTER.is_available()

    if __name__ == "__main__":
        import argparse
        p = argparse.ArgumentParser()
        p.add_argument("--query", required=True)
        p.add_argument("--max-results", type=int, default=5)
        a = p.parse_args()
        r = search(a.query, a.max_results)
        print(f"Status: {r.status}, tool: {r.tool_used}, content_len: {len(r.content)}")
        print(r.content[:2000])

except ImportError as e:
    print(f"FATAL: scrape_matrix.TavilyAdapter import failed: {e}", file=sys.stderr)
    print("Fix: ensure D:\\B166ER-OpenClaw\\workspace\\toolbox\\scrape_matrix.py exists.", file=sys.stderr)
    sys.exit(1)