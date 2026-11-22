# -*- coding: utf-8 -*-
"""v4 runner: 三情景 x 10/20 年 x 含隐性成本 —— 供第七部分"每方向每种可能"使用."""
import io, sys, os, json
_D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
sys.stdout = open(os.path.join(_D, "run_v4.txt"), "w", encoding="utf-8", buffering=1)
sys.stderr = sys.stdout
sys.path.insert(0, _D)
import hotel_irr_calc_zongfu_v2 as Z

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
    out = {}
    for k, p in Z.build_presets().items():
        key = k.rsplit('_', 1)[0]
        q = dict(p)
        q.update(TRANS.get(key, {}))
        q['horizon'] = horizon
        q['baseline'] = dict(p['baseline'])
        q['baseline']['horizon'] = horizon
        out[k] = Z.calc_zongfu2(q)
    return out


if __name__ == '__main__':
    pk = list(Z.build_presets().keys())
    print("PRESET KEYS:", pk)
    res = {H: run(H) for H in (10, 20)}
    print("SAMPLE yearly[1] keys:", sorted(res[20][pk[0]]['yearly'][1].keys()))
    print("SAMPLE params keys:", sorted(res[20][pk[0]]['params'].keys()))
    print("SAMPLE inc keys:", sorted(res[20][pk[0]]['inc'].keys()))
    dump = {}
    for H in (10, 20):
        dump[str(H)] = {}
        for k in pk:
            r = res[H][k]
            dump[str(H)][k] = {
                'params': r['params'],
                'y1': r['yearly'][1],
                'inc': {kk: vv for kk, vv in r['inc'].items()},
            }
    p = os.path.join(_D, "zf_calc_results_v4.json")
    json.dump(dump, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("json:", p)
