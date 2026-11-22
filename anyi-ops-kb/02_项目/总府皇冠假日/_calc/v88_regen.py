# -*- coding: utf-8 -*-
"""v88：从 v87.json（唯一权威源）重生成报告全部表格、图表、Excel，并重建 Word
   —— 消除报告内部并存的两套财务数
"""
import io, os, sys, re, json, glob, shutil, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v88.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
J = json.load(open(os.path.join(T, "v87.json"), encoding="utf-8"))
B = {r["key"]: r for r in J["brands"]}
ORDER = J["order"]
BASE = J["base"]; OWN = J["own"]; PATHS = J["paths"]; CL = J["closure"]
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return "{:.2f}%".format(v * 100) if v is not None else "无可解"
def sg(v): return ("+" + N(v)) if v >= 0 else ("−" + N(abs(v)))
def M(v, d=1):
    """带符号，负号用 U+2212"""
    return ("+" + N(v, d)) if v >= 0 else ("−" + N(abs(v), d))

MD5 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
lines = open(MD5, encoding="utf-8").read().split("\n")
FAIL = []
def find(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    return -1
def put_between(a, b, content, tag):
    global lines
    i = find(a)
    if i < 0: FAIL.append(tag); L("[MISS]", tag); return
    j = find(b, i + 1)
    if j < 0: FAIL.append(tag+" end"); L("[MISS]", tag, "end"); return
    lines[i:j] = content.rstrip("\n").split("\n") + [""]
    L("[OK]  ", tag)

# ══ 表格行生成 ══
brand_rows = []
for k in ORDER:
    r = B[k]
    pc = "{:.0f}".format(r["adr"]) if r["price_src"] == "OTA 实测" else "推定"
    brand_rows.append("| {k} | {nm} | {tr} | {ar:.0f} | {n} | {d} | {pc} | {rev} | {nr} | {cx} | {pk} | {npv} | {irr} | {vac} |".format(
        k=k, nm=r["name"], tr=r["tier_cn"], ar=r["area_th"], n=r["n"], d=r["n"]-402, pc=pc,
        rev=N(r["total_rev"]), nr=N(r["seg"]["fnb"]+r["seg"]["banq"]+r["seg"]["misc"]),
        cx=N(r["capex"]), pk=N(r["per_key_total"],2), npv=M(r["npv"]), irr=P(r["irr"]), vac=r["vacancy"]))
BRAND_ROWS = "\n".join(brand_rows)
order_rows = []
for i, k in enumerate(ORDER):
    r = B[k]
    order_rows.append("| {i} | {nm} | {npv} | {irr} | {inc} | {vac} |".format(
        i=i+1, nm=r["name"], npv=M(r["npv"]), irr=P(r["irr"]), inc=M(r["inc_npv"]), vac=r["vacancy"]))
ORDER_ROWS = "\n".join(order_rows)
cost_rows = []
for k in ORDER:
    r = B[k]
    cost_rows.append("| {nm} | {n} | {mep} | {rc} | {rk} | {pc} | {ps} | {ot} | {tot} |".format(
        nm=r["name"], n=r["n"], mep=N(r["mep"]), rc=N(r["room_cost_total"]),
        rk=N(r["room_cost_per_key"],2), pc=N(r["pub_cost"]),
        ps="{:,.0f}".format(r["pub_per_sqm"]*10000), ot=N(r["other"]), tot=N(r["capex"])))
COST_ROWS = "\n".join(cost_rows)
# 总资金需求
need_rows = []
for k in ORDER:
    r = B[k]
    need_rows.append("| {nm} | {cx} | {cl} | {tn} |".format(
        nm=r["name"], cx=N(r["capex"]), cl=N(CL["12"][0]), tn=N(r["capex"]+CL["12"][0])))
NEED_ROWS = "\n".join(need_rows)

# ══ 第五章（五）重写 ══
FR55 = open(os.path.join(KB, "_calc", "_frag", "fr_5_5.md"), encoding="utf-8").read()
FR55 = (FR55.replace("{{BRAND_ROWS}}", BRAND_ROWS).replace("{{ORDER_ROWS}}", ORDER_ROWS)
        .replace("{{B3}}", N(B["B03"]["npv"])).replace("{{B8}}", N(B["B08"]["npv"]))
        .replace("{{B5}}", N(B["B05"]["npv"])).replace("{{B10}}", N(B["B10"]["npv"]))
        .replace("{{B2}}", N(B["B02"]["npv"])))
# 读数段按 v87 数字校正
FR55 = re.sub(r"\*\*读数一：.*?\*\*读数二：",
              "**读数一：面积要求是房量的唯一决定因素，房量减少直接吃掉收入基数。** 402 间不变只能容纳上高端全服务档（皇冠假日基础房 25.35 平方米）；一旦进入规模化奢华档（瑞吉 65 平方米、尼依格罗 50 平方米、康莱德 46 平方米），房量降至 145 至 205 间，**较现状减少 197 至 257 间**。这解释了为什么瑞吉的年营业收入（{b06} 万元）反而低于皇冠假日（{b01} 万元）——**尽管瑞吉实测房价 1,342 元是皇冠假定 880 元的 1.5 倍**。房价与房量是反向作用，价格提升被房量减少抵消。\n\n**读数二：",
              FR55, flags=re.S)
FR55 = FR55.replace("{b06}", N(B["B06"]["total_rev"])).replace("{b01}", N(B["B01"]["total_rev"]))
FR55 = re.sub(r"\*\*读数二：\*\*.*?\*\*读数三：",
              "**读数二：因此「402 间卖 1,000 元以上」的组合在算术上不成立。** 以尼依格罗 50 平方米基础房、1,290 元房价计，188 间的年客房收入为 8,853 万元；而维持 402 间、假设 1,100 元房价的年客房收入为 16,140 万元——**两者相差 7,287 万元，相当于改造投资的三分之一强**。任何品牌方案都必须同时回答「房量降到多少」与「价格做到多少」两个问题。\n\n**读数三：",
              FR55, flags=re.S)
FR55 = re.sub(r"\*\*读数三：净现值排序与空位判断排序同样不一致，须并读。\*\*",
              "**读数三：净现值排序与空位判断排序同样不一致，须并读。**", FR55)
FR55 = re.sub(r"\*\*修正后的可争取品牌清单：.*?\*\*",
              "**修正后的可争取品牌清单：真正存在空位的是康莱德（净现值 {b3} 万）、柏悦（{b8} 万）、Sofitel（{b5} 万）、六善（{b10} 万）四项，加洲至奢选（同集团可换牌，{b2} 万），共五项；而净现值最高的 LXR 前提最弱（总府路 28 号项目 2023-03 单方官宣后 3 年无落地、希尔顿从未官方确认）。**\n\n**读数四：洲至奢选是本轮实测修订后降幅最大的品牌。** 其基础房面积由同档次推定 40 平方米订正为 OTA 实测 45 平方米（标准房 45 平方米／尊贵房 52 平方米／行政层 54 至 58 平方米／套房 106 平方米），房量由 235 间降至 209 间，净现值由 +2,787.2 万元降至 +61.0 万元。**这一修订说明「预估品牌面积」是不可靠的输入条件——同一品牌在相差 5 平方米的要求下，经济性相差 45 倍。**\n\n",
              FR55, flags=re.S)
FR55 = FR55.replace("{b3}", N(B["B03"]["npv"])).replace("{b8}", N(B["B08"]["npv"]))
FR55 = FR55.replace("{b5}", N(B["B05"]["npv"])).replace("{b10}", N(B["B10"]["npv"]))
FR55 = FR55.replace("{b2}", N(B["B02"]["npv"]))
FR55 = FR55.replace("**在品牌方书面确认前，本节全部测算均为按同档次样本推定，属决策预研口径，不构成对任何品牌的承诺或排他性判断。**",
 "**在品牌方书面确认前，本节全部测算均为按同档次样本推定，属决策预研口径，不构成对任何品牌的承诺或排他性判断。**\n\n**本轮实测修订的直接教训：品牌客房面积要求是不可由业主方假定的输入条件。** 洲至奢选一家的面积由 40 平方米订正为 45 平方米，即房量 235 间降至 209 间、净现值由 +2,787.2 万元降至 +61.0 万元。**因此品牌方对基础房型面积的书面确认，是比价格与投资规模更优先的前置条件。**")
put_between("### （五）品牌方案比选", "### （六）可保留项利用方案", FR55, "⑤ 第五章（五）品牌比选")

# ══ 第五章（八）自有品牌 ══
FR58 = """### （八）为什么不以集团自有高端品牌作为推荐方案

集团自有品牌体系（锦宾国际、锦江宾馆、锦著）在本次比选中被单列测算。**测算结果是：自有高端品牌路径的净现值 {own} 万元、内部收益率 {ownirr}，优于皇冠现状续约的 {b01npv} 万元与 {b01irr}，在全部十二个候选品牌中位列第三。** 这一结果本身值得集团正视。

**但不作为推荐方案，理由有四：**

**其一，客源获取成本未被模型覆盖。** 自有品牌不承担国际集团会员体系的直销贡献。按内部品牌分级分类表，希尔顿会员匹配满意度 88 分为五强最高、IHG 体系 48 分垫底、马尔代 59 分、凯悦 53 分、雅高 49 分。**自有品牌在起步期须以更低的房价换取同等入住率，而本模型对自有品牌采用了与皇冠相同的平均房价假设，该假设偏乐观。**

**其二，价格认知须从零建立。** 核心商圈 2,000 元以上的价格带目前由居舍、尼依格罗、瑞吉、丽思卡尔顿、华尔道夫等十余家国际品牌共同支撑，消费者对成都高端酒店的认知锚点已经形成。自有品牌进入该价格带，无品牌溢价可依赖。

**其三，集团现有品牌资产集中在中高端。** 现有自有品牌矩阵的定位区间与五星级全服务并不重合，从零建设一套全服务高端产品的运营体系（管家服务、宴会与会议能力、多语种服务、文化主理人岗位）所需周期长于本项目的改造周期。

**其四，落地前提不属本项目可评估范围。** 自有品牌路径的完整成立依赖品牌中心从零搭建高端品牌产品线并完成市场验证，这不是本报告可以评估的范畴，也不应在投资决策前作为备选路径消耗谈判窗口。

**结论：自有高端品牌是本项目在中长期（改造完成之后）具备战略价值的选项，但不具备本轮改造决策阶段的可执行性。** 建议将其单列为集团品牌建设的中长期课题，与本项目改造脱钩推进。
""".format(own=M(OWN["npv"]), ownirr=P(OWN["irr"]), b01npv=M(B["B01"]["npv"]), b01irr=P(B["B01"]["irr"]))
put_between("### （八）为什么不以集团自有高端品牌作为推荐方案", "## 第六章", FR58, "⑤ 第五章（八）自有品牌")

# ══ 第六章（二）各品牌改造投资 + （四）总资金需求 ══
FR61 = open(os.path.join(KB, "_calc", "_frag", "fr_6_1.md"), encoding="utf-8").read()
FR61 = FR61.replace("{{COST_ROWS}}", COST_ROWS)
put_between("### （一）估算基准", "### （二）各品牌方案的改造投资", FR61, "⑧ 第六章（一）三分口径")
FR62 = """### （二）各品牌方案的改造投资

按三分口径列示，单位：万元。

| 品牌 | 房量（间） | 机电设备与隐蔽（万元） | 客房改造（万元） | 客房单间（万元/间） | 公区改造（万元） | 公区单平（元/㎡） | 其他（万元） | 改造投资合计（万元） |
|---|---|---|---|---|---|---|---|---|
""" + COST_ROWS + """

**说明：段二机电设备与隐蔽工程（11,060.0 万元）与品牌无关；品牌档次带来的增量全部落在客房改造与公区改造两段。** 客房改造随房量减少而单间造价上升；公区改造不随房量减少，**因此减房方案在成本端也不占便宜**——这是此前被漏计的一项。

"""
put_between("### （二）各品牌方案的改造投资", "### （三）人防工程专项处置", FR62, "⑧ 第六章（二）改造投资")
FR64 = """### （四）项目总资金需求

单位：万元。段一A 为停业期刚性现金支出（计入资金需求）；停业造成的营业收入归零（段一B）不计入资金需求，仅在财务评价的现金流中体现。

| 品牌 | 改造投资 | 段一A 停业期刚性现金支出 | 总资金需求 |
|---|---|---|---|
""" + NEED_ROWS + """

**口径说明：** 12 个月停业对应的段一A 为 """ + N(CL["12"][0]) + """ 万元，与集团 715 定稿「总府停业一年刚性支出 3,674 万元」量级一致（人工 1,412 万元等）。停业期营业收入归零 """ + N(CL["12"][1]) + """ 万元属经营损失，不计入需投入资金。

"""
put_between("### （四）项目总资金需求", "### （五）资金筹措", FR64, "⑧ 第六章（四）总资金需求")

open(MD5, "w", encoding="utf-8").write("\n".join(lines))
L("")
L("阶段A 完成，未命中 {0} 处".format(len(FAIL)))
for f in FAIL: L("   MISS:", f)
L("DONE-A")
