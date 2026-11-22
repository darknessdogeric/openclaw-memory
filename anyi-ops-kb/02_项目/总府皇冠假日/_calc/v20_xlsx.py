# -*- coding: utf-8 -*-
"""v20：测算附表 v2.0 —— 去额度参照系、加三情景与前置条件表、更新大数对照表与风险登记册"""
import io, os, sys, re, json, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v20.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

RES = {x["key"]: x for x in json.load(open(os.path.join(T, "v9.json"), encoding="utf-8"))}
ECON = {x["dk"]: x for x in json.load(open(os.path.join(T, "v10_econ.json"), encoding="utf-8"))}
SC = json.load(open(os.path.join(T, "v18.json"), encoding="utf-8"))
A, B, C = SC["A"], SC["B"], SC["C"]
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return ("%.2f%%" % (v*100)) if v is not None else "无可解内部收益率"

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
OLD = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v1.0_2026-11-14.xlsx")
NEW = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v2.0_2026-11-14.xlsx")
wb = load_workbook(OLD)
THIN = Side(style="thin", color="BFBFBF"); BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BOLD = Font(bold=True); T13 = Font(bold=True, size=13)
BAD = PatternFill("solid", fgColor="FFC7CE"); HD = PatternFill("solid", fgColor="D9E2F3")
def hd(ws, r, hs, widths=None):
    for i, h in enumerate(hs, 1):
        c = ws.cell(row=r, column=i, value=h); c.font = BOLD; c.fill = HD; c.border = BD
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    if widths:
        for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = ws.cell(row=r+1, column=1)
    return r + 1
def put(ws, r, vs, fm=None, fl=None):
    from openpyxl.styles import Font as _F
    from openpyxl.styles.fills import Fill as _Fi
    for i, v in enumerate(vs, 1):
        c = ws.cell(row=r, column=i, value=v); c.border = BD
        if fm and i <= len(fm) and fm[i-1]: c.number_format = fm[i-1]
        if fl and i <= len(fl) and fl[i-1]:
            o = fl[i-1]
            if isinstance(o, _F): c.font = o
            elif isinstance(o, _Fi): c.fill = o
    return r + 1

# ══ 01 大数对照表：整体重写（去额度参照系，加前置条件与三情景）══
del wb["01 报告大数对照表"]
ws = wb.create_sheet("01 报告大数对照表", 0)
ws["A1"] = "报告正文大数与测算来源对照表"; ws["A1"].font = T13
ws["A2"] = "每一条正文数字均可回溯到本表；本表数字取自 02—15 各表"
r = 4
r = hd(ws, r, ["报告位置","正文大数","数值","来源表","口径说明"], [30, 40, 20, 24, 58])
M = [
 ("第一章（一）项目概况","改造投资区间","17,995.6—56,850.9 万元","08 / 14","随情景与方案变化"),
 ("第一章（一）项目概况","停业损失区间","6,520—16,300 万元","03 / 14","815 万元每月，随停业月数变化"),
 ("第一章（一）项目概况","项目总资金需求","24,515.6—73,150.9 万元","08 / 14","改造投资加停业损失"),
 ("第一章（一）前置条件","第三方安全评估结论","认定整体改造／可分段／可维持三种情形","14 三情景与前置条件","**结论决定投资规模与项目性质**"),
 ("第一章（三）背景","改造前年均经营现金流","−1,924 万元","10 三口径对照","业主口径实测，改造前为负"),
 ("第一章（三）背景","审计标准符合性","95.92% → 69.6%","12 参数与假设","2024—2026 三年品牌方审计"),
 ("第二章（二）商圈","酒店密度","1.5 平方公里 134 家，超高端 3 家","13 数据源","居舍、君悦、尼依格罗"),
 ("第二章（三）价格空间","现状每间可售房收入","257.6 元，为全市高端 834 元的 31%","13 数据源","STR 2024 全市高端平均"),
 ("第二章（四）在营项目","2026 年新开","兰博基尼 168 间、丽笙精选 178 间","13 数据源","2026-03-28 / 2026-06-16 开业"),
 ("第四章（二）实物条件","建筑总面积","69,026.08 ㎡","02 面积底稿","地上 58,064.43、地下 8,611.20"),
 ("第四章（二）实物条件","客房套内面积","10,192 ㎡，平均 25.35 ㎡/间","02 面积底稿","客房物理 415 间、在售 402 间"),
 ("第四章（三）面积结论","减房后建面","约 84.5 ㎡/间","02 面积底稿","客房层 22,645.47 ㎡ ÷ 268 间"),
 ("第五章（一）前置条件","评估范围","消防、机电设备、结构三方面","14 三情景与前置条件","与本次实测问题一一对应"),
 ("第五章（四）方案比选","基准方案 S1 改造投资","21,313.6 万元","08 八方案造价总表","内部收益率 4.60%，集团口径回收 10.15 年"),
 ("第五章（四）方案比选","S4 换牌增量代价","9,322.1 万元","08 八方案造价总表","段三 +6,877.1 ＋ 段一 +2,445"),
 ("第五章（五）可保留项","节约额","4,538.7 万元，占装修 44.3%","07 可保留项与节约","相对同品牌同房量拆除重做基准"),
 ("第六章（三）关键读数","段二品牌无关","11,060（不减房）／11,600（3改2）","04 段二机电水电强弱电","43 项基础 9,000 ＋ 实测修正 2,060"),
 ("第九章（三）财务指标","全口径内部收益率","S1 4.60%／S4 6.13%","10 三口径对照","其余方案 1.35% 至 −4.08%"),
 ("第九章（四）评价结论","参照回收期 5—8 年","S4 8.96 年／S1 10.15 年","10 三口径对照","八个方案无一落入"),
 ("第九章（五）达标所需房价","8 年／6 年／5 年隐含平均房价","985／1,314／1,576 元","14 三情景与前置条件","为 2024 全市高端 834 元的 1.18／1.57／1.89 倍"),
 ("第九章（六）三情景","情形二 段二压缩","7,742 万元，停业 8 个月","14 三情景与前置条件","参数化示例，区间须以评估结论替换"),
 ("第九章（六）三情景","情形三 局部整改","4,584 万元，不停业","14 三情景与前置条件","5 年净现值 −12,266 万元，劣于不改造 −7,682 万元"),
 ("第九章（七）敏感性","改造投资 ±15%","4.52%—4.68%","11 敏感性","最大敏感因子"),
 ("第十一章 风险","风险项数","18 项","12 参数与假设","R-01 前置条件未落实为首要风险"),
]
for row in M:
    r = put(ws, r, list(row))

# ══ 08 八方案造价总表：删「相对集团 1.8 亿额度」列 ══
ws8 = wb["08 八方案造价总表"]
hdr_r = None
for rr in range(1, 8):
    if ws8.cell(row=rr, column=1).value == "方案":
        hdr_r = rr; break
last_col = ws8.max_column
if hdr_r and ws8.cell(row=hdr_r, column=last_col).value and "额度" in str(ws8.cell(row=hdr_r, column=last_col).value):
    ws8.delete_cols(last_col)
    L("[XLS] 08 表已删额度列")
# 删表下说明中的参照系
for rr in range(hdr_r + 1, ws8.max_row + 1):
    v = ws8.cell(row=rr, column=1).value
    if isinstance(v, str) and ("集团" in v and "六家" in v):
        ws8.cell(row=rr, column=1, value="读法：段二在八方案间几乎不变（品牌无关），段一是随停业月数变化的硬支出，段三才是品牌决策变量。「换品牌」的真实代价＝段三增加额＋段一停业延长额，而非总投资差额。")
        L("[XLS] 08 表说明已改")

# ══ 12 参数与假设：风险登记册 R-03 替换 ══
ws12 = wb["12 参数与假设"]
for rr in range(1, ws12.max_row + 1):
    if str(ws12.cell(row=rr, column=1).value) == "R-03":
        ws12.cell(row=rr, column=2, value="第三方安全评估结论不及预期（认定可维持经营条件），导致本报告投资规模高估、方案不成立")
        ws12.cell(row=rr, column=3, value="高")
        ws12.cell(row=rr, column=4, value="高")
        ws12.cell(row=rr, column=6, value="先行委托评估，作为第一优先动作；同步准备情形三的局部整改方案")
        ws12.cell(row=rr, column=7, value="产业发展部")
        L("[XLS] 12 表 R-03 已替换")
        break
# 追加 R-19
rr = ws12.max_row + 1
for v in ("R-19", "评估结论与设计方案在实施中不一致", "低", "高", "中", "评估结论须写入设计任务书，方案变更须重新评估", "工程部、产业发展部"):
    pass
put(ws12, rr, ["R-19", "评估结论与设计方案在实施中不一致", "低", "高", "中", "评估结论须写入设计任务书，方案变更须重新评估", "工程部、产业发展部"])

# ══ 新增 14 三情景与前置条件 ══
if "14 三情景与前置条件" in wb.sheetnames:
    del wb["14 三情景与前置条件"]
ws = wb.create_sheet("14 三情景与前置条件")
ws["A1"] = "前置条件：第三方安全评估结论 → 三情景方案空间与财务含义"; ws["A1"].font = T13
ws["A2"] = "第三方安全评估（消防、机电设备、结构）认定结论是本项目成立与否的第一层条件；三种情形下投资规模与项目性质完全不同"
r = 4
r = put(ws, r, ["【一】评估范围与本次实测问题对应"])
ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["评估方面","本次论证对应的实测问题"], [20, 120])
for a, b in [
 ("消防","喷淋管网 1994 年；报警线路 1996 年且绝缘值严重不达标；报警主机 2026-07 全面瘫痪；气体灭火仅 1 套；消防水炮 0 台；台账年份矛盾（2024-06 对 2018-06）"),
 ("机电设备","4 台约克离心机 1996 年；锅炉 2009 年设计 15 年；发电机 1996 年；低压柜 34 面与电容柜 9 面 1996 年；排污泵 14 台 1996 年且 1 台已坏；排污管内壁锈蚀 90%；储油设施已按市政要求拆除"),
 ("结构与竖井","1996 年各机电系统同竖井叠加，竖井须分层重排"),
]:
    r = put(ws, r, [a, b])
r += 1
r = put(ws, r, ["【二】三种认定结论与项目含义"])
ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["情形","评估结论","对项目的含义","改造投资（万元）","停业月数","总资金需求（万元）","S1 全口径内部收益率","S4 全口径内部收益率"],
       [10, 30, 42, 18, 11, 18, 16, 16])
r = put(ws, r, ["情形一", "认定消防与机电设备现状已无法满足经营条件与标准要求，须整体改造",
                "第五章至第九章全部结论适用", 21313.6, 12, 31093.6, P(A["S1"]["irr20"]), P(A["S4"]["irr20"])],
        ["General","General","General","#,##0.0","0","#,##0.0","0.00","0.00"])
r = put(ws, r, ["情形二", "认定部分系统须整体更换、部分可延寿并分段实施",
                "段二与停业月数同步下降；参数化区间，区间取值须以评估结论替换，本报告不预设结论",
                17995.6, 8, 24515.6, P(B["S1"]["irr20"]), P(B["S4"]["irr20"])],
        ["General","General","General","#,##0.0","0","#,##0.0","0.00","0.00"])
r = put(ws, r, ["情形三", "认定现状可通过维修与局部更换维持经营条件与标准要求",
                "整体改造前提消失，仅保留必要局部整改 4,584.0 万元，可分区实施不停业",
                4584.0, 0, 4584.0, "不适用（方案不成立）", "不适用（方案不成立）"],
        ["General","General","General","#,##0.0","0","#,##0.0","General","General"])
r += 1
r = put(ws, r, ["情形二取值依据：段二按可压缩 30% 计（2024 底稿部分系统按整体更换口径列支，而第二批次台账显示 1#—8# 电梯已于 2022—2026 更换、部分给排水与配电设备服役状态优于预期）；停业月数由 12 个月压缩至 8 个月，对应分段实施。"])
r += 1
r = put(ws, r, ["【三】达标所需房价的自证分析（不依赖任何投资计划）"])
ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["目标回收期（年）","所需业主年度经营利润（万元）","所需营业收入（万元）","隐含平均房价（元/间/晚）","相当于 2024 成都全市高端 834 元的倍数"],
       [16, 26, 22, 22, 30])
for yrs, o, rv, ad in [(8, 2664.2, 14368.9, 985), (6, 3552.3, 19157.9, 1314), (5, 4262.7, 22989.5, 1576)]:
    r = put(ws, r, [yrs, o, rv, ad, round(ad/834.0, 2)],
            ["0","#,##0.0","#,##0.0","#,##0","0.00"])
r += 1
r = put(ws, r, ["结论：靠提价实现 5—8 年回收期在当前市场条件下不成立。8 年反解隐含平均房价 985 元已高于全市高端 834 元，而 834 元的每间可售房收入还建立在 100% 满房倒算基础上（行业实际出租率 67.5%）。现实路径是降本与缩短停业期。"])
ws.cell(row=r-1, column=1).font = BOLD
r += 1
r = put(ws, r, ["【四】情形三：必要局部整改明细（万元）"])
ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["项目", "金额（万元）", "说明"], [60, 16, 60])
for nm, v in C["items"]:
    r = put(ws, r, [nm, v, ""], ["General","#,##0","General"])
r = put(ws, r, ["合计", C["local_total"], "可分区实施，不产生停业损失"], None, [BOLD, None, None])
r += 1
r = put(ws, r, ["【五】情形三的财务含义（如实）"])
ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["路径","5 年净现值（万元）","说明"], [30, 20, 90])
r = put(ws, r, ["完全不改造", C["npv_keep_5y"], "年经营现金流 −1,924 万元持续 5 年"])
r = put(ws, r, ["仅必要局部整改", C["npv_local_5y"], "投入 4,584 万元但不改善盈利能力，净现值劣于不改造"], None, [None, None, BAD])
r = put(ws, r, ["结论：局部整改的价值在于消除安全合规隐患与经营中断风险（不可量化的合规价值），而非改善财务回报。这正是必须先取得第三方安全评估结论的原因：同一笔投资在三种结论下的性质完全不同。"])

wb.save(NEW)
L("XLSX v2.0 %.1f KB | %d sheets" % (os.path.getsize(NEW)/1024, len(wb.sheetnames)))
L("sheets:", wb.sheetnames)
os.remove(OLD)
L("removed 测算附表 v1.0")
