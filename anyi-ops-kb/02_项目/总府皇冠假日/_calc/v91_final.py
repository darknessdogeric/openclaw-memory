# -*- coding: utf-8 -*-
"""v91：收官 —— ① 补图5 ② Excel 按 v87.json 重建 ③ Word 重建
        ④ 陈旧数字审计（两套数并存检查）⑤ 终检 ⑥ memory/README"""
import io, os, sys, re, json, glob, shutil, subprocess, importlib.util
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
FIG = os.path.join(KB, "_figs")
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v91.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
J = json.load(open(os.path.join(T, "v87.json"), encoding="utf-8"))
B = {r["key"]: r for r in J["brands"]}; ORDER = J["order"]
BASE = J["base"]; OWN = J["own"]; PATHS = J["paths"]; CL = J["closure"]; CON = J["constants"]
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return "{:.2f}%".format(v * 100) if v is not None else "无可解"
def M(v, d=1): return ("+" + N(v, d)) if v >= 0 else ("−" + N(abs(v), d))

# ══ ① 图5（停业情景由 v87.json 直接读取，不再 exec 模型源）══
CAND = ["Microsoft YaHei", "SimHei", "DengXian"]
CC = J["close_cases"]
sv = [None if c["label"].startswith("全停业 4 月") else c["npv"] for c in CC]
HAVE = {f.name for f in font_manager.fontManager.ttflist}

F = next((c for c in CAND if c in HAVE), None)
if F: plt.rcParams["font.sans-serif"] = [F]
plt.rcParams["axes.unicode_minus"] = False
C1, C2, C3 = "#1F4E79", "#C00000", "#2E7D32"
sl = ["全停业 4 月\n（原设想，不可行）", "全停业 12 月\n一次复业", "全停业 12 月\n分区滚动开业",
      "全停业 16 月\n分区滚动开业", "全停业 20 月\n分区滚动开业"]
fig, ax = plt.subplots(figsize=(9, 4.4))
ax.bar([0], [0], color="#BFBFBF", alpha=.8)
bars = ax.bar(list(range(1, 5)), sv[1:], color=[C2 if v < 0 else C3 for v in sv[1:]], alpha=.88, width=.55)
for i, v in enumerate(sv):
    if v is None:
        ax.annotate("消防与机电工程\n12 个月不可压缩", (0, 120), ha="center", fontsize=9, color="#8C8C8C", weight="bold")
    else:
        ax.annotate("%+.0f" % v, (i, v), textcoords="offset points", xytext=(0, 6 if v >= 0 else -16),
                    ha="center", fontsize=10, weight="bold", color=C3 if v >= 0 else C2)
ax.set_xticks(list(range(5))); ax.set_xticklabels(sl, fontsize=8.8)
ax.set_ylabel("净现值（万元，30 年口径）", fontsize=10)
ax.set_title("图 5　停业方案与净现值（停业月数是最大的单一变量）", fontsize=13, color=C1, pad=12, weight="bold")
ax.grid(axis="y", alpha=.28, ls="--")
fig.savefig(os.path.join(FIG, "fig05_停业方案.png"), dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)
L("[图] fig05 已重绘：{0}".format([None if v is None else round(v, 1) for v in sv]))

# ══ ② Excel 按 v87 重建 ══
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
XL = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v5.0_2026-11-14.xlsx")
if os.path.exists(XL): os.remove(XL)
wb = Workbook(); wb.remove(wb.active)
THIN = Side(style="thin", color="BFBFBF"); BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BOLD = Font(bold=True); T13 = Font(bold=True, size=13); HD = PatternFill("solid", fgColor="D9E2F3")
OKF = PatternFill("solid", fgColor="C6EFCE"); BADF = PatternFill("solid", fgColor="FFC7CE"); WARNF = PatternFill("solid", fgColor="FFEB9C")
def mk(name, title, note, hdrs, widths=None):
    ws = wb.create_sheet(name)
    ws["A1"] = title; ws["A1"].font = T13
    ws["A2"] = note; ws["A2"].alignment = Alignment(wrap_text=True)
    r = 4
    for i, h in enumerate(hdrs, 1):
        c = ws.cell(row=r, column=i, value=h); c.font = BOLD; c.fill = HD; c.border = BD
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    if widths:
        for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = ws.cell(row=r+1, column=1)
    return ws, r + 1
def put(ws, r, vals, fm=None, fl=None):
    for i, v in enumerate(vals, 1):
        c = ws.cell(row=r, column=i, value=v); c.border = BD
        if fm and i <= len(fm) and fm[i-1]: c.number_format = fm[i-1]
        if fl and i <= len(fl) and fl[i-1]:
            o = fl[i-1]
            if isinstance(o, str) and o.startswith("!"):
                c.fill = {"!OK": OKF, "!BAD": BADF, "!WARN": WARNF}[o]
    return r + 1

ws, r = mk("01 改造前基线", "改造前基线（近 24 个月实测，USALI 利润表交叉验证）",
 "本表为全部财务测算的基准；旧稿曾用 2026-09 单月低点 363.99 元，低估客房收入 771.6 万元（20.4%），已修正",
 ["指标","数值","单位","说明"], [34,16,12,62])
for a,b,c,d in [("房量",BASE["rooms"],"间","物理 415 间，扣除 13 间不可正常售卖"),
 ("平均房价",round(BASE["adr"],1),"元/间/晚","24 个月月均值"),
 ("出租率",round(BASE["occ"]*100,2),"%","24 个月月均值"),
 ("每间可售房收入",round(BASE["revpar"],1),"元","24 个月月均值"),
 ("营业收入",round(BASE["total_rev"],1),"万元","24 个月折年"),
 ("客房收入",round(BASE["room"],1),"万元","占 67.2%"),
 ("餐饮收入",round(BASE["fnb"],1),"万元","占 13.8%"),
 ("会议收入",round(BASE["banq"],1),"万元","占 13.1%"),
 ("其他收入",round(BASE["misc"],1),"万元","占 5.9%"),
 ("部门营业利润",round(BASE["gop"],1),"万元","利润率 21.6%"),
 ("人工",round(BASE["labor"],1),"万元","利润表"),
 ("能耗",round(BASE["energy"],1),"万元","利润表"),
 ("维修",round(BASE["maint"],1),"万元","利润表"),
 ("不改造年经营现金流",-1924.0,"万元/年","业主口径实测"),
 ("不改造 20 年 8% 折现净现值",round(BASE["base_npv"],1),"万元","全部增量判断的真实反事实基准")]:
    r = put(ws, r, [a,b,c,d], ["General","#,##0.00","General","General"])

ws, r = mk("02 面积要求与房量", "品牌客房面积要求 → 本物业可行房量",
 "客房套内总面积 10,192 ㎡；移卫耦合折损 8%；面积要求来源见备注（OTA 实测优先，未开业者按同档次样本推定）",
 ["序","品牌","档次","面积要求（㎡）","可行房量（间）","较现状 402 间","面积要求来源","房量结论"],
 [8,26,14,16,16,16,62,26])
for k in ORDER:
    x = B[k]
    r = put(ws, r, [k, x["name"], x["tier_cn"], x["area_th"], x["n"], x["n"]-402,
                    x["area_src"], "须减房" if x["reduced"] else "不减房"],
            ["General","General","General","0.0","0","+0;-0","General","General"])

ws, r = mk("03 分品牌详算", "十二品牌完整测算（阶段一全停 12 月＋阶段二分区滚动 12 月、30 年期、8% 折现）",
 "房量由面积要求反推；收入含客房与非房四板块；造价按机电／客房／公区三分口径组合",
 ["序","品牌","档次","面积要求（㎡）","房量（间）","出租率","平均房价（元）","客房收入（万元）","餐饮收入（万元）",
  "会议收入（万元）","其他收入（万元）","年营业收入（万元）","机电设备与隐蔽（万元）","客房改造（万元）","客房单间（万元）",
  "公区改造（万元）","公区单平（元/㎡）","其他（万元）","改造投资（万元）","单房投资（万元）","净现值（万元）","内部收益率",
  "增量净现值（万元）","空位判断"],
 [8,24,14,14,12,10,14,16,16,16,14,18,20,18,16,16,18,12,18,16,16,12,16,26])
for k in ORDER:
    x = B[k]; s = x["seg"]
    r = put(ws, r, [k, x["name"], x["tier_cn"], x["area_th"], x["n"], x["occ"], x["adr"],
                    s["room"], s["fnb"], s["banq"], s["misc"], s["total"],
                    x["mep"], x["room_cost_total"], x["room_cost_per_key"], x["pub_cost"],
                    x["pub_per_sqm"]*10000, x["other"], x["capex"], x["per_key_total"],
                    x["npv"], x["irr"], x["inc_npv"], x["vacancy"]],
            ["General"]*4 + ["0","0.0%","#,##0"] + ["#,##0.0"]*5 + ["#,##0.0","#,##0.0","#,##0.00","#,##0.0","#,##0","#,##0.0","#,##0.0","#,##0.00","#,##0.0","0.00%","#,##0.0","General"],
            [None]*9 + [None]*9 + [None, "!OK" if x["npv"] > 8000 else ("!BAD" if x["npv"] < 0 else None), None])

ws, r = mk("04 收入结构基准", "四板块收入结构基准（按档次）",
 "行业基准：五星级全服务酒店客房约 50%—60%、餐饮与会议约 25%—35%；非房部分按餐饮 58%、会议 30%、其他 12% 拆分",
 ["档次","客房收入占比","餐饮收入占比","会议收入占比","其他收入占比","部门营业利润率","平均房价取值方式","依据"],
 [18,18,18,18,18,18,26,44])
for tname, note in [("上高端全服务","行业基准客房约 50%—60%、餐饮会议约 25%—35%"),
                    ("规模化奢华","行业基准，高端全服务典型结构"),
                    ("高端奢华","高星奢华非房占比高于上高端"),
                    ("超奢华","顶奢非房占比最高")]:
    key = {"上高端全服务":"B01","规模化奢华":"B03","高端奢华":"B05","超奢华":"B12"}[tname]
    y = B[key]; rs = y["room_share"]; nr = 1 - rs
    r = put(ws, r, [tname, rs, nr*0.58, nr*0.30, nr*0.12, y["gop_rate"],
                    ("OTA 实测" if y["price_src"] == "OTA 实测" else "同档次样本推定"), note],
            ["General","0%","0%","0%","0%","0.0%","General","General"])

ws, r = mk("05 造价三分口径", "改造投资三分口径：机电设备（全楼）／客房改造（单间）／公区改造（单平）",
 "机电设备与隐蔽工程与品牌无关；品牌溢价全部落在客房与公区两段；减房不减少公区，单平造价上升",
 ["品牌","房量（间）","机电设备与隐蔽（万元）","客房改造（万元）","客房单间（万元/间）","公区改造（万元）","公区单平（元/㎡）","其他（万元）","改造投资合计（万元）"],
 [26,14,20,18,18,18,18,14,20])
for k in ORDER:
    x = B[k]
    r = put(ws, r, [x["name"], x["n"], N(x["mep"]), N(x["room_cost_total"]), N(x["room_cost_per_key"],2),
                    N(x["pub_cost"]), "{:,.0f}".format(x["pub_per_sqm"]*10000), N(x["other"]), N(x["capex"])],
            ["General","0","#,##0.0","#,##0.0","#,##0.00","#,##0.0","#,##0","#,##0.0","#,##0.0"])

ws, r = mk("06 停业方案", "停业方案与财务结果",
 "阶段一 12 个月不可压缩：1996 年建成的全楼消防与机电更新工程量本身需约 12 个月，且住建部令第 58 号第十四条要求整体消防验收合格方可投入使用",
 ["停业方案","段一A 刚性现金支出（万元）","段一B 营业收入归零（万元）","净现值（万元）","内部收益率","说明"],
 [30,24,24,20,16,58])
for lbl, mo, ph, note in [("全停业 4 月（原设想）",4,False,"消防与机电工程无法在 4 个月内完成，且整体消防验收为前置条件"),
 ("全停业 12 月 ＋ 一次复业",12,False,"—"),
 ("全停业 12 月 ＋ 分区滚动开业",12,True,"★ 基准方案：复业时点提前至第 13 个月"),
 ("全停业 16 月 ＋ 分区滚动开业",16,True,"—"),
 ("全停业 20 月 ＋ 分区滚动开业",20,True,"—")]:
    cc = [c for c in CC if c["months"] == mo and c["phased"] == ph][0]
    v = None if mo == 4 else cc["npv"]
    r = put(ws, r, [lbl, cc["A"], cc["B"], (v if v is not None else "不成立"), (P(cc["irr"]) if v is not None else "不适用"), note],
            ["General","#,##0.0","#,##0.0","#,##0.0","0.00%","General"])

ws, r = mk("07 净现值转正路径", "净现值转正路径分解（皇冠假日续约基准，20 年口径）",
 "三项条件均为可具体争取的条件，非假设性利好",
 ["路径","措施","净现值（万元）","较基准改善（万元）","内部收益率","性质"], [10,42,20,22,16,46])
base20 = PATHS[0][2]
for lbl, desc, npv, irr, nat in PATHS:
    d = "不适用" if lbl == "基准" else M(npv - base20)
    r = put(ws, r, [lbl, desc, M(npv), d, P(irr), nat], ["General","General","#,##0.0","#,##0.0","0.00%","General"])

ws, r = mk("08 政策资金与筹措", "资金筹措路径分类",
 "按「不宜作主渠道／有时效窗口／需集团争取／可自行安排」四类管理",
 ["类别","渠道","覆盖比例","关键约束","建议动作"], [20,44,22,50,48])
for a,b,c,d,e in [("不宜作主渠道","地方政府专项债","不适用","纯酒店类产业建筑通常存在负面清单或公益性认定限制，申报不确定性高","不作为方案的主资金假设"),
 ("不宜作主渠道","酒店自身经营结余","不适用","停业期经营现金流归零","不作为改造支出的来源"),
 ("有时效窗口","锦江区设备更新奖励","超 100/300/500 万元分别奖 5/8/10 万元；营业额增速高于住宿业 10 个百分点再奖 10 万元","政策有效期至 2026-12-31；须开工前完成项目入库申报","评估结论落地前先行启动入库前期技术对接"),
 ("有时效窗口","锦江区重大文旅项目奖励","按市级奖励金额 30% 给予最高 30 万元","符合《四川省文化旅游领域设备更新清单》且单个投资额不低于 1,000 万元","与设备更新奖励合并申报"),
 ("需集团争取","旅投集团内部政策支持","不适用","须具体化为资本金注入／内部借款利率优惠／集团统筹授信额度","请集团明确倾向性或组合"),
 ("需集团争取","合作方或品牌方带资","目标承担改造投入 20%—40%","须明确承担方式与对价（股权、租金、收益权）","意向性市场测试，不形成实质承诺"),
 ("需集团争取","停业期固定成本兜底","不适用","人工留存、存量负债利息、基本维护","请集团指定兜底来源，否则资金平衡表无法闭合"),
 ("可自行安排","自有资金","按资本金比例要求","按投资决策节奏安排","按资本金比例要求安排"),
 ("可自行安排","债务融资","按项目条件","须同步明确融资方案与年利率","按资本金比例要求安排")]:
    r = put(ws, r, [a,b,c,d,e])

ws, r = mk("09 品牌档案与空位", "候选品牌档案、面积要求与空位判断",
 "空位按预期判断（决策时点该品牌是否已锁定成都核心商圈物业），不按当前是否开业判断",
 ["序","品牌","档次","面积要求（㎡）","成都现状","价格实测（元）","房量","空位判断（按预期）","依据","净现值（万元）","内部收益率"],
 [8,26,14,16,40,26,10,28,50,16,14])
PRICE = {"B01":"363.99—427.4（现状 24 个月均值）","B02":"900—1,500（OTA 实测，约 $127 起）","B03":"未在蓉开业，无实测",
 "B04":"900—2,200（OTA 实测，原棕榈泉物业）","B05":"未在蓉开业，无实测","B06":"1,291—1,393（OTA 实测，基础房 65 ㎡）",
 "B07":"1,180—1,400（OTA 实测，基础房 50 ㎡）","B08":"未在蓉开业，无实测","B09":"未在蓉开业，无实测（2029Q3）",
 "B10":"未在蓉开业，无实测","B11":"未在蓉开业，无实测（2028）","B12":"未在蓉开业，无实测"}
for k in ORDER:
    x = B[k]
    r = put(ws, r, [k, x["name"], x["tier_cn"], x["area_th"], x["rooms_exist"], PRICE.get(k,"—"),
                    x["n"], x["vacancy"], x["basis"], x["npv"], x["irr"]],
            ["General","General","General","0.0","General","General","0","General","General","#,##0.0","0.00%"],
            [None]*9 + ["!OK" if x["npv"] > 8000 else ("!BAD" if x["npv"] < 0 else None), None])

ws, r = mk("10 数据源清单", "数据源清单",
 "全部数据标注来源与复核状态；OTA 数据为 2026 年 10 月实测",
 ["类别","数据项","来源","复核日期","状态"], [16,60,62,16,28])
for row in [
 ("项目实测","房量 402 间、客房套内 10,192 ㎡、公共区 31,412.82 ㎡","工程部《物业基础档案》《楼层房间数量表》《房间分布表》","2026-11-02","已复核"),
 ("项目实测","近 24 个月 ADR 427.4 元／OCC 72.55%／营业收入 6,774.1 万元／四板块收入","财务部《近 24 个月主要经营指标》与 2026 年 10 月利润表","2026-11-09","已复核"),
 ("项目实测","业主方 43 项自编分项造价 18,000 万元","总府实业〔2024〕11 号排危升级改造专题报告第三章","2024","与洲际 PIP 勾稽通过"),
 ("合同","管理期限 2019-09-28 至 2029-09-27；续约谈判截止 2029-03-27","现行管理合同条款分析","2026-11-05","已复核"),
 ("品牌标准","四档分级分类、单房造价带、抽佣区间、成都位置匹配度","《高星级全服式酒店品牌分级分类（仅5★+）》","2026-10-23","内部权威"),
 ("OTA 实测","成都瑞吉 282 间／基础房 65 ㎡／¥1,291—1,393","携程酒店房型页 2026-10","2026-10","已实测"),
 ("OTA 实测","成都尼依格罗 230 间／基础房 50 ㎡／¥1,180—1,400","携程、hotelflock、topofhotel 房型页 2026-10","2026-10","已实测"),
 ("OTA 实测","★ 洲至奢选棕榈泉 标准房 45 ㎡／尊贵房 52 ㎡／行政层 54—58 ㎡／套房 106 ㎡","hotels.capital、bitvoya、klook 房型页 2026-11","2026-11","已实测"),
 ("OTA 实测","康莱德基础房 46 ㎡（北京）","restreserve 房型页 2026-10","2026-10","已实测"),
 ("OTA 实测","成都居舍房型阶梯 63／72／100／145／215／287 ㎡；米其林均价约 €839","upperhouse.com、guide.michelin.com 2026-10","2026-10","已实测"),
 ("签约状态","文华东方 2022-10-20 签约中海 489 米，267 间，2028 开业","中海与文华东方管理合同云签约（新浪、酒管财经）","2026-10-25","已复核"),
 ("签约状态","丽晶 2026-07-15 签约顺江路 D10 望江，180 间，2029Q3","IHG 与新希望地产签约（新浪、中国商报）","2026-10-25","已复核"),
 ("法规","《消防法》第十三条、第十五条；《建设工程消防设计审查验收管理暂行规定》第十四条","全国人大、住建部令第 58 号","2026-11-14","已复核"),
 ("政策","锦江区设备更新与文旅项目奖励（有效期至 2026-12-31）","锦发改发〔2025〕30 号","2026-11-14","已复核"),
 ("规划","《成都市锦江区国民经济和社会发展第十五个五年规划纲要》","锦江区八届人大六次会议 2026-01-09 批准","2026-11-14","已复核"),
 ("既有预测","成都三 Scale 2026—2030 走势、2029 分水岭、抢位窗口","《成都 UPSCALE / UPPER SCALE / LUXURY 市场分析与预测》","2026-10-23","内部；已订正两处旧结论"),
 ("行业基准","经济型 3—5 年／中端 5—8 年／中高端 6—10 年／高端 8—12 年；高端不以经营回本为唯一评估指标","迈点研究院、酒店之家投资白皮书","2026-11-14","已复核")]:
    r = put(ws, r, list(row))
wb.save(XL)
L("[XLS] v5.0 重建：{0:.1f} KB｜{1} sheets".format(os.path.getsize(XL)/1024, len(wb.sheetnames)))

# ══ ③ Word 重建 ══
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v5.py"), "w", encoding="utf-8").write(src)
subprocess.run([r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe", os.path.join(D, "v17_docx_v5.py")],
               capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

# ══ ④ 陈旧数字审计 ══
MD5 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
s = open(MD5, encoding="utf-8").read()
L("")
L("=== 陈旧数字审计（应全部为 0）===")
STALE = {
 "2,787.2": "洲至奢选旧 NPV（仅允许出现在「由…降至…」的修订说明中）",
 "235 间": "洲至奢选旧房量",
 "21,312.4": "旧 B01 改造投资",
 "4,507.0": "旧 B01 净现值",
 "6.10%": "旧 B01 内部收益率",
 "3,422.6": "旧基准净现值",
 "6,499.1": "旧 P5 净现值",
 "12,610.5": "旧 B01 营业收入",
 "14,647.7": "旧 B02 营业收入",
 "254.7": "旧 B01 净现值",
 "8.11%": "旧 B01 内部收益率",
 "4,750.9": "旧自有品牌净现值",
 "9.95%": "旧自有品牌内部收益率",
 "10,274.7": "占位",
}
for k, why in STALE.items():
    n = s.count(k)
    L("   %-10s %d 次  %s" % (k, n, ("← " + why) if n else "OK"))
L("")
L("=== 关键值存在性核对（v87 权威值应命中）===")
MUST = [N(B["B01"]["total_rev"]), M(B["B01"]["npv"]), P(B["B01"]["irr"]),
        M(B["B02"]["npv"]), str(B["B02"]["n"]), M(B["B12"]["npv"]),
        M(PATHS[0][2]), M(PATHS[-1][2]), P(PATHS[-1][3]),
        N(BASE["total_rev"]), N(BASE["room"]), M(OWN["npv"]), P(OWN["irr"]),
        "45 ㎡", "209 间", "65 ㎡", "50 ㎡", "282 间", "230 间", "2029-03-27"]
for k in MUST:
    L("   %-12s %s" % (k, "在" if k in s else "缺"))

# ══ ⑤ 终检 ══
from docx import Document as D2
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.docx")
d = D2(DOCX)
alltext = chr(10).join(p.text for p in d.paragraphs) + chr(10) + chr(10).join(
    c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
EMO = ("[" + chr(92) + "U0001F300-" + chr(92) + "U0001FAFF" + chr(92) + "U00002600-" + chr(92) + "U000027BF"
       + chr(92) + "U00002B50" + chr(92) + "uFE0F" + chr(92) + "u200D" + chr(92) + "u2764" + chr(92) + "u2B06"
       + chr(92) + "u2B07" + chr(92) + "u2B05" + chr(92) + "u274C" + chr(92) + "u2705" + chr(92) + "u26A0"
       + chr(92) + "u26A1" + chr(92) + "u2139" + chr(92) + "u24C2" + chr(92) + "u2B55]")
L("")
L("=== 终检 ===")
L("{0:.1f} KB | 段落 {1} | 表格 {2} | 空白格 {3} | 节 {4}".format(
    os.path.getsize(DOCX)/1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
for i, sec in enumerate(d.sections):
    L("   S{0} {1} {2:.0f}x{3:.0f} 页码域{4}".format(i, "横" if sec.page_width>sec.page_height else "纵",
        sec.page_width.cm, sec.page_height.cm, sec.footer._element.xml.count('w:instr="PAGE"')))
L("emoji:", len(re.findall(EMO, alltext)))
for ab in ("ADR","RevPAR","CAPEX","NPV","IRR","GOP"):
    n = len(re.findall(r"\b"+ab+r"\b", alltext))
    if n: L("   ⚠ 英文缩写 {0} ×{1}".format(ab, n))
md5 = s
m = re.search(r"^## 目录\n", md5, re.M)
ls = md5[m.end():].split("\n")
start = next((i for i,l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录↔正文: {0}（目录 {1} / 正文 {2}）".format(toc==bod, len(toc), len(bod)))
L("章节 {0} ｜ 图 {1} ｜ 风险 {2}".format(len(re.findall(r"^## 第", md5, re.M)),
   len(re.findall(r"!\[", md5)), len(re.findall(r"\| R-\d+ \|", md5))))
L("交付: {0}".format([os.path.basename(x) for x in glob.glob(os.path.join(REP,"总府皇冠改造_可行性研究报告*"))]))
L("      {0}".format([os.path.basename(x) for x in glob.glob(os.path.join(CAL,"总府皇冠改造_可行性研究报告*"))]))
L("桌面残留: {0}".format(len(glob.glob(r"C:\Users\ericz\Desktop\*总府*"))))
L("DONE")
