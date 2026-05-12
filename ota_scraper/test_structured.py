# -*- coding: utf-8 -*-
"""OTA-Scraper v1.1 结构化提取测试"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ota_scraper import OTAScraper

s = OTAScraper()

print("="*70)
print("OTA-Scraper v1.1 — CSS选择器驱动结构化提取测试")
print("="*70)

# 测试1: Booking.com with CSS selectors from platform config
print("\n>>> Booking.com — CSS选择器结构化提取")
t0 = time.time()
r = s.scrape(
    url="https://www.booking.com/searchresults.html?ss=Beijing&checkin=2026-06-01&checkout=2026-06-02&group_adults=1&no_rooms=1",
    task_type="search", max_pages=1,
)
elapsed = time.time() - t0
print(f"状态: {r.status.value} | 耗时: {elapsed:.1f}s | 酒店: {r.total_count}")
for a in r.attempts:
    print(f"  {a.backend.value}: {a.status.value} ({a.content_length} chars, {a.duration_ms/1000:.1f}s)")
if r.hotels:
    print(f"\n解析到的酒店 ({len(r.hotels)}家):")
    for i, h in enumerate(r.hotels[:8]):
        price = f"¥{h.prices[0].lowest_price:.0f}" if h.prices else "N/A"
        score = f"★{h.review.score:.1f}" if h.review and h.review.score else ""
        reviews = f"({h.review.review_count}评)" if h.review and h.review.review_count else ""
        addr = h.address[:35] if h.address else ""
        print(f"  {i+1}. {h.hotel_name[:45]:<47} {price:<10} {score}{reviews}")
        if addr: print(f"     {addr}")
else:
    print("  (未解析到酒店)")
    # Show raw content sample
    if r.attempts:
        raw_len = r.attempts[0].content_length
        print(f"  原始内容: {raw_len} chars (可能选择器未命中)")

# 输出保存
if r.hotels:
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "booking_struct.json")
    s.pipeline.export_json(r.hotels, out)
    print(f"\n💾 已保存: {out}")

print(f"\n{'='*70}")
print("核心改进: CSS选择器直接从HTML提取结构化字段")
print("旧方法: 全文提取→正则猜测 (33-52%质量)")
print("新方法: hotel_list选择器→卡片分割→字段选择器 (目标80%+质量)")
