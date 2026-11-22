# -*- coding: utf-8 -*-
"""v77：v5.0 装配（扁平结构，避免深层嵌套）"""
import io, os, sys, re, json, glob, shutil, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
FR = os.path.join(KB, "_calc", "_frag")
LOG = open(os.path.join(T, "v77.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, os.path.join(KB, "_calc"))
J = json.load(open(os.path.join(T, "v70.json"), encoding="utf-8"))
BR = {r["key"]: r for r in J["brands"]}
ORD = J["order"]
def N(v, d=1):
    return format(round(v, d), ",.%df" % d)
def P(v):
    if v is None:
        return "无可解"
    return "{:.2f}%".format(v * 100)

MD5 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
lines = open(MD5, encoding="utf-8").read().split("\n")
FAIL = []

def find(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix):
            return i
    return -1

def put_block(header, content, tag, stop="###"):
    global lines
    i = find(header)
    if i < 0:
        FAIL.append(tag)
        L("[MISS]", tag)
        return
    j = i + 1
    while j < len(lines) and not lines[j].startswith(stop):
        j += 1
    lines[i:j] = content.rstrip("\n").split("\n")
    L("[OK]  ", tag)

def read_frag(name, tokens):
    s = open(os.path.join(FR, name), encoding="utf-8").read()
    for k in tokens:
        s = s.replace("{{" + k + "}}", tokens[k])
    if "{{" in s:
        FAIL.append(name + " 残留占位符")
        L("[MISS]", name, "残留占位符")
    return s

# ── 表格行 ──
brand_rows = []
for k in ORD:
    r = BR[k]
    pc = "{:.0f}".format(r["adr"]) if str(r["price_src"]).startswith("OTA") else "推定"
    row = "| {k} | {nm} | {tr} | {ar:.0f} | {n} | {d} | {pc} | {rev} | {nr} | {cx} | {pk} | {npv} | {irr} | {vac} |".format(
        k=k, nm=r["name"], tr=r["tier_cn"], ar=r["area_th"], n=r["n"], d=r["n"] - 402, pc=pc,
        rev=N(r["total_rev"]), nr=N(r["seg"]["fnb"] + r["seg"]["banq"] + r["seg"]["misc"]),
        cx=N(r["capex"]), pk=N(r["per_key_total"], 2), npv=N(r["npv"]), irr=P(r["irr"]), vac=r["vacancy"])
    brand_rows.append(row)
BRAND_ROWS = "\n".join(brand_rows)

order_rows = []
for i, k in enumerate(ORD):
    r = BR[k]
    order_rows.append("| {i} | {nm} | {npv} | {irr} | {inc} | {vac} |".format(
        i=i + 1, nm=r["name"], npv=N(r["npv"]), irr=P(r["irr"]), inc=N(r["inc_npv"]), vac=r["vacancy"]))
ORDER_ROWS = "\n".join(order_rows)

cost_rows = []
for k in ORD:
    r = BR[k]
    cost_rows.append("| {nm} | {n} | {mep} | {rc} | {rk} | {pc} | {ps} | {ot} | {tot} |".format(
        nm=r["name"], n=r["n"], mep=N(r["mep"]), rc=N(r["room_cost_total"]),
        rk=N(r["room_cost_per_key"], 2), pc=N(r["pub_cost"]),
        ps="{:,.0f}".format(r["pub_per_sqm"] * 10000), ot=N(r["other"]), tot=N(r["capex"])))
COST_ROWS = "\n".join(cost_rows)

tok5 = {
    "BRAND_ROWS": BRAND_ROWS,
    "ORDER_ROWS": ORDER_ROWS,
    "B3": N(BR["B03"]["npv"]),
    "B8": N(BR["B08"]["npv"]),
    "B5": N(BR["B05"]["npv"]),
    "B10": N(BR["B10"]["npv"]),
    "B2": N(BR["B02"]["npv"]),
}
frag55 = read_frag("fr_5_5.md", tok5)
frag54 = read_frag("fr_5_4.md", {})
frag61 = read_frag("fr_6_1.md", {"COST_ROWS": COST_ROWS})

put_block("### （五）品牌方案比选", frag55, "9-5 品牌比选")
put_block("### （四）停业方案", frag54, "6-4 停业方案")
put_block("### （一）估算基准", frag61, "8-6 三分口径")

# ── 第十章（三）十五五对标补充 ──
i = find("### （三）对安逸十五五战略的体现")
if i < 0:
    FAIL.append("第十章（三）")
    L("[MISS]", "第十章（三）")
else:
    j = i + 1
    while j < len(lines) and not lines[j].startswith("###"):
        j += 1
    ADD = """
**四是本地文化作为产品内容而非装饰。** 集团十五五明确要求"一定要做文创化改造，而不是简单改造"，并把在地文化能力列为五大护城河之一。本项目与该战略的接口在于：总府所在街区的文化资产（明代四川都指挥使司"总府"、清光绪五年盐市口官盐店、1926 年智育电影院、2009 年盐市口汉代廊桥遗址、1924 年春熙路开路）**是可考证、可策展、可转化为产品与客群吸引力的具体内容**，而非可复制的符号装饰。这条接口同时决定了本项目的品牌适配方向：**候选品牌方中，谁能承接总府街的在地叙事，谁才是本物业的适配品牌。** 该判断已纳入第五章（五）品牌标准书面确认事项。

**五是锦江区"十五五"规划纲要的直接依据。** 《成都市锦江区国民经济和社会发展第十五个五年规划纲要》（2026 年 1 月 9 日锦江区第八届人民代表大会第六次会议批准）第六章"着力转变营城方式，扎实推进城市更新提质"与第七章"统筹传承与创新，繁荣发展高品位文化，推动锦江文脉赓续焕新"，为本项目的城市更新属性与文化取向提供了区级依据。
"""
    lines[j:j] = ADD.strip("\n").split("\n")
    L("[OK]  ", "10-3 十五五对标补充")

# ── 插图 ──
FIGDIR = os.path.join(KB, "_figs")
FIG_LIST = [
    ("### （三）市场行情", "fig01_五年曲线.png", "图 1　成都五星级酒店每间可售房收入五年走势（2021—2026）"),
    ("### （五）品牌方案比选", "fig02_品牌面积与房量.png", "图 2　品牌客房面积要求 → 总府可行房量"),
    ("### （三）市场行情", "fig03_实测房价带.png", "图 3　春熙路核心商圈五星级及奢华酒店实测房价带"),
    ("### （四）净现值为正的可行路径", "fig04_净现值路径.png", "图 4　净现值转正路径分解"),
    ("### （四）停业方案", "fig05_停业方案.png", "图 5　停业方案与净现值"),
]
for header, fn, cap in FIG_LIST:
    i = find(header)
    if i < 0:
        FAIL.append("图 " + fn)
        L("[MISS]", "图", fn)
        continue
    j = i + 1
    while j < len(lines) and not lines[j].startswith("###") and not lines[j].startswith("## "):
        j += 1
    lines[j:j] = ["![{c}](_figs/{f})".format(c=cap, f=fn), ""]
    L("[OK]  ", "插图 " + fn)

# ── 第一章（零）报告定位 ──
i = find("### （一）项目概况")
if i < 0:
    FAIL.append("第一章（零）")
    L("[MISS]", "第一章（零）")
else:
    POS = """### （零）本报告的性质与阅读指引

**本报告是决策预研框架，不是结论性可研报告。** 第三方安全评估结论尚未出具，检测评估机构对"消防系统与机电系统可分离性"及"是否存在结构层面停业整改触发条件"两项技术结论亦未明确，因此本报告**不给出"改不改、改什么、何时改"的结论**，而是做三件事：

**一是框定决策框架。** 把改造范围分成 A 底线整改、B 机电系统同步更新、C 整体停业改造三档，每一档对应评估结论可能给出的类型，列出各自的停业要求、成本量级与触发条件。

**二是算清关键变量。** 按品牌客房面积要求反推房量、按客房与非房四板块测算收入、按机电设备／客房改造／公区改造三分口径测算投资，给出各品牌方案的净现值与内部收益率，以及使净现值转正的具体条件。

**三是列明需要集团定夺的事项。** 见第十二章（三）请示事项。

**阅读路径建议**：第二、三章看必要性与市场底盘；第五章（五）与第九章看品牌与财务结论；第六章看造价三分口径与资金筹措；第十章看社会效益与战略价值；第十二章看需要集团拍板的事项。

**随附材料**：①《国际联号品牌标准项目前期策划文件（PIP / Pre-Opening Plan）模板》；②《可行性研究报告测算附表》（含分品牌逐项详算）；③《现状经营基线与设施设备实测台账》。

"""
    lines[i:i] = POS.rstrip("\n").split("\n") + [""]
    L("[OK]  ", "1-0 报告定位")

open(MD5, "w", encoding="utf-8").write("\n".join(lines))
L("")
L("装配完成，未命中 {0} 处".format(len(FAIL)))
for f in FAIL:
    L("   MISS:", f)
L("DONE")
