
# -*- coding: utf-8 -*-
"""md2docx.py - Markdown -> 排版 DOCX（通用，中文研判/报告规格）
用法: python md2docx.py <in.md> <out.docx> [--title "..."] [--subtitle "..."]
"""
import io, sys, os, re
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

INK   = RGBColor(0x23,0x16,0x10); INK2 = RGBColor(0x5C,0x46,0x30)
ACC   = RGBColor(0xA8,0x1E,0x2E); GOLD = RGBColor(0x8A,0x6A,0x2A)
PAPER = "FBF7EE"; HDR_FILL = "EFE3CC"; QUOTE_FILL = "FBF6EA"

def setfont(run, name="宋体", size=10.5, bold=False, color=INK, italic=False):
    run.font.name = name; run.font.size = Pt(size)
    run.bold = bold; run.italic = italic; run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rpr.append(rf)
    for a in ("w:ascii","w:hAnsi","w:eastAsia","w:cs"):
        rf.set(qn(a), name)

def shade(el, hexc):
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"),"clear"); sh.set(qn("w:color"),"auto"); sh.set(qn("w:fill"),hexc)
    el.append(sh)

def border_left(p, hexc="C9A96A", sz=18):
    pPr = p._p.get_or_add_pPr(); bd = OxmlElement("w:pBdr"); l = OxmlElement("w:left")
    l.set(qn("w:val"),"single"); l.set(qn("w:sz"),str(sz)); l.set(qn("w:space"),"8"); l.set(qn("w:color"),hexc)
    bd.append(l); pPr.append(bd)

def hrule(p, color="D9C69A", sz=8):
    pPr = p._p.get_or_add_pPr(); bd = OxmlElement("w:pBdr"); b = OxmlElement("w:bottom")
    b.set(qn("w:val"),"single"); b.set(qn("w:sz"),str(sz)); b.set(qn("w:space"),"1"); b.set(qn("w:color"),color)
    bd.append(b); pPr.append(bd)

def spacing(p, before=0, after=4, line=1.35):
    pf = p.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after); pf.line_spacing = line

def add_md_runs(p, text, size=10.5, color=INK):
    for seg in re.split(r"(\*\*.+?\*\*|`.+?`)", text):
        if not seg: continue
        if seg.startswith("**") and seg.endswith("**"):
            r = p.add_run(seg[2:-2]); setfont(r, "黑体", size, True, color)
        elif seg.startswith("`") and seg.endswith("`"):
            r = p.add_run(seg[1:-1]); setfont(r, "Consolas", size-0.5, False, INK2)
        else:
            r = p.add_run(seg); setfont(r, "宋体", size, False, color)

def is_sep(line):
    # ★ 必须 remove 全部竖线（含中间分隔符），只 strip 首尾会残留中间的 "|" 导致判定失败
    s = line.strip().replace("|", "").replace(" ", "").replace("\t", "")
    return len(s) > 0 and set(s) <= set("-:")

def build(md_path, out_path, title=None, subtitle=None):
    d = docx.Document()
    st = d.styles["Normal"]; st.font.name = "宋体"; st.font.size = Pt(10.5)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    sec = d.sections[0]
    sec.page_width = Cm(21); sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.0); sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.4); sec.right_margin = Cm(2.4)
    if title:
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        spacing(p, 0, 4, 1.25)
        r = p.add_run(title); setfont(r, "黑体", 19, True, INK)
    if subtitle:
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        spacing(p, 0, 10, 1.3)
        r = p.add_run(subtitle); setfont(r, "楷体", 10.5, False, INK2)
        hrule(p, "C9A96A", 12)
    lines = open(md_path, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1; continue
        # table
        if s.startswith("|") and i+1 < len(lines) and is_sep(lines[i+1]):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            ncol = max(len(r) for r in rows)
            tbl = d.add_table(rows=0, cols=ncol); tbl.style = "Table Grid"
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            for ri, row in enumerate(rows):
                if ri == 1 and is_sep("|" + "|".join(row) + "|"):
                    continue
                cells = tbl.add_row().cells
                for ci in range(ncol):
                    val = row[ci] if ci < len(row) else ""
                    cp = cells[ci].paragraphs[0]; spacing(cp, 1, 1, 1.15)
                    if ri == 0:
                        shade(cells[ci]._tc, HDR_FILL)
                        add_md_runs(cp, val, 9.5, INK)
                        for r2 in cp.runs: r2.bold = True
                    else:
                        add_md_runs(cp, val, 9.5, INK)
            d.add_paragraph(); continue
        if s.startswith("---"):
            p = d.add_paragraph(); spacing(p, 2, 6); hrule(p); i += 1; continue
        if s.startswith("### "):
            p = d.add_paragraph(); spacing(p, 9, 2, 1.2)
            r = p.add_run(s[4:]); setfont(r, "黑体", 12.5, True, INK); i += 1; continue
        if s.startswith("## "):
            p = d.add_paragraph(); spacing(p, 13, 4, 1.2)
            r = p.add_run(s[3:]); setfont(r, "黑体", 15, True, ACC)
            hrule(p, "C9A96A", 12); i += 1; continue
        if s.startswith("# "):
            p = d.add_paragraph(); spacing(p, 6, 4, 1.25)
            r = p.add_run(s[2:]); setfont(r, "黑体", 17, True, INK); i += 1; continue
        if s.startswith("> "):
            p = d.add_paragraph(); spacing(p, 3, 3, 1.4)
            border_left(p); shade(p._p, QUOTE_FILL)
            add_md_runs(p, s[2:], 10, INK2); i += 1; continue
        if s.startswith("*") and s.endswith("*") and not s.startswith("**"):
            p = d.add_paragraph(); spacing(p, 2, 4, 1.3)
            shade(p._p, "F4E7E2")
            add_md_runs(p, s.strip("*"), 9.5, ACC); i += 1; continue
        if s.startswith("- ") or s.startswith("\u2022 "):
            # ★ 列表：公文范式要求纯文字段落、无项目符号；缩进 2 字符
            p = d.add_paragraph(); spacing(p, 2, 4, 1.45)
            p.paragraph_format.left_indent = Cm(0.74)
            add_md_runs(p, s[2:]); i += 1; continue
        p = d.add_paragraph(); spacing(p, 2, 4, 1.45)
        add_md_runs(p, s); i += 1
    d.save(out_path)
    return out_path

if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2:
        print("用法: python md2docx.py <in.md> <out.docx> [--title T] [--subtitle S]"); raise SystemExit(1)
    src, dst = a[0], a[1]
    t = s = None
    if "--title" in a: t = a[a.index("--title")+1]
    if "--subtitle" in a: s = a[a.index("--subtitle")+1]
    out = build(src, dst, t, s)
    print("DOCX:", os.path.getsize(out), "B ->", out)
