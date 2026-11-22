# -*- coding: utf-8 -*-
"""v33 修复：① 恢复第五章（五）品牌方案比选表（v21 JSON 单一数据源）
        ② Excel 08/10 数值按正文精度取整（消除显示与存储差异）
        ③ 诊断并修复页脚页码域
        ④ 重出公文 Word + 终检"""
import io, os, sys, re, json, glob, shutil, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v33.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, os.path.join(KB, "_calc"))
from v22_text import CH5_NEW6

V21 = json.load(open(os.path.join(T, "v21.json"), encoding="utf-8"))
BASE = V21["base"]; SCH = {s["key"]: s for s in V21["schemes"]}
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return ("%.2f%%" % (v * 100)) if v is not None else "无可解内部收益率"
FEAS = {"S1":"基准候选","S2":"否决（收入仅增 8%）","S3":"否决","S4":"比价方案","S5":"否决","S6":"否决",
        "S7":"比价方案","S7B":"唯一全判据成立","S8":"不可行（客房面积不达标）"}
ORD = ("S1","S2","S3","S4","S5","S6","S7","S7B","S8")

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ① 恢复第五章（五）比选表
rows = ["| 方案 | 品牌标准 | 公区做法 | 房量做法 | 房量（间） | 改造后年营业收入（万元） | 收入增量（万元） | 收入倍数（对改造前） | 改造投资（万元） | 停业月数 | 全口径内部收益率 | 集团口径静态回收期（年） | 可行性 |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for k in ORD:
    s = SCH[k]
    b = "**" if k in ("S1", "S7B") else ""
    pbg = ("%s" % N(s["pb_grp"], 2)) if s["pb_grp"] else "不适用"
    rows.append("| %s | %s | %s | %s | %d | %s%s%s | %s%s%s | %s%s%s | %s | %d | %s | %s | %s |" % (
        k, s["brand"], s["pub_mode"], s["room_mode"], s["n_rooms"],
        b, N(s["steady_rev"]), b, b, N(s["rev_vs_base"]), b, b, N(s["rev_ratio"], 2), b,
        N(s["capex"]), s["months"], P(s["irr20"]), pbg, FEAS[k]))
TBL5 = "\n".join(rows)
m5 = re.search(r"^### （五）品牌方案比选.*?(?=^### （六）)", t, re.M | re.S)
assert m5, "未定位第五章（五）"
NEW5 = ("### （五）品牌方案比选\n\n"
        "以下比较在第五章第一节情形一假设下成立，并按第九章分档定价口径列示。"
        "**排序同时看收入增量与投资回报两条线，不可只看其一。**\n\n"
        + TBL5 + "\n\n" + CH5_NEW6.rstrip() + "\n\n")
t = t[:m5.start()] + NEW5 + t[m5.end():]
L("[MD] 第五章（五）比选表已恢复（%d 行数据）" % len(ORD))
open(MD, "w", encoding="utf-8").write(t)

# ② Excel 数值按正文精度取整
from openpyxl import load_workbook
XL = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v3.0_2026-11-14.xlsx")
wb = load_workbook(XL)
def roundcols(ws, r0, spec):
    n = 0
    for rr in range(r0, ws.max_row + 1):
        k = ws.cell(row=rr, column=1).value
        if not (isinstance(k, str) and k.startswith("S")): continue
        for ci, d in spec:
            v = ws.cell(row=rr, column=ci).value
            if isinstance(v, (int, float)):
                ws.cell(row=rr, column=ci).value = round(float(v), d); n += 1
    return n
ws8 = wb["08 九方案造价总表"]
n8 = roundcols(ws8, 5, [(7,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(16,2),(18,1)])
ws10 = wb["10 三口径对照"]
n10 = roundcols(ws10, 5, [(2,1),(3,1),(4,1),(5,1),(6,1),(7,2),(9,1),(12,2),(14,2)])
# 基线行
for rr in range(1, ws8.max_row + 1):
    if ws8.cell(row=rr, column=1).value == "改造前基线（不改造）":
        for ci, d in ((7,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(16,2)):
            v = ws8.cell(row=rr, column=ci).value
            if isinstance(v, (int, float)): ws8.cell(row=rr, column=ci).value = round(float(v), d)
wb.save(XL)
L("[XLS] 08 取整 %d 项 / 10 取整 %d 项" % (n8, n10))

# ③ 诊断页脚
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
d = Document(DOCX)
fx = d.sections[0].footer._element.xml
L("=== 页脚 XML 诊断（截取）===")
L(fx[:1500])
L("PAGE 出现次数:", fx.count("PAGE"), "| fldChar:", fx.count("fldChar"), "| instrText:", fx.count("instrText"))
L("DONE")
