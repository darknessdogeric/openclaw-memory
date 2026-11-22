# -*- coding: utf-8 -*-
"""v76：v5.0 装配 —— 片段替换 + 占位符注入 + 图表插入 + Excel 详算附件 + 公文 Word + 终检"""
import io, os, sys, re, json, glob, shutil, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
FR = os.path.join(KB, "_calc", "_frag")
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v76.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, os.path.join(KB, "_calc"))
J = json.load(open(os.path.join(T, "v70.json"), encoding="utf-8"))
BR = {r["key"]: r for r in J["brands"]}; ORD = J["order"]
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return ("{:.2f}%".format(v * 100)) if v is not None else "无可解"

MD5 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
lines = open(MD5, encoding="utf-8").read().split("\n")
FAIL = []
def find(pred, start=0):
    for i in range(start, len(lines)):
        if pred(lines[i]): return i
    return -1
def block(header, new, tag, stop="###"):
    global lines
    i = find(lambda l: l.startswith(header))
    if i < 0:
        FAIL.append(tag); L("[MISS]", tag); return
    j = i + 1
    while j < len(lines) and not lines[j].startswith(stop): j += 1
    lines[i:j] = new.rstrip("\n").split("\n")
    L("[OK]  ", tag)

# ── 表格行生成 ──
brand_rows = []
for k in ORD:
    r = BR[k]
    pc = "{:.0f}".format(r["adr"]) if str(r["price_src"]).startswith("OTA") else "推定"
    brand_rows.append("| {k} | {nm} | {tr} | {ar:.0f} | {n} | {d} | {pc} | {rev} | {nr} | {cx} | {pk} | {npv} | {irr} | {vac} |".format(
        k=k, nm=r["name"], tr=r["tier_cn"], ar=r["area_th"], n=r["n"], d=r["n"] - 402, pc=pc,
        rev=N(r["total_rev"]), nr=N(r["seg"]["fnb"] + r["seg"]["banq"] + r["seg"]["misc"]),
        cx=N(r["capex"]), pk=N(r["per_key_total"], 2), npv=N(r["npv"]), irr=P(r["irr"]), vac=r["vacancy"]))
BRAND_ROWS = "\n".join(brand_rows)

ORDER_ROWS = "\n".join(
    "| {i} | {nm} | {npv} | {irr} | {inc} | {vac} |".format(
        i=i + 1, nm=BR[k]["name"], npv=N(BR[k]["npv"]), irr=P(BR[k]["irr"]),
        inc=N(BR[k]["inc_npv"]), vac=BR[k]["vacancy"]) for i, k in enumerate(ORD))

COST_ROWS = "\n".join(
    "| {nm} | {n} | {mep} | {rc} | {rk} | {pc} | {ps} | {ot} | {tot} |".format(
        nm=BR[k]["name"], n=BR[k]["n"], mep=N(BR[k]["mep"]), rc=N(BR[k]["room_cost_total"]),
        rk=N(BR[k]["room_cost_per_key"], 2), pc=N(BR[k]["pub_cost"]),
        ps="{:,.0f}".format(BR[k]["pub_per_sqm"] * 10000), ot=N(BR[k]["other"]), tot=N(BR[k]["capex"]))
    for k in ORD)

# ── 片段装配 ──
def frag(name, tokens):
    s = open(os.path.join(FR, name), encoding="utf-8").read()
    for k, v in tokens.items():
        s = s.replace("{{" + k + "}}", v)
    if "{{" in s:
        FAIL.append(name + " 残留占位符")
        L("[MISS]", name, "残留占位符:", s[s.find("{{"):s.find("{{") + 30])
    return s

block("### （五）品牌方案比选", frag("fr_5_5.md", dict(
    BRAND_ROWS=BRAND_ROWS, ORDER_ROWS=ORDER_ROWS,
    B3=N(BR["B03"]["npv"]), B8=N(BR["B08"]["npv"]), B5=N(BR["B05"]["npv"]),
    B10=N(BR["B10"]["npv"]), B2=N(BR["B02"]["npv"])), "⑨ 第五章（五）")
block("### （四）停业方案", frag("fr_5_4.md", {}), "⑥ 第五章（四）停业方案")
block("### （一）估算基准", frag("fr_6_1.md", dict(COST_ROWS=COST_ROWS)), "⑧ 第六章（一）三分口径")

# ── 第十章 战略价值：补对安逸十五五战略的在地文化/在地化逻辑 ──
i = find(lambda l: l.startswith("### （三）对安逸十五五战略的体现"))
if i >= 0:
    j = i + 1
    while j < len(lines) and not lines[j].startswith("###"): j += 1
    ADD = """
**四是本地文化作为产品内容而非装饰。** 集团十五五明确"一定要做文创化改造，而不是简单改造"，并把在地文化能力列为五大护城河之一。本项目与该战略的接口在于：总府所在街区的文化资产（明代四川都指挥使司"总府"、清光绪五年盐市口官盐店、1926 年智育电影院、2009 年盐市口汉代廊桥遗址、1924 年春熙路开路）**是可考证、可策展、可转化为产品与客群吸引力的具体内容**，而非可复制的符号装饰。这条接口同时决定了本项目的品牌适配方向：**候选品牌方中，谁能承接总府街的在地叙事，谁才是本物业的适配品牌。** 该判断已纳入第五章（五）品牌标准书面确认事项。

**五是锦江区"十五五"规划纲要的直接依据。** 《成都市锦江区国民经济和社会发展第十五个五年规划纲要》（2026 年 1 月 9 日锦江区第八届人民代表大会第六次会议批准）第六章"着力转变营城方式，扎实推进城市更新提质"与第七章"统筹传承与创新，繁荣发展高品位文化，推动锦江文脉赓续焕新"，为本项目的城市更新属性与文化取向提供了区级依据。
"""
    lines[j:j] = ADD.strip("\n").split("\n")
    L("[OK]   第十章（三）十五五对标补充")
else:
    FAIL.append("第十章（三）"); L("[MISS]", "第十章（三）")

# ── 插图 ──
FIGDIR = os.path.join(KB, "_figs")
FIGS = [("### （三）市场行情", "fig01_五年曲线.png", "图 1　成都五星级酒店每间可售房收入五年走势（2021—2026）"),
        ("### （五）品牌方案比选", "fig02_品牌面积与房量.png", "图 2　品牌客房面积要求 → 总府可行房量"),
        ("### （三）市场行情", "fig03_实测房价带.png", "图 3　春熙路核心商圈五星级及奢华酒店实测房价带"),
        ("### （四）净现值为正的可行路径", "fig04_净现值路径.png", "图 4　净现值转正路径分解"),
        ("### （四）停业方案", "fig05_停业方案.png", "图 5　停业方案与净现值")]
for header, fn, cap in FIGS:
    i = find(lambda l: l.startswith(header))
    if i < 0: FAIL.append("图 " + fn); L("[MISS] 图", fn); continue
    j = i + 1
    while j < len(lines) and not lines[j].startswith("###") and not lines[j].startswith("## "): j += 1
    img = "![{c}](_figs/{f})".format(c=cap, f=fn)
    lines[j:j] = [img, ""]
    L("[OK]   插图", fn)

# ── 第一章 加"报告定位" ──
i = find(lambda l: l.startswith("### （一）项目概况"))
if i >= 0:
    POS = """
### （零）本报告的性质与阅读指引

**本报告是决策预研框架，不是结论性可研报告。** 第三方安全评估结论尚未出具，检测评估机构对"消防系统与机电系统可分离性"及"是否存在结构层面停业整改触发条件"两项技术结论亦未明确，因此本报告**不给出"改不改、改什么、何时改"的结论**，而是做三件事：

1. **框定决策框架**：把改造范围分成 A 底线整改、B 机电系统同步更新、C 整体停业改造三档，每一档对应评估结论可能给出的类型，列出各自的停业要求、成本量级与触发条件；
2. **算清关键变量**：按品牌客房面积要求反推房量、按四板块测算收入、按机电／客房／公区三分口径测算投资，给出各品牌方案的净现值与内部收益率，以及使净现值转正的具体条件；
3. **列明需要集团定夺的事项**：见第十二章（三）请示事项。

**阅读路径建议**：第二、三章看必要性与市场底盘；第五章（五）与第九章看品牌与财务结论；第六章看造价三分口径与资金筹措；第十章看社会效益与战略价值；第十二章看需要集团拍板的事项。

**附件**：①《国际联号品牌标准项目前期策划文件（PIP / Pre-Opening Plan）模板》（随附 docx）；②《可行性研究报告测算附表》（随附 xlsx，含分品牌逐项详算）；③《现状经营基线与设施设备实测台账》。

"""
    lines[i:i] = POS.strip("\n").split("\n") + [""]
    L("[OK]   第一章（零）报告定位")
else:
    FAIL.append("第一章（零）")

open(MD5, "w", encoding="utf-8").write("\n".join(lines))
L("")
L("装配完成：未命中 {0} 处".format(len(FAIL)))
for f in FAIL: L("   MISS:", f)
json.dump(dict(fail=FAIL), open(os.path.join(T, "v76_fail.json"), "w", encoding="utf-8"), ensure_ascii=False)
L("DONE")
