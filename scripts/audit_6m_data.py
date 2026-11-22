"""
6 月 + 上半年数据完整性审计脚本 v1.0
按 34 维度信源逐项检查 2026-06 + 2026 H1 数据是否齐全
"""
import os
import json
from datetime import datetime

# 34 维度信源清单（与 data-source-34-dimensions.md 一致）
SOURCES = {
    'A': {
        'name': '行业协会',
        'count': 5,
        'items': [
            '中国旅游饭店业协会',
            '中国饭店协会',
            '中国旅游协会',
            '云南省饭店协会',
            '州市级酒店/民宿协会'
        ]
    },
    'B': {
        'name': '国际权威研究机构',
        'count': 6,
        'items': [
            'STR Global',
            '浩华 Horwath HTL',
            'HVS',
            'CBRE 世邦魏理仕',
            'JLL 仲量联行',
            '戴德梁行'
        ]
    },
    'C': {
        'name': '国内行业研究',
        'count': 5,
        'items': [
            '迈点研究院 Meadin',
            '环球旅讯 TravelDaily',
            'Fastdata 极数',
            '浩联智库',
            '中国旅游研究院'
        ]
    },
    'D': {
        'name': 'OTA 平台',
        'count': 6,
        'items': [
            '携程',
            '美团',
            '飞猪',
            '去哪儿',
            'Booking.com',
            'Airbnb'
        ]
    },
    'E': {
        'name': '官方统计',
        'count': 5,
        'items': [
            '国家文化和旅游部',
            '国家统计局',
            '省/直辖市文旅厅',
            '州市统计局/政府',
            '县区级统计局/政府'
        ]
    },
    'F': {
        'name': '学术/智库',
        'count': 3,
        'items': [
            '北二外旅游管理学院',
            '中山大学旅游学院',
            '本地高校/智库'
        ]
    },
    'G': {
        'name': '财经/行业媒体',
        'count': 4,
        'items': [
            '第一财经 / DT 财经',
            '36 氪 / 虎嗅',
            '经济观察报 / 21 世纪',
            '财新 / 界面新闻'
        ]
    }
}


def audit_source(category, item, has_data_6m, has_data_h1, source_url='', notes=''):
    """单个信源的审计"""
    return {
        'category': category,
        'item': item,
        'has_data_6m': has_data_6m,
        'has_data_h1': has_data_h1,
        'source_url': source_url,
        'notes': notes,
        'status_6m': '[OK]' if has_data_6m else '[MISSING]',
        'status_h1': '[OK]' if has_data_h1 else '[MISSING]',
    }


def generate_audit_template():
    """生成 6 月+上半年审计模板"""
    template = {
        'metadata': {
            'audit_date': datetime.now().strftime('%Y-%m-%d'),
            'audit_window': '2026-06 + 2026 H1 (1-6 月)',
            'total_sources': 34,
            'categories': 7
        },
        'sources': []
    }

    # 为每个信源预填占位
    for cat, info in SOURCES.items():
        for item in info['items']:
            template['sources'].append(audit_source(
                cat, item, False, False, '', '待审核'
            ))

    return template


def print_audit_report(audit_data):
    """打印审计报告"""
    print('=' * 80)
    print('6 月 + 上半年数据完整性审计报告')
    print(f'审计窗口：2026-06 + 2026 H1（1-6 月）')
    print(f'审计时间：{audit_data["metadata"]["audit_date"]}')
    print('=' * 80)
    print()

    total = len(audit_data['sources'])
    has_6m = sum(1 for s in audit_data['sources'] if s['has_data_6m'])
    has_h1 = sum(1 for s in audit_data['sources'] if s['has_data_h1'])

    print(f'总信源数：{total}')
    print(f'6 月数据完整：{has_6m} / {total} = {has_6m/total*100:.1f}%')
    print(f'上半年数据完整：{has_h1} / {total} = {has_h1/total*100:.1f}%')
    print()

    # 按类别统计
    for cat, info in SOURCES.items():
        cat_sources = [s for s in audit_data['sources'] if s['category'] == cat]
        cat_6m = sum(1 for s in cat_sources if s['has_data_6m'])
        cat_h1 = sum(1 for s in cat_sources if s['has_data_h1'])

        print(f'【{cat} 类】{info["name"]}（{info["count"]} 个）')
        print(f'  6 月：{cat_6m}/{info["count"]} = {cat_6m/info["count"]*100:.0f}%')
        print(f'  上半年：{cat_h1}/{info["count"]} = {cat_h1/info["count"]*100:.0f}%')

        for s in cat_sources:
            mark_6m = '[OK]' if s['has_data_6m'] else '[--]'
            mark_h1 = '[OK]' if s['has_data_h1'] else '[--]'
            print(f'  {mark_6m} 6月  {mark_h1} H1 | {s["item"]}')
        print()


def save_audit_json(audit_data, filepath):
    """保存为 JSON"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(audit_data, f, ensure_ascii=False, indent=2)


# 执行
if __name__ == '__main__':
    audit_data = generate_audit_template()
    print_audit_report(audit_data)
    save_audit_json(audit_data, 'D:/B166ER-OpenClaw/workspace/reports/audit_6m_template.json')
    print(f'模板已保存：reports/audit_6m_template.json')
    print(f'下一步：人工或 AI 审核每个信源的 6 月数据可用性')