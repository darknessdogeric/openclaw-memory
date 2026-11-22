# -*- coding: utf-8 -*-
"""① 搜公文/汇报模板 ② 扫描成品 docx 的表格空白格"""
import io, os, sys, glob, re
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "scan.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return s.encode("unicode_escape").decode("ascii")

L("=== 1. 搜公文/汇报/模板 文件 ===")
ROOTS = [r"C:\Users\ericz\Desktop\产业发展部", r"C:\Users\ericz\Desktop",
         r"D:\B166ER-openclaw\workspace", r"D:\B166ER-openclaw"]
KEY = ("公文", "模板", "汇报", "红头", "template", "模版")
seen = set()
for root in ROOTS:
    if not os.path.isdir(root):
        continue
    for dirpath, dirs, files in os.walk(root):
        if any(x in dirpath for x in ("node_modules", ".git", "第一批次文件", "第二批次文件", "_历史版本")):
            dirs[:] = []
            continue
        for f in files:
            low = f.lower()
            if any(k.lower() in low for k in KEY) and low.endswith((".doc", ".docx", ".dot", ".dotx", ".wps", ".pdf", ".md", ".txt")):
                p = os.path.join(dirpath, f)
                if p in seen: continue
                seen.add(p)
                L("  %9.1f KB  %s" % (os.path.getsize(p)/1024, esc(os.path.relpath(p, root))))

L("\n=== 2. 目录名里带'公文/模板/汇报'的目录 ===")
for root in ROOTS[:3]:
    if not os.path.isdir(root): continue
    for dirpath, dirs, files in os.walk(root):
        for d in dirs:
            if any(k in d for k in ("公文", "模板", "汇报")):
                L("  DIR", esc(os.path.relpath(os.path.join(dirpath, d), root)))

L("\n=== 3. 成品 docx 表格空白格扫描 ===")
from docx import Document
DOC = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\改造报告交付\总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx"
d = Document(DOC)
empty_total = 0
for ti, tb in enumerate(d.tables, 1):
    blanks = []
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            txt = cell.text.strip()
            if txt == "" or txt in ("—", "-", "／", "/"):
                blanks.append((ri, ci))
    if blanks:
        empty_total += len(blanks)
        head = " | ".join(c.text.strip()[:16] for c in tb.rows[0].cells)[:110]
        L("  表%-3d %3d 空白  首行: %s" % (ti, len(blanks), esc(head)))
        for ri, ci in blanks[:8]:
            L("        行%d 列%d" % (ri, ci))
L("  表格总数 %d，空白格合计 %d" % (len(d.tables), empty_total))

L("\n=== 4. 正文里的占位符扫描（源 md）===")
MD = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.md"
t = open(MD, encoding="utf-8").read()
for i, l in enumerate(t.split("\n"), 1):
    if re.search(r"(_{2,}|待补|待填|××|XX|\?\?\?|待定|TBD|\u3010\s*\u3011)", l):
        L("  L%-5d %s" % (i, esc(l[:130])))
