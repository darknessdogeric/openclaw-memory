# -*- coding: utf-8 -*-
"""OTA-Scraper 实战测试 - 使用scrapling CLI后端 (已验证可用)"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ota_scraper import OTAScraper

s = OTAScraper()

# 健康检查
print("=== 后端健康检查 ===")
hc = s.healthcheck()
for name, info in hc.items():
    icon = "OK" if info['status'] == 'ok' else "FAIL"
    detail = info.get('latency_ms', info.get('error', ''))
    print(f"  {name}: {icon} ({detail})")
print()

# 测试1: TripAdvisor (反爬中等，英文站)
print("=== 测试 TripAdvisor ===")
t0 = time.time()
r = s.scrape(url="https://www.tripadvisor.com/Hotels-g294212-Beijing-Hotels.html",
             task_type="search", max_pages=1, force_backends=["scrapling_cli"])
elapsed = time.time() - t0
print(f"状态: {r.status.value} | 耗时: {elapsed:.1f}s | 酒店: {r.total_count}")
print(f"内容量: {sum(a.content_length for a in r.attempts)} chars")
if r.hotels:
    for h in r.hotels[:5]:
        print(f"  - {h.hotel_name[:60]}")
        if h.prices: print(f"    价格: ¥{h.prices[0].lowest_price}")
        if h.review: print(f"    评分: {h.review.score} ({h.review.review_count}评论)")
else:
    print("  (未解析到酒店)")
    print(f"  错误: {r.errors[:3]}")
print()

# 测试2: Kayak (反爬中等)  
print("=== 测试 Kayak ===")
t0 = time.time()
r = s.scrape(url="https://www.kayak.com/hotels/Beijing",
             task_type="search", max_pages=1, force_backends=["scrapling_cli"])
elapsed = time.time() - t0
print(f"状态: {r.status.value} | 耗时: {elapsed:.1f}s | 酒店: {r.total_count}")
print(f"内容量: {sum(a.content_length for a in r.attempts)} chars")
if r.hotels:
    for h in r.hotels[:5]:
        print(f"  - {h.hotel_name[:60]}")
else:
    print(f"  错误: {r.errors[:3]}")
