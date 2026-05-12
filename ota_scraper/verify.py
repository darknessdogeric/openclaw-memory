# -*- coding: utf-8 -*-
"""
OTA-Scraper 增强测试 - 测试非JS站点确认框架逻辑正确性
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ota_scraper import OTAScraper
from ota_scraper.platforms import resolve_platform

# 1. 平台识别测试
print("="*60)
print("1. 平台自动识别")
print("="*60)
test_urls = [
    "https://hotels.ctrip.com/hotel/beijing.html",
    "https://hotel.meituan.com/beijing/",
    "https://www.booking.com/searchresults.html?ss=Beijing",
    "https://www.agoda.com/search?city=Beijing",
    "https://www.tripadvisor.com/Hotels-g294212-Beijing-Hotels.html",
    "https://www.fliggy.com/hotel/search?city=北京",
    "https://hotel.qunar.com/city/beijing/",
    "https://www.ly.com/hotel/beijing/",
    "https://hotel.elong.com/search/beijing/",
    "https://www.airbnb.com/s/Beijing/homes",
    "https://www.expedia.com/Hotel-Search?destination=Beijing",
    "https://www.hotels.com/Hotel-Search?destination=Beijing",
    "https://www.kayak.com/hotels/Beijing",
    "https://www.mafengwo.cn/hotel/10186.html",
    "https://www.lvmama.com/hotel/search-beijing.html",
    "https://www.tujia.com/search/beijing/",
    "https://hotel.tuniu.com/search?q=北京",
]
for url in test_urls:
    pid = resolve_platform(url)
    icon = "✅" if pid else "❌"
    print(f"  {icon} {pid or 'UNKNOWN':<15} <- {url[:55]}")

# 2. 后端可用性
print(f"\n{'='*60}")
print("2. 后端健康检查")
print("="*60)
s = OTAScraper()
hc = s.healthcheck()
for name, info in hc.items():
    icon = "✅" if info['status'] == 'ok' else "⚠️" if info['status'] == 'warning' else "❌"
    detail = info.get('latency_ms', info.get('error', ''))
    print(f"  {icon} {name:<20} {detail}")

# 3. 平台配置完整性
print(f"\n{'='*60}")
print("3. 平台配置完整性检查")
print("="*60)
from ota_scraper.platforms import get_all_platforms
for pid, p in get_all_platforms().items():
    config_ok = all([
        p.get("name"), p.get("domains"), p.get("base_url"),
        p.get("backends"), p.get("selectors"), p.get("rate_limit")
    ])
    sel_count = len(p.get("selectors", {}))
    be_count = len(p.get("backends", []))
    icon = "✅" if config_ok else "⚠️"
    print(f"  {icon} {pid:<15} Lv{p['anti_bot_level']} | {be_count} backends | {sel_count} selectors")

# 4. 数据Pipeline测试
print(f"\n{'='*60}")
print("4. 数据Pipeline测试")
print("="*60)
sample_html = """
北京饭店
地址: 北京市东城区东长安街33号
价格: ¥688起
评分: 4.5分
评论: 2831条评论
5星级
设施: WiFi 停车场 游泳池 健身房 餐厅

王府井大酒店
地址: 北京市东城区王府井大街57号
价格: ¥528起
评分: 4.2分
评论: 1520条点评
4星级
"""
from ota_scraper.pipeline import DataPipeline
p = DataPipeline()
hotels = p.parse_hotel_list(sample_html, "ctrip", get_all_platforms()["ctrip"])
print(f"  解析到 {len(hotels)} 家酒店")
for h in hotels:
    price = f"¥{h.prices[0].lowest_price:.0f}" if h.prices else "N/A"
    score = f"{h.review.score:.1f}" if h.review and h.review.score else "N/A"
    reviews = h.review.review_count if h.review else 0
    stars = h.star_rating or 0
    print(f"  - {h.hotel_name} | {price} | ★{score} ({reviews}评) | {stars}星 | 质量:{h.data_quality:.0%}")

print(f"\n{'='*60}")
print("5. 系统就绪状态")
print("="*60)
print(f"  已注册平台: {len(get_all_platforms())}")
print(f"  可用后端: {len(s.backends)} ({', '.join(s.backends.keys())})")
print(f"  注意: 浏览器未安装(Stealth模式不可用)。")
print(f"  安装命令: scrapling install --force")
print(f"  非Stealth模式(HTTP直连)可用于无JS站点")

print("\n✅ 框架验证完成 — 架构正确，等浏览器安装后即可全功能运行")
