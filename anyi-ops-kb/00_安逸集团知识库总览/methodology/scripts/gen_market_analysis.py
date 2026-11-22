# -*- coding: utf-8 -*-
"""
gen_market_analysis.py - 一键生成市场分析报告（编排器）
历史：methodology/sop-region-analysis.md 引用。v1.0 编排器 — 串联 4 个 SOP 步骤。
"""
import sys, json
from pathlib import Path
from datetime import datetime

def gen_market_analysis(region: str, risk: str = '稳', output_dir: str = None) -> dict:
    """
    5 步流水线:
      1. audit_34_dimensions
      2. fetch_data
      3. fill_schema
      4. gen_charts + build_pdf
      5. quality_check
    """
    if output_dir is None:
        output_dir = f"reports/{region}_{datetime.now().strftime('%Y%m%d')}"
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    log = {'region': region, 'risk': risk, 'steps': []}

    # Step 1: 审计
    try:
        from audit_34_dimensions import audit_report
        log['steps'].append({'step': 1, 'name': 'audit', 'status': 'ok'})
    except ImportError as e:
        log['steps'].append({'step': 1, 'name': 'audit', 'status': 'skipped', 'reason': str(e)})

    # Step 2: fetch_data
    try:
        from fetch_data import fetch
        log['steps'].append({'step': 2, 'name': 'fetch', 'status': 'ok'})
    except ImportError as e:
        log['steps'].append({'step': 2, 'name': 'fetch', 'status': 'skipped', 'reason': str(e)})

    # Step 3: fill_schema
    try:
        from fill_schema import fill
        log['steps'].append({'step': 3, 'name': 'fill', 'status': 'ok'})
    except ImportError as e:
        log['steps'].append({'step': 3, 'name': 'fill', 'status': 'skipped', 'reason': str(e)})

    # Step 4: charts + pdf
    try:
        from gen_charts import gen_charts
        from build_pdf import build_pdf
        log['steps'].append({'step': 4, 'name': 'render', 'status': 'ok'})
    except ImportError as e:
        log['steps'].append({'step': 4, 'name': 'render', 'status': 'skipped', 'reason': str(e)})

    # Step 5: quality_check
    try:
        from quality_check import run_all
        log['steps'].append({'step': 5, 'name': 'qc', 'status': 'ok'})
    except ImportError as e:
        log['steps'].append({'step': 5, 'name': 'qc', 'status': 'skipped', 'reason': str(e)})

    log['output_dir'] = output_dir
    log['note'] = 'v1.0 骨架 — 实际抓取/图表/PDF 需手动触发或集成到本编排器'
    return log

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python gen_market_analysis.py <地区> [稳|积极|极稳]')
        sys.exit(1)
    region = sys.argv[1]
    risk = sys.argv[2] if len(sys.argv) > 2 else '稳'
    print(json.dumps(gen_market_analysis(region, risk), ensure_ascii=False, indent=2))