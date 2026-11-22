# -*- coding: utf-8 -*-
"""
invisible_playwright.py - 兼容垫片 (shim)
历史：AGENTS.md 提到 from invisible_playwright import ...，实际集成在 scrape_matrix.py 的 InvisiblePlaywrightAdapter。
"""
from __future__ import annotations
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

try:
    from toolbox.scrape_matrix import InvisiblePlaywrightAdapter  # type: ignore
    _ADAPTER = InvisiblePlaywrightAdapter()

    def scrape(url: str, **kwargs):
        return _ADAPTER.scrape(url, **kwargs)

    def is_available() -> bool:
        return _ADAPTER.is_available()

except ImportError as e:
    print(f"FATAL: scrape_matrix.InvisiblePlaywrightAdapter import failed: {e}", file=sys.stderr)
    sys.exit(1)