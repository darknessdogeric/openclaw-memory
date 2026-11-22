"""
6 月 + H1 数据完整性审计 v2.0 — 仅 L0 国家级 30 个信源
（Eric 2026-07-23 纠错：默认全国，逐级下沉）
"""
import json
from datetime import datetime

# L0 国家级 30 个信源（不包含 L1/L2/L3 槽位）
L0_SOURCES = {
    'A_行业协会': ['中国旅游饭店业协会', '中国饭店协会', '中国旅游协会'],
    'B_国际研究': ['STR Global', '浩华 Horwath HTL', 'HVS', 'CBRE 世邦魏理仕', 'JLL 仲量联行', '戴德梁行'],
    'C_国内研究': ['迈点研究院 Meadin', '环球旅讯 TravelDaily', 'Fastdata 极数', '浩联智库', '中国旅游研究院'],
    'D_OTA': ['携程', '美团', '飞猪', '去哪儿', 'Booking.com', 'Airbnb'],
    'E_官方统计': ['国家文化和旅游部', '国家统计局'],
    'F_学术': ['北二外旅游管理学院', '中山大学旅游学院'],
    'G_媒体': ['第一财经 / DT 财经', '36 氪 / 虎嗅', '经济观察报 / 21 世纪', '财新 / 界面新闻'],
}

# L0 审计结果（仅全国级数据）
L0_AUDIT = {
    'A_行业协会': {
        '中国旅游饭店业协会': {'6m': 'partial', 'h1': 'yes', 'note': '6 月无月度报告；H1 半年报'},
        '中国饭店协会': {'6m': 'no', 'h1': 'yes', 'note': 'H1 报告需直接查询'},
        '中国旅游协会': {'6m': 'yes', 'h1': 'yes', 'note': '端午 1.1 亿人次（+6.3%）/ 403.5 亿元（+8.1%）'},
    },
    'B_国际研究': {
        'STR Global': {'6m': 'no', 'h1': 'no', 'note': '6 月报告 Q3 末发；H1 报告 Q4 才发'},
        '浩华 Horwath HTL': {'6m': 'partial', 'h1': 'yes', 'note': 'Q2 报告 2026-04-17 已发（厚海 MSI·12 页）'},
        'HVS': {'6m': 'no', 'h1': 'no', 'note': '付费订阅'},
        'CBRE 世邦魏理仕': {'6m': 'no', 'h1': 'no', 'note': '付费报告'},
        'JLL 仲量联行': {'6m': 'yes', 'h1': 'yes', 'note': '2026-06-25 REITs 白皮书 + 上海 H1'},
        '戴德梁行': {'6m': 'no', 'h1': 'no', 'note': '付费报告'},
    },
    'C_国内研究': {
        '迈点研究院 Meadin': {'6m': 'yes', 'h1': 'yes', 'note': '5月报 + H1 民宿首超酒店'},
        '环球旅讯 TravelDaily': {'6m': 'partial', 'h1': 'yes', 'note': 'H1 行业新闻'},
        'Fastdata 极数': {'6m': 'partial', 'h1': 'yes', 'note': '2025 H1 报告'},
        '浩联智库': {'6m': 'no', 'h1': 'no', 'note': '智库需查'},
        '中国旅游研究院': {'6m': 'yes', 'h1': 'yes', 'note': '节假日预测 + H1 趋势'},
    },
    'D_OTA': {
        '携程': {'6m': 'yes', 'h1': 'yes', 'note': '可实时抓取'},
        '美团': {'6m': 'yes', 'h1': 'yes', 'note': '可实时抓取'},
        '飞猪': {'6m': 'yes', 'h1': 'yes', 'note': '阿里生态'},
        '去哪儿': {'6m': 'yes', 'h1': 'yes', 'note': '价格聚合'},
        'Booking.com': {'6m': 'no', 'h1': 'yes', 'note': '国际客源 6 月需直接访问'},
        'Airbnb': {'6m': 'yes', 'h1': 'yes', 'note': '民宿标杆（途家替代）'},
    },
    'E_官方统计': {
        '国家文化和旅游部': {'6m': 'yes', 'h1': 'yes', 'note': '端午 + 月度公报'},
        '国家统计局': {'6m': 'yes', 'h1': 'yes', 'note': 'GDP/CPI 7 月发'},
    },
    'F_学术': {
        '北二外旅游管理学院': {'6m': 'no', 'h1': 'no', 'note': '学术周期长'},
        '中山大学旅游学院': {'6m': 'no', 'h1': 'no', 'note': '学术周期长'},
    },
    'G_媒体': {
        '第一财经 / DT 财经': {'6m': 'yes', 'h1': 'yes', 'note': 'DT 4 月青年报告'},
        '36 氪 / 虎嗅': {'6m': 'yes', 'h1': 'yes', 'note': '6.04 民宿深度'},
        '经济观察报 / 21 世纪': {'6m': 'yes', 'h1': 'yes', 'note': '财经深度'},
        '财新 / 界面新闻': {'6m': 'yes', 'h1': 'yes', 'note': '7.14 JLL H1 报道'},
    }
}


def audit_l0(mode='h1'):
    """审计 L0 国家级"""
    total = 0
    yes = 0
    partial = 0
    no = 0
    for cat, items in L0_AUDIT.items():
        for src, data in items.items():
            total += 1
            s = data[mode]
            if s == 'yes':
                yes += 1
            elif s == 'partial':
                partial += 1
            else:
                no += 1
    return yes, partial, no, total


def print_l0_audit():
    print('=' * 90)
    print('【L0 国家级数据源 · 6 月 + H1 数据完整性审计】')
    print('原则（Eric 2026-07-23）：默认只看全国，逐级下沉按需')
    print('审计时间：2026-07-23')
    print('=' * 90)
    print()

    yes_h1, partial_h1, no_h1, total = audit_l0('h1')
    yes_6m, partial_6m, no_6m, _ = audit_l0('6m')

    pct_h1_full = (yes_h1 / total) * 100
    pct_h1_partial = ((yes_h1 + partial_h1) / total) * 100
    pct_6m_full = (yes_6m / total) * 100
    pct_6m_partial = ((yes_6m + partial_6m) / total) * 100

    print(f'【L0 国家级共 {total} 个信源】')
    print()
    print(f'H1（1-6 月）：')
    print(f'  完全齐：{yes_h1}/{total} = {pct_h1_full:.1f}%')
    print(f'  含部分：{yes_h1 + partial_h1}/{total} = {pct_h1_partial:.1f}%')
    print(f'  缺失：{no_h1}/{total} = {(no_h1/total)*100:.1f}%')
    print()
    print(f'6 月：')
    print(f'  完全齐：{yes_6m}/{total} = {pct_6m_full:.1f}%')
    print(f'  含部分：{yes_6m + partial_6m}/{total} = {pct_6m_partial:.1f}%')
    print(f'  缺失：{no_6m}/{total} = {(no_6m/total)*100:.1f}%')
    print()

    # 分类详情
    print('【分类详情】')
    for cat, items in L0_AUDIT.items():
        cat_total = len(items)
        cat_h1_yes = sum(1 for d in items.values() if d['h1'] == 'yes')
        cat_6m_yes = sum(1 for d in items.values() if d['6m'] == 'yes')
        cat_h1_part = sum(1 for d in items.values() if d['h1'] in ['yes', 'partial'])
        cat_6m_part = sum(1 for d in items.values() if d['6m'] in ['yes', 'partial'])
        print(f'  {cat}（{cat_total} 个）')
        print(f'    6 月：齐 {cat_6m_yes} / 含部分 {cat_6m_part} / {cat_total}')
        print(f'    H1 ：齐 {cat_h1_yes} / 含部分 {cat_h1_part} / {cat_total}')
    print()

    # 明细
    print('【L0 信源明细】')
    for cat, items in L0_AUDIT.items():
        print(f'\n{cat}：')
        for src, data in items.items():
            m6 = {'yes': '[OK]', 'partial': '[..]', 'no': '[--]'}.get(data['6m'], '[?]')
            mh1 = {'yes': '[OK]', 'partial': '[..]', 'no': '[--]'}.get(data['h1'], '[?]')
            print(f'  {m6} 6月 / {mh1} H1 | {src}')
    print()

    # 缺失清单
    print('【L0 缺失清单】')
    print('6 月未到的信源：')
    for cat, items in L0_AUDIT.items():
        for src, data in items.items():
            if data['6m'] == 'no':
                print(f'  - {src} ({cat}): {data["note"]}')
    print()
    print('H1 未到的信源：')
    for cat, items in L0_AUDIT.items():
        for src, data in items.items():
            if data['h1'] == 'no':
                print(f'  - {src} ({cat}): {data["note"]}')

    print()
    print('=' * 90)
    print('【总结】')
    print(f'L0 国家级 30 个信源')
    print(f'  H1 完全齐：{pct_h1_full:.1f}%')
    print(f'  H1 含部分：{pct_h1_partial:.1f}%')
    print(f'  6 月完全齐：{pct_6m_full:.1f}%')
    print(f'  6 月含部分：{pct_6m_partial:.1f}%')
    print('=' * 90)


if __name__ == '__main__':
    print_l0_audit()