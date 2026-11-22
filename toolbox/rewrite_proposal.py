# -*- coding: utf-8 -*-
"""
总府川宾可研报告重写方案 — 关键示例数据计算
B166ER · 2026-08-01 12:09-12:45 GMT+8
基于评审发现的方法论缺失, 给出重写后的具体示例
"""

import statistics
import json

# ===== 基础数据 (从原报告提取) =====
BASE = {
    'rooms': 165,
    'adr': 520,           # 元/间·夜 (稳定期)
    'occ': 0.856,         # 85.6%
    'revpar': 520 * 0.856,  # 445.12 元
    'investment_wan': 4932.26,  # 万元
    'room_revenue_wan': 2679,   # 稳定期年收入 (含税)
    'room_revenue_excl_tax': 2528,  # 不含税
    'rental_pct': 0.25,    # 25% 营收分成
    'rental_floor_per_sqm': 50,  # 元/m²/月 保底
    'total_sqm': 12155,    # 总建筑面积
    'rental_floor_monthly': 12155 * 50 / 10000,  # 万/月 = 60.78 万
    'rental_floor_annual': 12155 * 50 * 12 / 10000,  # 万/年 = 729.36 万
    'gop_rate': 0.43,      # 报告假设
    'ebitda_wan': 466,     # 报告 EBITDA (成熟期)
    'direct_cost_rate': 0.305,  # 直接成本率
    'payback_years': 11,
    'irr': 0.0406,
    'npv_wan': 169.1,
    'lpr_5y': 0.035,
}

# 7.6 单变量敏感性分析示例 — 4 维变量 × 7 档
print('=' * 100)
print('  【7.6 单变量敏感性分析示例】— 总府川宾 165 间')
print('=' * 100)

def calc_rev(adr, occ, days=365):
    return adr * occ * 165 * days / 10000  # 万元/年

def calc_rent(rev_wan, sqm=12155, floor_per_sqm=50):
    """实际租金 = max(营收 × 25%, sqm × floor × 12 / 10000)"""
    rev_share = rev_wan * 0.25
    floor_total = sqm * floor_per_sqm * 12 / 10000
    return max(rev_share, floor_total)

def calc_gop(rev_wan, direct_cost_rate=0.305, rent_wan=0):
    """简化 GOP = 营收 × (1 - 直接成本率) - 租金"""
    gop = rev_wan * (1 - direct_cost_rate) - rent_wan
    return gop

# 维度 1: ADR 敏感性
print('\n[维度 1] ADR 变动 (Occ 不变 = 85.6%)')
print(f'{"变动":>6} {"ADR":>6} {"营收(万)":>10} {"租金(万)":>10} {"GOP(万)":>10} {"GOP率":>8} {"相对基准"}')
base_rev = calc_rev(520, 0.856)
base_rent = calc_rent(base_rev)
base_gop = calc_gop(base_rev) - base_rent
for delta in [-0.20, -0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15]:
    adr = 520 * (1 + delta)
    rev = calc_rev(adr, 0.856)
    rent = calc_rent(rev)
    gop = calc_gop(rev) - rent
    gop_rate = gop / rev * 100 if rev > 0 else 0
    delta_gop = (gop - base_gop) / base_gop * 100 if base_gop != 0 else 0
    print(f'{delta*100:>+5.0f}% {adr:>6.0f} {rev:>10.0f} {rent:>10.0f} {gop:>10.0f} {gop_rate:>7.1f}% {delta_gop:>+8.1f}%')

# 维度 2: Occ 敏感性
print('\n[维度 2] Occ 变动 (ADR 不变 = 520 元)')
print(f'{"变动":>6} {"Occ":>6} {"营收(万)":>10} {"租金(万)":>10} {"GOP(万)":>10} {"GOP率":>8} {"相对基准"}')
for delta in [-0.15, -0.10, -0.05, -0.03, 0, 0.03, 0.05, 0.10]:
    occ = 0.856 + delta
    rev = calc_rev(520, occ)
    rent = calc_rent(rev)
    gop = calc_gop(rev) - rent
    gop_rate = gop / rev * 100 if rev > 0 else 0
    delta_gop = (gop - base_gop) / base_gop * 100 if base_gop != 0 else 0
    print(f'{delta*100:>+5.0f}% {occ*100:>5.1f}% {rev:>10.0f} {rent:>10.0f} {gop:>10.0f} {gop_rate:>7.1f}% {delta_gop:>+8.1f}%')

# 维度 3: 投资额敏感性
print('\n[维度 3] 投资额变动 (营收/租金不变)')
print(f'{"变动":>6} {"投资(万)":>10} {"对 IRR 影响":>12} {"对回收期影响":>14}')
for delta in [-0.20, -0.10, 0, 0.10, 0.20, 0.30]:
    inv = 4932.26 * (1 + delta)
    # 简化: IRR 与投资额反向变动 (线性近似)
    irr_delta = -delta * 0.5  # 经验估算: 投资 +10% → IRR 约降 0.5pp
    irr_adj = 0.0406 + irr_delta
    payback_adj = 11 * (1 + delta * 0.6)  # 投资 +10% → 回收期 +0.66 年
    print(f'{delta*100:>+5.0f}% {inv:>10.0f} {irr_delta*100:>+10.2f}pp {payback_adj:>12.1f} 年')

# 维度 4: 租金保底敏感性
print('\n[维度 4] 租金保底单价敏感性 (元/平方米/月)')
print(f'{"单价":>6} {"月租(万)":>10} {"年租(万)":>10} {"占营收比":>10} {"GOP影响":>12}')
for floor in [30, 40, 50, 60, 70, 80]:
    monthly_rent = 12155 * floor / 10000
    annual_rent = monthly_rent * 12
    rent_pct = annual_rent / base_rev * 100
    gop_impact = (annual_rent - 729.36) / 1  # 相对 50 元基准的差额
    print(f'{floor:>5} {monthly_rent:>10.2f} {annual_rent:>10.0f} {rent_pct:>9.1f}% {gop_impact:>+11.0f} 万')

# ===== 7.7 多变量敏感性分析示例 =====
print('\n' + '=' * 100)
print('  【7.7 多变量敏感性分析示例】— ADR × Occ 联合变动')
print('=' * 100)
print(f'\n{"ADR\\Occ":>10} {"80%":>10} {"83%":>10} {"85.6%":>10} {"88%":>10} {"90%":>10}')
adrs = [470, 490, 510, 520, 540, 560]
occs = [0.80, 0.83, 0.856, 0.88, 0.90]
matrix = {}
for adr in adrs:
    row = []
    for occ in occs:
        rev = calc_rev(adr, occ)
        rent = calc_rent(rev)
        gop = calc_gop(rev) - rent
        row.append(gop)
    matrix[adr] = row

# Print matrix
for adr in adrs:
    line = f'{adr:>10} '
    for gop in matrix[adr]:
        line += f'{gop:>10.0f}'
    print(line)
print('\n(数值为 GOP 万元/年, 基准 = ADR 520 × Occ 85.6% = ' + f'{base_gop:.0f} 万)')

# ===== 7.8 三情景分析 =====
print('\n' + '=' * 100)
print('  【7.8 三情景分析示例】— 悲观 / 基准 / 乐观')
print('=' * 100)
scenarios = {
    '悲观': {'adr': 470, 'occ': 0.75, 'ramp': 5, 'desc': '3-5 年才能达到成熟期, 新品牌 + 老楼改造 + 7 年停业'},
    '基准': {'adr': 520, 'occ': 0.856, 'ramp': 3, 'desc': '报告原假设, 3 年达到成熟期'},
    '乐观': {'adr': 560, 'occ': 0.88, 'ramp': 2, 'desc': '差异化定位成功, 2 年达到成熟期'},
}
print(f'\n{"情景":>6} {"ADR":>6} {"Occ":>6} {"营收(万)":>10} {"租金(万)":>10} {"GOP(万)":>10} {"IRR估算":>10} {"回收期":>8} {"说明"}')
for name, s in scenarios.items():
    rev = calc_rev(s['adr'], s['occ'])
    rent = calc_rent(rev)
    gop = calc_gop(rev) - rent
    # 简化 IRR 估算
    irr_est = 0.0406 * (rev / base_rev) ** 1.5
    payback = 11 / (rev / base_rev) ** 0.8
    print(f'{name:>6} {s["adr"]:>6} {s["occ"]*100:>5.1f}% {rev:>10.0f} {rent:>10.0f} {gop:>10.0f} {irr_est*100:>8.2f}% {payback:>6.1f} 年 {s["desc"]}')

# ===== 7.9 盈亏平衡分析 =====
print('\n' + '=' * 100)
print('  【7.9 盈亏平衡分析示例】')
print('=' * 100)

# 假设固定成本构成 (估算, 行业基准)
print('\n[年度固定成本估算]')
fixed_costs = {
    '人工成本 (按 30 人 × 8 万)': 240,
    '能源 (按 165 间 × 1500 元/间·年)': 25,  # 约 25 万
    '物业租金 (保底)': 729.36,
    '折旧摊销 (按 15 年直线)': 4932.26 / 15 * 0.7,  # 70% 可折旧
    '管理费': 80,
    '保险费': 30,
    '营销费 (固定部分)': 100,
}
total_fixed = sum(fixed_costs.values())
for k, v in fixed_costs.items():
    print(f'  {k:<35} {v:>8.1f} 万')
print(f'  {"合计":<35} {total_fixed:>8.1f} 万')

# 单位变动成本
print(f'\n[单位变动成本估算]')
unit_var_costs = {
    '低耗品 (按 30 元/间·夜)': 30,
    '洗涤 (按 25 元/间·夜)': 25,
    'OTA 佣金 (按 ADR × 15%)': 520 * 0.15,
    '销售提成 (按 ADR × 5%)': 520 * 0.05,
    '其他变动 (10 元/间·夜)': 10,
}
unit_var = sum(unit_var_costs.values())
for k, v in unit_var_costs.items():
    print(f'  {k:<35} {v:>8.1f} 元')
print(f'  {"合计单位变动成本":<35} {unit_var:>8.1f} 元/间·夜')

# 盈亏平衡入住率
unit_contribution = 520 - unit_var  # 单位贡献 = ADR - 单位变动成本
breakeven_rooms = total_fixed * 10000 / unit_contribution  # 间·年
breakeven_occ = breakeven_rooms / (165 * 365)
print(f'\n[盈亏平衡点]')
print(f'  单位贡献 (ADR - 单位变动)  = 520 - {unit_var:.0f} = {unit_contribution:.0f} 元/间·夜')
print(f'  年固定成本               = {total_fixed:.0f} 万')
print(f'  盈亏平衡售房数           = {total_fixed*10000/unit_contribution:.0f} 间·年')
print(f'  盈亏平衡入住率           = {breakeven_occ*100:.1f}%')
print(f'  行业基准盈亏平衡入住率   = 55-65%')
print(f'  本项目相对行业基准       = {"偏紧" if breakeven_occ*100 > 65 else "正常" if breakeven_occ*100 > 55 else "宽松"}')

# ===== 现金流瀑布 — 集团最大补贴需求 =====
print('\n' + '=' * 100)
print('  【7.4 深化】 集团最大补贴需求测算')
print('=' * 100)
print('\n[15 年现金流瀑布 — 简化版]')
print(f'{"年度":>4} {"营收":>8} {"GOP":>8} {"租金":>8} {"折旧摊销":>8} {"净现金流":>10} {"累计":>10} {"集团补贴需求":>12}')

cum_cashflow = 0
max_subsidy = 0
subsidy_year = 0
years_data = []
for y in range(1, 16):
    # 假设第 1-3 年爬坡
    if y == 1:
        adr_y, occ_y = 474, 0.745
    elif y == 2:
        adr_y, occ_y = 494, 0.826
    else:
        adr_y, occ_y = 520, 0.856

    rev_y = calc_rev(adr_y, occ_y)
    gop_y = calc_gop(rev_y)
    rent_y = calc_rent(rev_y)
    depreciation = 4932.26 / 15 * 0.7  # 简化
    # 净现金流 = GOP - 租金 (租金已含) ... 简化: GOP 已是 GOP
    net_cf = gop_y - rent_y - depreciation * 0.3  # 30% 现金影响
    cum_cashflow += net_cf

    # 集团补贴 = 当累计现金流转负时
    subsidy = max(0, -cum_cashflow) if cum_cashflow < 0 else 0
    if subsidy > max_subsidy:
        max_subsidy = subsidy
        subsidy_year = y

    years_data.append((y, rev_y, gop_y, rent_y, depreciation, net_cf, cum_cashflow, subsidy))

for d in years_data:
    print(f'{d[0]:>4} {d[1]:>8.0f} {d[2]:>8.0f} {d[3]:>8.0f} {d[4]:>8.0f} {d[5]:>10.0f} {d[6]:>10.0f} {d[7]:>12.0f}')

print(f'\n  【关键发现】 集团最大补贴需求 = {max_subsidy:.0f} 万元 (第 {subsidy_year} 年峰值)')
print(f'               集团最大补贴占投资比 = {max_subsidy/4932.26*100:.1f}%')
print(f'               报告完全没测算这个指标 — 是 B166ER 评审新增的关键风控点')

print('\n' + '=' * 100)
print('  计算完毕 — 数据用于可研报告方法论升级示例')
print('=' * 100)