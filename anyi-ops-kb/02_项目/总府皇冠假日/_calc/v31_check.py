# -*- coding: utf-8 -*-
"""v31 最后核查：公文要件（红头/目录/页码/版记）、正文↔Excel 数字一致性抽查、索引同步"""
import io, os, sys, re, json, glob
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v31.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
XLSX = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v3.0_2026-11-14.xlsx")
MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
from docx import Document
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]

# ① 公文要件
L("=== 公文要件核查 ===")
L("前 8 段:")
for i, p in enumerate(paras[:8]):
    if p.strip(): L("   [%d] %s" % (i, p.strip()[:80]))
L("后 8 段:")
for i, p in enumerate(paras[-8:]):
    if p.strip(): L("   %s" % p.strip()[:90])
# 页眉页脚
for si, s in enumerate(d.sections):
    ht = " ".join(p.text for p in s.header.paragraphs).strip()
    ft = " ".join(p.text for p in s.footer.paragraphs).strip()
    fx = s.footer._element.xml if s.footer is not None else ""
    hx = s.header._element.xml if s.header is not None else ""
    L("S%d 页眉:%r | 页脚:%r | 页脚域PAGE:%s | 页眉域:%s" % (
        si, ht[:40], ft[:40], ("PAGE" in fx), ("PAGE" in hx)))
# 目录
toc_idx = next((i for i, p in enumerate(paras) if p.strip() in ("目 录", "目录")), None)
L("目录段位置:", toc_idx)
if toc_idx is not None:
    L("目录后 16 行:")
    for p in paras[toc_idx + 1: toc_idx + 17]:
        if p.strip(): L("   %s" % p.strip()[:70])
L("fldChar/instrText 域:", d.element.xml.count("instrText"))

# ② 正文↔Excel 数字一致性抽查
from openpyxl import load_workbook
wb = load_workbook(XLSX)
ws = wb["08 九方案造价总表"]
xls = {}
for rr in range(5, ws.max_row + 1):
    k = ws.cell(row=rr, column=1).value
    if isinstance(k, str) and k.startswith("S"):
        xls[k] = [ws.cell(row=rr, column=c).value for c in range(1, 26)]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
L("=== 正文↔Excel 一致性抽查（08 表）===")
COLS = {"capex": 10, "total_need": 11, "adr": 12, "rev": 13, "delta": 15, "ratio": 16,
        "irr": 17, "npv": 18, "pb_grp": 21}
bad = 0
for k, row in xls.items():
    for name, ci in COLS.items():
        v = row[ci - 1]
        if v is None: continue
        s = ("%.2f" % v) if isinstance(v, float) else str(v)
        if isinstance(v, float):
            cands = ["%s" % format(round(v, 1), ",.1f"), "%s" % format(round(v, 2), ",.2f"),
                     "%.2f%%" % (v * 100), "%.1f%%" % (v * 100)]
            if v == 1.0: cands.append("1.00")
            hit = any(c in alltext for c in cands)
        else:
            hit = str(v) in alltext
        if not hit:
            L("   ⚠ %s.%s = %r 未在正文命中" % (k, name, v)); bad += 1
L("不一致条目:", bad if bad else "0（全部一致）")

# ③ MD 侧同样抽查
md = open(MD, encoding="utf-8").read()
bad2 = 0
for k, row in xls.items():
    for name, ci in COLS.items():
        v = row[ci - 1]
        if v is None: continue
        if isinstance(v, float):
            cands = [format(round(v, 1), ",.1f"), format(round(v, 2), ",.2f"), "%.2f%%" % (v * 100), "%.1f%%" % (v * 100)]
            hit = any(c in md for c in cands)
        else:
            hit = str(v) in md
        if not hit:
            L("   ⚠ MD %s.%s = %r 未命中" % (k, name, v)); bad2 += 1
L("MD 不一致条目:", bad2 if bad2 else "0（全部一致）")

# ④ 索引同步
RM = os.path.join(KB, "00_项目总览_README.md")
rm = open(RM, encoding="utf-8").read()
for need in ("v3.0", "分档定价", "S7B"):
    if need not in rm: L("   ⚠ README 缺:", need)
L("README 命中 v3.0/分档定价/S7B:", all(x in rm for x in ("v3.0", "分档定价", "S7B")))
L("=== 最终交付清单 ===")
for p in sorted(glob.glob(os.path.join(REP, "总府皇冠改造_可行性研究报告*"))) + sorted(glob.glob(os.path.join(CAL, "总府皇冠改造_可行性研究报告*"))):
    L("  %6.1f KB  %s" % (os.path.getsize(p) / 1024, os.path.basename(p)))
L("DONE")
