#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OTA-Scraper CLI - 命令行接口

用法:
  # 列出所有平台
  python ota_scraper/cli.py list

  # 搜索城市酒店
  python ota_scraper/cli.py search --platform ctrip --city 北京 --pages 2

  # 跨平台价格对比
  python ota_scraper/cli.py compare --city 上海 --platforms ctrip,meituan,qunar

  # 抓取单个URL
  python ota_scraper/cli.py fetch --url "https://hotels.ctrip.com/hotel/beijing.html"

  # 系统状态
  python ota_scraper/cli.py status
  python ota_scraper/cli.py health
"""
import sys
import os
import json
import argparse
import time

# 确保项目根在path中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ota_scraper import OTAScraper, scrape_ota
from ota_scraper.platforms import list_platforms, get_platform, get_all_platforms
from ota_scraper.pipeline import DataPipeline


def cmd_list(args):
    """列出所有支持的平台"""
    platforms = list_platforms()
    print(f"\n{'='*80}")
    print(f"OTA-Scraper v1.0 - 已注册 {len(platforms)} 个平台")
    print(f"{'='*80}")
    print(f"{'ID':<20} {'名称':<12} {'域名':<30} {'反爬级别':<10}")
    print("-" * 80)

    level_names = {1: "🟢 低", 2: "🟡 中", 3: "🟠 高", 4: "🔴 极高"}
    for p in platforms:
        level_str = level_names.get(p['anti_bot_level'], str(p['anti_bot_level']))
        domains = ", ".join(p['domains'][:2])
        print(f"{p['id']:<20} {p['name']:<12} {domains:<30} {level_str:<10}")
    print()


def cmd_status(args):
    """系统状态"""
    scraper = OTAScraper()
    report = scraper.report()

    print(f"\n{'='*60}")
    print(f"OTA-Scraper v{report['version']} - 系统状态")
    print(f"{'='*60}")
    print(f"可用后端: {', '.join(report['backends'].keys())}")
    print(f"已注册平台: {report['platforms']}")
    print()
    print("平台详情:")
    for p in report['platform_list']:
        print(f"  {p['id']:<15} {p['name']:<10} Lv{p['level']} - {p['desc']}")


def cmd_health(args):
    """健康检查"""
    scraper = OTAScraper()
    print("正在检查后端...")
    results = scraper.healthcheck()
    print(f"\n{'后端':<20} {'状态':<10} {'延迟'}")
    print("-" * 50)
    for name, info in results.items():
        status_icon = "✅" if info['status'] == 'ok' else "❌"
        latency = f"{info.get('latency_ms', '-')}ms" if info['status'] == 'ok' else info.get('error', '-')
        print(f"{name:<20} {status_icon:<10} {latency}")
    print()


def cmd_search(args):
    """搜索城市酒店"""
    scraper = OTAScraper()
    print(f"\n🔍 搜索: {args.platform} → {args.city} (翻页: {args.pages})")
    print("-" * 60)

    t0 = time.time()
    result = scraper.scrape(
        platform_id=args.platform,
        city=args.city,
        max_pages=args.pages,
        task_type="search"
    )

    _print_result(result, t0)

    # 输出到文件
    if args.output:
        scraper.pipeline.export_json(result.hotels, args.output)
        print(f"\n💾 已保存到: {args.output}")

def cmd_fetch(args):
    """抓取单个URL"""
    scraper = OTAScraper()
    print(f"\n📡 抓取: {args.url}")
    print("-" * 60)

    t0 = time.time()
    result = scraper.scrape(url=args.url, task_type=args.type)
    _print_result(result, t0)

    if args.output and result.hotels:
        scraper.pipeline.export_json(result.hotels, args.output)
        print(f"\n💾 已保存到: {args.output}")

def cmd_compare(args):
    """跨平台价格对比"""
    scraper = OTAScraper()
    platforms = [p.strip() for p in args.platforms.split(",")]
    print(f"\n📊 跨平台对比: {args.city} ({', '.join(platforms)})")
    print("=" * 80)

    all_hotels = []
    for pid in platforms:
        print(f"\n--- {get_platform(pid)['name']} ---")
        t0 = time.time()
        result = scraper.scrape(platform_id=pid, city=args.city,
                               task_type="search", max_pages=1)
        _print_result(result, t0)
        all_hotels.extend(result.hotels)
        if pid != platforms[-1]:
            time.sleep(2)

    print(f"\n{'='*80}")
    print(f"总计: {len(all_hotels)} 家酒店 ({len(platforms)} 个平台)")
    if args.output:
        scraper.pipeline.export_json(all_hotels, args.output)
        csv_path = args.output.replace('.json', '.csv')
        scraper.pipeline.export_csv(all_hotels, csv_path)
        print(f"💾 JSON: {args.output}")
        print(f"💾 CSV:  {csv_path}")

def _print_result(result, t0):
    """格式化输出结果"""
    elapsed = time.time() - t0
    status_icon = "✅" if result.status.value == "success" else "⚠️" if result.status.value == "partial" else "❌"
    print(f"状态: {status_icon} {result.status.value} | 酒店: {result.total_count} | "
          f"尝试: {len(result.attempts)} | 耗时: {elapsed:.1f}s")

    if result.errors:
        for e in result.errors[:3]:
            print(f"  错误: {e}")

    # 列出酒店
    if result.hotels:
        print(f"\n酒店列表:")
        for i, h in enumerate(result.hotels[:10]):
            price_str = f"¥{h.prices[0].lowest_price:.0f}" if h.prices else "N/A"
            score_str = f"{h.review.score:.1f}" if h.review and h.review.score else "N/A"
            print(f"  {i+1}. {h.hotel_name[:40]:<42} {price_str:<10} ★{score_str}")
        if len(result.hotels) > 10:
            print(f"  ... 还有 {len(result.hotels) - 10} 家")

    # 后端尝试详情
    if args and hasattr(args, 'verbose') and args.verbose:
        print(f"\n后端尝试:")
        for a in result.attempts:
            print(f"  {a.backend.value:<15} {a.status.value:<10} {a.duration_ms:.0f}ms "
                  f"{a.error[:60] if a.error else ''}")


# CLI入口
def main():
    parser = argparse.ArgumentParser(
        description="OTA-Scraper v1.0 - 攻破所有OTA和OTP网站的数据抓取系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # list
    subparsers.add_parser("list", help="列出所有支持的平台")

    # status
    subparsers.add_parser("status", help="系统状态")

    # health
    subparsers.add_parser("health", help="健康检查")

    # search
    p_search = subparsers.add_parser("search", help="搜索城市酒店")
    p_search.add_argument("--platform", "-p", required=True, help="平台ID (ctrip, meituan, ...)")
    p_search.add_argument("--city", "-c", required=True, help="城市名")
    p_search.add_argument("--pages", "-n", type=int, default=1, help="翻页数")
    p_search.add_argument("--output", "-o", help="输出JSON文件")
    p_search.add_argument("--verbose", "-v", action="store_true")

    # fetch
    p_fetch = subparsers.add_parser("fetch", help="抓取单个URL")
    p_fetch.add_argument("--url", "-u", required=True, help="目标URL")
    p_fetch.add_argument("--type", "-t", default="search",
                        choices=["search", "detail", "review"])
    p_fetch.add_argument("--output", "-o", help="输出JSON文件")
    p_fetch.add_argument("--verbose", "-v", action="store_true")

    # compare
    p_compare = subparsers.add_parser("compare", help="跨平台价格对比")
    p_compare.add_argument("--city", "-c", required=True, help="城市名")
    p_compare.add_argument("--platforms", "-p", default="ctrip,meituan,qunar,fliggy,tongcheng",
                          help="平台列表(逗号分隔)")
    p_compare.add_argument("--output", "-o", help="输出JSON文件")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        "list": cmd_list,
        "status": cmd_status,
        "health": cmd_health,
        "search": cmd_search,
        "fetch": cmd_fetch,
        "compare": cmd_compare,
    }

    cmd = commands.get(args.command)
    if cmd:
        cmd(args)


if __name__ == "__main__":
    main()
