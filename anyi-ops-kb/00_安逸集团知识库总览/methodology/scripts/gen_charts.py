# -*- coding: utf-8 -*-
"""
gen_charts.py - 9 张标准图表生成（骨架）
历史：methodology/sop-region-analysis.md 引用。v1.0 骨架 — matplotlib 实现。
"""
import sys, json
from pathlib import Path

def gen_charts(raw_data_path: str, output_dir: str) -> dict:
    """
    输入: raw_data.json
    输出: 9 张 PNG
        1. 分档次 OCC/ADR/RevPAR
        2. 头部4家 H1 业绩
        3. 全国总量对比
        4. OTA 供给变化
        5. 国际酒店 Q2
        6. 客流结构
        7. 政策叠加
        8. 5 维矩阵
        9. 供给 vs 需求增速
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        matplotlib.rcParams['axes.unicode_minus'] = False
    except ImportError:
        return {'error': 'matplotlib 未安装'}

    data = json.loads(Path(raw_data_path).read_text(encoding='utf-8'))
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    charts = data.get('charts', {})
    generated = []

    # 1. 分档次 OCC/ADR/RevPAR
    if '01_OCC_ADR_RevPAR_by_tier' in charts:
        c = charts['01_OCC_ADR_RevPAR_by_tier']
        tiers = list(c['data'].keys())
        occ = [c['data'][t]['OCC'] for t in tiers]
        adr = [c['data'][t]['ADR'] for t in tiers]
        revpar = [c['data'][t]['RevPAR'] for t in tiers]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        x = range(len(tiers))
        ax1.bar([i-0.2 for i in x], occ, 0.4, label='OCC (%)', color='steelblue')
        ax1.bar([i+0.2 for i in x], adr, 0.4, label='ADR (元)', color='coral')
        ax1.set_xticks(x); ax1.set_xticklabels(tiers)
        ax1.set_title(c['title']); ax1.legend()
        ax2.bar(x, revpar, color='seagreen')
        ax2.set_xticks(x); ax2.set_xticklabels(tiers)
        ax2.set_title('分档次 RevPAR (元)')
        path = out_dir / 'chart_01_OCC_ADR_RevPAR_by_tier.png'
        fig.savefig(path, dpi=120, bbox_inches='tight'); plt.close(fig)
        generated.append(str(path))

    # 2. 头部 4 家 H1 业绩
    if '02_头部4家_H1_业绩' in charts:
        c = charts['02_头部4家_H1_业绩']
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        x = range(len(c['labels']))
        ax1.bar(x, c['revenue'], color='steelblue', label='收入(亿元)')
        ax2.bar(x, c['profit'], color='coral', label='净利(亿元)')
        for ax, vals, title in [(ax1, c['revenue'], 'H1 收入(亿元)'), (ax2, c['profit'], 'H1 净利(亿元)')]:
            ax.set_xticks(x); ax.set_xticklabels(c['labels'])
            ax.set_title(title)
        path = out_dir / 'chart_02_头部4家_H1_业绩.png'
        fig.suptitle(c['title']); fig.savefig(path, dpi=120, bbox_inches='tight'); plt.close(fig)
        generated.append(str(path))

    # 3. 全国总量对比
    if '03_全国总量' in charts:
        c = charts['03_全国总量']
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(c['labels']))
        ax.bar([i-0.2 for i in x], c['y2025'], 0.4, label='2025', color='lightgray')
        ax.bar([i+0.2 for i in x], c['y2026'], 0.4, label='2026', color='steelblue')
        ax.set_xticks(x); ax.set_xticklabels(c['labels'], rotation=15)
        ax.set_title(c['title']); ax.legend()
        path = out_dir / 'chart_03_全国总量对比.png'
        fig.savefig(path, dpi=120, bbox_inches='tight'); plt.close(fig)
        generated.append(str(path))

    # 4. OTA 供给变化
    if '04_OTA供给' in charts:
        c = charts['04_OTA供给']
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(c['labels']))
        ax.bar([i-0.2 for i in x], c['y2025'], 0.4, label='2025', color='lightgray')
        ax.bar([i+0.2 for i in x], c['y2026'], 0.4, label='2026', color='coral')
        ax.set_xticks(x); ax.set_xticklabels(c['labels'], rotation=15)
        ax.set_title(c['title']); ax.legend()
        path = out_dir / 'chart_04_OTA供给变化.png'
        fig.savefig(path, dpi=120, bbox_inches='tight'); plt.close(fig)
        generated.append(str(path))

    # 5. 国际酒店 Q2
    if '05_国际酒店Q2' in charts:
        c = charts['05_国际酒店Q2']
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(c['labels'], c['revenue'], color='teal')
        for bar, val in zip(bars, c['revenue']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{val}', ha='center')
        ax.set_title(c['title']); ax.set_ylabel('亿美元')
        path = out_dir / 'chart_05_国际酒店Q2.png'
        fig.savefig(path, dpi=120, bbox_inches='tight'); plt.close(fig)
        generated.append(str(path))

    # 6. 客流结构饼图
    if '06_客流结构' in charts:
        c = charts['06_客流结构']
        fig, ax = plt.subplots(figsize=(8, 8))
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
        ax.pie(c['pct'], labels=c['labels'], autopct='%1.0f%%', colors=colors, startangle=90)
        ax.set_title(c['title'])
        path = out_dir / 'chart_06_客流结构.png'
        fig.savefig(path, dpi=120, bbox_inches='tight'); plt.close(fig)
        generated.append(str(path))

    # 7. 政策叠加
    if '07_政策叠加' in charts:
        c = charts['07_政策叠加']
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(c['labels'], c['scope'], color='mediumpurple')
        ax.set_title(c['title']); ax.set_xlabel('影响范围 (%)')
        path = out_dir / 'chart_07_政策叠加.png'
        fig.savefig(path, dpi=120, bbox_inches='tight'); plt.close(fig)
        generated.append(str(path))

    # 8. 5 维矩阵雷达
    if '08_5维矩阵' in charts:
        c = charts['08_5维矩阵']
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        import numpy as np
        angles = np.linspace(0, 2*np.pi, len(c['labels']), endpoint=False).tolist()
        scores = c['scores'] + c['scores'][:1]
        angles = angles + angles[:1]
        ax.fill(angles, scores, alpha=0.25, color='steelblue')
        ax.plot(angles, scores, 'o-', color='steelblue')
        ax.set_xticks(angles[:-1]); ax.set_xticklabels(c['labels'])
        ax.set_title(c['title']); ax.set_ylim(0, 100)
        path = out_dir / 'chart_08_5维矩阵.png'
        fig.savefig(path, dpi=120, bbox_inches='tight'); plt.close(fig)
        generated.append(str(path))

    # 9. 供给 vs 需求增速
    if '09_供给增速' in charts:
        c = charts['09_供给增速']
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(c['labels']))
        ax.plot(x, c['supply_growth'], 'o-', label='供给增速(%)', color='coral', linewidth=2)
        ax.plot(x, c['demand_growth'], 's-', label='需求增速(%)', color='steelblue', linewidth=2)
        ax.set_xticks(x); ax.set_xticklabels(c['labels'], rotation=15)
        ax.set_title(c['title']); ax.legend(); ax.grid(True, alpha=0.3)
        path = out_dir / 'chart_09_供给vs需求.png'
        fig.savefig(path, dpi=120, bbox_inches='tight'); plt.close(fig)
        generated.append(str(path))

    return {'charts': generated, 'count': len(generated)}

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('用法: python gen_charts.py <raw_data.json> <output_dir>')
        sys.exit(1)
    print(json.dumps(gen_charts(sys.argv[1], sys.argv[2]), ensure_ascii=False, indent=2))