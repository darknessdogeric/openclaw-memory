# -*- coding: utf-8 -*-
"""诊断: hotel.meituan.com 403 是否 Geo-IP / Cookie 链问题"""
from cloakbrowser import launch
import time, json

browser = launch(headless=True)
page = browser.new_page()

# 策略1: 先访问 meituan.com 拿 Cookie，再访问 hotel 子域
print("=== 策略1: Cookie 链 ===")
page.goto("https://www.meituan.com/", wait_until="domcontentloaded", timeout=15000)
page.wait_for_timeout(2000)
cookies = browser.contexts[0].cookies()
print(f"  www.meituan.com cookies: {len(cookies)}")
for c in cookies:
    print(f"    {c['name']}={c['value'][:30]}...")

# 再试 hotel
page.goto("https://hotel.meituan.com/xiangyang/", wait_until="domcontentloaded", timeout=15000)
page.wait_for_timeout(2000)
title = page.title()
if "403" in title:
    print("  ❌ Cookie 链无效 —— 确认非 Cookie 问题")

# 策略2: 加中国 Accept-Language
print("\n=== 策略2: 中文 Headers ===")
context2 = browser.new_context(
    locale="zh-CN",
    timezone_id="Asia/Shanghai",
)
page2 = context2.new_page()
page2.set_extra_http_headers({
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
})
page2.goto("https://hotel.meituan.com/xiangyang/", wait_until="domcontentloaded", timeout=15000)
page2.wait_for_timeout(2000)
title2 = page2.title()
length2 = len(page2.content())
print(f"  [{page2.url[:80]}] {title2[:60]} | {length2} chars")
if "403" not in title2:
    print("  ✅ Headers 有效!")

# 策略3: 试 i.meituan.com 移动端（已知可通）
print("\n=== 策略3: 移动端（对照） ===")
context3 = browser.new_context(
    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
    viewport={"width": 390, "height": 844},
    locale="zh-CN",
)
page3 = context3.new_page()
page3.goto("https://i.meituan.com/hotel/xiangyang/", wait_until="networkidle", timeout=15000)
page3.wait_for_timeout(2000)
print(f"  [{page3.url[:80]}] {page3.title()[:60]} | {len(page3.content())} chars")

# 策略4: 检查 403 响应头
print("\n=== 策略4: 403 响应头分析 ===")
resp = page2.goto("https://hotel.meituan.com/xiangyang/", wait_until="domcontentloaded", timeout=15000)
print(f"  Status: {resp.status}")
print(f"  Headers:")
for k, v in resp.headers.items():
    print(f"    {k}: {v}")

browser.close()
print("\n✅ 诊断完成")
