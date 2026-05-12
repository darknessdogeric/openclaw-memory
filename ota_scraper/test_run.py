# -*- coding: utf-8 -*-
"""OTA-Scraper 测试脚本"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ota_scraper import OTAScraper

def test_status():
    s = OTAScraper()
    print("=== 健康检查 ===")
    hc = s.healthcheck()
    for name, info in hc.items():
        status_icon = "OK" if info['status'] == 'ok' else "FAIL"
        detail = info.get('latency_ms', info.get('error', ''))
        print(f"  {name}: {status_icon} ({detail})")
    print()

def test_mafengwo():
    s = OTAScraper()
    print("=== 马蜂窝抓取测试 ===")
    t0 = time.time()
    r = s.scrape(url="https://www.mafengwo.cn/hotel/10186.html", task_type="search", max_pages=1)
    elapsed = time.time() - t0
    print(f"状态: {r.status.value} | 耗时: {elapsed:.1f}s")
    print(f"酒店数: {r.total_count}")
    print(f"后端尝试: {len(r.attempts)} 次")
    for a in r.attempts:
        print(f"  {a.backend.value}: {a.status.value} ({a.content_length} chars, {a.duration_ms:.0f}ms)")
    if r.hotels:
        print(f"\n抓取到的酒店 (前10):")
        for i, h in enumerate(r.hotels[:10]):
            price = f"¥{h.prices[0].lowest_price:.0f}" if h.prices else "N/A"
            score = f"{h.review.score:.1f}" if h.review and h.review.score else "N/A"
            print(f"  {i+1}. {h.hotel_name[:40]:<42} {price:<10} ★{score}")
    else:
        print("  (未解析到酒店)")
        if r.errors:
            for e in r.errors:
                print(f"  错误: {e}")
    print()

def test_platform_resolve():
    """测试平台自动识别"""
    from ota_scraper.platforms import resolve_platform
    tests = [
        "https://hotels.ctrip.com/hotel/beijing.html",
        "https://hotel.meituan.com/beijing/",
        "https://www.booking.com/searchresults.html?ss=Beijing",
        "https://www.agoda.com/search?city=Beijing",
        "https://www.tripadvisor.com/Hotels-g294212-Beijing-Hotels.html",
        "https://www.mafengwo.cn/hotel/10186.html",
        "https://www.fliggy.com/hotel/search?city=北京",
    ]
    print("=== 平台自动识别测试 ===")
    for url in tests:
        pid = resolve_platform(url)
        print(f"  {pid or 'UNKNOWN':<15} <- {url[:60]}")
    print()

if __name__ == "__main__":
    test_status()
    test_platform_resolve()
    test_mafengwo()
