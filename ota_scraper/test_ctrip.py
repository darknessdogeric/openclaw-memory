# -*- coding: utf-8 -*-
"""OTA-Scraper v1.1 — 携程结构化提取测试"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ota_scraper import OTAScraper

s = OTAScraper()

print("="*70)
print("携程 Ctrip — CSS选择器结构化提取")
print("="*70)

t0 = time.time()
r = s.scrape(
    url="https://hotels.ctrip.com/hotel/beijing1.html",
    task_type="search", max_pages=1,
)
elapsed = time.time() - t0

print(f"状态: {r.status.value} | 耗时: {elapsed:.1f}s | 酒店: {r.total_count}")
for a in r.attempts:
    print(f"  {a.backend.value}: {a.status.value} ({a.content_length} chars, {a.duration_ms/1000:.1f}s)")

if r.hotels:
    print(f"\n解析到的酒店 ({len(r.hotels)}家):")
    for i, h in enumerate(r.hotels[:12]):
        price = f"¥{h.prices[0].lowest_price:.0f}" if h.prices else "N/A"
        name = h.hotel_name[:50] if h.hotel_name else "(未解析)"
        addr = h.address[:30] if h.address else ""
        print(f"  {i+1:2d}. {name:<52} {price:<10} {addr}")
else:
    print("  (未解析到酒店)")
    print(f"  错误: {r.errors[:3]}")

if r.hotels:
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "ctrip_struct.json")
    s.pipeline.export_json(r.hotels, out)
    print(f"\n💾 已保存: {out}")
