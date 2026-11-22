# -*- coding: utf-8 -*-
"""
skyvern_client.py - 兼容垫片 (shim)
历史：AGENTS.md 提到 from toolbox.skyvern_client import diagnose，
实际 Skyvern 能力集成在 scrape_matrix.py 的 VisionAdapter / SkyvernAdapter。
"""
from __future__ import annotations
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

try:
    from toolbox.scrape_matrix import SkyvernAdapter, VisionAdapter  # type: ignore

    def diagnose(url: str = "", prompt: str = ""):
        """历史接口：等价于 VisionAdapter 的页面理解"""
        adapter = VisionAdapter() if VisionAdapter else SkyvernAdapter()
        return adapter.scrape(url, prompt=prompt) if hasattr(adapter, "scrape") else {"status": "no_scrape"}

    def get_status():
        return {
            "skyvern_available": True,
            "vision_available": True,
            "note": "via scrape_matrix VisionAdapter / SkyvernAdapter",
        }

except ImportError as e:
    print(f"FATAL: scrape_matrix Skyvern/Vision adapter import failed: {e}", file=sys.stderr)

    def diagnose(*args, **kwargs):
        return {"status": "unavailable", "error": "scrape_matrix not importable"}

    def get_status():
        return {"skyvern_available": False, "vision_available": False}