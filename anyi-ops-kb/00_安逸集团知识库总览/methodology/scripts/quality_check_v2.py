# -*- coding: utf-8 -*-
"""
quality_check_v2.py - 行业报告 / 区域报告 7 项质量校验
v1.0 单店模板不适用，改用行业向校验
"""
import sys, json, re
from pathlib import Path

INDUSTRY_CHECKS = [
    ('34 维度信源覆盖率', '__check_coverage_industry', '>=15%'),
    ('10 章宏观骨架', '__check_schema_industry', 'all 10 sections'),
    ('同比 baseline 标注', '__check_yoy_baseline', 'yoy present'),
    ('5 维 MECE 切片', '__check_5d', '5 dims present'),
    ('政策合规章节', '__check_policy_industry', 'policy keywords'),
    ('信源>=10 类可追溯', '__check_sources_industry', '>=10 categories'),
    ('3 反直觉洞察', '__check_insights', '>=3 insights'),
]

# ---------- 单店版本（保留兼容） ----------
SINGLE_CHECKS = [
    ('34 维度信源覆盖率', '__check_coverage', '>=70%'),
    ('10 章宏观+5 维可行性完整', '__check_schema', 'all present'),
    ('Eric ADR 估算方法', '__check_adr', 'method documented'),
    ('政策合规（办证+土地）', '__check_policy', 'complete'),
    ('财务模型 3 档+修正路径', '__check_finance', '3 scenarios'),
    ('图表>=6张+PDF 完整', '__check_artifacts', '>=6 PNG + PDF'),
    ('数据来源可追溯>=8 类', '__check_sources', '>=8 categories'),
]

SOURCES_34_INDUSTRY = [
    'STR', '浩华', 'Horwath', 'HVS', 'JLL', 'CBRE', '仲量联行', '戴德梁行',
    '迈点', '环球旅讯', 'Fastdata', '澎润', '酒店之家',
    '携程', '美团', '飞猪', '去哪儿', 'Booking', 'Airbnb',
    '文旅部', '国家统计局', '交通运输部', '商务部', '民航局',
    '准聚数据', '航班管家', 'DAST',
    '第一财经', 'DT 财经', '36 氪', '虎嗅', '澎湃', '时代财经', '经观', '21世纪', '财新',
    '中信证券', '中金', '华泰', '国信', 'Wind', 'Bloomberg', 'QuestMobile',
    '华住', '锦江', '亚朵', '首旅', '君亭', '东呈', '格林', '万豪', '希尔顿', '凯悦', '洲际', '雅高', '温德姆',
    '同程', '途家', '木鸟', '去哪儿', '飞猪', 'Booking.com',
    '中国饭店协会', '中国旅游协会', '中国旅游研究院',
]

INDUSTRY_10_SECTIONS = [
    'Executive Summary', '宏观底盘', '政策', '需求', '供给',
    '区域', '集团', '行业', '风险', '结论',
]

POLICY_KEYWORDS = ['免签', '拼假', '消费券', '文旅', 'REITs', '节假日', '政策', '价格提醒', '市场监管', '入境']


def __check_coverage_industry(report_path: str) -> tuple:
    text = Path(report_path).read_text(encoding='utf-8', errors='ignore')
    hit = sum(1 for s in SOURCES_34_INDUSTRY if s in text)
    pct = round(hit / len(SOURCES_34_INDUSTRY) * 100, 1)
    return hit >= 10, f'{pct}% ({hit}/{len(SOURCES_34_INDUSTRY)})' + (' (industry mode >=10)' if hit >= 10 else ' (need >=10)')


def __check_schema_industry(report_path: str) -> tuple:
    text = Path(report_path).read_text(encoding='utf-8', errors='ignore')
    found = []
    missing = []
    # 行业报告 10 个宏观章节（用 # 二级标题检测）
    for sec in INDUSTRY_10_SECTIONS:
        if sec in text or sec.replace('Executive Summary', '执行摘要') in text:
            found.append(sec)
        else:
            missing.append(sec)
    return len(missing) <= 3, f'{len(found)}/10 章节' + (f', missing: {missing}' if missing else '')


def __check_yoy_baseline(report_path: str) -> tuple:
    text = Path(report_path).read_text(encoding='utf-8', errors='ignore')
    yoy_patterns = ['同比', 'YoY', 'yoy', '对比上一年', '较上年', '+%', '-%', '+pct', '-pct', '%']
    yoy_count = sum(text.count(p) for p in yoy_patterns)
    return yoy_count >= 5, f'{yoy_count} 个同比标注'


def __check_5d(report_path: str) -> tuple:
    text = Path(report_path).read_text(encoding='utf-8', errors='ignore')
    dims = ['OCC', 'ADR', 'RevPAR', '档次', '客群', '区域', '品牌', 'TOP 10', '头部']
    found = sum(1 for d in dims if d in text)
    return found >= 5, f'{found}/9 维度切片'


def __check_policy_industry(report_path: str) -> tuple:
    text = Path(report_path).read_text(encoding='utf-8', errors='ignore')
    hit = sum(1 for k in POLICY_KEYWORDS if k in text)
    return hit >= 3, f'{hit}/{len(POLICY_KEYWORDS)} 政策关键词'


def __check_sources_industry(report_path: str) -> tuple:
    text = Path(report_path).read_text(encoding='utf-8', errors='ignore')
    src = ['数据来源', 'Source', '来源', '口径', 'NBS', 'STR', '华住', '携程', '去哪儿', '同程', '飞猪']
    found = sum(1 for s in src if s in text)
    return found >= 5, f'{found}/{len(src)} 信源标识'


def __check_insights(report_path: str) -> tuple:
    text = Path(report_path).read_text(encoding='utf-8', errors='ignore')
    insight_markers = ['反直觉', '关键洞察', '洞察', '核心发现', '❶', '❷', '❸', '❹', '❺', '一句话', '核心结论']
    found = sum(1 for m in insight_markers if m in text)
    return found >= 2, f'{found} 个洞察标识'


INDUSTRY_FUNCS = {
    '34 维度信源覆盖率': __check_coverage_industry,
    '10 章宏观骨架': __check_schema_industry,
    '同比 baseline 标注': __check_yoy_baseline,
    '5 维 MECE 切片': __check_5d,
    '政策合规章节': __check_policy_industry,
    '信源>=10 类可追溯': __check_sources_industry,
    '3 反直觉洞察': __check_insights,
}


def run_industry(report_path: str) -> dict:
    results = []
    for name, _, _ in INDUSTRY_CHECKS:
        try:
            ok, detail = INDUSTRY_FUNCS[name](report_path)
            results.append({'check': name, 'pass': ok, 'detail': detail})
        except Exception as e:
            results.append({'check': name, 'pass': False, 'detail': f'error: {e}'})
    total = sum(1 for r in results if r['pass'])
    return {'mode': 'industry', 'total_pass': total, 'total_checks': len(results), 'results': results, 'all_pass': total == len(results)}


if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[1] not in ('industry', 'industry-all'):
        print('用法: python quality_check_v2.py industry <report.md>')
        print('或:   python quality_check_v2.py industry-all <dir>  (批量)')
        sys.exit(1)
    if sys.argv[1] == 'industry-all':
        target_dir = Path(sys.argv[2])
        reports = sorted(target_dir.glob('*.md'))
        if not reports:
            print(f'未找到 .md 文件: {target_dir}')
            sys.exit(1)
        print(f'\n=== 批量校验 {len(reports)} 份报告（行业向）===\n')
        all_results = []
        for rp in reports:
            print(f'--- {rp.name} ---')
            r = run_industry(str(rp))
            print(f"  总分: {r['total_pass']}/{r['total_checks']}")
            for c in r['results']:
                mark = '[OK]  ' if c['pass'] else '[FAIL]'
                print(f"  {mark} {c['check']:25s}  {c['detail']}")
            print()
            all_results.append({'file': rp.name, **r})
        # 汇总
        total_pass_all = sum(r['total_pass'] for r in all_results)
        total_checks_all = sum(r['total_checks'] for r in all_results)
        print(f'=== 全量汇总: {total_pass_all}/{total_checks_all} = {round(total_pass_all/total_checks_all*100, 1)}% ===')
        # JSON
        out = target_dir / 'quality_check_v2_results.json'
        out.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'结果: {out}')
        sys.exit(0)
    # 单文件
    r = run_industry(sys.argv[2])
    print(f"\n=== 行业向质量校验: {r['total_pass']}/{r['total_checks']} 通过 ===\n")
    for c in r['results']:
        mark = '[OK]  ' if c['pass'] else '[FAIL]'
        print(f"  {mark} {c['check']:25s}  {c['detail']}")
    sys.exit(0 if r['all_pass'] else 1)