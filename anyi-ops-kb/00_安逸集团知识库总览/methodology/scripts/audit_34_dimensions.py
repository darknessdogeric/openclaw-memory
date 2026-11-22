# -*- coding: utf-8 -*-
"""
audit_34_dimensions.py - 34 维度信源覆盖率审计
历史：methodology/sop-region-analysis.md / quality-checklist.md 引用，但未实现。
现状：v1.0 骨架 — 扫描 markdown 报告，统计 34 个信源被引用的次数。
"""
import re, sys, json
from pathlib import Path

# 34 维度信源清单（v4.0 终版）
SOURCES_34 = {
    'A': ['中国旅游饭店业协会', '中国饭店协会', '中国旅游协会', '中国演出行业协会', '中国饭店与餐饮协会'],
    'B': ['STR Global', '浩华', 'Horwath', 'HVS', 'CBRE', '世邦魏理仕', 'JLL', '仲量联行', '戴德梁行'],
    'C': ['迈点', 'Meadin', '环球旅讯', 'TravelDaily', 'Fastdata', '思瀚', '未来智库', '澎润'],
    'D': ['携程', '美团', '飞猪', '去哪儿', 'Booking.com', 'Airbnb'],
    'E': ['国家文化和旅游部', '文旅部', '国家统计局', '国家移民管理局', '商务部'],
    'F': ['准聚数据', '航班管家', 'DAST', '酒店之家'],
    'G': ['第一财经', 'DT 财经', '36 氪', '虎嗅', '澎湃', '时代财经', '经观', '21世纪', '财新', '界面'],
    'H': ['中信证券', '中金', '华泰证券', '国信证券', 'Wind', 'Bloomberg', 'QuestMobile'],
}

def audit_report(md_path: str) -> dict:
    p = Path(md_path)
    if not p.exists():
        return {'error': f'文件不存在: {md_path}'}
    text = p.read_text(encoding='utf-8', errors='ignore')
    coverage = {}
    total = 0
    hit = 0
    for cat, sources in SOURCES_34.items():
        for s in sources:
            total += 1
            if s in text:
                hit += 1
                coverage[f'{cat}-{s}'] = text.count(s)
    return {
        'file': md_path,
        'total_sources': total,
        'hit': hit,
        'coverage_pct': round(hit / total * 100, 1) if total else 0,
        'by_source': coverage,
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python audit_34_dimensions.py <report.md>')
        print('或: python audit_34_dimensions.py --check <md> (>=70% pass)')
        sys.exit(1)
    if sys.argv[1] == '--check':
        r = audit_report(sys.argv[2])
        ok = r.get('coverage_pct', 0) >= 70
        print(f"覆盖率: {r.get('coverage_pct', 0)}%  {'✓ PASS' if ok else '✗ FAIL'}")
        sys.exit(0 if ok else 1)
    r = audit_report(sys.argv[1])
    print(json.dumps(r, ensure_ascii=False, indent=2))