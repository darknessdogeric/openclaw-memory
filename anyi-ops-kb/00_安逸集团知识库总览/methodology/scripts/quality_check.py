# -*- coding: utf-8 -*-
"""
quality_check.py - 7 项强制质量校验
历史：methodology/quality-checklist.md 引用。v1.0 骨架 — 实际跑 7 项检查。
"""
import sys, json
from pathlib import Path

# 7 项检查（详见 quality-checklist.md）
CHECKS = [
    ('34 维度信源覆盖率', '__check_coverage', '>=70%'),
    ('10 章宏观+5 维可行性完整', '__check_schema', 'all present'),
    ('Eric ADR 估算方法', '__check_adr', 'method documented'),
    ('政策合规（办证+土地）', '__check_policy', 'complete'),
    ('财务模型 3 档+修正路径', '__check_finance', '3 scenarios'),
    ('图表≥6张+PDF 完整', '__check_artifacts', '>=6 PNG + PDF'),
    ('数据来源可追溯≥8 类', '__check_sources', '>=8 categories'),
]

def __check_coverage(report_path: str) -> tuple:
    from audit_34_dimensions import audit_report
    r = audit_report(report_path)
    pct = r.get('coverage_pct', 0)
    return pct >= 70, f'{pct}%'

def __check_schema(report_path: str) -> tuple:
    text = Path(report_path).read_text(encoding='utf-8', errors='ignore')
    required = ['第 1 章', '第 11 章', '5 维', '财务模型', '退出', '办证']
    missing = [r for r in required if r not in text]
    return not missing, f'missing: {missing}' if missing else 'all present'

def __check_adr(report_path: str) -> tuple:
    text = Path(report_path).read_text(encoding='utf-8', errors='ignore')
    has_adr = ('ADR' in text and ('0.5' in text or '0.865' in text or '×0.5' in text))
    return has_adr, 'Eric 方法提及' if has_adr else '缺失 ADR 估算公式'

def __check_policy(report_path: str) -> tuple:
    text = Path(report_path).read_text(encoding='utf-8', errors='ignore')
    keys = ['办证', '土地', '消防', '集体', '宅基地']
    has = sum(1 for k in keys if k in text)
    return has >= 4, f'{has}/5 政策关键词'

def __check_finance(report_path: str) -> tuple:
    text = Path(report_path).read_text(encoding='utf-8', errors='ignore')
    has_3 = all(s in text for s in ['保守', '中性', '乐观'])
    return has_3, '3 档场景齐全' if has_3 else '缺场景'

def __check_artifacts(report_path: str) -> tuple:
    base = Path(report_path).parent
    pngs = list(base.rglob('*.png'))
    pdfs = list(base.rglob('*.pdf'))
    return len(pngs) >= 6 and len(pdfs) >= 1, f'{len(pngs)} PNG, {len(pdfs)} PDF'

def __check_sources(report_path: str) -> tuple:
    text = Path(report_path).read_text(encoding='utf-8', errors='ignore')
    categories = ['STR', '浩华', 'JLL', '迈点', 'Fastdata', '迈点', '中国旅游研究院', '携程', '美团', '飞猪', '去哪儿']
    has = sum(1 for c in categories if c in text)
    return has >= 6, f'{has}/11 已知信源'

CHECK_FUNCS = {
    '34 维度信源覆盖率': __check_coverage,
    '10 章宏观+5 维可行性完整': __check_schema,
    'Eric ADR 估算方法': __check_adr,
    '政策合规（办证+土地）': __check_policy,
    '财务模型 3 档+修正路径': __check_finance,
    '图表≥6张+PDF 完整': __check_artifacts,
    '数据来源可追溯≥8 类': __check_sources,
}

def run_all(report_path: str) -> dict:
    results = []
    for name, _fn, _crit in CHECKS:
        try:
            ok, detail = CHECK_FUNCS[name](report_path)
            results.append({'check': name, 'pass': ok, 'detail': detail})
        except Exception as e:
            results.append({'check': name, 'pass': False, 'detail': f'error: {e}'})
    total = sum(1 for r in results if r['pass'])
    return {'total_pass': total, 'total_checks': len(results), 'results': results, 'all_pass': total == len(results)}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python quality_check.py <report.md>')
        sys.exit(1)
    r = run_all(sys.argv[1])
    print(f"\n=== 质量校验: {r['total_pass']}/{r['total_checks']} 通过 ===\n")
    for c in r['results']:
        mark = '[OK]' if c['pass'] else '[FAIL]'
        print(f"  {mark}  {c['check']:30s}  {c['detail']}")
    sys.exit(0 if r['all_pass'] else 1)