# -*- coding: utf-8 -*-
"""v29 终检与清理：核验 Word v3.0 落盘与内容、清理旧版、同步索引、桌面残留"""
import io, os, sys, re, json, glob, shutil, hashlib
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v29.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
XLSX = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v3.0_2026-11-14.xlsx")

# ① Word 落盘核验
L("=== Word v3.0 落盘 ===")
L("存在:", os.path.exists(DOCX), "| %.1f KB" % (os.path.getsize(DOCX) / 1024))
from docx import Document
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
L("段落 %d / 表格 %d / 空白格 %d / 节 %d" % (len(d.paragraphs), len(d.tables), blank, len(d.sections)))
secs = []
for s in d.sections:
    secs.append("%dx%d" % (s.page_width.cm, s.page_height.cm))
L("页面尺寸:", secs)
# 目录域
has_toc = "TOC" in d.element.xml
L("目录域:", has_toc)
# 页码域
L("页码域:", "PAGE" in d.element.xml)
# 关键数字
KEYS = ["1,500", "1,750", "3,000", "11.33", "16,916.8", "6,774.0", "518.5", "5.61", "31,229.1",
        "40.48 万家", "1,979 万间", "2,000—3,000", "1,180—1,800", "736.66", "4,602.96", "28,190.7",
        "21,313.6", "31,093.6", "4,538.7", "S7B"]
miss = [k for k in KEYS if k not in alltext]
L("Word 关键数字缺失:", miss if miss else "无")
# 章节完整性
chs = [p.strip() for p in paras if re.match(r"^第[一二三四五六七八九十]+章", p.strip())]
L("章节数:", len(chs))
for c in chs: L("   ", c[:40])
# emoji
EMO = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
L("Word emoji:", len(re.findall(EMO, alltext)))
# 英文缩写残留
for ab in ("IRR", "NPV", "CAPEX", "GOP", "ADR", "RevPAR"):
    n = len(re.findall(r"\b%s\b" % ab, alltext))
    if n: L("   ⚠ 英文缩写 %s × %d" % (ab, n))
# 内部工作符号
for sym in ("TODO", "FIXME", "XXX", "待填", "占位"):
    if sym in alltext: L("   ⚠ 内部符号:", sym)
# 旧数字残留
OLD = ["S4 6.13%", "6.13%", "2.45%", "-2.67%", "−2.67%", "−4.08%", "1.8 亿元", "1.8亿", "4.08 亿", "6 家酒店改造"]
for o in OLD:
    if o in alltext: L("   ⚠ 旧数残留:", o)
# 集团参照系
for g in ("六家", "集团六家", "额度"):
    if g in alltext:
        for i, l in enumerate(paras, 1):
            if g in l: L("   ⚠ 集团词:", l[:100]); break
L("=== Word 核验完成 ===")

# ② Excel 核验
from openpyxl import load_workbook
wb = load_workbook(XLSX)
L("=== Excel v3.0 ===")
L("%.1f KB | %d sheets" % (os.path.getsize(XLSX) / 1024, len(wb.sheetnames)))
for n in wb.sheetnames: L("   ", n)
ws = wb["08 八方案造价总表"]
L("08 行数:", ws.max_row, "列数:", ws.max_column)
bad = 0
for nm in wb.sheetnames:
    w = wb[nm]
    for rr in w.iter_rows():
        for c in rr:
            if c.value is None and c.row > 3: bad += 1
L("空单元格(>3行):", bad)

# ③ MD 一致性
m = re.search(r"^## 目录\n", t, re.M)
ls = t[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("=== MD 目录与正文一致:", toc == bod, "| 目录", len(toc), "正文", len(bod))
if toc != bod:
    for a, b in zip(toc, bod):
        if a != b: L("   差异:", a, "||", b)
L("MD emoji:", len(re.findall(EMO, t)))
L("MD 章节:", len([l for l in t.split("\n") if l.startswith("## ") and re.match(r"^## 第", l)]))

# ④ 清理旧版
for p in (os.path.join(REP, "总府皇冠改造_可行性研究报告_v2.0_2026-11-14.docx"),):
    if os.path.exists(p):
        try:
            os.remove(p); L("removed", os.path.basename(p))
        except Exception as e:
            L("[仍被占用]", os.path.basename(p), e)
L("=== 最终交付 ===")
for p in sorted(glob.glob(os.path.join(REP, "*"))) + sorted(glob.glob(os.path.join(CAL, "*"))):
    L("  [%-8s] %6.1f KB  %s" % (os.path.splitext(p)[1][1:], os.path.getsize(p) / 1024, os.path.basename(p)))
L("桌面根目录总府残留:", len(glob.glob(r"C:\Users\ericz\Desktop\*总府*")))
L("DONE")
