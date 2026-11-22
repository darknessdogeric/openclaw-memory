# -*- coding: utf-8 -*-
"""v17：生成正式公文版《可行性研究报告》Word（GB/T 9704 体例）+ 宽表横向页 + 页码 + 版记
   正文大数原则：细节测算见配套 Excel 附表
"""
import io, os, sys, re, json, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(os.path.join(T, "v17.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

MD_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                  "总府皇冠改造_可行性研究报告_v16.0_2026-11-16.md")
OUT = os.path.join(REP, "总府皇冠改造_可行性研究报告_v16.0_2026-11-16.docx")
t = open(MD_PATH, encoding="utf-8").read()
lines = t.split("\n")

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── 字体常量（GB/T 9704 公文式例）──
FS_BIAOSONG = "方正小标宋简体"     # 发文机关标志、标题
FS_SONG = "仿宋_GB2312"           # 发文字号、正文、主送
FS_HEI = "黑体"                   # 一级标题
FS_KAI = "楷体_GB2312"            # 二级标题
FS_NUM = "宋体"                   # 页码
SZ_LV1 = 42      # 小初 发文机关标志
SZ_TITLE = 22    # 2号 标题
SZ_BODY = 16     # 3号 正文
SZ_H1 = 16       # 3号 一级标题
SZ_H2 = 16       # 3号 二级标题
SZ_H3 = 16       # 3号 三级标题
SZ_TBL = 10.5    # 五号 表格
LINE = 28.8      # 固定行距 28.8 磅（3号字 22行/页）
BT = chr(96)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.top_margin, sec.bottom_margin = Cm(3.7), Cm(3.5)
sec.left_margin, sec.right_margin = Cm(2.8), Cm(2.6)
sec.header_distance, sec.footer_distance = Cm(2.0), Cm(2.0)

st = doc.styles["Normal"]
st.font.name = FS_SONG
st.font.size = Pt(SZ_BODY)
st._element.rPr.rFonts.set(qn("w:eastAsia"), FS_SONG)
st.paragraph_format.space_before = Pt(0)
st.paragraph_format.space_after = Pt(0)

def setfont(run, name, size=None, bold=None, color=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    if size is not None: run.font.size = Pt(size)
    if bold is not None: run.bold = bold
    if color is not None: run.font.color.rgb = color

def para(text="", align="just", font=FS_SONG, size=SZ_BODY, bold=False, indent=True,
         space_before=0, space_after=0, line=LINE, color=None):
    p = doc.add_paragraph()
    p.alignment = {"just": WD_ALIGN_PARAGRAPH.JUSTIFY, "left": WD_ALIGN_PARAGRAPH.LEFT,
                   "center": WD_ALIGN_PARAGRAPH.CENTER, "right": WD_ALIGN_PARAGRAPH.RIGHT}[align]
    pf = p.paragraph_format
    pf.space_before, pf.space_after = Pt(space_before), Pt(space_after)
    if line: pf.line_spacing = Pt(line)
    if indent: pf.first_line_indent = Pt(size * 2)
    if text:
        r = p.add_run(text); setfont(r, font, size, bold, color)
    return p

INLINE = re.compile(r"(\*\*.+?\*\*|`[^`]+`|~~.+?~~)")
def inline_runs(p, text, font=FS_SONG, size=SZ_BODY, color=None):
    for part in INLINE.split(text):
        if not part: continue
        if part.startswith("**") and part.endswith("**"):
            r = p.add_run(part[2:-2]); setfont(r, font, size, True, color)
        elif part.startswith("~~") and part.endswith("~~"):
            r = p.add_run(part[2:-2]); setfont(r, font, size, False, color); r.font.strike = True
        elif part.startswith(BT) and part.endswith(BT):
            r = p.add_run(part[1:-1]); setfont(r, "Consolas", size - 1, False, color)
        else:
            r = p.add_run(part); setfont(r, font, size, False, color)

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)

def set_borders(tb, sz=4):
    tblPr = tb._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0"); e.set(qn("w:color"), "000000")
        borders.append(e)
    tblPr.append(borders)

def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader"); th.set(qn("w:val"), "true"); trPr.append(th)

def add_table(cells_rows, has_header, widths=None, fs=SZ_TBL):
    ncol = max(len(r) for r in cells_rows)
    tb = doc.add_table(rows=0, cols=ncol)
    tb.style = "Table Grid"
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_borders(tb)
    for ri, cells in enumerate(cells_rows):
        row = tb.add_row()
        for ci in range(ncol):
            cell = row.cells[ci]
            txt = cells[ci] if ci < len(cells) else ""
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (has_header and ri == 0) else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            p.paragraph_format.line_spacing = Pt(14)
            inline_runs(p, txt, FS_SONG, fs)
            if has_header and ri == 0:
                shade(cell, "D9E2F3")
                for r_ in p.runs: r_.bold = True
        if has_header and ri == 0:
            repeat_header(row)
    if widths:
        for ci, w in enumerate(widths):
            if ci < ncol:
                for row in tb.rows:
                    row.cells[ci].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return tb

def add_page_footer():
    for s in doc.sections:
        f = s.footer
        # 多个 section 可能共享同一 footer part，跳过已写入的，避免页码域重复追加
        if "PAGE" in f._element.xml:
            continue
        p = f.paragraphs[0] if f.paragraphs else f.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = Pt(14)
        r = p.add_run("— "); setfont(r, FS_NUM, 14)
        fld = OxmlElement("w:fldSimple"); fld.set(qn("w:instr"), "PAGE")
        rr = OxmlElement("w:r"); rpr = OxmlElement("w:rPr")
        sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "28"); rpr.append(sz)
        rf = OxmlElement("w:rFonts"); rf.set(qn("w:eastAsia"), FS_NUM); rpr.append(rf)
        rr.append(rpr); tnode = OxmlElement("w:t"); tnode.text = "1"; rr.append(tnode)
        fld.append(rr); p._p.append(fld)
        r2 = p.add_run(" —"); setfont(r2, FS_NUM, 14)

# ═══════════ 解析 MD_PATH 为块 ═══════════
blocks = []
i = 0
n = len(lines)
while i < n:
    l = lines[i]
    if l.startswith("|"):
        rows = []
        while i < n and lines[i].startswith("|"):
            rows.append(lines[i]); i += 1
        cells = []
        for rr in rows:
            if re.match(r"^\|[\s\-:|]+\|$", rr): continue
            cells.append([c.strip() for c in rr.strip().strip("|").split("|")])
        blocks.append(("table", cells))
        continue
    if l.strip() == "---":
        blocks.append(("hr", None)); i += 1; continue
    m = re.match(r"^(#{1,4})\s+(.*)$", l)
    if m:
        blocks.append(("h%d" % len(m.group(1)), m.group(2).strip())); i += 1; continue
    if l.startswith(">"):
        buf = []
        while i < n and lines[i].startswith(">"):
            buf.append(lines[i].lstrip(">").strip()); i += 1
        blocks.append(("quote", " ".join(x for x in buf if x)))
        continue
    if re.match(r"^\s*[-*]\s+", l):
        items = []
        while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
            items.append(re.sub(r"^\s*[-*]\s+", "", lines[i])); i += 1
        blocks.append(("ul", items)); continue
    if re.match(r"^\s*\d+\.\s+", l):
        items = []
        while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
            items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i])); i += 1
        blocks.append(("ol", items)); continue
    if not l.strip():
        i += 1; continue
    buf = []
    while i < n and lines[i].strip() and not re.match(r"^(#{1,4}\s|\||>|---$|\s*[-*]\s|\s*\d+\.\s)", lines[i]):
        buf.append(lines[i].strip()); i += 1
    blocks.append(("p", " ".join(buf)))

L("解析块数:", len(blocks))
L("  表:", sum(1 for b in blocks if b[0] == "table"))

# ═══════════ 输出 ═══════════
RED = RGBColor(0xC0, 0x00, 0x00)
chap = 0
sec_no = 0
cur_h2 = ""
in_toc = False
head_done = False
land = None

def wide_table(cells):
    """宽表 → 横向页"""
    global land
    s = doc.add_section(WD_SECTION.NEW_PAGE)
    s.orientation = WD_ORIENT.LANDSCAPE
    s.page_width, s.page_height = Cm(29.7), Cm(21.0)
    s.top_margin, s.bottom_margin = Cm(2.2), Cm(2.0)
    s.left_margin, s.right_margin = Cm(2.0), Cm(2.0)
    s.footer_distance = Cm(1.2)
    land = s

def back_portrait():
    global land
    if land is None: return
    s = doc.add_section(WD_SECTION.NEW_PAGE)
    s.orientation = WD_ORIENT.PORTRAIT
    s.page_width, s.page_height = Cm(21.0), Cm(29.7)
    s.top_margin, s.bottom_margin = Cm(3.7), Cm(3.5)
    s.left_margin, s.right_margin = Cm(2.8), Cm(2.6)
    s.footer_distance = Cm(2.0)
    land = None

tbl_no = 0
for kind, val in blocks:
    if kind == "hr":
        continue
    # ── 文首（红头区）──
    if not head_done:
        if kind == "p" and "份号" in val:
            p = para(val.replace("**", ""), "right", FS_SONG, 12, False, False, 0, 2, 14)
            continue
        if kind == "p" and "安逸酒店集团有限责任公司" in val:
            p = para(val.replace("**", "").replace("　", "").strip(), "center", FS_BIAOSONG, SZ_LV1, False, False, 6, 0, 40, RED)
            continue
        if kind == "p" and "〔2026〕" in val:
            para(val.replace("**", "").strip(), "center", FS_SONG, SZ_BODY, False, False, 2, 2, LINE)
            continue
        if kind == "p" and val.startswith("签发人"):
            para(val.replace("**", "").strip(), "right", FS_SONG, SZ_BODY, False, False, 2, 10, LINE)
            continue
        if kind == "h1":
            para(val, "center", FS_BIAOSONG, SZ_TITLE, False, False, 10, 4, 36)
            continue
        if kind == "h2" and val.startswith("（讨论稿）"):
            para(val, "center", FS_KAI, SZ_BODY, False, False, 0, 6, LINE)
            continue
        if kind == "p" and val.startswith("主送"):
            para(val.replace("**", "").strip(), "left", FS_SONG, SZ_BODY, False, False, 0, 0, LINE)
            continue
        if kind == "p" and val == "各有关单位：":
            para(val, "left", FS_SONG, SZ_BODY, False, False, 0, 2, LINE)
            head_done = True
            continue
        if kind == "h2" and val == "目录":
            in_toc = True
            p = para("目　录", "center", FS_HEI, SZ_H1, False, False, 10, 10, LINE)
            continue
        # 目录条目
        if in_toc and kind == "p" and re.match(r"^\d+\.\s", val):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = Pt(24)
            inline_runs(p, val, FS_SONG, SZ_BODY)
            continue
        # 目录条目（Markdown 有序列表整体成块时的处理）
        if in_toc and kind == "ol":
            for _i, _it in enumerate(val, 1):
                pp = doc.add_paragraph()
                pp.alignment = WD_ALIGN_PARAGRAPH.LEFT
                pf = pp.paragraph_format
                pf.space_before, pf.space_after = Pt(0), Pt(2)
                pf.line_spacing = Pt(24)
                inline_runs(pp, "%d. %s" % (_i, _it), FS_SONG, SZ_BODY)
            continue
        # 修正：目录状态须在遇到章节标题(h1/h2/h3/h4)或非目录条目段落时退出，
        # 否则 h2 章节标题与其后第一张表会被 L285 的 `if in_toc: continue` 一并吞掉
        if in_toc and kind in ("p", "h1", "h2", "h3", "h4") \
                and not (kind == "p" and re.match(r"^\d+\.\s", val)):
            in_toc = False
        if in_toc:
            continue
    if in_toc and kind != "table":
        if not (kind == "p" and re.match(r"^\d+\.\s", val)):
            in_toc = False
    # ── 正文 ──
    if kind == "h2":
        back_portrait()
        chap += 1
        para(val, "left", FS_HEI, SZ_H1, False, False, 14, 8, LINE)
        tbl_no = 0
        continue
    if kind == "h3":
        sec_no += 1
        cur_h2 = val
        para(val, "left", FS_KAI, SZ_H2, False, True, 6, 4, LINE)
        continue
    if kind == "h4":
        para(val, "left", FS_SONG, SZ_H3, True, True, 4, 3, LINE)
        continue
    if kind == "p" and re.match(r"^!\[[^\]]*\]\([^)]+\)\s*$", val.strip()):
        mm = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", val.strip())
        alt, rel = mm.group(1), mm.group(2)
        ip = rel if os.path.isabs(rel) else os.path.join(os.path.dirname(MD_PATH), rel)
        if os.path.exists(ip):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf = p.paragraph_format
            pf.space_before, pf.space_after = Pt(4), Pt(2)
            p.add_run().add_picture(ip, width=Cm(15.8))
            L("  [IMG] %s" % os.path.basename(ip))
        else:
            L("  [IMG-MISS] %s" % ip)
        continue
    if kind == "p":
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.space_before, pf.space_after = Pt(0), Pt(0)
        pf.line_spacing = Pt(LINE)
        pf.first_line_indent = Pt(SZ_BODY * 2)
        inline_runs(p, val, FS_SONG, SZ_BODY)
        continue
    if kind == "quote":
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.left_indent = Pt(SZ_BODY)
        pf.space_before, pf.space_after = Pt(3), Pt(3)
        pf.line_spacing = Pt(LINE)
        inline_runs(p, val, FS_KAI, SZ_BODY)
        continue
    if kind == "ul":
        for it in val:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            pf = p.paragraph_format
            pf.left_indent = Pt(SZ_BODY * 2)
            pf.first_line_indent = Pt(-SZ_BODY)
            pf.space_after = Pt(0)
            pf.line_spacing = Pt(LINE)
            inline_runs(p, "— " + it, FS_SONG, SZ_BODY)
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        continue
    if kind == "ol":
        for it in val:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            pf = p.paragraph_format
            pf.left_indent = Pt(SZ_BODY * 2)
            pf.first_line_indent = Pt(-SZ_BODY)
            pf.space_after = Pt(2)
            pf.line_spacing = Pt(LINE)
            inline_runs(p, it, FS_SONG, SZ_BODY)
        continue
    if kind == "table":
        ncol = max(len(r) for r in val)
        tbl_no += 1
        # 表题
        cap = "表 %d-%d　%s" % (chap, tbl_no, re.sub(r"^（[一二三四五六七八九十]+）\s*", "", cur_h2) or "测算表")
        p = para(cap, "center", FS_HEI, 12, False, False, 6, 3, 18)
        if ncol >= 6:
            wide_table(val)
            avail = 29.7 - 4.0
            fs = 9 if ncol <= 12 else 8
            add_table(val, True, [avail / ncol] * ncol, fs)
            back_portrait()
        else:
            avail = 21.0 - 5.4
            fs = 10.5 if ncol <= 5 else 9
            add_table(val, True, [avail / ncol] * ncol, fs)
        continue

add_page_footer()
doc.save(OUT)
L("DOCX %.1f KB" % (os.path.getsize(OUT) / 1024))

# ═══════════ 终检 ═══════════
from docx import Document as D2
d = D2(OUT)
blank = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "—", "-", "／", "/"):
                blank += 1
                L("  BLANK 表%d 行%d 列%d : %s" % (ti, ri, ci, " || ".join(cell.text.strip()[:22] for cell in row.cells)))
L("段落 %d / 表格 %d / 空白格 %d / 节 %d" % (len(d.paragraphs), len(d.tables), blank, len(d.sections)))
EMO = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
L("emoji:", len(re.findall(EMO, t)))
bad = [l for l in t.split("\n") if l.startswith("#") and ("|" in l or "**" in l or len(l) > 95)]
L("标题异常:", len(bad))
L("DONE")
