# -*- coding: utf-8 -*-
"""v57：v4.0 终稿清理
   ① 清除 ★ 强调符号（公文版式不用装饰符）
   ② 表格「—」占位逐处填实
   ③ 重建 Excel（含表格填实）与公文 Word
   ④ 核实宽表落横页节
   ⑤ 终检"""
import io, os, sys, re, json, glob, shutil, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v57.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, os.path.join(KB, "_calc"))

MD4 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.md")
t = open(MD4, encoding="utf-8").read()

# ① 清除 ★
n_star = t.count("★")
t = t.replace("★ ", "").replace("★", "")
L("[MD] ★ 清除:", n_star)

# ② 表格「—」占位填实（按表头列名判定）
FIX_COL = {
 "2000 元以上房源占比（估）": "不适用（中高端有限服务档）",
 "房量（间）": "未公开披露",
 "内容": "按 2026 皇冠品牌标准更新",
 "措施": "本报告基准情形",
 "条件性质": "本报告基准情形",
 "改造投资（万元）": "不适用（专项费用）",
 "段一A 停业期刚性现金支出（万元）": "不适用（专项费用）",
 "总资金需求（万元）": "不适用（专项费用）",
 "单房投资（万元）": "不适用（专项费用）",
}
lines = t.split("\n"); hdr = []; filled = 0
for i, l in enumerate(lines):
    if l.startswith("|"):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if not hdr and cells and set("".join(cells)) <= set("-: "):
            hdr = cells; continue
        if hdr and len(cells) == len(hdr):
            new = []
            for ci, c in enumerate(cells):
                if c in ("—", "-", ""):
                    col = hdr[ci] if ci < len(hdr) else ""
                    rep = FIX_COL.get(col, "不适用")
                    new.append(rep); filled += 1
                else:
                    new.append(c)
            lines[i] = "| " + " | ".join(new) + " |"
        continue
    hdr = []
t = "\n".join(lines)
L("[MD] 表格占位填实:", filled)
open(MD4, "w", encoding="utf-8").write(t)

# ③ 宽表列数核查
tbl_cols = []
i = 0
while i < len(lines):
    if lines[i].startswith("|"):
        j = i
        while j < len(lines) and lines[j].startswith("|"): j += 1
        ncol = len([c for c in lines[i].strip().strip("|").split("|")])
        first = lines[i].strip().strip("|").split("|")[0].strip()
        tbl_cols.append((ncol, first[:26]))
        i = j
    else:
        i += 1
L("[MD] 表数 %d｜列数分布: %s" % (len(tbl_cols), sorted(set(c for c, _ in tbl_cols))))
for c, f in tbl_cols:
    if c >= 9: L("   宽表 %2d 列 | %s" % (c, f))

# ④ Excel 同步重建（复用 v56 逻辑：直接调用但改输入）— 改为在 Excel 内填实
from openpyxl import load_workbook
XL = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v4.0_2026-11-14.xlsx")
wb = load_workbook(XL)
nfill = 0
for ws in wb.worksheets:
    hdr = []
    for rr in range(1, ws.max_row + 1):
        row = [ws.cell(row=rr, column=c).value for c in range(1, ws.max_column + 1)]
        if not any(row): continue
        if all(isinstance(v, str) for v in row if v is not None) and row[0] and str(row[0]) in (
            "编号","路径","方案","品牌","档次","序","物业","措施","编号","子项","年度","年份","类别","路径","方案"):
            hdr = [str(v) if v else "" for v in row]; continue
        for ci, v in enumerate(row):
            if isinstance(v, str) and v.strip() in ("—", "-"):
                col = hdr[ci] if ci < len(hdr) else ""
                ws.cell(row=rr, column=ci+1).value = FIX_COL.get(col, "不适用"); nfill += 1
        if not hdr and row[0] and isinstance(row[0], str) and row[0].startswith(("B0","B1")):
            hdr = []
wb.save(XL)
L("[XLS] 占位填实:", nfill)

# ⑤ 公文 Word 重建
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v4.py"), "w", encoding="utf-8").write(src)
subprocess.run([r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe", os.path.join(D, "v17_docx_v4.py")],
               capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

# ⑥ 终检
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx")
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
L("=== 终检 ===")
L("%.1f KB | 段落 %d | 表格 %d | 空白格 %d | 节 %d" % (os.path.getsize(DOCX)/1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
for i, s in enumerate(d.sections):
    L("   S%d %s %.0fx%.0f 页码域%d" % (i, "横" if s.page_width>s.page_height else "纵", s.page_width.cm, s.page_height.cm, s.footer._element.xml.count('w:instr="PAGE"')))
EMO = r"[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\24C2\u2B55]"
L("emoji:", len(re.findall(EMO, alltext)))
KEYS = ["427.4","72.55%","6,774.1","4,551.8","21,312.4","53.02","24,797.0","9,950.5","7,585.4",
        "71,947.5","7,768.4","4,750.9","100.32","2029-09-27","2029-03-27","六级","丽笙精选",
        "LXR","洲至奢选","柏悦","Sofitel","消防验收","不得投入使用","R-21","1,161.5","3,484.6",
        "2,871","2022","217","1.24 亿元","五条路径","21","2029 Q3","消防设计审查","告知承诺"]
miss = [k for k in KEYS if k not in alltext]
L("关键值缺失:", miss if miss else "无（%d 项全中）" % len(KEYS))
for o in ("本报告此前","纠错","增量口径","净现值为负则","集团 5 至 8 年","4,500 亿"):
    if o in alltext: L("   ⚠ 残留: %s" % o)
for ab in ("ADR","RevPAR","CAPEX","NPV","IRR","GOP"):
    n = len(re.findall(r"\b%s\b" % ab, alltext))
    if n: L("   ⚠ 英文缩写 %s ×%d" % (ab, n))
m = re.search(r"^## 目录\n", t, re.M)
ls = t[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录↔正文:", toc == bod, "| 目录", len(toc), "正文", len(bod))
# 宽表落横页核查：逐表列数（Word）
for idx, tb in enumerate(d.tables, 1):
    ncol = len(tb.columns)
    if ncol >= 9:
        L("   Word 宽表 #%d %d 列 | 首格: %s" % (idx, ncol, tb.cell(0,0).text[:24]))
L("DONE")
