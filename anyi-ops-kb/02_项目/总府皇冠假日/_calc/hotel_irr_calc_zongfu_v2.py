# -*- coding: utf-8 -*-
"""
总府皇冠假日酒店改造 · 国际联号口径投资测算引擎 v2.0 (2026-11-03)

⭐ v2.0 相对 v1.0 的根本升级：**从"国内 5 星及以下口径"改为"国际联号高星级/奢华口径"**
  v1.0 用的是集团通用模版的国内分级参数库（20 类，GOP 率、非房占比、单房投资均为国内中端口径）
  v2.0 按国际联号（HMA）标准重建：
   ① 收入模型：USALI 部门制（客房 / 餐饮 / 会议宴会 / 其他经营部门 / 其他），
      取代 v1.0 的"客房 + 非房"两分法
   ② 部门成本：按国际基准的**部门 GOP 率**（Rooms 65-75% / F&B 15-30% / Banquets 25-40%）
   ③ 品牌费用结构完整建模（国际 HMA 标准）：
      基础管理费（总营收）｜激励管理费（GOP）｜市场推广与分销费（总营收）
      ｜忠诚度计划费（客房收入）｜FF&E 储备金（总营收 3-5%）｜技术服务费（pre-opening）
   ④ "减房不减收"用 **TRevPAR**（总收入/可售房）度量，而非只算客房
   ⑤ 保留 v1.0 的增量口径（baseline）与全部 7 处扩展

数据来源：
 - 国际基准：Hotel News Resource / Pulse RevOps 2027 / Stirling Hospitality
   / Visions Alliance / Angel in Dubai 2026-10（多源交叉）
 - 总府现状：业主第一批次实测（USALI 口径《2026年10月利润表》+《近24个月主要经营指标》）
 - 洲际费率：一手沟通纪要 F2-29
"""
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\toolbox")
import hotel_irr_calc as E

RAMP_RENOVATION = {
    'adr': [0.95, 1.00, 1.00, 1.00, 1.00, 0.98, 0.96, 0.93, 0.91, 0.89],
    'occ': [0.90, 1.00, 1.00, 1.00, 1.00, 0.98, 0.96, 0.93, 0.90, 0.87],
}
E.RAMP_CURVES['renovation'] = RAMP_RENOVATION
E.RAMP_CURVES['flat'] = {'adr': [1.0] * 10, 'occ': [1.0] * 10}
# ⭐ 20 年曲线（对齐国资评估"孰短原则"下的 23-25 年收益年期口径）
_d = [0.95, 1.00, 1.00, 1.00, 1.00] + [round(0.98 - 0.008 * i, 4) for i in range(15)]
_o = [0.90, 1.00, 1.00, 1.00, 1.00] + [round(0.98 - 0.008 * i, 4) for i in range(15)]
E.RAMP_CURVES['renovation20'] = {'adr': _d[:20], 'occ': _o[:20]}
E.RAMP_CURVES['flat20'] = {'adr': [1.0] * 20, 'occ': [1.0] * 20}
E.RAMP_CURVES['renovation30'] = {'adr': _d + [0.86] * 10, 'occ': _o + [0.86] * 10}
E.RAMP_CURVES['flat30'] = {'adr': [1.0] * 30, 'occ': [1.0] * 30}


def _stage(y):
    if y < 1: return '爬坡'
    if y < 2: return '成熟'
    if y < 5: return '峰值'
    if y < 7: return '稳定'
    if y < 10: return '微降'
    if y < 14: return '回落'
    return '回升'


def _ramp_for(q, H):
    """按模型年限自动选爬坡曲线：10 年 / 20 年 / 30 年"""
    key = q.get('ramp_type', 'renovation')
    if H > 25:
        return E.RAMP_CURVES.get(key + '30') or E.RAMP_CURVES[key]
    if H > 12:
        return E.RAMP_CURVES.get(key + '20') or E.RAMP_CURVES[key]
    return E.RAMP_CURVES[key]

# ══════════════ 国际联号口径参数库（替代国内分级参数库）══════════════
INTL = {
    # tier: 收入结构(客房/餐饮/会议宴会/其他部门/其他) + 部门GOP率 + 品牌费率结构
    'intl_luxury': {          # 奢华/顶奢（半岛 / 文华东方 / 丽晶 / 瑰丽级）
        'mix': dict(rooms=0.575, fnb=0.350, banq=0.050, other_dept=0.020, misc=0.005),
        'dept_gop': dict(rooms=0.60, fnb=0.20, banq=0.29, other_dept=0.46, misc=0.85),
        'fees': dict(base=0.020, incentive=0.10, marketing=0.020,
                     loyalty=0.020, tech=250.0, ffe_reserve=0.040),
    },
    'intl_upper_upscale': {   # 上奢/高端全服务（洲至奢选 / 瑞吉 / 君悦级）
        'mix': dict(rooms=0.625, fnb=0.250, banq=0.075, other_dept=0.030, misc=0.020),
        'dept_gop': dict(rooms=0.58, fnb=0.19, banq=0.28, other_dept=0.45, misc=0.85),
        'fees': dict(base=0.020, incentive=0.08, marketing=0.020,
                     loyalty=0.020, tech=150.0, ffe_reserve=0.035),
    },
    'intl_current_crowne': {  # 现状口径（皇冠委托管理）
        'mix': dict(rooms=0.649, fnb=0.134, banq=0.144, other_dept=0.020, misc=0.053),
        'dept_gop': dict(rooms=0.30, fnb=0.16, banq=0.26, other_dept=0.40, misc=0.60),
        'fees': dict(base=0.020, incentive=0.06, marketing=0.030,
                     loyalty=0.020, tech=0.0, ffe_reserve=0.020),
    },
}

# ══════════════ 洲际口径（一手证据，F2-29 沟通纪要）══════════════
# 特许管理费 = 客房收入 5%（取代现行"基本管理费-委托管理经调整总收入 2% + 鼓励性管理费"）
# 其他基金收费一致：科技费 / 营销与预定进款 / 频繁旅行计划
IHG_VIGNETTE = dict(base=0.000, incentive=0.000, marketing=0.020, loyalty=0.020,
                    tech=100.0, ffe_reserve=0.030, room_rev_fee=0.050)


def _dept_rev(p, mix, rooms, adr, occ, arn, other_dept_base):
    """按 USALI 部门制分配收入。
    客房收入由 ADR×OCC×间夜 驱动；餐饮/会议/其他部门按"占客房收入比例"派生
    （国际惯例：餐饮与宴会随住店客流与 ADR 同步放大，是"减房不减收"的机制）"""
    room_rev = adr * occ * arn / 10000.0
    # 非房部门以客房收入为基准（而非以总营收为基准），避免循环
    scale = room_rev / mix['rooms'] if mix['rooms'] > 0 else 0
    fnb = scale * mix['fnb']
    banq = scale * mix['banq']
    other = scale * mix['other_dept']
    misc = scale * mix['misc']
    tot = room_rev + fnb + banq + other + misc
    return dict(rooms=room_rev, fnb=fnb, banq=banq, other_dept=other, misc=misc, total=tot)


def calc_zongfu2(p):
    q = dict(p)
    q.setdefault('discount_rate', 0.08)
    q.setdefault('tax_rate', 0.25)
    q.setdefault('labor_in_gop', True)
    q.setdefault('building_depreciation_years', 10)
    q.setdefault('debt_service_annual', 0)
    q.setdefault('closure_months', 0)
    q.setdefault('closure_loss_monthly', 0)
    q.setdefault('rent_annual', 0)
    q.setdefault('tier_params', 'intl_upper_upscale')
    q.setdefault('fee_override', None)

    tier = INTL[q['tier_params']]
    mix, dgop = tier['mix'], tier['dept_gop']
    fees = dict(tier['fees'])
    if q.get('fee_override'):
        fees.update(q['fee_override'])

    rooms = q['rooms']
    H = int(q.get('horizon', 10))
    ramp = _ramp_for(q, H)
    arn = rooms * 365
    bv = q.get('building_value_existing') or (q['total_invest'] * 0.60)
    emv = q.get('electromechanical_value') or (q['total_invest'] * 0.25)
    bdep = q['building_depreciation_years']

    yearly = []
    tr_years = int(q.get('transition_years', 0))
    drag_pct = q.get('transition_drag_pct', 0.0)
    extra_cost = q.get('transition_extra_cost_annual', 0.0)
    for y in range(H):
        adr = q['peak_adr'] * ramp['adr'][y]
        occ = q['peak_occ'] * ramp['occ'][y]
        rev = _dept_rev(q, mix, rooms, adr, occ, arn, None)
        # ⭐ 隐性成本：停业后过渡期收入折损 + 过渡期额外成本（团队重建/声誉修复/会员挽回）
        drag = drag_pct if y < tr_years else 0.0
        if drag:
            for k in ('rooms', 'fnb', 'banq', 'other_dept', 'misc'):
                rev[k] *= (1 - drag)
            rev['total'] *= (1 - drag)
        # 部门成本 → 部门 GOP
        gop_dept = {
            'rooms': rev['rooms'] * dgop['rooms'],
            'fnb': rev['fnb'] * dgop['fnb'],
            'banq': rev['banq'] * dgop['banq'],
            'other_dept': rev['other_dept'] * dgop['other_dept'],
            'misc': rev['misc'] * dgop['misc'],
        }
        gop = sum(gop_dept.values())
        # ⭐ 基线锚定实测口径（经营毛利率），避免用"标准部门率"高估现状低配部门的效率
        if q.get('gop_measured_rate'):
            gop = rev['total'] * q['gop_measured_rate']
        # 品牌费用（国际 HMA 结构）
        fee_base = rev['total'] * fees['base']
        fee_inc = gop * fees['incentive']
        fee_mkt = rev['total'] * fees['marketing']
        fee_loy = rev['rooms'] * fees['loyalty']
        fee_roomrev = rev['rooms'] * fees.get('room_rev_fee', 0.0)
        fee_tech = fees.get('tech', 0.0)
        fee_ffe = rev['total'] * fees['ffe_reserve']
        brand_fees = fee_base + fee_inc + fee_mkt + fee_loy + fee_roomrev + fee_tech + fee_ffe
        # 业主在激励费前先取（Owner Priority，按投资额固定门槛）
        op = q.get('owner_priority', 0.0)
        fee_inc_pay = max(0.0, fee_inc - min(op, gop))
        brand_fees = brand_fees - fee_inc + fee_inc_pay
        gop_net = gop - brand_fees          # 业主口径 GOP（扣品牌费用后）

        dep_exist = bv / min(bdep, 10) if bdep else 0
        dep_new = (q['total_invest'] / 10.0) if q.get('include_new_dep', True) else 0.0
        dep = dep_exist + dep_new
        ptax = bv * 0.7 * 0.012
        pins = (bv + q['total_invest']) * 0.00035
        mins = emv * 0.00045
        rent = q.get('rent_annual', 0)
        debt = q['debt_service_annual']
        labor_deduct = 0.0 if q['labor_in_gop'] else q['labor_cost_annual']

        pbt = gop_net - dep - ptax - pins - mins - rent - debt - labor_deduct - (extra_cost if y < tr_years else 0)
        tax = max(0, pbt * q['tax_rate'])
        ni = pbt - tax
        cf = ni + dep
        yearly.append({
            'year': y + 1, 'stage': _stage(y),
            'drag_pct': round(drag * 100, 1),
            'adr': round(adr, 2), 'occ': round(occ * 100, 1),
            'room_revenue': round(rev['rooms'], 1), 'fnb_revenue': round(rev['fnb'], 1),
            'banq_revenue': round(rev['banq'], 1), 'other_dept_revenue': round(rev['other_dept'], 1),
            'misc_revenue': round(rev['misc'], 1),
            'total_revenue': round(rev['total'], 1),
            'non_room_revenue': round(rev['total'] - rev['rooms'], 1),
            'gop': round(gop, 1),
            'gop_rate': round(gop / rev['total'] * 100, 1),
            'brand_fees': round(brand_fees, 1),
            'brand_fee_rate': round(brand_fees / rev['total'] * 100, 1),
            'fee_base': round(fee_base, 1), 'fee_inc': round(fee_inc_pay, 1),
            'fee_mkt': round(fee_mkt, 1), 'fee_loy': round(fee_loy, 1),
            'fee_ffe': round(fee_ffe, 1), 'fee_tech': round(fee_tech, 1),
            'fee_roomrev': round(fee_roomrev, 1),
            'gop_net': round(gop_net, 1),
            'gop_net_rate': round(gop_net / rev['total'] * 100, 1),
            'depreciation': round(dep, 1), 'property_tax': round(ptax, 1),
            'insurance': round(pins + mins, 1), 'rent': round(rent, 1),
            'debt_service': round(debt, 1),
            'labor': q['labor_cost_annual'], 'labor_deducted': labor_deduct,
            'profit_before': round(pbt, 1), 'tax': round(tax, 1),
            'net_profit': round(ni, 1), 'cash_flow': round(cf, 1),
            'trevpar': round(rev['total'] * 10000 / arn, 1),   # 元/间 总收入
        })

    closure_loss = q['closure_months'] * q['closure_loss_monthly']
    # ⭐ 隐性成本一次性项：客源/会员迁移流失、品牌违约与关系修复等
    oneoff = q.get('transition_oneoff', 0.0)
    cfs = [-q['total_invest'] - closure_loss - oneoff] + [y['cash_flow'] for y in yearly]
    rate = q['discount_rate']
    irr = _irr_robust(cfs)
    npv_each = [cfs[0]] + [c / ((1 + rate) ** (i + 1)) for i, c in enumerate(cfs[1:])]
    npv = sum(npv_each)

    inc = {}
    base = q.get('baseline')
    if base:
        bq = dict(base); bq['horizon'] = H
        bc = calc_zongfu2(bq)
        base_cfs = bc['cash_flows']
        inc_cfs = [cfs[0] - base_cfs[0]] + [cfs[i + 1] - base_cfs[i + 1] for i in range(H)]
        r_irr = _irr_robust(inc_cfs)
        inc['base_cfs'] = base_cfs
        inc['inc_cfs'] = [round(c, 1) for c in inc_cfs]
        inc['cum_pos_yr'] = _cum_positive_year(inc_cfs)
        inc['inc_irr'] = None if (r_irr is None or r_irr <= -0.95 or r_irr > 3.0) else r_irr
        inc['inc_npv'] = sum([inc_cfs[0]] + [c / ((1 + rate) ** (i + 1)) for i, c in enumerate(inc_cfs[1:])])
        inc['inc_pb'] = E.calc_static_payback(inc_cfs)
        inc['base_annual_cf'] = sum(base_cfs[1:]) / float(H)
        inc['post_annual_cf'] = sum(cfs[1:]) / float(H)
        inc['annual_delta'] = inc['post_annual_cf'] - inc['base_annual_cf']
        inc['base_trevpar'] = bc['yearly'][1]['trevpar']
        inc['post_trevpar'] = yearly[1]['trevpar']
        inc['base_total_rev'] = bc['yearly'][1]['total_revenue']
        inc['post_total_rev'] = yearly[1]['total_revenue']
        inc['base_gop_net_rate'] = bc['yearly'][1]['gop_net_rate']
        inc['post_gop_net_rate'] = yearly[1]['gop_net_rate']
        inc['base_brand_fee_rate'] = bc['yearly'][1]['brand_fee_rate']
        inc['post_brand_fee_rate'] = yearly[1]['brand_fee_rate']

    return {
        'project_name': q.get('project_name', ''), 'scenario': q.get('scenario', ''),
        'params': q, 'yearly': yearly,
        'cash_flows': [round(c, 1) for c in cfs],
        'closure_loss': round(closure_loss, 1),
        'irr': round(irr * 100, 2) if (irr is not None and irr > -0.95 and irr <= 3.0) else None,
        'npv': round(npv, 1), 'npv_each': [round(x, 1) for x in npv_each],
        'cum_pos_yr': _cum_positive_year(cfs),
        'static_payback': E.calc_static_payback(cfs),
        'total_invest': q['total_invest'], 'rooms': rooms,
        'peak_adr': q['peak_adr'], 'peak_occ': q['peak_occ'],
        'tier_params': q['tier_params'], 'fees': fees, 'inc': inc,
    }


# ══════════════ 总府参数 ══════════════
# 现状（USALI 实测，近 24 个月月度）：客房 64.9% / 餐饮 13.4% / 会议 14.4% / 其他 7.3%
# 年化：客房约 4,000 万 / 总营收 6,374 万（2026 年化）
BASELINE = dict(
    project_name='总府皇冠 · 改造前基线(2026现状USALI)', scenario='基线',
    tier_params='intl_current_crowne',
    rooms=402, peak_adr=386.7, peak_occ=0.7078,
    ramp_type='flat', include_new_dep=False,
    total_invest=0, closure_months=0, closure_loss_monthly=0,
    building_value_existing=21949.0, building_depreciation_years=10,
    electromechanical_value=0.0,
    labor_in_gop=True, labor_cost_annual=2023.0,
    debt_service_annual=1785.0, rent_annual=0,
    discount_rate=0.08, tax_rate=0.25,
    # ⭐ 基线锚定实测经营毛利率（2026-09 实测 9.74%），已含未分配费用
    gop_measured_rate=0.0974,
)

# 方向 → tier + 情景
SCEN = {'保守': (0.85, -0.02, -0.03, 0.012), '中性': (1.00, 0.00, 0.00, 0.006), '乐观': (1.10, 0.02, 0.02, 0.003)}

PATHS = [
    ('d1a', '方向一A 保留皇冠·仅机电安全', 'intl_current_crowne', 402, 600, 0.72, 12, 14600, None),
    ('d1b', '方向一B 保留皇冠·机电+客房同窗', 'intl_current_crowne', 402, 620, 0.73, 15, 18400, None),
    ('d2', '方向二 换洲至奢选(3改2)', 'intl_upper_upscale', 268, 950, 0.76, 18, 32000, IHG_VIGNETTE),
    ('d3', '方向三 换外部奢牌(3改2)', 'intl_luxury', 268, 1450, 0.78, 21, 44000, None),
]


def build_presets():
    P = {}
    for key, name, tier, rooms, adr, occ, clm, inv, fo in PATHS:
        for sc, (dm, occ_d, mix_d, fee_d) in SCEN.items():
            t = dict(INTL[tier])
            t['mix'] = dict(t['mix'])
            for k in t['mix']:
                t['mix'][k] = max(0.01, t['mix'][k] + mix_d * (0.4 if k != 'rooms' else -0.9))
            t['fees'] = dict(t['fees'])
            for k in ('base', 'incentive', 'marketing', 'loyalty', 'ffe_reserve'):
                t['fees'][k] = max(0.0, t['fees'][k] + fee_d)
            p = dict(BASELINE)
            p.update(
                project_name=f"总府皇冠 · {name}", scenario=sc, tier_params=tier,
                rooms=rooms, peak_adr=adr * dm, peak_occ=min(0.90, occ + occ_d),
                non_room_ratio=1 - t['mix']['rooms'],
                closure_months=clm, total_invest=inv, include_new_dep=True,
                ramp_type='renovation',
                electromechanical_value=inv * 0.30,
                baseline=dict(BASELINE),
            )
            if key in ('d1a', 'd1b'):
                # 方向一保留皇冠：用改造后的部门效率（现状+改造达成），不用实测率
                p['gop_measured_rate'] = None
            else:
                p['gop_measured_rate'] = None
            p['_tier_override'] = t
            p['_fee_override'] = fo
            P[f"{key}_{sc}"] = p
    return P


def _prep(p):
    q = dict(p)
    if q.get('_tier_override'):
        t = q['_tier_override']
        q['tier_params'] = None
        q['_mix'] = t['mix']; q['_dept_gop'] = t['dept_gop']; q['_fees'] = t['fees']
    if q.get('_fee_override'):
        q['_fees'] = {**q['_fees'], **q['_fee_override']}
    return q


def _irr_robust(cfs):
    """稳健 IRR：区间扫描符号变化根，取经济意义根（|r| 最小）。
    ⭐ 替代引擎自带 bisection：首期巨额负现金流（投资+停业损失）时会产生
       570%/777% 这类假根，上会材料绝不能用。"""
    def npv(r):
        return sum(cf / (1.0 + r) ** i for i, cf in enumerate(cfs))
    grid = [-0.90, -0.60, -0.40, -0.30, -0.20, -0.10, -0.05, 0.0,
            0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.60, 0.80, 1.00, 1.50, 2.00, 3.00]
    roots = []
    prev_r, prev_v = grid[0], npv(grid[0])
    for r in grid[1:]:
        v = npv(r)
        if prev_v == 0:
            roots.append(prev_r)
        elif prev_v * v < 0:
            lo, hi, flo = prev_r, r, prev_v
            for _ in range(200):
                mid = (lo + hi) / 2
                fm = npv(mid)
                if abs(fm) < 1e-7:
                    lo = hi = mid
                    break
                if flo * fm < 0:
                    hi = mid
                else:
                    lo, flo = mid, fm
            roots.append((lo + hi) / 2)
        prev_r, prev_v = r, v
    return min(roots, key=abs) if roots else None


def _cum_positive_year(cfs):
    """累计现金流首次转正的年份（判断模型期内能否回本）"""
    cum = 0.0
    for i, cf in enumerate(cfs):
        cum += cf
        if cum >= 0 and i > 0:
            return i
    return None


_orig = calc_zongfu2


def calc_zongfu2(p):
    q = _prep(p)
    global INTL
    if q.get('tier_params') is None:
        # 临时注入自定义 tier
        tmp = '_tmp_custom'
        INTL[tmp] = dict(mix=q['_mix'], dept_gop=q['_dept_gop'], fees=q['_fees'])
        q['tier_params'] = tmp
        try:
            return _orig(q)
        finally:
            INTL.pop(tmp, None)
    return _orig(q)


if __name__ == '__main__':
    presets = build_presets()
    results = {}
    for k, p in presets.items():
        results[k] = calc_zongfu2(p)
    print("=" * 132)
    print(f"{'方案':<26}{'情景':<5}{'房':>4}{'ADR':>6}{'OCC':>5}{'客房收入':>9}{'总营收':>9}"
          f"{'TRevPAR':>9}{'GOP率':>7}{'品牌费率':>8}{'业主GOP':>9}{'年均CF':>9}{'增量NPV':>10}")
    print("=" * 132)
    for k, r in results.items():
        p = r['params']; y = r['yearly'][1]; inc = r['inc']
        print(f"{p['project_name'].replace('总府皇冠 · ',''):<26}{p['scenario']:<5}{p['rooms']:>4}"
              f"{p['peak_adr']:>6.0f}{p['peak_occ']*100:>5.0f}{y['room_revenue']:>9,.0f}{y['total_revenue']:>9,.0f}"
              f"{y['trevpar']:>9,.0f}{y['gop_rate']:>7.1f}{y['brand_fee_rate']:>8.1f}{y['gop_net']:>9,.0f}"
              f"{inc['post_annual_cf']:>9,.0f}{inc['inc_npv']:>10,.0f}")
    print("=" * 132)
    b = results['d2_中性']['inc']
    print(f"\n【改造前基线】客房 64.9% / 餐饮 13.4% / 会议 14.4% / 其他 7.3%（USALI 实测）")
    print(f"  年均经营现金流 {b['base_annual_cf']:,.0f} 万 ｜ 总营收 {b['base_total_rev']:,.0f} 万 "
          f"｜ TRevPAR {b['base_trevpar']:,.0f} 元/间 ｜ 业主GOP率 {b['base_gop_net_rate']:.1f}% "
          f"｜ 品牌费率 {b['base_brand_fee_rate']:.1f}%")
    for k in ('d1a', 'd1b', 'd2', 'd3'):
        r = results[f'{k}_中性']; i = r['inc']
        print(f"  {r['params']['project_name'].replace('总府皇冠 · ',''):<26} 总营收 {i['post_total_rev']:>9,.0f} 万 "
              f"｜ TRevPAR {i['post_trevpar']:>8,.0f} ｜ 年均CF {i['post_annual_cf']:>9,.0f} "
              f"｜ 增量 {i['annual_delta']:>8,.0f} ｜ 增量NPV {i['inc_npv']:>10,.0f}")
