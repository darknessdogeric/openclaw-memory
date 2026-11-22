# -*- coding: utf-8 -*-
"""v26 模型（终版）：市场分析价格 → 反算投资承受力
★口径修正（对照 039 完整造价构成表 2026-11-14、2026-10 实测利润表、专题会纪要 2026-10-16）：
 1) 现金流引擎＝实测利润表结构复现：项目口径经营现金流 = Adjusted GOP − 激励费 − FF&E 储备
    实测校核：Adjusted GOP 1,672.68 − 激励费 83.63 = 1,589.05 万元/年 ✔
 2) 非房收入不随 ADR 等比放大：按开房率缩放 ＋ 12% 房价联动（覆盖数随客流而非房价）
 3) 反事实臂＝最小合规臂（纪要「依法合规进行停业整改」）：段二 11,060 + 停业 15 月 + 无产品力提升
 4) 造价：段二用 039 表 07 G 列 11,060／11,600；段三用 039 表 07 H 列；品牌专项净 1,620
    （1,990 中网络 270＋电视 100 已在 039 段二内，不重复计列）
 5) A4 段三＝洲至奢选·重做·不减房 28,490.7（原误用「保留」口径 17,130.7）
"""
import io, os, sys, json, math
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
T = r'D:\B166ER-openclaw\workspace\.tmp'

# ═══════ 1. 实测标定（2026-10 利润表 YTD 10 个月年化，万元）════════
M = dict(
    total_rev=6078.07, room_rev=4036.0,
    goi_rate=0.6273, unalloc_rate=0.3321,
    ag=671.3, it=95.3,
    energy_rate=0.05573, pom_rate=0.05465,
    adj_gop=1672.68, inc_fee=83.63, nop_actual=-499.81, onop_total=2088.86,
    occ_now=0.7375, adr_now=373.1, adr_oct=418.6,
    cf_degrade=0.05, energy_new=0.65, pom_new=0.75,
    nonroom_link=0.12,
)
M['nonroom_base'] = round(M['total_rev']-M['room_rev'], 2)
M['unalloc_total'] = round(M['total_rev']*M['unalloc_rate'], 2)
M['fixed_agit'] = round(M['ag']+M['it'], 1)
M['var_rate'] = round((M['unalloc_total']-M['fixed_agit'])/M['total_rev'], 6)
M['cf_pre_project'] = round(M['adj_gop']-M['inc_fee'], 1)
print('=== 实测标定（2026 年 10 月利润表 YTD 年化，万元）===')
print('  总收入 %.2f｜客房 %.0f｜非房 %.2f｜GOI %.2f (%.2f%%)｜未分配 %.2f (%.2f%%)｜Adjusted GOP %.2f' % (
    M['total_rev'], M['room_rev'], M['nonroom_base'], M['total_rev']*M['goi_rate'], M['goi_rate']*100,
    M['unalloc_total'], M['unalloc_rate']*100, M['adj_gop']))
print('  ★项目口径经营现金流 = Adjusted GOP %.2f − 激励费 %.2f = %.1f 万元/年' % (
    M['adj_gop'], M['inc_fee'], M['cf_pre_project']))
print('  校核：实测 NOP %.2f ＋ Other Non-Operating %.2f = %.2f ✔' % (
    M['nop_actual'], M['onop_total'], M['nop_actual']+M['onop_total']))

# ═══════ 2. 抛物线经营曲线（7 年一循环）════════
CYCLE = 7
R_ADR = [0.72, 0.86, 0.95, 1.00, 0.99, 0.97, 0.94]
R_OCC = [0.78, 0.89, 0.96, 1.00, 1.00, 0.99, 0.98]
PEAK  = [1.00, 0.97, 0.93]
def factors(t):
    c = min((t-1)//CYCLE, len(PEAK)-1); j = (t-1) % CYCLE
    return R_ADR[j]*PEAK[c], R_OCC[j]*PEAK[c]

# ═══════ 3. 造价（039 完整造价构成表 2026-11-14）════════
S2_NO_CUT, S2_CUT = 11060.0, 11600.0
S3_039 = {
 'A1': 10253.6,   # S1 皇冠·保留·不减房·402
 'A3': 18111.3,   # S3 皇冠·重做·不减房·402
 'A4R': 17130.7,   # S4 洲至奢选·保留·不减房·402
 'A4': 28490.7,   # S5 洲至奢选·重做·不减房·402
 'B1': 32781.3,   # S6 洲至奢选·重做·3改2·268
 'C1': 45250.9,   # S7 外部奢牌·重做·3改2·268
 'C2': 39216.7,   # S8 外部奢牌·重做·不减房·402
}
S5_ROOM = round(402*25.35*15000/1e4, 1)
S5_PUB  = 10200.7
S5_DIFF = round(28490.7 - S5_ROOM - S5_PUB, 1)
S3_039['B2'] = round(201*50.71*15000/1e4 + S5_PUB*0.50 + S5_DIFF*0.50, 1)
BRAND_SPECIAL_IHG = 1620.0
BRAND_SELF_SYS = 1500.0

# ═══════ 4. 品牌参数 ═══════
BRANDS = {
 '皇冠':     dict(tier='五星全服', lic=0.020, inc=0.050, ffe=0.020, uplift=0.000,
                  gate=35.0, note='现行标准续牌；合同至 2029-09-27'),
 '洲至奢选': dict(tier='上奢',     lic=0.020, inc=0.080, ffe=0.035, uplift=0.010,
                  gate=40.0, note='体系内换牌；需品牌方书面面积例外'),
 '外部奢牌': dict(tier='顶奢',     lic=0.020, inc=0.100, ffe=0.040, uplift=0.020,
                  gate=45.0, note='全委管理；要求全新视觉'),
 '自营':     dict(tier='自营五星', lic=0.005, inc=0.000, ffe=0.020, uplift=0.005,
                  gate=0.0,  note='集团自有品牌；无面积门槛、无品牌基础费'),
}
# ═══════ 5. 路径 ═══════

# ═══════ 4.5 停业期工程流水（停业月数由流水推得，不手填；与 v25 同法）══════
FL, CREW, WK_M, CH_LEAD, CH_INS = 20, 3, 4.345, 9.0, 3.0
SCHED26 = {
 ('皇冠','保留','不减房'):dict(prep=1.0,demo=2.0,mep=4.0,wk=4,comm=5.0,bp=0.0),
 ('皇冠','重做','不减房'):dict(prep=1.0,demo=2.5,mep=4.5,wk=6,comm=6.0,bp=0.0),
 ('皇冠','保留','3改2'):dict(prep=1.0,demo=3.0,mep=4.0,wk=8,comm=6.5,bp=0.0),
 ('皇冠','重做','3改2'):dict(prep=1.0,demo=3.0,mep=4.0,wk=8,comm=6.5,bp=0.0),
 ('皇冠','重做','2改1'):dict(prep=1.0,demo=3.5,mep=4.5,wk=9,comm=7.0,bp=0.0),
 ('皇冠','重做','全套房'):dict(prep=1.0,demo=4.0,mep=5.0,wk=11,comm=8.0,bp=0.0),
 ('自营','保留','不减房'):dict(prep=1.0,demo=2.0,mep=4.0,wk=4,comm=5.0,bp=0.0),
 ('洲至奢选','保留','不减房'):dict(prep=1.0,demo=2.0,mep=4.0,wk=4,comm=5.0,bp=1.0),
 ('洲至奢选','重做','不减房'):dict(prep=1.0,demo=2.5,mep=4.5,wk=6,comm=6.0,bp=1.0),
 ('洲至奢选','保留','3改2'):dict(prep=1.0,demo=3.0,mep=4.0,wk=8,comm=6.5,bp=1.0),
 ('洲至奢选','重做','3改2'):dict(prep=1.0,demo=3.0,mep=4.0,wk=8,comm=6.5,bp=1.0),
 ('洲至奢选','重做','2改1'):dict(prep=1.0,demo=3.5,mep=4.5,wk=9,comm=7.0,bp=1.0),
 ('洲至奢选','重做','全套房'):dict(prep=1.0,demo=4.0,mep=5.0,wk=11,comm=8.0,bp=1.0),
 ('外部奢牌','重做','3改2'):dict(prep=1.0,demo=3.0,mep=4.0,wk=8,comm=6.5,bp=1.0),
 ('外部奢牌','重做','2改1'):dict(prep=1.0,demo=3.5,mep=4.5,wk=9,comm=7.0,bp=1.0),
 ('外部奢牌','重做','全套房'):dict(prep=1.0,demo=4.0,mep=5.0,wk=11,comm=8.0,bp=1.0),
 ('最小合规','段二','不减房'):dict(prep=1.0,demo=0.0,mep=4.0,wk=2,comm=4.0,bp=0.0),
}
def dt_calc(key):
    s=SCHED26[key]; fm=s['wk']*FL/CREW/WK_M
    t_mep=s['prep']+s['demo']+s['mep']; t_fl=t_mep+fm
    t_eq=max(t_fl,CH_LEAD+CH_INS); t_pub=t_mep+s['comm']
    t_cm=max(t_eq,t_pub); t_fire=t_cm+2.0; t_fix=t_fire+1.5
    t_br=t_fix+s['bp']+1.0; t_tr=t_br+1.0
    return dict(total=t_tr, floor_m=round(fm,1), t_mep=round(t_mep,1), t_floor=round(t_fl,1),
                t_eq=round(t_eq,1), t_pub=round(t_pub,1), t_comm=round(t_cm,1), t_fire=round(t_fire,1),
                t_fix=round(t_fix,1), t_brand=round(t_br,1), t_trial=round(t_tr,1),
                wk=s['wk'], comm=s['comm'], bp=s['bp'], prep=s['prep'], demo=s['demo'], mep=s['mep'])
SCHED_PATH = {'A1':('皇冠','保留','不减房'), 'A2':('自营','保留','不减房'),
 'A3':('皇冠','重做','不减房'), 'A4R':('洲至奢选','保留','不减房'),
 'A4':('洲至奢选','重做','不减房'), 'B1':('洲至奢选','重做','3改2'),
 'B2':('洲至奢选','重做','2改1'), 'C1':('外部奢牌','重做','3改2')}

PATHS = [
 dict(k='A1', nm='保留客房体量·轻改·皇冠假日', grp='①保留体量·轻改', b='皇冠',
      rooms=402, suite=25.35, sale=30.57, du=19, s2=S2_NO_CUT, s3=S3_039['A1'],
      s3_src='039 表07 H5（S1 皇冠·保留·402）', special=BRAND_SPECIAL_IHG,
      mkt=(550, 650, 750), src='维持现状＋产品力达标档（现价 364，+51%~+79%）',
      note='客房段轻改、公区局部更新；沿用现行标准'),
 dict(k='A2', nm='保留客房体量·轻改·安逸自营五星', grp='①保留体量·轻改', b='自营',
      rooms=402, suite=25.35, sale=30.57, du=18, s2=S2_NO_CUT, s3=S3_039['A1'],
      s3_src='039 表07 H5 实体标准（自营同级）', special=BRAND_SELF_SYS,
      mkt=(500, 590, 680), src='维持现状＋产品力档，自营品牌力折让',
      note='无国际品牌面积门槛与基础费；须自建收益管理与客源体系'),
 dict(k='A3', nm='保留客房体量·重改·皇冠假日', grp='②保留体量·重改', b='皇冠',
      rooms=402, suite=25.35, sale=30.57, du=23, s2=S2_NO_CUT, s3=S3_039['A3'],
      s3_src='039 表07 H7（S3 皇冠·重做·402）', special=BRAND_SPECIAL_IHG,
      mkt=(580, 680, 780), src='维持现状＋产品力达标档（重改加成）',
      note='客房与公区全量重做'),
 dict(k='A4R', nm='保留客房体量·轻改·洲至奢选', grp='①保留体量·轻改', b='洲至奢选',
      rooms=402, suite=25.35, sale=30.57, du=19, s2=S2_NO_CUT, s3=S3_039['A4R'],
      s3_src='039 表07 H8（S4 洲至奢选·保留·402）', special=BRAND_SPECIAL_IHG,
      mkt=(620, 720, 820), src='洲际换牌档下限（面积不达标，不可取全溢价）',
      note='洲至体系换牌、客房段轻改；面积差 14.65 ㎡，需品牌方书面例外'),
 dict(k='A4', nm='保留客房体量·重改·洲至奢选', grp='②保留体量·重改', b='洲至奢选',
      rooms=402, suite=25.35, sale=30.57, du=20, s2=S2_NO_CUT, s3=S3_039['A4'],
      s3_src='039 表07 H9（S5 洲至奢选·重做·402）', special=BRAND_SPECIAL_IHG,
      mkt=(620, 720, 820), src='洲际换牌档下限（面积不达标，不可取全溢价）',
      note='洲至体系换牌；面积差 14.65 ㎡，例外难度最高'),
 dict(k='B1', nm='客房体量变化·重改·洲至奢选 3改2', grp='③体量变化·重改', b='洲至奢选',
      rooms=268, suite=38.03, sale=45.85, du=26, s2=S2_CUT, s3=S3_039['B1'],
      s3_src='039 表07 H10（S6 洲至奢选·重做·268）', special=BRAND_SPECIAL_IHG,
      mkt=(750, 880, 1000), src='洲际换牌档（14 个月过渡）',
      note='面积例外仅差 1.97 ㎡，妥协可行性最高'),
 dict(k='B2', nm='客房体量变化·重改·洲至奢选 2改1', grp='③体量变化·重改', b='洲至奢选',
      rooms=201, suite=50.71, sale=61.15, du=29, s2=S2_CUT, s3=S3_039['B2'],
      s3_src='039 表04 单间造价＋表05 公区＋差额项重建', special=BRAND_SPECIAL_IHG,
      mkt=(900, 1050, 1200), src='洲际换牌档＋房量减半的规模溢价',
      note='面积完全达标；房量损失 50%'),
 dict(k='C1', nm='客房体量变化·重改·外部奢牌 3改2', grp='③体量变化·重改', b='外部奢牌',
      rooms=268, suite=38.03, sale=45.85, du=29, s2=S2_CUT, s3=S3_039['C1'],
      s3_src='039 表07 H11（S7 外部奢牌·重做·268）', special=BRAND_SPECIAL_IHG,
      mkt=(850, 1000, 1150), src='顶奢档（外部奢牌展示价锚）',
      note='顶奢单价最高；面积差 6.97 ㎡'),
]
for p in PATHS:
    p['dt'] = dt_calc(SCHED_PATH[p['k']]); p['du'] = int(round(p['dt']['total']))

for p in PATHS:
    B = BRANDS[p['b']]; p['tier']=B['tier']; p['fees']=B; p['brie']=B['note']; p['thr']=B['gate']
    p['capex'] = round(p['s2']+p['s3']+p['special'], 1)
    p['down_loss_econ'] = round(815.0*p['du'], 1)
    p['down_rigid'] = round(162.5*p['du'], 1)
    p['gate_gap'] = 0.0 if p['suite']>=p['thr'] else round(p['thr']-p['suite'], 2)
    p['gate'] = '达标' if p['suite']>=p['thr'] else '面积差 %.2f ㎡（需书面例外）'%p['gate_gap']

# ═══════ 6. 反事实臂：最小合规臂 ═══════
MIN_COMPLY = dict(rooms=402, adr=373.1, occ=0.7375, capex=S2_NO_CUT, du=15,
                  s2=S2_NO_CUT, s3=0.0, b='皇冠',
                  note='依法合规停业整改：仅段二机电管线隐蔽与消防；客房与公区不改造，产品力维持现状并逐年老化')
MIN_COMPLY['du'] = int(round(dt_calc(('最小合规','段二','不减房'))['total']))
RIGID_M = 162.5

# ═══════ 7. 现金流引擎 ═══════
RA = 0.08; OP_Y = 20
def arm_cash(p, adr, occ, capex=None, du=None, s3=None, new_equip=True,
             cf_decay=0.0, decay_start=1):
    """项目臂月度现金流。
       cf_decay: 年度经营现金流自然衰减（反事实臂用：无翻新导致的产品老化）；decay_start: 从第几年起
    """
    du = p['du'] if du is None else du
    F = p['fees']; cfs = []
    capex = p['capex'] if capex is None else capex
    s3 = p['s3'] if s3 is None else s3
    capm = capex/du
    for m in range(1, du+1): cfs.append((m, -capm - RIGID_M))
    for y in range(1, OP_Y+1):
        af, of = factors(y)
        room = p['rooms']*365*occ*adr*af/1e4
        # 非房收入：按开房率缩放 ＋ 房价联动（覆盖数随客流，非随房价）
        nonroom = (M['nonroom_base']*(occ/M['occ_now'])
                   * (1 + M['nonroom_link']*(adr/M['adr_now']-1)))
        R = room + nonroom
        goi = R*M['goi_rate']
        scale = (p['rooms']/402.0)**0.35
        var = M['var_rate']
        if new_equip:
            var = var - M['energy_rate']*(1-M['energy_new']) - M['pom_rate']*(1-M['pom_new'])
        unalloc = M['fixed_agit']*scale + R*var + R*F['uplift']
        adj_gop = goi - unalloc - R*F['lic']
        fee_inc = max(0.0, adj_gop)*F['inc']
        fee_other = R*F['ffe']
        cf = adj_gop - fee_inc - fee_other
        if cf_decay and y >= decay_start: cf *= ((1-cf_decay)**(y-decay_start+1))
        for k in range(12): cfs.append((du+(y-1)*12+k+1, cf/12.0))
    return cfs
def npv(cfs, r=RA):
    rm = (1+r)**(1/12.0)-1
    return sum(v/((1+rm)**m) for m, v in cfs)
def irr(cfs):
    lo, hi = -0.95, 5.0
    def g(r):
        rm = (1+r)**(1/12.0)-1
        return sum(v/((1+rm)**m) for m, v in cfs)
    if g(lo)*g(hi) > 0: return None
    for _ in range(200):
        mid=(lo+hi)/2
        if g(lo)*g(mid) <= 0: hi=mid
        else: lo=mid
    return (lo+hi)/2
def payback(cfs):
    cum=0.0
    for m,v in cfs:
        cum+=v
        if cum>=0 and m>0: return m/12.0
    return None
def bisect(fn, lo, hi, n=60, rev=False):
    flo, fhi = fn(lo), fn(hi)
    if flo*fhi > 0: return None
    for _ in range(n):
        mid=(lo+hi)/2.0; pos = fn(mid) > 0
        if rev:
            if pos: lo=mid
            else: hi=mid
        else:
            if pos: hi=mid
            else: lo=mid
    return (lo+hi)/2.0

# 最小合规臂（反事实）：段二已装、停业 15 月、402 间、ADR 373.1 逐年老化、2029 合同到期后加速
_p0 = dict(du=MIN_COMPLY['du'], fees=BRANDS[MIN_COMPLY['b']], rooms=MIN_COMPLY['rooms'],
           s3=0.0, s2=MIN_COMPLY['s2'], capex=MIN_COMPLY['capex'])
CF_CF = arm_cash(_p0, MIN_COMPLY['adr'], MIN_COMPLY['occ'], new_equip=True,
                 cf_decay=M['cf_degrade'], decay_start=1)
def inc_arm(p, adr, occ, **kw):
    c = arm_cash(p, adr, occ, **kw); b = dict(CF_CF)
    return [(m, v-b.get(m,0.0)) for m,v in c]

# ═══════ 8. 校核 ═══════
print()
print('=== 引擎校核 1：改造前实测复现（ADR 373.1 / OCC 73.75% / 满负荷 / 未换机电）===')
def _engine_check(adr, occ, new_equip):
    room = 402*365*occ*adr/1e4
    nonroom = M['nonroom_base']*(occ/M['occ_now'])*(1+M['nonroom_link']*(adr/M['adr_now']-1))
    R = room+nonroom
    goi = R*M['goi_rate']
    var = M['var_rate']
    if new_equip: var = var - M['energy_rate']*(1-M['energy_new']) - M['pom_rate']*(1-M['pom_new'])
    ua = M['fixed_agit'] + R*var
    adj = goi - ua - R*0.020
    inc = max(0.0, adj)*0.050
    return R, goi, adj, inc, adj-inc
_R,_G,_A,_I,_C = _engine_check(373.1, 0.7375, False)
print('  模型总收入 %.1f（实测 %.2f，误差 %.2f%%）｜GOI %.1f（实测 %.2f）' % (_R,M['total_rev'],abs(_R/M['total_rev']-1)*100,_G,M['total_rev']*M['goi_rate']))
print('  模型 Adjusted GOP %.1f（实测 %.2f，误差 %.2f%%）｜激励费 %.1f（实测 %.2f）' % (_A,M['adj_gop'],abs(_A/M['adj_gop']-1)*100,_I,M['inc_fee']))
print('  模型项目口径经营现金流 %.1f（实测 %.1f，误差 %.2f%%）✔' % (_C,M['cf_pre_project'],abs(_C/M['cf_pre_project']-1)*100))
print('=== 引擎校核 2：最小合规臂（反事实）===')
print('  停业 %d 月｜段二投资 %.0f 万元｜复业 ADR %.1f，年衰减 %.0f%%（2029 合同到期后另计加速）' % (
    MIN_COMPLY['du'], MIN_COMPLY['capex'], MIN_COMPLY['adr'], M['cf_degrade']*100))
print('  20 年反事实臂 NPV（项目口径）%.0f 万元｜首年经营现金流 %.0f 万元' % (
    npv(CF_CF), sum(v for m,v in CF_CF if m>MIN_COMPLY['du'] and m<=MIN_COMPLY['du']+12)))

# ═══════ 9. 主计算 ═══════
print()
print('=== 路径与造价（039 原值，万元）===')
print('%-3s %-26s %-9s %4s %4s %8s %8s %8s %9s %9s' % (
    '#','路径','档次','房量','停业','段二','段三','品牌专项','改造投资','停业损失(经济)'))
for p in PATHS:
    print('%-3s %-26s %-9s %4d %4d %8.0f %8.0f %8.0f %9.0f %9.0f' % (
        p['k'], p['nm'], p['tier'], p['rooms'], p['du'], p['s2'], p['s3'], p['special'],
        p['capex'], p['down_loss_econ']))
print()
print('=== 市场分析价格下的 20 年结果（OCC 75%）===')
print('%-3s %-26s %-3s %5s %10s %10s %8s %8s %8s' % (
    '#','路径','档','ADR','项目NPV','增量NPV','IRR全','IRR增','回收增'))
RES=[]; GRID={}; GRID_INC={}
for p in PATHS:
    for lbl, adr in zip(('低','中','高'), p['mkt']):
        c = arm_cash(p, adr, 0.75); ic = inc_arm(p, adr, 0.75)
        full=npv(c); inc=npv(ic); ir=irr(c); iri=irr(ic); pb=payback(ic)
        RES.append(dict(k=p['k'],lbl=lbl,adr=adr,full=full,inc=inc,irr=ir,irr_inc=iri,pb=pb))
        print('%-3s %-26s %-3s %5d %10.0f %10.0f %8s %8s %8s' % (
            p['k'],p['nm'],lbl,adr,full,inc,('%.2f%%'%(100*ir)) if ir else '为负',
            ('%.2f%%'%(100*iri)) if iri else '为负', ('%.1f年'%pb) if pb else '>20'))
    print()
print('=== 反算一：盈亏平衡点（OCC 75%，NPV=0 的 ADR）===')
print('%-3s %-26s %8s %9s %9s %9s' % ('#','路径','平衡ADR全','折元/㎡夜','平衡ADR增','折元/㎡夜'))
BE={}
for p in PATHS:
    bf = bisect(lambda x: npv(arm_cash(p,x,0.75)), 100.0, 8000.0)
    bi = bisect(lambda x: npv(inc_arm(p,x,0.75)), 100.0, 8000.0)
    BE[p['k']]=dict(be_full=bf, be_inc=bi)
    print('%-3s %-26s %8s %9s %9s %9s' % (p['k'],p['nm'],
      ('%d'%bf) if bf else '不可达', ('%.1f'%(bf/p['sale'])) if bf else '—',
      ('%d'%bi) if bi else '不可达', ('%.1f'%(bi/p['sale'])) if bi else '—'))
print()
print('=== 反算二：投资承受力（按市场分析价格，NPV=0 的最大改造投资）===')
print('%-3s %-26s %-3s %5s %10s %11s %11s %10s' % (
    '#','路径','档','ADR','估算改造投资','全口径上限','增量上限','增量缺口'))
CAP={}
for p in PATHS:
    CAP[p['k']]={}
    for lbl, adr in zip(('低','中','高'), p['mkt']):
        def gf(x, adr=adr):
            return npv(arm_cash(p,adr,0.75,capex=x,s3=max(0.0,x-p['s2']-p['special'])))
        def gi(x, adr=adr):
            return npv(inc_arm(p,adr,0.75,capex=x,s3=max(0.0,x-p['s2']-p['special'])))
        cf_ = bisect(gf, 3000.0, 150000.0, rev=True); ci_ = bisect(gi, 3000.0, 150000.0, rev=True)
        CAP[p['k']][lbl]=dict(cap_full=cf_, cap_inc=ci_)
        gap = (p['capex']-ci_) if ci_ else None
        print('%-3s %-26s %-3s %5d %10.0f %11s %11s %10s' % (
            p['k'],p['nm'],lbl,adr,p['capex'],('%.0f'%cf_) if cf_ else '不可达',
            ('%.0f'%ci_) if ci_ else '不可达', ('%.0f'%gap) if gap is not None else '—'))
    print()
print('=== 反算三：平衡点左右的指标阈值区间 ===')
THR=[]
for p in PATHS:
    be = BE[p['k']]['be_full']
    if not be: THR.append(dict(k=p['k'],be=None,rows=[])); continue
    def cap_npv(x): return npv(arm_cash(p,be,0.75,capex=x,s3=max(0.0,x-p['s2']-p['special'])))
    rows=[('改造投资 −20%',cap_npv(p['capex']*0.80)),('改造投资 −10%',cap_npv(p['capex']*0.90)),
          ('改造投资 ＋10%',cap_npv(p['capex']*1.10)),('改造投资 ＋20%',cap_npv(p['capex']*1.20)),
          ('开房率 −5pp',npv(arm_cash(p,be,0.70))),('开房率 ＋5pp',npv(arm_cash(p,be,0.80))),
          ('停业期 −3 月',npv(arm_cash(p,be,0.75,du=p['du']-3))),
          ('停业期 ＋3 月',npv(arm_cash(p,be,0.75,du=p['du']+3))),
          ('ADR −10%',npv(arm_cash(p,be*0.90,0.75))),('ADR ＋10%',npv(arm_cash(p,be*1.10,0.75)))]
    THR.append(dict(k=p['k'],be=be,rows=rows))
    print('%-3s %-26s 平衡 ADR %d' % (p['k'],p['nm'],be))
    for n,v in rows: print('      %-16s NPV %+9.0f' % (n,v))
    print()
print('=== 15 格动态区间（3 档价格 × 5 档开房率）项目口径 NPV（百万元）===')
for p in PATHS:
    print('  %-3s %-26s' % (p['k'],p['nm']))
    print('      价\\率  ' + '  '.join('%6d%%'%(o*100) for o in (0.65,0.70,0.75,0.80,0.85)))
    for lbl, adr in zip(('低','中','高'), p['mkt']):
        row=[]; irow=[]
        for o in (0.65,0.70,0.75,0.80,0.85):
            row.append(round(npv(arm_cash(p,adr,o)),1))
            irow.append(round(npv(inc_arm(p,adr,o)),1))
        GRID.setdefault(p['k'],[]).append((lbl,adr,row))
        GRID_INC.setdefault(p['k'],[]).append((lbl,adr,irow))
        print('      %s档%5d 全口径 ' % (lbl,adr) + '  '.join('%8.1f'%(v/1000.0) for v in row)
              + '   增量 ' + '  '.join('%8.1f'%(v/1000.0) for v in irow))
    print()
json.dump(dict(P=[{k:v for k,v in p.items() if k!='fees'} for p in PATHS], RES=RES, M=M, SCHED26={'%s|%s|%s'%k:v for k,v in SCHED26.items()},
  DU_BY_CFG={'%s|%s|%s'%kk:int(round(dt_calc(kk)['total'])) for kk,vv in SCHED26.items()},
  BE=BE, CAP=CAP, THR=THR, GRID=GRID, GRID_INC=GRID_INC, CF_CF=CF_CF, MIN_COMPLY=MIN_COMPLY,
  BRANDS={'%s'%k:dict(v) for k,v in BRANDS.items()},
  S3_039=S3_039, S5_DIFF=S5_DIFF, S5_ROOM=S5_ROOM, S5_PUB=S5_PUB,
  PARAMS=dict(RA=RA, OP_Y=OP_Y, RIGID_M=RIGID_M, CYCLE=CYCLE,
   S2_NO_CUT=S2_NO_CUT, S2_CUT=S2_CUT, BRAND_SPECIAL_IHG=BRAND_SPECIAL_IHG,
   BRAND_SELF_SYS=BRAND_SELF_SYS, ENERGY_NEW=M['energy_new'], POM_NEW=M['pom_new'],
   NONROOM_LINK=M['nonroom_link'])),
  open(os.path.join(T,'v26a.json'),'w',encoding='utf-8'),ensure_ascii=False,default=str)
print('saved v26a.json')
