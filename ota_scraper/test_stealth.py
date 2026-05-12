# -*- coding: utf-8 -*-
"""Stealth模式实战测试 - 测试Booking.com"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ota_scraper.backends import ScraplingBackend, CacheManager

be = ScraplingBackend()

# 测试1: httpbin (确认Stealth正常)
print("=== 1. httpbin ===")
try:
    resp = be.fetch("https://httpbin.org/get", stealth=True, wait_ms=2000, timeout=20)
    print(f"OK: {len(resp.content)} chars")
    print(resp.content[:200])
except Exception as e:
    print(f"FAIL: {e}")

print()

# 测试2: Booking.com
print("=== 2. Booking.com ===")
try:
    resp = be.fetch(
        "https://www.booking.com/searchresults.html?ss=Beijing",
        stealth=True, wait_ms=8000, timeout=40
    )
    print(f"OK: {len(resp.content)} chars")
    if resp.content:
        print("FIRST 500:")
        print(resp.content[:500])
    else:
        print("(empty - trying HTML extraction)")
except Exception as e:
    print(f"FAIL: {e}")

print()

# 测试3: Ctrip
print("=== 3. 携程 ===")
try:
    resp = be.fetch(
        "https://hotels.ctrip.com/hotel/beijing1.html",
        stealth=True, wait_ms=8000, timeout=40
    )
    print(f"OK: {len(resp.content)} chars")
    if resp.content:
        print("FIRST 500:")
        print(resp.content[:500])
    else:
        print("(empty)")
except Exception as e:
    print(f"FAIL: {e}")
