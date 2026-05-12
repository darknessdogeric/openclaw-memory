# -*- coding: utf-8 -*-
"""v1.2深化测试: Booking评分 + 携程评分/评论"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ota_scraper import OTAScraper

s = OTAScraper()

# 1. Booking - 评分/评论修正
print("="*70)
print("1. Booking.com — 评分/评论修正")
print("="*70)
t0 = time.time()
r = s.scrape(
    url="https://www.booking.com/searchresults.html?ss=Beijing&checkin=2026-06-01&checkout=2026-06-02&group_adults=1&no_rooms=1",
    task_type="search", max_pages=1,
)
print(f"耗时: {time.time()-t0:.1f}s | 酒店: {r.total_count}")
if r.hotels:
    for i, h in enumerate(r.hotels[:8]):
        price = f"¥{h.prices[0].lowest_price:.0f}" if h.prices else "N/A"
        score = f"★{h.review.score:.1f}" if h.review and h.review.score else ""
        reviews = f"({h.review.review_count}评)" if h.review and h.review.review_count else ""
        print(f"  {i+1}. {h.hotel_name[:45]:<47} {price:<10} {score} {reviews}")

# 2. 携程 - 增强文本解析
print(f"\n{'='*70}")
print("2. 携程 — 评分/评论文本提取")
print("="*70)
t0 = time.time()
r2 = s.scrape(
    url="https://hotels.ctrip.com/hotel/beijing1.html",
    task_type="search", max_pages=1,
)
print(f"耗时: {time.time()-t0:.1f}s | 酒店: {r2.total_count}")
if r2.hotels:
    for i, h in enumerate(r2.hotels[:8]):
        score = f"★{h.review.score:.1f}" if h.review and h.review.score else ""
        reviews = f"({h.review.review_count}评)" if h.review and h.review.review_count else ""
        print(f"  {i+1}. {h.hotel_name[:45]:<47} {score} {reviews} {h.address[:30]}")
    # 显示数据质量
    print(f"\n  质量: {r2.data_quality:.0%}")

# 3. 跨平台对比 (快速)
print(f"\n{'='*70}")
print("3. 跨平台对比: 北京")
print("="*70)
all_r = [r, r2]
for rr in all_r:
    pname = rr.platform
    pricing = ""
    if rr.hotels:
        prices = [h.prices[0].lowest_price for h in rr.hotels if h.prices and h.prices[0].lowest_price]
        if prices:
            pricing = f"¥{min(prices):.0f}~¥{max(prices):.0f}"
    print(f"  {pname:<15} {rr.total_count:>3}家 {pricing:<20} 质量:{rr.data_quality:.0%}")
