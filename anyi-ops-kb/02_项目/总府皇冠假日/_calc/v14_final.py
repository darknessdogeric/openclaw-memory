# -*- coding: utf-8 -*-
"""v14 收官：第八节表补列（split 重写）、修 SWOT O5 旧值、Excel 补相对额度列、出 v3.2、终检"""
import io, os, sys, re, json, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v14.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return str(s).encode("unicode_escape").decode("ascii")

MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v3.2_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ══ ① 第六章第八节表：补「相对集团 1.8 亿额度」列（split 重写）══
OVER = {"S1": 3313.6, "S2": 3288.0, "S3": 11171.3, "S4": 10190.7,
        "S5": 21550.7, "S6": 26381.3, "S7": 38850.9, "S8": 32276.7}
lines = t.split("\n")
i0 = next((i for i, l in enumerate(lines) if l.startswith("| 方案 | 品牌标准 | 公区做法")), None)
assert i0 is not None, "未找到第八节表头"
n = 0
for i in range(i0 + 2, len(lines)):
    l = lines[i]
    if not l.startswith("|"):
        break
    cells = [c.strip() for c in l.split("|")[1:-1]]
    if len(cells) < 10 or not re.match(r"^S[1-8]$", cells[0]):
        continue
    k = cells[0]
    if len(cells) >= 11 and cells[10]:
        continue
    cells = cells[:10] + ["+%s" % format(OVER[k], ",.1f")]
    lines[i] = "| " + " | ".join(cells) + " |"
    n += 1
t = "\n".join(lines)
L("第八节表补列行数:", n)

# ══ ② SWOT O5 旧值 ══
OLD = "净结果是 20 年内部收益率由 5.37% 降至 3.66%"
NEW = "净结果须以 20 年全口径重算后另行判定"
if OLD in t:
    t = t.replace(OLD, NEW); L("[FIX] SWOT O5")
else:
    L("[MISS] SWOT O5")
# 兜底：清掉任何残留的 5.37%／3.66%
for bad, good in (("20 年内部收益率由 5.37% 降至 3.66%", "净结果须以 20 年全口径重算后另行判定"),):
    if bad in t:
        t = t.replace(bad, good); L("[FIX2]", bad[:20])

open(MD, "w", encoding="utf-8").write(t)

# ══ ③ Excel：07 表补「相对集团 1.8 亿额度」列 ══
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
XL = os.path.join(CAL, "总府皇冠改造_完整造价构成表_v1.0_2026-11-14.xlsx")
wb = load_workbook(XL)
THIN = Side(style="thin", color="BFBFBF"); BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
B = Font(bold=True); HD = PatternFill("solid", fgColor="D9E2F3")
BAD = PatternFill("solid", fgColor="FFC7CE")
ws = wb["07 八方案造价总表"]
hr = None
for r in range(1, 8):
    if ws.cell(row=r, column=1).value == "方案":
        hr = r; break
if hr:
    lastcol = ws.max_column
    c = ws.cell(row=hr, column=lastcol + 1, value="相对集团 1.8 亿额度（万元）")
    c.font = B; c.fill = HD; c.border = BD
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.column_dimensions[chr(64 + lastcol + 1) if lastcol + 1 <= 26 else "A"].width = 22
    rr = hr + 1
    for k in ("S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"):
        if ws.cell(row=rr, column=1).value != k:
            break
        cc = ws.cell(row=rr, column=lastcol + 1, value=OVER[k])
        cc.number_format = "+#,##0.0"; cc.border = BD
        if k == "S8":
            cc.fill = BAD
        rr += 1
    L("[XLS] 07 表补列 OK")
wb.save(XL)
L("XLSX %.1f KB" % (os.path.getsize(XL)/1024))

# ══ ④ 出 Word + 大纲 ══
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v3.2_2026-11-14.docx")
convert(MD, out)
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
TMP = os.path.join(T, "_v32e.docx")
d = Document(out)
def set_outline(p, lvl):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:outlineLvl")):
        pPr.remove(old)
    e = OxmlElement("w:outlineLvl"); e.set(qn("w:val"), str(lvl)); pPr.append(e)
cnt = {"0": 0, "1": 0, "2": 0}
for p in d.paragraphs:
    tx = p.text.strip()
    if not tx or len(tx) > 60: continue
    if re.match(r"^\d+\. [一二三四五六七八九十]+、", tx): continue
    lvl = None
    if tx == "关于总府皇冠假日酒店改造升级工作思路的报告": lvl = 0
    elif re.match(r"^[一二三四五六七八九十]+、\S", tx): lvl = 1
    elif re.match(r"^（[一二三四五六七八九十]+）", tx): lvl = 2
    elif re.match(r"^\d+\.\d+\s", tx): lvl = 2
    if lvl is not None:
        set_outline(p, lvl); p.paragraph_format.keep_with_next = True; cnt[str(lvl)] += 1
d.save(TMP); shutil.move(TMP, out)
L("DOCX %.1f KB | 大纲 L0=%d L1=%d L2=%d" % (os.path.getsize(out)/1024, cnt["0"], cnt["1"], cnt["2"]))

# ══ ⑤ 终检 ══
d = Document(out)
blank = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "\u2014", "-", "\uff0f", "/"):
                blank += 1
                L("  BLANK 表%d 行%d 列%d : %s" % (ti, ri, ci, " || ".join(cell.text.strip()[:22] for cell in row.cells)))
L("docx: 段落 %d / 表格 %d / 空白格 %d" % (len(d.paragraphs), len(d.tables), blank))
EMO = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
L("emoji:", len(re.findall(EMO, t)), "| ??:", len(re.findall(r"\?\?", t)), "| 单问号:", len(re.findall(r"\?(?=[\d(（])", t)))
L("=== 旧值残留 ===")
for k in ("14,401", "5.37%", "19.93%", "12.48%", "7.10 年", "9,919", "14,061", "27,919", "32,061", "38,784", "20,724", "3.66%"):
    c = t.count(k)
    if c: L("  [旧值]", k, c)
L("=== 关键新值 ===")
for k in ("21,313.6", "31,093.6", "4,538.7", "4.60%", "6.13%", "1,186 元", "11,060", "9,780", "76.2%", "13,040", "28,190.7", "56,850.9", "+3,313.6", "+38,850.9"):
    L("  %-12s %s" % (k, "在" if k in t else "缺"))
bad = [l for l in t.split("\n") if l.startswith("#") and ("|" in l or "**" in l or len(l) > 95)]
L("标题异常:", len(bad))
m = re.search(r"^## 目录\n", t, re.M)
ls = t[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc_items = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
body_items = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录与正文一致:", toc_items == body_items, "| 目录", len(toc_items), "正文", len(body_items))
L("MD bytes:", len(t.encode("utf-8")))

# ══ ⑥ 清理旧版 ══
for n in ("总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx",
          "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.docx",
          "总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.docx",
          "总府皇冠改造_立项报告_集团汇报件_v3.1_2026-11-14.docx"):
    p = os.path.join(REP, n)
    if os.path.exists(p):
        try:
            os.remove(p); L("removed", n)
        except Exception:
            L("[仍被 Word 占用]", n)
for f in glob.glob(os.path.join(REP, "~$*")):
    try:
        os.remove(f); L("removed lock", os.path.basename(f))
    except Exception:
        L("[锁文件残留]", os.path.basename(f))

L("\n=== 最终交付 ===")
for f in sorted(glob.glob(os.path.join(REP, "*.docx"))):
    if os.path.basename(f).startswith("~$"): continue
    if not re.search(r"立项报告_集团汇报件|立项方案_数据源清单", f): continue
    L("  [报告] %-68s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
for f in sorted(glob.glob(os.path.join(CAL, "*.xlsx"))):
    L("  [测算] %-68s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
L("DONE")
