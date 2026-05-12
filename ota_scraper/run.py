#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OTA-Scraper 快速调用入口
用法: python ota_scraper/run.py ctrip beijing
      python ota_scraper/run.py booking "New York"
      python ota_scraper/run.py compare beijing
      python ota_scraper/run.py list
"""
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ota_scraper import OTAScraper
from ota_scraper.platforms import list_platforms, get_platform

def main():
    if len(sys.argv) < 2:
        print("OTA-Scraper v1.0 - 快速调用")
        print()
        print("用法:")
        print("  python ota_scraper/run.py list                        # 列出所有平台")
        print("  python ota_scraper/run.py <platform> <city> [pages]   # 搜索酒店")
        print("  python ota_scraper/run.py compare <city>              # 跨平台对比")
        print("  python ota_scraper/run.py status                      # 系统状态")
        print()
        print("平台: ctrip, meituan, qunar, fliggy, elong, tongcheng,")
        print("      mafengwo, lvmama, tujia, tuniu,")
        print("      booking, agoda, expedia, tripadvisor, airbnb, hotels, kayak")
        return

    cmd = sys.argv[1].lower()
    scraper = OTAScraper()

    if cmd == "list":
        platforms = list_platforms()
        print(f"\n{'='*70}")
        print(f"OTA-Scraper v1.0 — {len(platforms)} 个平台")
        print(f"{'='*70}")
        for p in platforms:
            print(f"  {p['id']:<15} {p['name']:<12} {', '.join(p['domains'][:2])}")
        print()

    elif cmd == "status":
        report = scraper.report()
        print(f"\nOTA-Scraper v{report['version']}")
        print(f"后端: {', '.join(report['backends'].keys())}")
        print(f"平台: {report['platforms']}")
        hc = scraper.healthcheck()
        for name, info in hc.items():
            icon = "✅" if info['status'] == 'ok' else "❌"
            print(f"  {icon} {name}")

    elif cmd == "compare":
        city = sys.argv[2] if len(sys.argv) > 2 else "北京"
        results = scraper.compare_prices(city)
        print(f"\n📊 跨平台对比: {city}")
        print("="*70)
        for r in results:
            icon = "✅" if r.success else "❌"
            pname = get_platform(r.platform)['name']
            price_range = ""
            if r.hotels:
                prices = [h.prices[0].lowest_price for h in r.hotels if h.prices]
                if prices:
                    price_range = f"¥{min(prices):.0f}~¥{max(prices):.0f}"
            print(f"  {icon} {pname:<10} {r.total_count}家酒店 {price_range} {r.duration_seconds:.1f}s")

    else:
        platform_id = cmd
        city = sys.argv[2] if len(sys.argv) > 2 else "北京"
        pages = int(sys.argv[3]) if len(sys.argv) > 3 else 1

        platform = get_platform(platform_id)
        if not platform:
            print(f"未知平台: {platform_id}")
            print(f"可用: {', '.join(p['id'] for p in list_platforms())}")
            return

        print(f"\n🔍 {platform['name']} → {city} (翻页: {pages})")
        print("-"*60)

        t0 = time.time()
        result = scraper.scrape(platform_id=platform_id, city=city,
                               task_type="search", max_pages=pages)
        elapsed = time.time() - t0

        status_icon = "✅" if result.success else "❌"
        print(f"{status_icon} {result.status.value} | {result.total_count}家酒店 | {elapsed:.1f}s")
        print(f"   尝试: {len(result.attempts)}次后端 | 质量: {result.data_quality:.0%}")

        if result.hotels:
            print(f"\n酒店列表 (前10):")
            for i, h in enumerate(result.hotels[:10]):
                price = f"¥{h.prices[0].lowest_price:.0f}" if h.prices else "N/A"
                score = f"★{h.review.score:.1f}" if h.review and h.review.score else ""
                print(f"  {i+1:2d}. {h.hotel_name[:45]:<47} {price:<10} {score}")

        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        scraper.pipeline.export_json(result.hotels,
            os.path.join(out_dir, f"{platform_id}_{city}.json"))
        scraper.pipeline.export_csv(result.hotels,
            os.path.join(out_dir, f"{platform_id}_{city}.csv"))
        print(f"\n💾 已保存到: ota_scraper/output/{platform_id}_{city}.json|csv")

if __name__ == "__main__":
    main()
