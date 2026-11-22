# -*- coding: utf-8 -*-
"""v3 runner: 10年/20年双年限 + 隐性成本 + 五大系统投资包（原因支撑）."""
import io, sys, os, json
_LOG = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\run_v3.txt"
sys.stdout = open(_LOG, "w", encoding="utf-8", buffering=1)
sys.stderr = sys.stdout
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc")
import hotel_irr_calc_zongfu_v2 as Z

# ⭐ 隐性成本参数（依据见说明文档 §隐性成本清单）
TRANS = {
    'd1a': dict(transition_drag_pct=0.12, transition_years=2,
                transition_extra_cost_annual=400.0, transition_oneoff=1200.0),
    'd1b': dict(transition_drag_pct=0.12, transition_years=2,
                transition_extra_cost_annual=400.0, transition_oneoff=1200.0),
    'd2':  dict(transition_drag_pct=0.20, transition_years=2,
                transition_extra_cost_annual=550.0, transition_oneoff=1800.0),
    'd3':  dict(transition_drag_pct=0.25, transition_years=2,
                transition_extra_cost_annual=700.0, transition_oneoff=2200.0),
}


def run(horizon):
    presets = Z.build_presets()
    out = {}
    for k, p in presets.items():
        key = k.rsplit('_', 1)[0]
        q = dict(p)
        q.update(TRANS.get(key, {}))
        q['horizon'] = horizon
        q['baseline'] = dict(p['baseline']); q['baseline']['horizon'] = horizon
        out[k] = Z.calc_zongfu2(q)
    return out


if __name__ == '__main__':
    for H in (10, 20):
        res = run(H)
        print("=" * 140)
        print(f"【{H} 年模型】国际联号口径 · 含隐性成本 · 中性情景")
        print(f"{'方案':<26}{'房':>4}{'ADR':>6}{'总营收':>9}{'TRevPAR':>9}{'GOP率':>7}"
              f"{'品牌费率':>8}{'业主GOP':>9}{'年均CF':>9}{'增量IRR':>9}{'增量NPV':>10}{'回收期':>8}")
        print("=" * 140)
        for key, name, tier, rooms, adr, occ, clm, inv, fo in Z.PATHS:
            r = res[f"{key}_中性"]; p = r['params']; y = r['yearly'][1]; inc = r['inc']
            ii = inc.get('inc_irr')
            ii_s = f"{ii*100:.2f}%" if ii is not None else "不存在"
            pb = inc.get('inc_pb')
            pb_s = f"{pb:.1f}" if pb else "不回本"
            cp = inc.get('cum_pos_yr')
            print(f"{name:<26}{rooms:>4}{adr:>6.0f}{y['total_revenue']:>9,.0f}{y['trevpar']:>9,.0f}"
                  f"{y['gop_rate']:>7.1f}{y['brand_fee_rate']:>8.1f}{y['gop_net']:>9,.0f}"
                  f"{inc['post_annual_cf']:>9,.0f}{ii_s:>9}{inc['inc_npv']:>10,.0f}{pb_s:>8}"
                  f"  累计转正Y{cp if cp else '>'}")
        b = res['d2_中性']['inc']
        print(f"  ▸ 改造前基线：年均CF {b['base_annual_cf']:>9,.0f} 万 ｜ 总营收 {b['base_total_rev']:>8,.0f} 万 "
              f"｜ TRevPAR {b['base_trevpar']:>7,.0f} ｜ 业主GOP率 {b['base_gop_net_rate']:>5.1f}% "
              f"｜ 品牌费率 {b['base_brand_fee_rate']:>5.1f}%")
        print()

    # 10 vs 20 对照（中性）
    r10, r20 = run(10), run(20)
    print("=" * 140)
    print("【10 年 vs 20 年 对照】中性情景 · 增量口径")
    print(f"{'方案':<26}{'增量IRR@10':>12}{'增量IRR@20':>12}{'增量NPV@10':>13}{'增量NPV@20':>13}"
          f"{'回收期@10':>11}{'回收期@20':>11}{'年均增量@10':>12}{'年均增量@20':>12}")
    print("=" * 140)
    for key, name, *_ in Z.PATHS:
        a, b = r10[f"{key}_中性"], r20[f"{key}_中性"]
        ia = a['inc'].get('inc_irr'); ib = b['inc'].get('inc_irr')
        sa = f"{ia*100:.2f}%" if ia is not None else "不存在"
        sb = f"{ib*100:.2f}%" if ib is not None else "不存在"
        pa = a['inc'].get('inc_pb'); pb = b['inc'].get('inc_pb')
        ca = a['inc'].get('cum_pos_yr'); cb2 = b['inc'].get('cum_pos_yr')
        print(f"{name:<26}{sa:>12}{sb:>12}{a['inc']['inc_npv']:>13,.0f}{b['inc']['inc_npv']:>13,.0f}"
              f"{(f'{pa:.1f}' if pa else '不回本'):>11}{(f'{pb:.1f}' if pb else '不回本'):>11}"
              f"{a['inc']['annual_delta']:>12,.0f}{b['inc']['annual_delta']:>12,.0f}"
              f"  转正Y{ca if ca else '>'}→Y{cb2 if cb2 else '>'}")
    print("=" * 140)
    # 导出
    out = {}
    for H, res in ((10, r10), (20, r20)):
        out[H] = {k: {'irr': v['inc'].get('inc_irr'), 'npv': v['inc']['inc_npv'],
                      'pb': v['inc'].get('inc_pb'), 'delta': v['inc']['annual_delta'],
                      'post_cf': v['inc']['post_annual_cf'], 'base_cf': v['inc']['base_annual_cf'],
                      'total_rev': v['inc']['post_total_rev'], 'trevpar': v['inc']['post_trevpar'],
                      'brand_fee_rate': v['inc']['post_brand_fee_rate']}
                 for k, v in res.items()}
    p = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\zf_calc_results_v3.json"
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("json:", p)
