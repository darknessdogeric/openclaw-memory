# -*- coding: utf-8 -*-
"""CloakBrowser 测试 - 美团 PC 站 + 移动端登录"""
import json, time, sys

print("=" * 60)
print("CloakBrowser v0.3.28 — 美团全线突破测试")
print("=" * 60)

from cloakbrowser import launch

# ============================================
# 测试1: PC 站 hotel.meituan.com
# ============================================
print("\n=== 测试1: PC站 hotel.meituan.com ===")
try:
    browser = launch(headless=True)
    page = browser.new_page()
    
    urls = [
        "https://hotel.meituan.com/xiangyang/",
        "https://hotel.meituan.com/",
        "https://www.meituan.com/",
    ]
    
    for url in urls:
        try:
            t0 = time.time()
            resp = page.goto(url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(2000)
            elapsed = time.time() - t0
            
            status = resp.status if resp else "?"
            title = page.title()
            html = page.content()
            length = len(html)
            
            # 检测是否被拦
            blocked = "403" in title or "Forbidden" in html[:300]
            icon = "❌ BLOCKED" if blocked else "✅ PASS"
            
            print(f"  {icon} [{status}] {url:55s} | {length:>8,} chars | {elapsed:.1f}s | {title[:60]}")
            
            if not blocked:
                # 检查酒店数据
                for kw in ['hotel','poi','price','room','¥','元','起']:
                    cnt = html.count(kw)
                    if cnt > 5:
                        print(f"    '{kw}': {cnt} occurrences")
                        
        except Exception as e:
            print(f"  ❌ {url:55s} | {type(e).__name__}: {str(e)[:80]}")
    
    browser.close()
    
except Exception as e:
    print(f"  ❌ CloakBrowser 启动失败: {e}")
    import traceback
    traceback.print_exc()


# ============================================
# 测试2: 移动端登录 (如果PC站也能通就不用)
# ============================================
print("\n=== 测试2: 移动端搜索页 ===")
try:
    browser = launch(headless=True)
    page = browser.new_page()
    
    # 移动端 UA
    page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"
    })
    page.set_viewport_size({"width": 390, "height": 844})
    
    resp = page.goto("https://i.meituan.com/hotel/xiangyang/", 
                     wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    title = page.title()
    length = len(page.content())
    print(f"  [{resp.status}] {title[:60]} | {length:,} chars")
    
    # 尝试点搜索（看是否跳登录）
    try:
        page.evaluate('document.querySelector("button")?.click()')
        page.wait_for_timeout(3000)
        after_url = page.url
        if 'passport' in after_url:
            print(f"  ⚠️ 搜索触发登录 (预期内)")
        else:
            print(f"  ✅ 搜索未触发登录! URL: {after_url[:100]}")
    except Exception as e:
        print(f"  搜索测试: {e}")
    
    browser.close()
    
except Exception as e:
    print(f"  ❌ {e}")

print(f"\n{'='*60}")
print("测试完成")
print("=" * 60)
