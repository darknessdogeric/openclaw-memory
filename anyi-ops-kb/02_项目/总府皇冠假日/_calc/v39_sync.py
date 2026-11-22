# -*- coding: utf-8 -*-
"""v39：Excel 同步（16 现实性检验表；08/10 增列增量净现值；S7B 标注修正）+ 公文 Word 重出 + 终检"""
import io, os, sys, re, json, glob, shutil, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v39.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

V21 = json.load(open(os.path.join(T, "v21.json"), encoding="utf-8"))
BASE = V21["base"]; SCH = {s["key"]: s for s in V21["schemes"]}
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return ("%.2f%%" % (v * 100)) if v is not None else "无可解内部收益率"
BASE_NPV = round(BASE["owner_cf"] * sum(1 / 1.08 ** i for i in range(20)), 1)   # -20,401.3

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
XL = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v3.0_2026-11-14.xlsx")
wb = load_workbook(XL)
THIN = Side(style="thin", color="BFBFBF"); BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BOLD = Font(bold=True); HD = PatternFill("solid", fgColor="D9E2F3")
BAD = PatternFill("solid", fgColor="FFC7CE"); OK = PatternFill("solid", fgColor="C6EFCE"); WARN = PatternFill("solid", fgColor="FFEB9C")
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
ORD = ("S1","S2","S3","S4","S5","S6","S7","S7B","S8")

# ══ 08 总表：增列「增量净现值」，并修 S7B 可行性 ══
ws = wb["08 九方案造价总表"]
# 找到可行性列（第 25 列）
hc = 25
c = ws.cell(row=4, column=hc, value="增量净现值（相对不改造，万元）"); c.font = BOLD; c.fill = HD; c.border = BD
c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws.column_dimensions[get_column_letter(hc)].width = 20
for rr in range(5, ws.max_row + 1):
    k = ws.cell(row=rr, column=1).value
    if not (isinstance(k, str) and k.startswith("S")): continue
    inc = round(SCH[k]["npv20"] - BASE_NPV, 1)
    cc = ws.cell(row=rr, column=hc, value=inc); cc.border = BD; cc.number_format = "#,##0.0"
    if k == "S7B":
        cc.fill = WARN
# S7B 可行性标注
for rr in range(5, ws.max_row + 1):
    if ws.cell(row=rr, column=1).value == "S7B":
        ws.cell(row=rr, column=25).value = "上限情景，前提不成立（见 16 表）"
        ws.cell(row=rr, column=25).fill = WARN
L("[XLS] 08 已增列增量净现值，S7B 标注修正")

# ══ 10 三口径：增列增量净现值 + 反事实基准说明 ══
ws = wb["10 三口径对照"]
hc = ws.max_column + 1
c = ws.cell(row=4, column=hc, value="增量净现值（相对不改造，万元）"); c.font = BOLD; c.fill = HD; c.border = BD
c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws.column_dimensions[get_column_letter(hc)].width = 20
for rr in range(5, ws.max_row + 1):
    k = ws.cell(row=rr, column=1).value
    if not (isinstance(k, str) and k.startswith("S")): continue
    cc = ws.cell(row=rr, column=hc, value=round(SCH[k]["npv20"] - BASE_NPV, 1)); cc.border = BD; cc.number_format = "#,##0.0"
    if k == "S7B": cc.fill = WARN
r = ws.max_row + 2
ws.cell(row=r, column=1, value="【反事实基准】不改造：年经营现金流 −1,924.0 万元（实测失血），20 年 8%% 折现净现值 %s 万元；现状消防报警主机 2026-07 已全面瘫痪，继续原状经营在合规上本身不成立。故判断方案优劣以增量口径为主判据。" % N(BASE_NPV)).font = BOLD
ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
L("[XLS] 10 已增列增量净现值 + 反事实基准说明")

# ══ 新增 16 外部奢牌现实性检验 ══
if "16 外部奢牌现实性检验" in wb.sheetnames:
    del wb["16 外部奢牌现实性检验"]
ws = wb.create_sheet("16 外部奢牌现实性检验")
ws["A1"] = "外部奢牌方案（S7B）现实性压力测试"; ws["A1"].font = Font(bold=True, size=13)
ws["A2"] = "检验结论：S7B 前提不成立，由「唯一全判据成立方案」修正为「上限情景的战略期权」"
r = 4
r = put(ws, r, ["【一】客房面积门槛的物理约束"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["项目", "数值"], [40, 30])
for a, b in [("客房套内总面积（工程部实测）", "10,192 ㎡"), ("在售房量", "402 间"),
             ("单间套内面积", "25.35 ㎡"), ("客房层单间建面（含走廊分摊）", "56.33 ㎡"),
             ("S7B 模型房量", "268 间"), ("268 间 × 40 ㎡ 所需套内", "10,720 ㎡"),
             ("⭐ 面积缺口", "−528 ㎡（物理不成立）")]:
    r = put(ws, r, [a, b])
r += 1
r = hd(ws, r, ["候选奢牌面积门槛", "套内口径物理最大房量", "较 268 间减少", "收入基数影响"], [26, 24, 16, 14])
for a, b, c_, d in [("40 ㎡（尼依格罗口径）", 254, "减 14 间", "−5%"),
                    ("45 ㎡", 226, "减 42 间", "−16%"),
                    ("49 ㎡（兰博基尼口径）", 208, "减 60 间", "−22%"),
                    ("60 ㎡（丽晶全大户型口径）", 169, "减 99 间", "−37%")]:
    r = put(ws, r, [a, b, c_, d])
r += 1
r = put(ws, r, ["【二】盈亏平衡平均房价（净现值 = 0 解算；改造投资 56,850.9 万、停业 20 月、268 间）"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["出租率", "部门营业利润率 30%", "部门营业利润率 35%", "部门营业利润率 40%（模型取值）"], [14, 24, 24, 26])
for occ, a, b, c_ in [("65%", 4138, 3140, 2529), ("70%（模型取值）", 3843, 2915, 2349), ("75%", 3586, 2721, 2192)]:
    r = put(ws, r, [occ, a, b, c_], ["General", "#,##0", "#,##0", "#,##0"],
            [None, None, WARN if occ.startswith("70") else None, None])
r += 1
r = put(ws, r, ["【三】与居舍的经营强度对标"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["对象", "参数", "单房客房年收入（万元）"], [30, 34, 24])
for a, b, c_ in [("成都居舍（100 间客房）", "2,500 元 × 75%（中档假设）", 68.4),
                 ("成都居舍（保守）", "2,000 元 × 75%", 54.8),
                 ("S7B 268 间", "3,000 元 × 70%", 76.7),
                 ("S7B 268 间", "2,500 元 × 70%", 63.9)]:
    r = put(ws, r, [a, b, c_], ["General", "General", "#,##0.0"])
r += 1
r = put(ws, r, ["【四】概率加权期望值"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["情景", "参数", "净现值（万元）", "概率"], [16, 34, 18, 30])
for a, b, c_, d in [("全兑现", "3,000 元 / 70% / 40%", 16916.8, "品牌方接盘 12% × 价格带兑现 30% = 3.6%"),
                    ("中性", "2,500 元 / 70% / 35%", -12937.4, "12% × 70% = 8.4%"),
                    ("低落", "2,000 元 / 65% / 30%", -35511.2, "品牌方未接盘 88%"),
                    ("⭐ 概率加权期望", "—", -31727.6, "100%")]:
    r = put(ws, r, [a, b, c_, d], ["General", "General", "#,##0.0", "General"],
            [None, None, BAD if a == "⭐ 概率加权期望" else None, None])
r += 1
r = put(ws, r, ["【五】外部奢牌路径的真实可行形态：品牌方分摊改造投入"]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["房量", "品牌方分摊", "业主承担改造投资（万元）", "增量净现值（万元）", "增量口径内部收益率"], [12, 16, 24, 22, 22])
for n_, sh, own, inc, irr in [(254, "0%", 55337.1, 35015.3, "15.08%"), (254, "30%", 38736.0, 51223.0, "21.28%"),
                              (254, "50%", 27668.6, 62028.1, "28.28%"), (226, "0%", 51960.2, 29879.4, "14.49%"),
                              (226, "30%", 36372.1, 45098.0, "20.55%"), (208, "30%", 34904.9, 41296.6, "20.05%")]:
    r = put(ws, r, [n_, sh, own, inc, irr], ["General", "General", "#,##0.0", "#,##0.0", "General"],
            [None, None, None, None, OK if sh == "30%" and n_ == 254 else None])
r += 1
r = put(ws, r, ["【六】九方案增量口径重排（相对不改造，基准净现值 %s 万元）" % N(BASE_NPV)]); ws.cell(row=r-1, column=1).font = BOLD
r = hd(ws, r, ["方案", "品牌·做法", "改造投资（万元）", "绝对净现值（万元）", "增量净现值（万元）", "增量口径内部收益率", "增量口径静态回收期（年）"], [10, 18, 18, 20, 20, 20, 22])
for k in ORD:
    s = SCH[k]
    inc = round(s["npv20"] - BASE_NPV, 1)
    r = put(ws, r, [k, "%s·%s" % (s["brand"], s["room_mode"]), s["capex"], s["npv20"], inc,
                    P(s["irr_inc"]), (s["pb_inc"] or "未回收")],
            ["General"]*7, [None]*7)
r += 1
ws.cell(row=r, column=1, value="★ 修正后结论：S1 增量口径内部收益率 15.61% 高于 S7B 的 15.32%，而投资仅为 S7B 的 37%。外部奢牌路径的实质门槛是品牌方分摊 30% 以上改造投入，而非价格带本身。").font = BOLD
ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
L("[XLS] 16 外部奢牌现实性检验已建（%d 行）" % (r - 3))
wb.save(XL)
L("XLSX %.1f KB | %d sheets" % (os.path.getsize(XL) / 1024, len(wb.sheetnames)))

# ══ 公文 Word 重出 ══
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v3.py"), "w", encoding="utf-8").write(src)
PY = r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe"
subprocess.run([PY, os.path.join(D, "v17_docx_v3.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

# ══ 终检 ══
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
md = open(MD, encoding="utf-8").read()
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
L("=== 终检 ===")
L("%.1f KB | 段落 %d | 表格 %d | 空白格 %d | 节 %d" % (os.path.getsize(DOCX) / 1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
emo = len(re.findall("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]", alltext))
L("emoji:", emo)
KEYS = ["10,720", "10,192", "254 间", "208 间", "2,915", "−31,727.6", "−20,401.3", "14,398.4",
        "15.61%", "15.32%", "21.28%", "28.28%", "76.7", "68.4", "31,727.6", "上限情景", "投入分担"]
miss = [k for k in KEYS if k not in alltext]
L("关键值缺失:", miss if miss else "无（%d 项全中）" % len(KEYS))
for o in ("唯一全判据成立", "唯一在全部判据上成立的方案是 S7B", "唯一同时满足"):
    if o in alltext: L("   ⚠ 旧判据残留: %s" % o)
m = re.search(r"^## 目录\n", md, re.M)
ls = md[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录↔正文:", toc == bod, "| 目录", len(toc), "正文", len(bod))
for f in ("总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx",):
    pass
L("交付:", [os.path.basename(x) for x in glob.glob(os.path.join(REP, "总府皇冠改造_可行性研究报告*"))],
  [os.path.basename(x) for x in glob.glob(os.path.join(CAL, "总府皇冠改造_可行性研究报告*"))])
L("桌面残留:", len(glob.glob(r"C:\Users\ericz\Desktop\*总府*")))
L("DONE")
