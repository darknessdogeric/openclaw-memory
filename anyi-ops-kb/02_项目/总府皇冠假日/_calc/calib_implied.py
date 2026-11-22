# -*- coding: utf-8 -*-
"""口径再校正：集团口径 = 改造后绝对现金流 ÷ 改造投资
   → 集团 17%/5.6% 隐含平均房价约 1,160 元（远高于市场锚点）
   → 按集团自身算法，方向一回收期 9 年，四个方向均未落入 5-8 年
"""

# 集团口径反推（用 D1 的费用结构反解）
ROOMS_D1 = 402
OCC = 0.70
NONROOM = 1.42
GOP_RATE = 0.293
FEES = 0.020 + 0.030 + 0.020 + 0.000 + 0.020   # 基础费+营销+忠诚+预订+FF&E储备
INCENTIVE = 0.06
OWNER_COEF = GOP_RATE - FEES - GOP_RATE * INCENTIVE   # 业主经营利润 / 营业收入

GROUP_INV = 18000.0
GROUP_PB = 5.6
GROUP_IRR = 0.17

def irr_level(target, inv, n=20):
    lo, hi = 0.0, inv * 3
    for _ in range(200):
        mid = (lo + hi) / 2
        cf = [-inv] + [mid] * n
        def f(r): return sum(c / (1 + r) ** i for i, c in enumerate(cf))
        a, b = f(-0.9), f(3.0)
        # 二分求 IRR
        l2, h2 = -0.9, 3.0
        if f(l2) * f(h2) > 0:
            hi = mid; continue
        for _ in range(200):
            m2 = (l2 + h2) / 2
            if f(l2) * f(m2) <= 0: h2 = m2
            else: l2 = m2
        if (l2 + h2) / 2 < target: lo = mid
        else: hi = mid
    return (lo + hi) / 2

CF_BY_PB = GROUP_INV / GROUP_PB                 # 3,214 万/年
CF_BY_IRR = irr_level(GROUP_IRR, GROUP_INV)     # 约 3,198 万/年
CF_AVG = (CF_BY_PB + CF_BY_IRR) / 2

REV_NEEDED = CF_AVG / OWNER_COEF                # 所需营业收入
ROOM_REV_NEEDED = REV_NEEDED / NONROOM
ADR_NEEDED = ROOM_REV_NEEDED * 1e4 / (ROOMS_D1 * 365 * OCC)
ADR_NEEDED_430 = ROOM_REV_NEEDED * 1e4 / (430 * 365 * OCC)

# 本次测算 D1 实际
D1_REV = 10938.7
D1_OWNER = 2028.3
D1_ADR = 750.0
D1_CAPEX = 14401.0
D1_GROUP_CAL_PB = D1_CAPEX / (D1_OWNER / (D1_REV / (D1_OWNER / OWNER_COEF)))  # 集团可比口径（无爬坡）

OUT = dict(
    owner_coef=round(OWNER_COEF, 5),
    cf_by_pb=round(CF_BY_PB, 1), cf_by_irr=round(CF_BY_IRR, 1), cf_avg=round(CF_AVG, 1),
    rev_needed=round(REV_NEEDED, 1), room_rev_needed=round(ROOM_REV_NEEDED, 1),
    adr_needed_402=round(ADR_NEEDED, 0), adr_needed_430=round(ADR_NEEDED_430, 0),
    d1_rev=D1_REV, d1_owner=D1_OWNER, d1_adr=D1_ADR,
    d1_group_cal_pb=round(D1_CAPEX / (D1_OWNER / OWNER_COEF), 1),
    gap_cf=round(CF_AVG - D1_OWNER, 1),
)

if __name__ == "__main__":
    for k, v in OUT.items():
        print("%-18s %s" % (k, v))
