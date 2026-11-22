# -*- coding: utf-8 -*-
"""
RGI 对标法反推 — 四川宾馆改造项目 (165 间)
数据源: Eric 提供截图 (2026-08-01 10:00 GMT+8)
"""
import statistics

hotels = [
    # name, year, distance_km, distance_min, rooms, area_m2, adr, occ, rev_mil, rating_score, rating_count
    ('蓉福朋喜来登',          2025, 0.57,  5, 322, '33-40', 483, 0.81,  4598, 4.7,  4942),
    ('太古里春熙路步行街城际',  2025, 2.10, 18, 210, '28-33', 489, 0.925, 3467, 4.8,  3080),
    ('蓉希尔顿花园(太古里店)',   2024, 2.00, 12, 174, '28-41', 550, 0.95,  3318, 4.8,  5021),
    ('pagoda君亭设计(太古里店)',  2022, 0.86,  8, 206, '40-45', 660, 0.88,  4367, 4.7, 15061),
    ('蓉希尔顿欢朋',           2020, 0.83,  6, 253, '27-35', 523, 0.93,  4491, 4.7, 13319),
    ('太古里春熙美居',          2018, 0.63,  3, 374, '28-32', 505, 0.92,  6342, 4.8, 23186),
]

print('=' * 100)
print('  RGI 对标法反推 — 四川宾馆改造项目 (165 间)')
print('=' * 100)

# --- 1. 基础 RevPAR ---
print()
print('【1. 竞争集 RevPAR 计算】')
print(f'{"酒店":<28} {"ADR":>6} {"Occ":>7} {"RevPAR":>9} {"客房年收入(万)":>15}')
revpar_list = []
for h in hotels:
    name, year, dist_km, dist_min, rooms, area, adr, occ, rev, rs, rc = h
    revpar = adr * occ
    annual_rev = revpar * rooms * 365 / 10000
    revpar_list.append(revpar)
    print(f'{name:<28} {adr:>6} {occ*100:>6.1f}% {revpar:>9.1f} {annual_rev:>15,.0f}')

# --- 2. 整体统计 ---
print()
print('【2. 竞争集整体统计】')
adrs = [h[6] for h in hotels]
occs = [h[7] for h in hotels]
print(f'  ADR    均值 = {statistics.mean(adrs):>6.1f}  中位数 = {statistics.median(adrs):>6.1f}  极差 = [{min(adrs)}-{max(adrs)}]')
print(f'  Occ    均值 = {statistics.mean(occs)*100:>5.2f}% 中位数 = {statistics.median(occs)*100:>5.2f}% 极差 = [{min(occs)*100:.1f}%-{max(occs)*100:.1f}%]')
print(f'  RevPAR 均值 = {statistics.mean(revpar_list):>6.1f}  中位数 = {statistics.median(revpar_list):>6.1f}  极差 = [{min(revpar_list):.1f}-{max(revpar_list):.1f}]')

# --- 3. 距离分层 ---
print()
print('【3. 按距离分层】')
near = [h for h in hotels if h[2] < 1.0]
far  = [h for h in hotels if h[2] >= 1.0]
for label, group in [('近距离(<1km)', near), ('远距离(>1km)', far)]:
    a = statistics.mean([h[6] for h in group])
    o = statistics.mean([h[7] for h in group])
    r = a * o
    print(f'  {label}  n={len(group):<2}  ADR={a:>5.1f}  Occ={o*100:>5.2f}%  RevPAR={r:>6.1f}')

# --- 4. RGI=100 简单均值法 ---
print()
print('【4. RGI = 100 反推 — 简单均值法】')
target_rooms = 165
mean_adr = statistics.mean(adrs)
mean_occ = statistics.mean(occs)
mean_revpar = statistics.mean(revpar_list)
annual_simple = 165 * mean_revpar * 365 / 10000
print(f'  目标 ADR    = {mean_adr:.1f} 元/间·夜')
print(f'  目标 Occ    = {mean_occ*100:.2f} %')
print(f'  目标 RevPAR = {mean_revpar:.1f} 元')
print(f'  客房年收入 = 165 × {mean_revpar:.1f} × 365 / 10000 = {annual_simple:,.0f} 万元')

# --- 5. 加权均值法 ---
print()
print('【5. RGI = 100 反推 — 加权均值法 (按房间数加权)】')
total_weight = sum(h[4] for h in hotels)
weighted_adr = sum(h[6]*h[4] for h in hotels) / total_weight
weighted_occ = sum(h[7]*h[4] for h in hotels) / total_weight
weighted_revpar = sum(h[6]*h[7]*h[4] for h in hotels) / total_weight
annual_weighted = 165 * weighted_revpar * 365 / 10000
print(f'  目标 ADR    = {weighted_adr:.1f} 元/间·夜')
print(f'  目标 Occ    = {weighted_occ*100:.2f} %')
print(f'  目标 RevPAR = {weighted_revpar:.1f} 元')
print(f'  客房年收入 = 165 × {weighted_revpar:.1f} × 365 / 10000 = {annual_weighted:,.0f} 万元')

# --- 6. 近距对标法 ---
print()
print('【6. RGI = 100 反推 — 近距对标法 (距川宾 ≤1km, 4 家, 最贴近市场)】')
near_revpar = statistics.mean([h[6]*h[7] for h in near])
near_adr = statistics.mean([h[6] for h in near])
near_occ = statistics.mean([h[7] for h in near])
annual_near = 165 * near_revpar * 365 / 10000
print(f'    蓉福朋喜来登(5min) + pagoda君亭(8min) + 希尔顿欢朋(6min) + 美居(3min)')
print(f'  近距 ADR    = {near_adr:.1f} 元/间·夜')
print(f'  近距 Occ    = {near_occ*100:.2f} %')
print(f'  近距 RevPAR = {near_revpar:.1f} 元')
print(f'  客房年收入  = 165 × {near_revpar:.1f} × 365 / 10000 = {annual_near:,.0f} 万元')

# --- 7. 档次定位 ---
print()
print('【7. 按品牌档次分层 (决定定价天花板)】')
luxury_intl = [h for h in hotels if any(k in h[0] for k in ['希尔顿花园','希尔顿欢朋','福朋喜来登','美居'])]
design = [h for h in hotels if 'pagoda' in h[0] or '君亭' in h[0] or '设计' in h[0]]
chain_mid = [h for h in hotels if '城际' in h[0] or '步行街' in h[0]]
for label, group in [('国际中高端品牌(希尔顿/福朋/美居)', luxury_intl),
                     ('设计品牌(pagoda/君亭)', design),
                     ('连锁中端(城际/步行街)', chain_mid)]:
    if group:
        a = statistics.mean([h[6] for h in group])
        o = statistics.mean([h[7] for h in group])
        r = a * o
        print(f'  {label}  n={len(group):<2}  ADR={a:>5.0f}  Occ={o*100:>5.2f}%  RevPAR={r:>6.0f}')

print()
print('=' * 100)
print('  RGI 对标反推 — 核心结论 (RGI=100 / 达到市场均值水平)')
print('=' * 100)