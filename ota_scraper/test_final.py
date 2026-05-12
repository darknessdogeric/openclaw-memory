# -*- coding: utf-8 -*-
"""OTA-Scraper v1.3 最终验证: 星级 + 全字段"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ota_scraper import OTAScraper

s = OTAScraper()

# ═══════════════ Booking.com ═══════════════
print("="*70)
print("Booking.com — 25家酒店")
print("="*70)
t0 = time.time()
r_bk = s.scrape(
    url="https://www.booking.com/searchresults.html?ss=Beijing&checkin=2026-06-01&checkout=2026-06-02&group_adults=1&no_rooms=1",
    task_type="search", max_pages=1,
)
print(f"耗时: {time.time()-t0:.1f}s | 酒店: {r_bk.total_count} | 质量: {r_bk.data_quality:.0%}")
for i, h in enumerate(r_bk.hotels[:6]):
    price = f"¥{h.prices[0].lowest_price:.0f}" if h.prices else "N/A"
    score = f"★{h.review.score:.1f}" if h.review and h.review.score else ""
    reviews = f"({h.review.review_count}评)" if h.review and h.review.review_count else ""
    stars = f"{'⭐'*h.star_rating}" if h.star_rating else ""
    print(f"  {i+1}. {h.hotel_name[:42]:<44} {price:<10} {score} {reviews} {stars}")

# ═══════════════ 携程 ═══════════════
print(f"\n{'='*70}")
print("携程 — 15家酒店 + 星级")
print("="*70)
t0 = time.time()
r_ct = s.scrape(
    url="https://hotels.ctrip.com/hotel/beijing1.html",
    task_type="search", max_pages=1,
)
print(f"耗时: {time.time()-t0:.1f}s | 酒店: {r_ct.total_count} | 质量: {r_ct.data_quality:.0%}")
for i, h in enumerate(r_ct.hotels[:8]):
    score = f"★{h.review.score:.1f}" if h.review and h.review.score else ""
    reviews = f"({h.review.review_count}评)" if h.review and h.review.review_count else ""
    stars = f"{'⭐'*h.star_rating}" if h.star_rating else ""
    sid = f"[{h.hotel_id}]" if h.hotel_id else ""
    print(f"  {i+1}. {h.hotel_name[:38]:<40} {stars:<8} {score} {reviews} {sid}")

# ═══════════════ 跨平台对比 ═══════════════
print(f"\n{'='*70}")
print("跨平台对比: 北京酒店")
print("="*70)
print(f"{'平台':<15} {'酒店数':>6} {'价格范围':<22} {'评分':>8} {'质量':>6}")
print("-"*70)
for r in [r_bk, r_ct]:
    pname = r.platform
    pricing = "N/A"
    if r.hotels:
        prices = [h.prices[0].lowest_price for h in r.hotels if h.prices and h.prices[0].lowest_price]
        if prices:
            pricing = f"¥{min(prices):.0f}~¥{max(prices):.0f}"
    scores = [h.review.score for h in r.hotels if h.review and h.review.score]
    avg_score = f"★{sum(scores)/len(scores):.1f}" if scores else "N/A"
    print(f"{pname:<15} {r.total_count:>6} {pricing:<22} {avg_score:>8} {r.data_quality:.0%}")

# 导出
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
s.pipeline.export_json(r_bk.hotels, os.path.join(out_dir, "booking_final.json"))
s.pipeline.export_json(r_ct.hotels, os.path.join(out_dir, "ctrip_final.json"))
s.pipeline.export_csv(r_bk.hotels + r_ct.hotels, os.path.join(out_dir, "comparison.csv"))
print(f"\n💾 导出: booking_final.json, ctrip_final.json, comparison.csv")
