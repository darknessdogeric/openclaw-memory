# -*- coding: utf-8 -*-
"""合并 v1.3：Eric 版（酒店经营指标维度）＋ 集团口径三段式修正 ＋ 公式与房量补正"""
import os
from copy import copy
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

SRC = r"C:\Users\ericz\Desktop\一企一策分析表_管理建议修订版_v1.2_含酒店经营指标维度_2026-11-12.xlsx"
OUT = r"C:\Users\ericz\Desktop\一企一策分析表_管理建议修订版_v1.3_合并集团口径_2026-11-12.xlsx"
FONT = '等线'; NAVY = '1F3864'
thin = Side(style='thin', color='BFBFBF'); BD = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = openpyxl.load_workbook(SRC)
ws = wb["一企一策测算表"]
wsi = wb["酒店经营指标"]

# 列位（Eric 版）：3业态 4我的建议 5调整类型 6依据 7优先序 8投资额回收期 9缺口 10原建议
# 16财务费用(N) 23EBITDA(U) 32经营现金流(AF) 35可售房数 36RGI 37回收期 38回收期依据
C_CF, C_EBITDA, C_FIN = 32, 23, 16
C_ROOMS = 35

# ============ 1. 修正经营现金流公式：EBITDA − 财务费用（=U-N），原表口径 ============
fixed = 0
for r in range(2, 30):
    if not ws.cell(r, 2).value:
        break
    u = ws.cell(r, C_EBITDA).value
    n = ws.cell(r, C_FIN).value
    cell = ws.cell(r, C_CF)
    if isinstance(u, (int, float)) and isinstance(n, (int, float)):
        cell.value = "=U{0}-N{0}".format(r)
        fixed += 1
    else:
        cell.value = "待补（缺 EBITDA 或财务费用）"
print("经营现金流公式修正行数:", fixed)

# ============ 2. 补可售房数缺口（KB《安逸集团酒店名录三表内化 v1.0》2026-09-16）============
ROOM_SRC = {
    "新良宾馆": (345, "KB 酒店名录三表 v1.0：新良大酒店 345 间（2026-09-16）"),
    "梦温泉": (101, "KB 酒店名录三表 v1.0：雅安梦温泉酒店 101 间（2026-09-16）"),
}
for r in range(2, 30):
    nm = ws.cell(r, 2).value
    if not nm:
        break
    if nm in ROOM_SRC and not ws.cell(r, C_ROOMS).value:
        cnt, src = ROOM_SRC[nm]
        ws.cell(r, C_ROOMS).value = cnt
        print("  补房量:", nm, cnt)
# 同步到经营指标表
for r in range(2, wsi.max_row + 1):
    nm = wsi.cell(r, 2).value
    if nm in ROOM_SRC:
        cnt, src = ROOM_SRC[nm]
        wsi.cell(r, 4).value = cnt
        wsi.cell(r, 5).value = src

# ============ 3. 集团口径：三段式修正（对齐 11-11 资产经营策略研讨会）============
FIX = {
    "华龙宾馆": (
        "第一选项自营：按12万元/间投入标准测算，目标把4000㎡房产租金挣回来并覆盖利息与折旧摊销；现账上单房造价30万元远超标准，须先做减值处理。第二选项出租80万元/年。第三选项整体转让。落脚点是自营要达到什么效果、差在哪、怎么补，不是直接提卖",
        "★ 集团口径：算账不是要卖要租，是给运营提要求（11-11 资产经营策略研讨会）＋范式校验出资产负债率203.2%与改造建议自相矛盾",
        "按12万元/间标准测算GOP与租金缺口，装修须先减值",
        "负债284.79万元、净资产-144.66万元"),
    "蒙顶山茶业": (
        "茶叶贸易业务退出止损（2025年亏700多万元、5月即应关停，属有令不行）；茶业主体仍须有2027年EBITDA转正、2028年经营现金流转正、2029年利润总额转正三段目标，达不到则整体出租100万元/年、租不出则关停处置；16.65万㎡土地另行论证开发路径（含与商投甄选新零售合作）；安逸茶山已申报省级补贴1200万元，转入业态落地",
        "★ 全表最大一处价值低估：16.65万㎡土地被一句“出租100万元”带过；实缴2.03亿元却做年营收1130万的茶叶贸易。表述按集团三段式口径改写",
        "茶叶贸易关停节约与土地开发前期投入待测算",
        "累计亏损-1.09亿元"),
    "天府山庄": (
        "第一选项自营或联合开发：作为在建与待开发载体，与东部新区、体育学院、西藏航空路径统筹，目标覆盖利息并实现资产增值。第二选项出租168万元/年。第三选项整体转让，底价8967万元。土地5.92万㎡、房产5122.99㎡，出租价明显低于土地价值",
        "★ 正在谈的旗舰项目载体（藏航/悦榕/体院三路径），不能按闲置资产处理；表述按集团三段式口径改写",
        "联合开发前期投入与覆盖利息测算待补",
        "不适用"),
    "梦温泉": (
        "第一选项自营或合作开发：土地3.78万㎡、房产3945.01㎡，地价与售房价倒挂，优先论证与雅安文旅集团等的合作开发。第二选项出租50万元/年。第三选项整体转让1300万元。集团“不要把鸡蛋放在一个篮子里”，改造类试点与合作开发试点均保留",
        "土地3.78万㎡、整包卖1300万元地价倒挂；表述按集团三段式口径改写",
        "合作开发前期投入待测算",
        "不适用"),
    "花园宾馆": (
        "改造调整为分步实施：先公区与客房段、投后复评，不与新良同批全量改造；EBITDA-241.74万元、ROE-39.2%为四家标杆中经营最弱，但集团明确标杆具社会与政治效益（把花园做亮可获国资委、省委、省政府支持），故不宜排末位，改造前须提交增量与回收期测算",
        "与深圳川宾、新良同为标杆却未排序，条件差异极大；且标杆的政治价值不能仅按 EBITDA 排序",
        "须提交改造投资额与回收期测算",
        "不适用"),
}
ORDER = {"新良宾馆": "1", "深圳川宾": "2", "花园宾馆": "3", "乐山嘉州": "4", "金桥宾馆": "5"}
for r in range(2, 30):
    nm = ws.cell(r, 2).value
    if not nm:
        break
    if nm in FIX:
        sug, why, inv, gap = FIX[nm]
        ws.cell(r, 4).value = sug
        ws.cell(r, 6).value = why
        ws.cell(r, 8).value = inv
        ws.cell(r, 9).value = gap
    if nm in ORDER:
        ws.cell(r, 7).value = ORDER[nm]
    # 依据列若含原优先序表述，同步更新
    if nm == "乐山嘉州":
        ws.cell(r, 4).value = ("维持分年度转正路线图不变；同步纳入嘉州区域（峨眉山、乐山）定价与渠道联动，"
                              "单店改善幅度有限；ROE口径须写明分母为平均净资产")
    if nm == "金桥宾馆":
        ws.cell(r, 4).value = ("转正节奏调整为2027年淡季止损、旺季保本、2028年GOP转正；96间房、年收入仅313.77万元"
                              "且西昌季节性极强，评估改作夏半年产品，不作重投")
        ws.cell(r, 7).value = "5"

# ============ 4. 人工成本率口径失真标注（分母近零）============
for r in range(2, wsi.max_row + 1):
    nm = wsi.cell(r, 2).value
    if nm in ("亚丁宾馆", "梦温泉"):
        wsi.cell(r, 8).value = "口径失真（分母营收近零），不可用于横向比较"
        wsi.cell(r, 23).value = (str(wsi.cell(r, 23).value or "") + " ｜ 人工成本率失真：营收近零致比值畸高")

# ============ 5. RGI 量化结论（补进改造回收期依据列）============
RGI_CONC = {
    "国堰酒管": "★ RGI 56.2：RevPAR 80.4 对 四川四星 2024（ADR 281／OCC 50.8%／RevPAR 143）需提 78%。"
               "解法是提效（保档次、提 OCC 与 ADR 到四川四星水平），不是像花园那样重做——国堰全店营收 1431 万中餐饮占 44%，RevPAR 看不到第二台发动机，须同时看 TRevPAR 与餐饮会议收入",
    "花园宾馆": "★ RGI 32：RevPAR 103.76 对 春熙路 6 家竞品均值（OCC 80%／ADR 400／RevPAR 320）需提 208%。"
               "解法是重做（改造投资 3000 万／174 间＝17.2 万每间，增量 GOP 576.3 万，静态回收期 5.2 年；含爬坡与停业期 583 万为 6.0 年）。"
               "与国堰同属四星但 RGI 差 24 个点，两者的改造逻辑不同，不能同一套方案",
}
for r in range(2, 30):
    nm = ws.cell(r, 2).value
    if not nm:
        break
    if nm in RGI_CONC:
        ws.cell(r, 38).value = RGI_CONC[nm]

# ============ 6. 修订汇总追加集团口径段 ============
s2 = wb["修订汇总"]
r0 = s2.max_row + 2
add = [
    ("=== 11-12 集团口径校准 ===", "", ""),
    ("★ 公式纠正", "经营现金流 = EBITDA − 财务费用",
     "1107 原件第 25 列公式为 =P-I（P=第16列EBITDA、I=第9列财务费用），与 11-11 审计治理会议“经营利润必须覆盖利息”口径一致，本就正确；"
     "24/28 行 #VALUE! 源于 v1.1 用 insert_cols 插列导致引用平移错位（v1.1 的缺陷）；v1.2 改为 =W-P（人工成本−财务费用）口径仍错且未解决空值。"
     "v1.3 已统一改回 =U-N（EBITDA−财务费用），并对 EBITDA/财务费用缺失行标注“待补”"),
    ("★ 已用集团口径反校验", "股东回报要求 = 实缴资本 × 3.5%",
     "14 家逐行吻合（安逸本部 215336.35×3.5%=7536.77；古尔沟 970.71；总府皇冠 1111.16；新良 31.5；花园 20.48）；"
     "股东投资损益 = 利润总额 − 股东回报要求 亦逐行吻合（总府 −2469.68−1111.16=−3580.84；古尔沟 −5398−970.71=−6368.71；新良 471.04−31.5=439.54）"),
    ("★ 出售价/出租价来源", "资产部已评估值；未评估按同等地段市场价测算", "会议 A 第 197 行；本表第 20/21 列口径已确认"),
    ("★ 三选项框架（上位方法）", "①自营（从出租算、从卖资产算倒逼目标）②达不到则出租③出租还不行才卖掉",
     "会议 B。落脚点是“我们怎么经营好”，不是“卖不卖”——v1.3 已把华龙、蒙顶山茶业、天府山庄、梦温泉四条改为三段式表述"),
    ("★ 装修减值口径（新增维度）", "当时让你管，投入标准 12 万/间，实际投 30 万/间——“神仙也做不回来”",
     "按 12 万算运营做得到，按账上 30 万做不出来 ⇒ 是历史资产问题，该做减值，不是经营团队的问题。会议 B"),
    ("★ 标杆的政治价值", "把花园做得很亮，“国资委、省委、省政府会大力支持”",
     "会议 B。故花园不能仅按 EBITDA 排末位，同策略内优先序调整为 新良1／深圳川宾2／花园3／乐山嘉州4／金桥5"),
    ("★ 聚焦赛道", "“我们什么都想去做一下，结果啥也没做。绝对做不了全赛道……跟地方政府谈、跟国资谈，民营的不用花精力”",
     "会议 B。对应轻资产拓展的主战场选择"),
]
for i, (a, b, c) in enumerate(add):
    rr = r0 + i
    ca = s2.cell(rr, 1, a); cb = s2.cell(rr, 2, b); cc = s2.cell(rr, 3, c)
    ca.font = Font(name=FONT, size=10, bold=True, color='1F3864')
    ca.alignment = Alignment(horizontal='left', vertical='top')
    cb.font = Font(name=FONT, size=10, bold=True)
    cb.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
    cc.font = Font(name=FONT, size=9)
    cc.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
    ca.border = BD; cb.border = BD; cc.border = BD

wb.save(OUT)
print('SAVED:', OUT, os.path.getsize(OUT))
