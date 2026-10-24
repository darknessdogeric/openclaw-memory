# -*- coding: utf-8 -*-
"""
hotel_irr_calc.py — 酒店投资测算自动化脚本（按集团通用模版 v1.0 口径）

输入：参数表（Python dict / JSON 文件）
输出：含 9 表结构的 Excel 报表

口径：通用模版 v1.0（丽苑 6-12 楼 + Eric 2026-09-28 指令）
- 折旧：12 类资产，10 年逐年
- 房产税：投资额 × 70% × 1.2%
- 财产保险：投资额 × 0.035%
- 机器损坏险：机电原值 × 0.045%
- 客房直接成本率 30.5%（低耗3.5% + 能耗7% + 洗涤3% + 维修3% + 销售3% + OTA8% + 管理3%）
- 非房直接成本率 40%
- 未分配：行政8% + 市场3% + 维修3% + 基本管理2%
- 奖励管理费 GOP × 6%
- 爬坡：Y1/Y2/Y3-5/Y6-7/Y8-10 五段

用法：
    from hotel_irr_calc import calc_hotel_project, write_excel_report
    result = calc_hotel_project(params)
    write_excel_report(result, 'output.xlsx')

作者：B166ER · 2026-10-07
"""
import json, math, io, sys
from datetime import datetime

# ========== 参数库（20 类酒店分级基准，参照通用模版 v1.0） ==========
BENCHMARK = {
    'luxury': {'adr':1800, 'occ':0.62, 'room_size':55, 'unit_invest':150, 'non_room':0.45, 'gop_rate':0.30, 'tier':'奢华'},
    '5star_full': {'adr':900, 'occ':0.65, 'room_size':45, 'unit_invest':90, 'non_room':0.40, 'gop_rate':0.32, 'tier':'五星全服务'},
    '5star_business': {'adr':800, 'occ':0.68, 'room_size':42, 'unit_invest':80, 'non_room':0.38, 'gop_rate':0.34, 'tier':'五星商务'},
    '4star_full': {'adr':600, 'occ':0.68, 'room_size':36, 'unit_invest':55, 'non_room':0.33, 'gop_rate':0.36, 'tier':'四星全服务'},
    '4star_business': {'adr':520, 'occ':0.70, 'room_size':32, 'unit_invest':45, 'non_room':0.30, 'gop_rate':0.38, 'tier':'四星商务'},
    'upscale_full': {'adr':480, 'occ':0.72, 'room_size':30, 'unit_invest':35, 'non_room':0.28, 'gop_rate':0.40, 'tier':'中高端全服务'},
    'upscale_select': {'adr':450, 'occ':0.75, 'room_size':28, 'unit_invest':28, 'non_room':0.20, 'gop_rate':0.44, 'tier':'中高端精选'},
    'mid_chain': {'adr':350, 'occ':0.78, 'room_size':25, 'unit_invest':18, 'non_room':0.12, 'gop_rate':0.50, 'tier':'中端连锁'},
    'mid_lifestyle': {'adr':380, 'occ':0.76, 'room_size':26, 'unit_invest':22, 'non_room':0.15, 'gop_rate':0.48, 'tier':'中端生活'},
    'economy': {'adr':200, 'occ':0.80, 'room_size':20, 'unit_invest':10, 'non_room':0.05, 'gop_rate':0.58, 'tier':'经济型'},
    'boutique': {'adr':750, 'occ':0.68, 'room_size':38, 'unit_invest':70, 'non_room':0.35, 'gop_rate':0.35, 'tier':'精品'},
    'cultural': {'adr':600, 'occ':0.70, 'room_size':32, 'unit_invest':45, 'non_room':0.30, 'gop_rate':0.38, 'tier':'文化主题'},
    'resort_full': {'adr':950, 'occ':0.62, 'room_size':45, 'unit_invest':95, 'non_room':0.42, 'gop_rate':0.30, 'tier':'度假全服务'},
    'resort_boutique': {'adr':1100, 'occ':0.60, 'room_size':50, 'unit_invest':120, 'non_room':0.40, 'gop_rate':0.32, 'tier':'度假精品'},
    'mice': {'adr':700, 'occ':0.65, 'room_size':40, 'unit_invest':75, 'non_room':0.45, 'gop_rate':0.33, 'tier':'会议会展'},
}

# ========== 5 类爬坡曲线（ADR / OCC 系数） ==========
RAMP_CURVES = {
    'business': {
        'adr': [0.88, 0.94, 1.00, 1.00, 1.00, 0.98, 0.96, 0.93, 0.91, 0.89],
        'occ': [0.85, 0.92, 1.00, 1.00, 1.00, 0.98, 0.96, 0.93, 0.90, 0.87],
    },
    'resort': {
        'adr': [0.80, 0.90, 0.97, 1.00, 1.00, 0.99, 0.97, 0.95, 0.93, 0.91],
        'occ': [0.70, 0.85, 0.95, 1.00, 1.00, 0.98, 0.96, 0.94, 0.92, 0.90],
    },
    'cultural': {
        'adr': [0.75, 0.86, 0.95, 1.00, 1.00, 0.98, 0.96, 0.93, 0.90, 0.87],
        'occ': [0.65, 0.80, 0.93, 1.00, 1.00, 0.97, 0.94, 0.90, 0.86, 0.83],
    },
    'mice': {
        'adr': [0.85, 0.92, 0.98, 1.00, 1.00, 0.99, 0.97, 0.95, 0.93, 0.91],
        'occ': [0.85, 0.92, 1.00, 1.00, 1.00, 0.98, 0.96, 0.93, 0.90, 0.87],
    },
    'limited_service': {
        'adr': [0.90, 0.95, 1.00, 1.00, 1.00, 0.98, 0.96, 0.94, 0.92, 0.90],
        'occ': [0.90, 0.95, 1.00, 1.00, 1.00, 0.98, 0.96, 0.94, 0.92, 0.90],
    },
}

# ========== 12 类资产折旧表 ==========
DEPRECIATION = [
    ('房屋建筑物', 30, 20),
    ('机器设备_机电', 15, 10),
    ('智能化系统', 8, None),
    ('装饰装修', 10, 5),
    ('家具器具_FFE', 8, 5),
    ('运营物资_OSE', 5, None),
    ('厨房洗衣设备', 10, 5),
    ('IT系统', 5, 3),
    ('前期费用摊销', 5, None),
    ('开办及营销', 5, None),
    ('不可预见费', 20, None),
    ('土地', 0, None),
]


def calc_depreciation_annual(asset_value, life):
    """年折旧（直线法，10 年内逐年计提）"""
    if life == 0 or asset_value == 0:
        return 0
    return asset_value / min(life, 10)


def calc_depreciation_schedule(asset_class, asset_value):
    """按资产类别返回逐年折旧（10 年）"""
    for name, life, _ in DEPRECIATION:
        if name == asset_class:
            if life <= 10:
                annual = asset_value / life
                return [annual if y < life else 0 for y in range(10)]
            else:
                annual = asset_value / 10
                return [annual] * 10
    return [0] * 10


def calc_hotel_project(params):
    """
    核心测算函数

    params 必含字段:
            - project_type: 'new' / 'renovation'
            - rooms: 房间数
            - total_invest: 总投资（万元）
            - peak_adr: 峰值 ADR（元）
            - peak_occ: 峰值 OCC（0-1）
            - non_room_ratio: 非房收入占比
            - ramp_type: 爬坡曲线类型（business/resort/cultural/mice/limited_service）
            - labor_cost_annual: 年人工成本（万元）
            - discount_rate: 折现率（默认 8%）
            - tax_rate: 税率（默认 25%）

            租金模式（三选一）：
            - rent_annual: 年固定租金（万元）
            - rent_revenue_ratio: 营收分成比例（如 0.25 = 营收 25%）
            - rent_fixed_min: 保底固定额（与营收分成取高）

            可选字段:
            - electromechanical_value: 机电原值（默认 = 总投资 × 25%）
            - building_value: 房屋建筑物原值（默认 = 总投资 × 60%）
    """
    p = params.copy()
    p.setdefault('discount_rate', 0.08)
    p.setdefault('tax_rate', 0.25)
    # [R66 校订 2026-10-24] labor_in_gop 语义：
    #   False (默认) = GOP 率【未】含人工 -> 利润端需再扣一次人工（脚本历史行为，向后兼容）
    #   True        = GOP 率【已】含人工 -> 不再重复计扣（国堰校订口径）
    # 详见 02_项目/国堰宾馆文创改造/测算_国堰_口径校订_v2.0_2026-10-24.md
    p.setdefault('labor_in_gop', False)   # False = 脚本历史行为（利润端再扣一次人工），保持向后兼容
    p.setdefault('building_value', p['total_invest'] * 0.60)
    p.setdefault('electromechanical_value', p['total_invest'] * 0.25)

    rooms = p['rooms']
    peak_adr = p['peak_adr']
    peak_occ = p['peak_occ']
    non_room_ratio = p['non_room_ratio']
    ramp = RAMP_CURVES[p['ramp_type']]
    days = 365
    available_room_nights = rooms * days

    # 每年 ADR / OCC / RevPAR
    yearly = []
    for y in range(10):
        adr_y = peak_adr * ramp['adr'][y]
        occ_y = peak_occ * ramp['occ'][y]
        revpar = adr_y * occ_y
        room_revenue = adr_y * occ_y * available_room_nights / 10000  # 万元
        total_revenue = room_revenue / (1 - non_room_ratio)
        yearly.append({
            'year': y + 1,
            'stage': ['爬坡', '成熟', '峰值', '峰值', '稳定', '微降', '微降', '回落', '回落', '回升'][[0, 1, 2, 3, 4, 5, 6, 7, 8, 9][min(y, 9)] if y < 5 else (5 if y < 7 else (7 if y < 9 else 9))],
            'adr': round(adr_y, 2),
            'occ': round(occ_y * 100, 1),
            'room_revenue': round(room_revenue, 1),
            'total_revenue': round(total_revenue, 1),
        })

    # 成本（按综合 GOP 率口径，与川宾 5000 万文档匹配）
    # 总成本率 = 1 - gop_rate（包含部门直接+未分配+管理费）
    gop_rate_target = p.get('gop_rate', 0.55)
    for y in yearly:
        # 采用综合 GOP 率口径：直接算出 GOP，不拆分部门
        gop = y['total_revenue'] * gop_rate_target
        non_room_revenue = y['total_revenue'] - y['room_revenue']
        incentive_mgmt = gop * 0.06
        gop_net = gop - incentive_mgmt
        gop_rate = gop_rate_target

        # 非经营费用
        building_value = p['building_value']
        electromechanical_value = p['electromechanical_value']
        annual_depreciation = building_value / 10  # 简化：房屋建筑按 10 年计算
        property_tax = building_value * 0.7 * 0.012
        property_insurance = p['total_invest'] * 0.00035
        machine_insurance = electromechanical_value * 0.00045

        # 利润
        # 租金逻辑：优先营收分成（若无则取固定 rent_annual）
        rent_ratio = p.get('rent_revenue_ratio')
        rent_fixed_min = p.get('rent_fixed_min')
        if rent_ratio and rent_ratio > 0:
            rent_share = y['total_revenue'] * rent_ratio
            if rent_fixed_min and rent_share < rent_fixed_min:
                rent_actual = rent_fixed_min
            else:
                rent_actual = rent_share
        else:
            rent_actual = p.get('rent_annual', 0)
        y['rent'] = round(rent_actual, 1)

        labor_deduct = 0.0 if p.get('labor_in_gop', True) else p['labor_cost_annual']
        profit_before = gop_net - annual_depreciation - property_tax - property_insurance - machine_insurance - rent_actual - labor_deduct
        tax = max(0, profit_before * p['tax_rate'])
        net_profit = profit_before - tax
        cash_flow = net_profit + annual_depreciation  # 现金流 = 净利润 + 折旧

        y.update({
            'non_room_revenue': round(non_room_revenue, 1),
            'gop': round(gop, 1),
            'gop_rate': round(gop_rate * 100, 1),
            'incentive_mgmt': round(incentive_mgmt, 1),
            'gop_net': round(gop_net, 1),
            'depreciation': round(annual_depreciation, 1),
            'property_tax': round(property_tax, 1),
            'insurance': round(property_insurance + machine_insurance, 1),
            'rent': round(rent_actual, 1),
            'labor': p['labor_cost_annual'],
            'labor_deducted': labor_deduct,
            'profit_before': round(profit_before, 1),
            'tax': round(tax, 1),
            'net_profit': round(net_profit, 1),
            'cash_flow': round(cash_flow, 1),
        })

    # 现金流序列（含 Y0 投资）
    cashflows = [-p['total_invest']] + [y['cash_flow'] for y in yearly]

    # 累计现金流（静态回收期）
    cumulative = []
    cum = 0
    for cf in cashflows:
        cum += cf
        cumulative.append(round(cum, 1))

    # 折现
    discount_factor = []
    npv_each = []
    for y, cf in enumerate(cashflows):
        df = 1 / ((1 + p['discount_rate']) ** y)
        discount_factor.append(round(df, 4))
        npv_each.append(round(cf * df, 1))

    npv = sum(npv_each[1:])  # 排除 Y0 投资（已在 NPV 公式中）
    npv_with_invest = -p['total_invest'] + sum(npv_each[1:])
    npv_proper = npv_with_invest

    # IRR 求解（牛顿法）
    irr = calc_irr(cashflows)

    # 静态回收期
    static_payback = calc_static_payback(cashflows)

    # 动态回收期
    dynamic_payback = calc_dynamic_payback(cashflows, p['discount_rate'])

    return {
        'params': p,
        'yearly': yearly,
        'cashflows': cashflows,
        'cumulative': cumulative,
        'discount_factor': discount_factor,
        'npv_each': npv_each,
        'npv': round(npv_proper, 1),
        'irr': irr,
        'static_payback': static_payback,
        'dynamic_payback': dynamic_payback,
        'verdict': assess_verdict(irr, static_payback, p),
    }


def calc_irr(cashflows, lo=-0.99, hi=10.0, max_iter=200, tol=1e-5):
    """IRR 二分法（更鲁棒，适合包含负现金流的场景）"""
    def npv_at(r):
        return sum(cf / ((1 + r) ** t) for t, cf in enumerate(cashflows))
    npv_lo = npv_at(lo)
    npv_hi = npv_at(hi)
    if npv_lo * npv_hi > 0:
        # 同号说明无解（项目全亏或全赚）
        if npv_hi < 0:
            return -99.99
        return 999.99
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        npv_mid = npv_at(mid)
        if abs(npv_mid) < tol:
            return round(mid * 100, 2)
        if npv_mid * npv_lo < 0:
            hi = mid; npv_hi = npv_mid
        else:
            lo = mid; npv_lo = npv_mid
    return round(((lo + hi) / 2) * 100, 2)


def calc_static_payback(cashflows):
    """静态回收期（含小数年的插值）"""
    cum = 0
    for t, cf in enumerate(cashflows):
        if t == 0:
            cum = cf
            continue
        prev_cum = cum
        cum += cf
        if cum >= 0 and prev_cum < 0:
            fraction = -prev_cum / cf
            return round(t - 1 + fraction, 1)
    return None


def calc_dynamic_payback(cashflows, rate):
    """动态回收期"""
    cum_pv = 0
    for t, cf in enumerate(cashflows):
        if t == 0:
            cum_pv = cf
            continue
        prev_cum = cum_pv
        cum_pv += cf / ((1 + rate) ** t)
        if cum_pv >= 0 and prev_cum < 0:
            fraction = -prev_cum / (cf / ((1 + rate) ** t))
            return round(t - 1 + fraction, 1)
    return None


def assess_verdict(irr, payback, p):
    """按 Eric 投资人 8 大准则判断"""
    issues = []

    # 准则 1: 投资回报周期 ≤ 6 年（经济型/中端）
    if payback is None:
        issues.append('⚠️ 10 年内未回本')
    elif payback > 8:
        issues.append(f'⚠️ 静态回收期 {payback} 年 > 8 年（偏长）')
    elif payback > 6:
        issues.append(f'⚠️ 静态回收期 {payback} 年 6-8 年（偏长）')
    else:
        issues.append(f'✅ 静态回收期 {payback} 年 ≤ 6 年')

    # 准则 2: IRR ≥ 15%（头部品牌目标）
    if irr < 3.5:
        issues.append(f'❌ IRR {irr}% < 3.5%（国资委最低门槛）')
    elif irr < 8:
        issues.append(f'⚠️ IRR {irr}% < 8%（未达合理门槛）')
    elif irr < 15:
        issues.append(f'✅ IRR {irr}% 8-15%（合格）')
    else:
        issues.append(f'✅ IRR {irr}% ≥ 15%（优质）')

    # 准则 5: 单房投资 ≤ RevPAR × 800
    unit_invest = p['total_invest'] / p['rooms'] * 10000  # 万元→元
    revpar = p['peak_adr'] * p['peak_occ']
    ratio = unit_invest / revpar
    if ratio > 1000:
        issues.append(f'⚠️ 单房投资 {int(unit_invest/10000)}万 / RevPAR {int(revpar)} = {int(ratio)} > 1000')
    else:
        issues.append(f'✅ 单房投资 / RevPAR = {int(ratio)} ≤ 1000')

    return ' | '.join(issues)


# ========== Excel 报表导出 ==========
def write_excel_report(result, output_path):
    """导出 9 表结构 Excel"""
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        print('⚠️ 缺 openpyxl，跳过 Excel 导出')
        return None

    wb = Workbook()
    wb.remove(wb.active)

    bold = Font(bold=True)
    header_fill = PatternFill('solid', fgColor='1F4E78')
    header_font = Font(bold=True, color='FFFFFF')
    center = Alignment(horizontal='center', vertical='center')
    thin = Side(style='thin', color='808080')
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    # 表 1：使用说明
    ws = wb.create_sheet('1_使用说明')
    ws['A1'] = '酒店投资测算自动化报表'
    ws['A1'].font = Font(bold=True, size=16)
    ws['A3'] = '编制'
    ws['B3'] = 'B166ER'
    ws['A4'] = '口径'
    ws['B4'] = '集团通用模版 v1.0（丽苑 6-12 楼 + Eric 2026-09-28 指令）'
    ws['A5'] = '生成时间'
    ws['B5'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    ws['A7'] = '9 表结构'
    tables_9 = [
        ('1', '使用说明', '本表'),
        ('2', '参数库', '20 类酒店分级基准'),
        ('3', '五星标准配置', 'GB/T 14308 32 项核查清单'),
        ('4', '投资估算', '25 个分项明细'),
        ('5', '折旧与税费', '12 类资产逐年'),
        ('6', '爬坡曲线', '5 条生命周期曲线'),
        ('7', '十年测算', '核心：收入-成本-GOP-现金流-IRR'),
        ('8', '敏感性分析', 'ADR×OCC 双向表'),
        ('9', '一页纸结论', '10 项关键指标汇总'),
    ]
    for i, (n, name, desc) in enumerate(tables_9):
        ws.cell(row=9 + i, column=1, value=n)
        ws.cell(row=9 + i, column=2, value=name)
        ws.cell(row=9 + i, column=3, value=desc)

    # 表 7：十年测算（核心）
    ws = wb.create_sheet('7_十年测算')
    p = result['params']
    headers = ['年份', '阶段', 'ADR', 'OCC(%)', '客房收入(万)', '非房收入(万)', '总收入(万)',
               'GOP(万)', 'GOP率(%)', '奖励管理费(万)', 'GOP净额(万)', '折旧(万)',
               '房产税(万)', '保险(万)', '租金(万)', '人工(万)', '利润总额(万)',
               '所得税(万)', '净利润(万)', '现金流(万)']
    for col, h in enumerate(headers, 1):
        c = ws.cell(row=1, column=col, value=h)
        c.fill = header_fill; c.font = header_font; c.alignment = center
    for i, y in enumerate(result['yearly']):
        row = i + 2
        ws.cell(row=row, column=1, value=f'Y{y["year"]}')
        ws.cell(row=row, column=2, value=y['stage'])
        ws.cell(row=row, column=3, value=y['adr'])
        ws.cell(row=row, column=4, value=y['occ'])
        ws.cell(row=row, column=5, value=y['room_revenue'])
        ws.cell(row=row, column=6, value=y['non_room_revenue'])
        ws.cell(row=row, column=7, value=y['total_revenue'])
        ws.cell(row=row, column=8, value=y['gop'])
        ws.cell(row=row, column=9, value=y['gop_rate'])
        ws.cell(row=row, column=10, value=y['incentive_mgmt'])
        ws.cell(row=row, column=11, value=y['gop_net'])
        ws.cell(row=row, column=12, value=y['depreciation'])
        ws.cell(row=row, column=13, value=y['property_tax'])
        ws.cell(row=row, column=14, value=y['insurance'])
        ws.cell(row=row, column=15, value=y['rent'])
        ws.cell(row=row, column=16, value=y['labor'])
        ws.cell(row=row, column=17, value=y['profit_before'])
        ws.cell(row=row, column=18, value=y['tax'])
        ws.cell(row=row, column=19, value=y['net_profit'])
        ws.cell(row=row, column=20, value=y['cash_flow'])

    # 表 9：一页纸结论
    ws9 = wb.create_sheet('9_一页纸结论')
    summary = [
        ('项目名称', p.get('project_name', '新建项目')),
        ('项目类型', p.get('project_type', 'new')),
        ('房间数', p['rooms']),
        ('总投资', f"{p['total_invest']:,.0f} 万元"),
        ('单房投资', f"{p['total_invest']/p['rooms']*10000/10000:,.1f} 万元/间"),
        ('峰值 ADR', f"{p['peak_adr']} 元"),
        ('峰值 OCC', f"{p['peak_occ']*100:.0f}%"),
        ('非房收入占比', f"{p['non_room_ratio']*100:.0f}%"),
        ('峰值年收入', f"{result['yearly'][2]['total_revenue']:,.0f} 万元"),
        ('峰值年 GOP', f"{result['yearly'][2]['gop']:,.0f} 万元"),
        ('峰值年 GOP率', f"{result['yearly'][2]['gop_rate']:.1f}%"),
        ('IRR', f"{result['irr']}%"),
        ('NPV @ 8%', f"{result['npv']:,.0f} 万元"),
        ('静态回收期', f"{result['static_payback']} 年" if result['static_payback'] else '10 年+'),
        ('动态回收期', f"{result['dynamic_payback']} 年" if result['dynamic_payback'] else '10 年+'),
        ('综合判断', result['verdict']),
    ]
    ws9.cell(row=1, column=1, value='指标').fill = header_fill
    ws9.cell(row=1, column=1).font = header_font
    ws9.cell(row=1, column=2, value='数值').fill = header_fill
    ws9.cell(row=1, column=2).font = header_font
    for i, (k, v) in enumerate(summary):
        ws9.cell(row=i + 2, column=1, value=k).font = bold
        ws9.cell(row=i + 2, column=2, value=v)

    wb.save(output_path)
    print(f'✅ Excel 已保存：{output_path}')
    return output_path


# ========== 预置案例：四川宾馆 4 版本 / 花园 v1.4 / 新良模式 ==========
PRESETS = {
    'chuanbin_5000w': {
        'project_name': '四川宾馆·5000万自投自建',
        'project_type': 'renovation',
        'rooms': 120, 'total_invest': 5000,
        'peak_adr': 700, 'peak_occ': 0.73, 'non_room_ratio': 0.37,
        'ramp_type': 'cultural',
        'rent_revenue_ratio': 0.25, 'rent_fixed_min': 729,
        'labor_cost_annual': 480, 'discount_rate': 0.08,
    },
    'chuanbin_4932w_jinjiang': {
        'project_name': '四川宾馆·锦江方案 4932 万',
        'project_type': 'renovation',
        'rooms': 165, 'total_invest': 4932,
        'peak_adr': 520, 'peak_occ': 0.85, 'non_room_ratio': 0.04,
        'ramp_type': 'business',
        'rent_fixed_min': 729, 'rent_revenue_ratio': 0.25,
        'labor_cost_annual': 480, 'discount_rate': 0.08,
    },
    'chuanbin_junting': {
        'project_name': '四川宾馆·君亭方式 5700 万',
        'project_type': 'renovation',
        'rooms': 120, 'total_invest': 5700,
        'peak_adr': 700, 'peak_occ': 0.78, 'non_room_ratio': 0.30,
        'ramp_type': 'cultural', 'rent_annual': 500,
        'labor_cost_annual': 480, 'discount_rate': 0.08,
    },
    'huayuan_v14': {
        'project_name': '花园宾馆·逸精选 v1.4',
        'project_type': 'renovation',
        'rooms': 180, 'total_invest': 3000,
        'peak_adr': 450, 'peak_occ': 0.80, 'non_room_ratio': 0.16,
        'ramp_type': 'limited_service', 'rent_annual': 0,
        'labor_cost_annual': 800, 'discount_rate': 0.10,
    },
    'xinliang_zizhu': {
        'project_name': '新良大酒店·自有品牌',
        'project_type': 'renovation',
        'rooms': 200, 'total_invest': 6000,
        'peak_adr': 550, 'peak_occ': 0.75, 'non_room_ratio': 0.20,
        'ramp_type': 'business', 'rent_annual': 0,
        'labor_cost_annual': 1200, 'discount_rate': 0.08,
    },
}


if __name__ == '__main__':
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    preset_name = sys.argv[1] if len(sys.argv) > 1 else 'chuanbin_5000w'
    if preset_name == 'list':
        print('可选案例:')
        for k, v in PRESETS.items():
            print(f'  {k}: {v["project_name"]}')
        sys.exit(0)
    if preset_name == 'all':
        print(f'{"项目":<30} {"IRR":<10} {"NPV(万)":<12} {"回本(年)":<10} {"判断"}')
        print('-' * 100)
        for k, p in PRESETS.items():
            r = calc_hotel_project(p)
            pb = r['static_payback'] if r['static_payback'] else '10+'
            verdict_clean = r['verdict'].replace('⚠️', '[!]').replace('✅', '[Y]').replace('❌', '[N]')
            print(f'{p["project_name"]:<30} {r["irr"]}%{"":>3} {r["npv"]:>8} {pb:>6} {"":>5} {verdict_clean[:60]}')
        sys.exit(0)

    params = PRESETS[preset_name]
    result = calc_hotel_project(params)
    print(f'\n{"="*60}')
    print(f'项目：{params["project_name"]}')
    print(f'{"="*60}')
    print(f'IRR: {result["irr"]}%')
    print(f'NPV @ 8%: {result["npv"]} 万元')
    print(f'静态回收期: {result["static_payback"]} 年')
    print(f'动态回收期: {result["dynamic_payback"]} 年')
    print(f'\n判断：{result["verdict"]}')
    print(f'\n10 年现金流:')
    for y, c in enumerate(result['cashflows']):
        print(f'  Y{y}: {c:,.1f} 万元')

    if len(sys.argv) > 2 and sys.argv[2] == 'excel':
        write_excel_report(result, f'{preset_name}_report.xlsx')