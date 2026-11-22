# -*- coding: utf-8 -*-
"""
总府皇冠假日酒店改造 · 专用投资测算引擎 v1.0 (2026-11-03)

基于集团通用引擎 toolbox/hotel_irr_calc.py（v1.0，2026-10-24 校订版）扩展，
**不修改原引擎**，保持其 5 个既有 preset 结果可复现。

针对总府项目的 5 处扩展：
 1. mgmt_fee_rate        管理费/抽佣可调（方向二的价值主张：8-14% → 5.3-7.3%），从 GOP 前扣除
 2. gop_rate_gross       GOP 率拆为"管理费前"口径，gop_rate_gross - mgmt_fee_rate = 净 GOP 率
 3. closure_months /     停业期损失建模（Y0 与投资同期发生）
    closure_loss_monthly  （隐蔽工程整改必然停业，停业期综合损失 815 万/月）
 4. debt_service_annual  经营期贷款利息（引擎无此维度，存量贷款 1,785 万/年）
 5. building_value_existing + building_depreciation_years
                        存量房产评估值与改造投资分离（引擎原将 building_value 默认=总投×60%，
                        对存量物业是错的；房产税与折旧均按存量房产原值计）
 6. ramp_type='renovation' 改造项目专用爬坡：开业即近成熟（爬坡期已在停业期消耗）

口径纪律（承接国堰校订）：
 - labor_in_gop=True  → GOP 已含人工，利润端不重复计扣
 - 停业期保留人工 1,312 万/年 属停业期损失，**不是**经营期人工，不得进利润端
 - 奖励管理费并入 mgmt_fee_rate，不再单独硬编码 6%
"""
import io, sys, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\toolbox")
import hotel_irr_calc as E

# ---- 改造项目专用爬坡曲线：Y1 即近成熟（软开业 3 个月 = 0.95）----
RAMP_RENOVATION = {
    'adr': [0.95, 1.00, 1.00, 1.00, 1.00, 0.98, 0.96, 0.93, 0.91, 0.89],
    'occ': [0.90, 1.00, 1.00, 1.00, 1.00, 0.98, 0.96, 0.93, 0.90, 0.87],
}
E.RAMP_CURVES['renovation'] = RAMP_RENOVATION
# ⭐ 基线专用：在营存量酒店，无新店爬坡期（每年按年化值持平）
E.RAMP_CURVES['flat'] = {'adr': [1.0] * 10, 'occ': [1.0] * 10}

STAGES = ['爬坡', '成熟', '峰值', '峰值', '稳定', '微降', '微降', '回落', '回落', '回升']


def calc_zongfu(p):
    """总府专用项目测算。返回与引擎同构的结果字典（供 assess_verdict / write_excel_report 复用）。"""
    q = dict(p)
    q.setdefault('discount_rate', 0.08)
    q.setdefault('tax_rate', 0.25)
    q.setdefault('labor_in_gop', True)          # GOP 已含人工
    q.setdefault('building_depreciation_years', 10)
    q.setdefault('debt_service_annual', 0)
    q.setdefault('closure_months', 0)
    q.setdefault('closure_loss_monthly', 0)
    q.setdefault('mgmt_fee_rate', 0.06)         # 引擎原硬编码 6% 奖励管理费
    q.setdefault('rent_annual', 0)

    rooms = q['rooms']
    ramp = E.RAMP_CURVES[q['ramp_type']]
    days = 365
    arn = rooms * days
    gop_gross_rate = q['gop_rate_gross']
    mf = q['mgmt_fee_rate']

    bv_existing = q.get('building_value_existing') or (q['total_invest'] * 0.60)
    emv = q.get('electromechanical_value') or (q['total_invest'] * 0.25)
    bld_dep_years = q['building_depreciation_years']

    yearly = []
    for y in range(10):
        adr_y = q['peak_adr'] * ramp['adr'][y]
        occ_y = q['peak_occ'] * ramp['occ'][y]
        room_rev = adr_y * occ_y * arn / 10000.0
        tot_rev = room_rev / (1 - q['non_room_ratio'])
        gop_gross = tot_rev * gop_gross_rate
        mgmt_fee = gop_gross * mf               # 管理费从 GOP 前扣（方向二核心）
        gop_net = gop_gross - mgmt_fee

        # 折旧：存量房产原值 + 改造新增资产（改造投资按 10 年摊）
        # ⭐ 改造后利润端折旧 = 存量折旧 + 改造新增折旧；基线只有存量折旧 → 增量口径自然分离
        dep_exist = bv_existing / min(bld_dep_years, 10) if bld_dep_years else 0
        dep_new = (q['total_invest'] / 10.0) if q.get('include_new_dep', True) else 0.0
        dep = dep_exist + dep_new
        ptax = bv_existing * 0.7 * 0.012
        pins = (bv_existing + q['total_invest']) * 0.00035
        mins = emv * 0.00045
        rent = q.get('rent_annual', 0)
        debt = q['debt_service_annual']
        labor_deduct = 0.0 if q['labor_in_gop'] else q['labor_cost_annual']

        pbt = gop_net - dep - ptax - pins - mins - rent - debt - labor_deduct
        tax = max(0, pbt * q['tax_rate'])
        ni = pbt - tax
        cf = ni + dep
        yearly.append({
            'year': y + 1, 'stage': STAGES[y],
            'adr': round(adr_y, 2), 'occ': round(occ_y * 100, 1),
            'room_revenue': round(room_rev, 1), 'total_revenue': round(tot_rev, 1),
            'non_room_revenue': round(tot_rev - room_rev, 1),
            'gop': round(gop_gross, 1), 'gop_rate': round(gop_gross_rate * 100, 1),
            'incentive_mgmt': round(mgmt_fee, 1), 'mgmt_fee_rate': round(mf * 100, 1),
            'gop_net': round(gop_net, 1),
            'gop_net_rate': round((gop_net / tot_rev) * 100, 1),
            'depreciation': round(dep, 1), 'property_tax': round(ptax, 1),
            'insurance': round(pins + mins, 1), 'rent': round(rent, 1),
            'debt_service': round(debt, 1),
            'labor': q['labor_cost_annual'], 'labor_deducted': labor_deduct,
            'profit_before': round(pbt, 1), 'tax': round(tax, 1), 'net_profit': round(ni, 1),
            'cash_flow': round(cf, 1),
        })

    closure_loss = q['closure_months'] * q['closure_loss_monthly']
    cfs = [-q['total_invest'] - closure_loss] + [y['cash_flow'] for y in yearly]
    irr = E.calc_irr(cfs)
    pb = E.calc_static_payback(cfs)
    rate = q['discount_rate']
    npv_each = [cfs[0]] + [c / ((1 + rate) ** (i + 1)) for i, c in enumerate(cfs[1:])]
    npv = sum(npv_each)
    dp = E.calc_dynamic_payback(cfs, rate)

    # ============ ⭐ 增量口径（决策正确口径）============
    # 改造前基线：同一资产口径（同样的存量折旧/房产税/利息），不做改造
    # ⭐ 关键：总府改造前经营现金流本身为负，全口径 IRR 会把存量资产的亏损算进分子，
    #    导致"改造不划算"的错误结论。决策必须看增量。
    inc = {}
    base = q.get('baseline')
    if base:
        bc = calc_zongfu(base)
        base_cfs = bc['cash_flows']
        inc_cfs = [cfs[0] - base_cfs[0]] + [cfs[i + 1] - base_cfs[i + 1] for i in range(10)]
        r_irr = E.calc_irr(inc_cfs)
        inc['base_cfs'] = base_cfs
        inc['inc_cfs'] = [round(c, 1) for c in inc_cfs]
        inc['inc_irr'] = None if (r_irr is not None and r_irr <= -0.999) else r_irr
        inc['inc_npv'] = sum([inc_cfs[0]] + [c / ((1 + rate) ** (i + 1)) for i, c in enumerate(inc_cfs[1:])])
        inc['inc_pb'] = E.calc_static_payback(inc_cfs)
        inc['inc_dp'] = E.calc_dynamic_payback(inc_cfs, rate)
        inc['base_irr'] = bc['irr']
        inc['base_annual_cf'] = sum(base_cfs[1:]) / 10.0
        inc['post_annual_cf'] = sum(cfs[1:]) / 10.0
        inc['annual_delta'] = inc['post_annual_cf'] - inc['base_annual_cf']
        inc['base_cf'] = base_cfs[2]
        inc['post_cf'] = cfs[2]
    res = {
        'project_name': q.get('project_name', ''),
        'scenario': q.get('scenario', ''),
        'params': q,
        'yearly': yearly,
        'cash_flows': [round(c, 1) for c in cfs],
        'closure_loss': round(closure_loss, 1),
        'irr': round(irr * 100, 2) if irr is not None else None,
        'npv': round(npv, 1),
        'npv_each': [round(x, 1) for x in npv_each],
        'static_payback': pb,
        'dynamic_payback': dp,
        'total_invest': q['total_invest'],
        'rooms': rooms,
        'peak_adr': q['peak_adr'],
        'peak_occ': q['peak_occ'],
        'gop_rate_gross': gop_gross_rate,
        'mgmt_fee_rate': mf,
        'inc': inc,
    }
    try:
        res['verdict'] = E.assess_verdict(res['irr'], pb, q)
    except Exception:
        res['verdict'] = {}
    return res


# ======================= 总府 9 组 PRESETS（3 方向/方案 × 3 情景）=======================
# 实测基线（第一批次 125 份）：
#   月均营收 531 万；停业期综合损失 815 万/月；经营期人工已含在 GOP 内
#   停业期保留人工 1,312 万/年（业主已测算）｜存量贷款利息 1,785 万/年
#   客房 402 间（物理 415）｜客房总面积 10,192 ㎡｜均 25.35 ㎡
# 存量房产评估值参照：华安锦江 21 个酒店资产单房价值均值 54.6 万/间 → 402 间 ≈ 21,949 万
#   ⚠️ 参照值，须以正式评估报告替换（国资委口径关键变量）

COMMON = dict(
    project_type='renovation', ramp_type='renovation', discount_rate=0.08, tax_rate=0.25,
    labor_in_gop=True, labor_cost_annual=2023.0,        # 经营期人工（仅记录，不重复扣）
    rent_annual=0, debt_service_annual=1785.0,          # 存量贷款利息
    building_value_existing=21949.0,                     # ⚠️ 参照值待评估替换
    building_depreciation_years=10,
    electromechanical_value=None,
    closure_loss_monthly=815.0,
)

SCEN = {  # 情景: (adr_delta, occ, gop_gross, mgmt_fee)
    '保守': (0.85, 0.74, -0.03, 0.12),
    '中性': (1.00, 0.76, 0.00, 0.06),
    '乐观': (1.10, 0.78, 0.02, 0.03),
}

PATHS = [
    # key, 名称, 房量, 峰值ADR, 峰值OCC, 非房比, GOP前率, 抽佣率, 停业月, 总投资(万), 客房/公区结构
    ('d1a', '方向一A 仅机电安全+开业后滚动', 402, 600, 0.72, 0.37, 0.22, 0.11, 12, 14600),
    ('d1b', '方向一B 机电+客房同窗(推荐)', 402, 620, 0.73, 0.37, 0.23, 0.11, 15, 18400),
    ('d2', '方向二 换洲至奢选(3改2)', 268, 950, 0.76, 0.40, 0.34, 0.063, 18, 32000),
    ('d3', '方向三 换外部奢牌(3改2更激进)', 268, 1450, 0.78, 0.46, 0.36, 0.09, 21, 44000),
]


# 改造前基线（2026 现状实测）：同一资产口径
BASELINE = dict(
    project_name='总府皇冠 · 改造前基线(2026现状)',
    scenario='基线',
    rooms=402, peak_adr=386.7, peak_occ=0.7078, non_room_ratio=0.37,
    gop_rate_gross=0.0974, mgmt_fee_rate=0.11,      # 现状经营毛利率 9.74%；抽佣 8-14% 中值 11%
    total_invest=0, closure_months=0, closure_loss_monthly=0,
    ramp_type='flat', include_new_dep=False,
    building_value_existing=21949.0, building_depreciation_years=10,
    electromechanical_value=0.0,
    labor_in_gop=True, labor_cost_annual=2023.0,
    debt_service_annual=1785.0, rent_annual=0,
    discount_rate=0.08, tax_rate=0.25,
)


def build_presets():
    P = {}
    for key, name, rooms, adr, occ, nrr, gopg, mf, clm, inv in PATHS:
        for sc, (dm, occ_s, gop_d, mf_d) in SCEN.items():
            p = dict(COMMON)
            p.update(
                project_name=f"总府皇冠 · {name}",
                scenario=sc,
                rooms=rooms,
                peak_adr=adr * dm,
                peak_occ=occ_s,
                non_room_ratio=nrr,
                gop_rate_gross=max(0.05, gopg + gop_d),
                mgmt_fee_rate=mf + mf_d,
                closure_months=clm,
                total_invest=inv,
                include_new_dep=True,
            )
            p['electromechanical_value'] = inv * 0.30
            p['baseline'] = dict(BASELINE)
            P[f"{key}_{sc}"] = p
    return P


def sensitivity(key, sc='中性'):
    """ADR × OCC 双向敏感性（对总府口径）：IRR 表。"""
    base = build_presets()[f"{key}_{sc}"]
    adrs = [base['peak_adr'] * m for m in (0.85, 0.925, 1.0, 1.075, 1.15)]
    occs = [base['peak_occ'] - 0.06, base['peak_occ'] - 0.03, base['peak_occ'],
            base['peak_occ'] + 0.03, base['peak_occ'] + 0.06]
    rows = []
    for a in adrs:
        r = []
        for o in occs:
            p = dict(base); p['peak_adr'] = a; p['peak_occ'] = o
            res = calc_zongfu(p)
            r.append(res['irr'])
        rows.append(r)
    return adrs, occs, rows


def sens_critical(key='d2', sc='中性'):
    """⭐ 关键未知量敏感性：存量房产评估值 × 存量贷款利息
    这两个是"改造前经营现金流为负"这一核心结论的最大变量。"""
    base = build_presets()[f"{key}_{sc}"]
    bvs = [15000.0, 21949.0, 30000.0]
    debts = [1000.0, 1785.0, 2600.0]
    out = []
    for bv in bvs:
        row = []
        for d in debts:
            p = dict(base); p['building_value_existing'] = bv; p['debt_service_annual'] = d
            p['baseline'] = dict(BASELINE)
            p['baseline']['building_value_existing'] = bv
            p['baseline']['debt_service_annual'] = d
            r = calc_zongfu(p)
            row.append((round(r['inc']['base_annual_cf'], 1),
                        round(r['inc']['post_annual_cf'], 1),
                        round(r['inc']['annual_delta'], 1),
                        round(r['inc']['inc_npv'], 0),
                        (r['inc']['inc_pb'] or '>10年')))
        out.append(row)
    return bvs, debts, out


def write_excel(all_res, path):
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    wb = openpyxl.Workbook()
    HDR = PatternFill('solid', fgColor='1F3864')
    HDRF = Font(name='微软雅黑', size=10, bold=True, color='FFFFFF')
    BD = Font(name='微软雅黑', size=10)
    BOLD = Font(name='微软雅黑', size=10, bold=True)
    OK = PatternFill('solid', fgColor='C6EFCE')
    BAD = PatternFill('solid', fgColor='FFC7CE')
    MID = PatternFill('solid', fgColor='FFEB9C')
    thin = Side(style='thin', color='BFBFBF')
    BD2 = Border(left=thin, right=thin, top=thin, bottom=thin)

    def style_header(ws, row=1, ncol=12):
        for c in range(1, ncol + 1):
            cell = ws.cell(row, c); cell.fill = HDR; cell.font = HDRF
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = BD2

    # ---- S1 汇总 ----
    ws = wb.active; ws.title = '汇总对比'
    ws['A1'] = '总府皇冠假日酒店改造 · 三方向九情景测算汇总（口径③ 全口径）'
    ws['A1'].font = Font(name='微软雅黑', size=13, bold=True, color='1F3864')
    ws['A2'] = '数据：业主第一批次实测 125 份 + 洲际沟通 + 合作方清单口径② ｜ 引擎：hotel_irr_calc_zongfu v1.0（2026-11-03）'
    ws['A2'].font = Font(name='微软雅黑', size=9, color='808080')
    hdr = ['方案', '情景', '房量', '峰值ADR', '峰值OCC', 'GOP前率', '抽佣率', '停业月',
           '总投资(万)', '停业损失(万)', '全口径IRR(%)', '全口径NPV@8%(万)', '全口径回收期(年)',
           '⭐增量IRR(%)', '⭐增量NPV@8%(万)', '⭐增量回收期(年)', '年均现金流增量(万)', '改造前年均CF(万)']
    for i, h in enumerate(hdr, 1):
        ws.cell(4, i, h)
    style_header(ws, 4, len(hdr))
    r = 5
    for key, res in all_res.items():
        p = res['params']
        inc = res.get('inc', {})
        ii = inc.get('inc_irr')
        vals = [p['project_name'].replace('总府皇冠 · ', ''), p['scenario'], p['rooms'],
                round(p['peak_adr'], 1), round(p['peak_occ'] * 100, 1),
                round(p['gop_rate_gross'] * 100, 1), round(p['mgmt_fee_rate'] * 100, 1),
                p['closure_months'], p['total_invest'], res['closure_loss'],
                res['irr'], res['npv'], res['static_payback'],
                round(ii * 100, 2) if ii is not None else 'n/a',
                round(inc.get('inc_npv', 0), 1),
                round(inc.get('inc_pb'), 1) if inc.get('inc_pb') else '不回本',
                round(inc.get('annual_delta', 0), 1),
                round(inc.get('base_annual_cf', 0), 1)]
        for i, v in enumerate(vals, 1):
            c = ws.cell(r, i, v); c.font = BD; c.border = BD2
            if i in (11, 14) and isinstance(v, (int, float)):
                c.fill = OK if v >= 8 else (MID if v >= 3.5 else BAD)
            if i == 14:
                c.font = BOLD
        r += 1
    for i, w in enumerate([30, 8, 8, 11, 10, 11, 10, 9, 13, 13, 13, 15, 15, 12, 14, 14, 15, 15], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = 'A5'

    # ---- S2 十年测算明细（每方案一表） ----
    for key, res in all_res.items():
        if res['params']['scenario'] != '中性':
            continue
        ws = wb.create_sheet(res['params']['project_name'].replace('总府皇冠 · ', '')[:30])
        ws['A1'] = res['params']['project_name'] + ' · 十年现金流'
        ws['A1'].font = Font(name='微软雅黑', size=12, bold=True, color='1F3864')
        ws['A2'] = (f"停业 {res['params']['closure_months']} 月 · 停业损失 {res['closure_loss']:,.0f} 万 · "
                    f"总投资 {res['params']['total_invest']:,.0f} 万 · 抽佣 {res['params']['mgmt_fee_rate']*100:.1f}% · "
                    f"GOP前 {res['params']['gop_rate_gross']*100:.1f}%")
        ws['A2'].font = Font(name='微软雅黑', size=9, color='808080')
        cols = ['年', '阶段', 'ADR', 'OCC%', '客房收入', '非房收入', '总营收', 'GOP', '管理费',
                '净GOP', '折旧', '房产税', '保险', '贷款利息', '税前利润', '所得税', '净利润', '现金流', '折现现金流']
        for i, h in enumerate(cols, 1):
            ws.cell(4, i, h)
        style_header(ws, 4, len(cols))
        ws.cell(5, 1, 'Y0'); ws.cell(5, 2, '投资+停业')
        ws.cell(5, 18, -res['params']['total_invest'] - res['closure_loss'])
        ws.cell(5, 19, -res['params']['total_invest'] - res['closure_loss'])
        for c in (1, 2, 18, 19):
            ws.cell(5, c).font = BOLD; ws.cell(5, c).fill = PatternFill('solid', fgColor='F2F2F2')
        rr = 6
        for y in res['yearly']:
            vals = [f"Y{y['year']}", y['stage'], y['adr'], y['occ'], y['room_revenue'],
                    y['non_room_revenue'], y['total_revenue'], y['gop'], y['incentive_mgmt'],
                    y['gop_net'], y['depreciation'], y['property_tax'], y['insurance'],
                    y['debt_service'], y['profit_before'], y['tax'], y['net_profit'],
                    y['cash_flow'], res['npv_each'][rr - 5]]
            for i, v in enumerate(vals, 1):
                c = ws.cell(rr, i, v); c.font = BD; c.border = BD2
            rr += 1
        ws.cell(rr + 1, 2, 'IRR').font = BOLD
        ws.cell(rr + 1, 3, f"{res['irr']}%").font = BOLD
        ws.cell(rr + 2, 2, 'NPV@8%').font = BOLD
        ws.cell(rr + 2, 3, f"{res['npv']:,.0f} 万").font = BOLD
        ws.cell(rr + 3, 2, '静态回收期').font = BOLD
        ws.cell(rr + 3, 3, f"{res['static_payback']} 年").font = BOLD
        ws.cell(rr + 4, 2, '动态回收期@8%').font = BOLD
        ws.cell(rr + 4, 3, f"{res['dynamic_payback']} 年").font = BOLD
        for i in range(1, len(cols) + 1):
            ws.column_dimensions[get_column_letter(i)].width = 11
        ws.column_dimensions['A'].width = 7
        ws.column_dimensions['B'].width = 9

    # ---- S3 敏感性（ADR × OCC → IRR） ----
    for key, name, *_ in PATHS:
        ws = wb.create_sheet(f'敏感性_{name[:18]}')
        adrs, occs, rows = sensitivity(key)
        ws['A1'] = f'{name} · IRR 敏感性（中性情景基准，ADR × OCC）'
        ws['A1'].font = Font(name='微软雅黑', size=12, bold=True, color='1F3864')
        ws['A2'] = '国资门槛：IRR ≥ 3.5% 最低 / 8% 合理（绿=达标 / 黄=过底线 / 红=不达标）'
        ws['A2'].font = Font(name='微软雅黑', size=9, color='808080')
        ws['A4'] = 'ADR \\ OCC'
        for j, o in enumerate(occs, 2):
            ws.cell(4, j, f"{o*100:.0f}%")
        for i, a in enumerate(adrs, 5):
            ws.cell(i, 1, f"¥{a:.0f}")
        for i, a in enumerate(adrs, 5):
            for j, o in enumerate(occs, 2):
                v = rows[i - 5][j - 2]
                c = ws.cell(i, j, v if v is not None else 'n/a')
                c.font = BD; c.border = BD2
                if isinstance(v, (int, float)):
                    c.fill = OK if v >= 8 else (MID if v >= 3.5 else BAD)
        style_header(ws, 4, 6)
        for c in range(1, 7):
            ws.cell(4, c).fill = HDR; ws.cell(4, c).font = HDRF
        ws.column_dimensions['A'].width = 14
        for j in range(2, 7):
            ws.column_dimensions[get_column_letter(j)].width = 12

    # ---- S4 参数表 ----
    ws = wb.create_sheet('参数与口径')
    ws['A1'] = '参数表与口径说明'
    ws['A1'].font = Font(name='微软雅黑', size=13, bold=True, color='1F3864')
    rows = [
        ('项', '值', '来源/等级'),
        ('客房数（在售）', '402 间（物理 415）', '🟢 第一批次实测'),
        ('客房总面积 / 均面积', '10,192 ㎡ / 25.35 ㎡', '🟢 实测（作废旧口径 15.8 ㎡）'),
        ('月均营收', '531 万', '🟢 实测 2026'),
        ('年化营收', '6,374 万', '🟢 实测'),
        ('停业期综合损失', '815 万/月（固定 284 + 收入损失 531）', '🟢+🟠'),
        ('停业期保留人工', '1,312 万/年（52 人）', '🟢 业主已测算 —— 属停业期损失，不进利润端'),
        ('存量贷款利息', '1,785 万/年', '🟢 实测（改造后新增融资利息待定）'),
        ('经营期人工', '约 2,023 万/年', '🟢 实测年化 —— 已含在 GOP 内（labor_in_gop=True）'),
        ('存量房产评估值', '21,949 万（参照）', '⚠️ 华安锦江单房价值均值 54.6 万×402 —— 须以正式评估报告替换'),
        ('折现率', '8%', '集团标准'),
        ('税率', '25%', '法定'),
        ('爬坡曲线', 'renovation（Y1 0.95/0.90 → Y2 即成熟）', '改造项目专用：爬坡期已在停业期消耗'),
        ('管理费口径', '从 GOP 前按 mgmt_fee_rate 扣', '⭐ 方向二核心：8-14% → 5.3-7.3%'),
        ('GOP 口径', 'gop_rate_gross（管理费前）', '与通用模版"综合 GOP 率"口径不同，已拆开'),
        ('房屋折旧', 'building_value_existing / 10', '存量房产原值，非改造投资'),
        ('房产税', '存量房产原值 × 70% × 1.2%', '从价计征'),
        ('国资门槛', 'IRR ≥ 3.5% 最低 / 8% 合理', '集团通用模版"快速判定流程"'),
        ('静态回收期参考', '6–8 年为合理区间', '同上'),
    ]
    for i, rw in enumerate(rows, 1):
        for j, v in enumerate(rw, 1):
            c = ws.cell(i, j, v); c.font = BOLD if i == 1 else BD; c.border = BD2
            if i == 1:
                c.fill = HDR; c.font = HDRF
    for i, w in enumerate([22, 44, 46], 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    # ---- S5 关键未知量敏感性（存量房产评估值 × 存量贷款利息） ----
    ws = wb.create_sheet('敏感性_关键未知量')
    ws['A1'] = '⭐ 关键未知量敏感性（方向二中性）：存量房产评估值 × 存量贷款利息'
    ws['A1'].font = Font(name='微软雅黑', size=13, bold=True, color='1F3864')
    ws['A2'] = ('每个单元格：改造前年均CF / 改造后年均CF / 增量 / 增量NPV@8% / 增量回收期（年）'
                '　⚠️ 存量房产评估值目前为参照值（华安锦江单房价值均值 54.6 万×402），须以正式评估报告替换')
    ws['A2'].font = Font(name='微软雅黑', size=9, color='C00000')
    bvs, debts, rows5 = sens_critical('d2', '中性')
    r0 = 4
    ws.cell(r0, 1, '存量房产评估值 ＼ 存量贷款利息(万/年)').font = BOLD
    for j, d in enumerate(debts, 2):
        c = ws.cell(r0, j, f"{d:,.0f}"); c.font = HDRF; c.fill = HDR
        c.alignment = Alignment(horizontal='center')
    ws.cell(r0, 1).fill = HDR; ws.cell(r0, 1).font = HDRF
    for i, bv in enumerate(bvs, 1):
        ws.cell(r0 + i, 1, f"{bv:,.0f} 万").font = BOLD
        for j, d in enumerate(debts, 2):
            bcf, pcf, dlt, npv, pb = rows5[i - 1][j - 2]
            c = ws.cell(r0 + i, j, f"{bcf:,.0f} / {pcf:,.0f} / {dlt:,.0f} / {npv:,.0f} / {pb}")
            c.font = BD; c.border = BD2
            if isinstance(pcf, (int, float)):
                c.fill = OK if pcf > 0 else (MID if pcf > -800 else BAD)
    for j, w in enumerate([30, 34, 34, 34], 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    r1 = r0 + len(bvs) + 2
    ws.cell(r1, 1, '读法').font = BOLD
    ws.cell(r1 + 1, 1, '① 改造前年均经营现金流为负 —— 即酒店现在每年净流出现金，改造的本质是"止血 + 增值"，不是"投资赚钱"')
    ws.cell(r1 + 2, 1, '② 评估值越高、利息越高 → 改造前亏得越多 → 改造的"止血价值"越大（增量口径）')
    ws.cell(r1 + 3, 1, '③ 但增量 NPV 在所有格子里仍为负 → 纯财务口径不成立 → 必须走国资口径的"必要性 + 评估增值率 + 评估增值"路径')
    for k in range(1, 5):
        ws.cell(r1 + k, 1).font = BD
        ws.cell(r1 + k, 1).alignment = Alignment(wrap_text=True, vertical='top')

    wb.save(path)
    return path


if __name__ == '__main__':
    OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\总府皇冠改造_投资测算表_三方向九情景_v1.0_2026-11-03.xlsx"
    presets = build_presets()
    results = {}
    for k, p in presets.items():
        results[k] = calc_zongfu(p)
    print("=" * 108)
    print(f"{'方案':<34}{'情景':<6}{'房':>5}{'ADR':>7}{'OCC':>6}{'GOP前':>7}{'抽佣':>6}"
          f"{'停业月':>7}{'投资(万)':>11}{'IRR':>8}{'NPV@8%':>10}{'回收期':>8}")
    print("=" * 108)
    for k, res in results.items():
        p = res['params']
        inc = res.get('inc', {})
        ii = inc.get('inc_irr')
        ii_s = f"{ii*100:.2f}%" if ii is not None else "n/a"
        ipb = inc.get('inc_pb')
        ipb_s = f"{ipb:.1f}" if ipb else "n/a"
        print(f"{p['project_name'].replace('总府皇冠 · ',''):<28}{p['scenario']:<4}{p['rooms']:>5}"
              f"{p['peak_adr']:>6.0f}{p['peak_occ']*100:>5.0f}{p['gop_rate_gross']*100:>6.1f}"
              f"{p['mgmt_fee_rate']*100:>6.1f}{p['closure_months']:>4}{p['total_invest']:>9,}"
              f" | 增量IRR {ii_s:>9} 增量NPV {inc.get('inc_npv',0):>9,.0f} 增量回收 {ipb_s:>6}"
              f" 年均CF增量 {inc.get('annual_delta',0):>8,.0f} 改造前年均CF {inc.get('base_annual_cf',0):>8,.0f}")
    print("=" * 108)
    path = write_excel(results, OUT)
    print("\nExcel 已生成:", path, f"({os.path.getsize(path)/1024:.1f} KB, {len(results)} 组结果)")
    # 敏感性摘要
    for key, name, *_ in PATHS:
        adrs, occs, rows_ = sensitivity(key)
        vals = [v for r in rows_ for v in r if isinstance(v, (int, float))]
        print(f"[敏感性] {name[:26]:<28} IRR 区间 {min(vals):.2f}% ~ {max(vals):.2f}%")
    bvs, debts, rows5 = sens_critical('d2', '中性')
    print("\n[关键未知量敏感性 · 方向二中性] 存量房产评估值(行) × 存量贷款利息(列)")
    print("        单元: 改造前年均CF / 改造后年均CF / 增量 / 增量NPV / 增量回收期")
    for i, bv in enumerate(bvs):
        print(f"  评估值 {bv:>7,.0f} 万 |", " | ".join(
            f"{a:,.0f}/{b:,.0f}/{c:,.0f}/{d:,.0f}/{e}" for a, b, c, d, e in rows5[i]))
