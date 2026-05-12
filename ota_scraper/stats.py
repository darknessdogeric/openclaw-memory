# -*- coding: utf-8 -*-
"""OTA-Scraper 统计引擎 — 从已有JSON数据生成对比报告"""
import sys, os, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def load_results(*filenames):
    """加载已有JSON输出"""
    hotels = []
    for fn in filenames:
        fp = ROOT / "output" / fn
        if fp.exists():
            with open(fp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for h in data:
                h['_source_file'] = fn
            hotels.extend(data)
    return hotels

def generate_stats(hotels):
    """生成统计报告"""
    if not hotels:
        return "无数据"
    
    platforms = {}
    for h in hotels:
        pid = h.get('platform', 'unknown')
        if pid not in platforms:
            platforms[pid] = {'hotels': [], 'prices': [], 'scores': [], 'stars': []}
        platforms[pid]['hotels'].append(h)
        if h.get('prices'):
            for p in h['prices']:
                if p.get('lowest_price'):
                    platforms[pid]['prices'].append(p['lowest_price'])
        if h.get('review_score'):
            platforms[pid]['scores'].append(h['review_score'])
        if h.get('star_rating'):
            platforms[pid]['stars'].append(h['star_rating'])
    
    lines = []
    lines.append("# OTA酒店数据统计报告\n")
    lines.append(f"**生成时间**: {__import__('time').strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**数据来源**: OTA-Scraper v1.3\n")
    
    # 总览表
    lines.append("## 总览\n")
    lines.append("| 平台 | 酒店数 | 最低价 | 最高价 | 均价 | 平均评分 | 星级分布 |")
    lines.append("|------|--------|--------|--------|------|----------|----------|")
    
    for pid, data in sorted(platforms.items()):
        count = len(data['hotels'])
        prices = data['prices']
        scores = data['scores']
        stars = data['stars']
        
        p_min = f"¥{min(prices):.0f}" if prices else "N/A"
        p_max = f"¥{max(prices):.0f}" if prices else "N/A"
        p_avg = f"¥{sum(prices)/len(prices):.0f}" if prices else "N/A"
        s_avg = f"★{sum(scores)/len(scores):.1f}" if scores else "N/A"
        
        # 星级分布
        star_dist = ""
        if stars:
            from collections import Counter
            sc = Counter(stars)
            star_dist = ", ".join([f"{k}星:{v}" for k,v in sorted(sc.items())])
        
        lines.append(f"| {pid} | {count} | {p_min} | {p_max} | {p_avg} | {s_avg} | {star_dist} |")
    
    lines.append("")
    
    # 价格对比
    all_prices = {pid: data['prices'] for pid, data in platforms.items() if data['prices']}
    if len(all_prices) >= 2:
        lines.append("## 价格区间对比\n")
        lines.append("```")
        max_name_len = max(len(n) for n in all_prices)
        max_price = max(max(v) for v in all_prices.values())
        bar_width = 40
        for name, prices in all_prices.items():
            avg = sum(prices) / len(prices)
            bar = int(avg / max_price * bar_width)
            lines.append(f"{name:<{max_name_len}} ¥{avg:>6.0f} {'█'*bar}{'░'*(bar_width-bar)}")
        lines.append("```\n")
    
    # Top 10 最贵酒店
    all_hotels = [(h['hotel_name'], h['platform'], 
                   h['prices'][0]['lowest_price'] if h.get('prices') else 0,
                   h.get('review_score', 0))
                  for h in hotels if h.get('prices')]
    all_hotels.sort(key=lambda x: -x[2])
    
    lines.append("## Top 10 价格最高\n")
    lines.append("| # | 酒店 | 平台 | 价格 | 评分 |")
    lines.append("|---|------|------|------|------|")
    for i, (name, plat, price, score) in enumerate(all_hotels[:10]):
        lines.append(f"| {i+1} | {name[:30]} | {plat} | ¥{price:.0f} | ★{score:.1f} |")
    
    lines.append("")
    
    # Bottom 10 最便宜酒店
    cheap = [(h['hotel_name'], h['platform'],
              h['prices'][0]['lowest_price'] if h.get('prices') else 0,
              h.get('review_score', 0))
             for h in hotels if h.get('prices')]
    cheap.sort(key=lambda x: x[2])
    
    lines.append("## Top 10 最经济\n")
    lines.append("| # | 酒店 | 平台 | 价格 | 评分 |")
    lines.append("|---|------|------|------|------|")
    for i, (name, plat, price, score) in enumerate(cheap[:10]):
        lines.append(f"| {i+1} | {name[:30]} | {plat} | ¥{price:.0f} | ★{score:.1f} |")
    
    return "\n".join(lines)

if __name__ == "__main__":
    args = sys.argv[1:]
    files = args if args else ["booking_final.json", "ctrip_final.json"]
    
    hotels = []
    for fn in files:
        fp = ROOT / "output" / fn
        if fp.exists():
            with open(fp, 'r', encoding='utf-8') as f:
                hotels.extend(json.load(f))
    
    report = generate_stats(hotels)
    
    out = ROOT / "output" / "stats_report.md"
    with open(out, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\n📊 报告已保存: {out}")
