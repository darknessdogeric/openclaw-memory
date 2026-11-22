# -*- coding: utf-8 -*-
"""v105：交付终检（跨文件数字一致性）"""
import io, os, re, sys, glob, json
from docx import Document
from openpyxl import load_workbook
sys.stdout.reconfigure(encoding="utf-8")

T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
D = json.load(open(os.path.join(T, "v98.json"), encoding="utf-8"))
R = D["results"]

DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v6.0_2026-11-15.docx")
XLSX = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v6.0_2026-11-15.xlsx")
MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v6.0_2026-11-15.md")

print("=" * 78)
print("一、交付文件清单")
print("=" * 78)
for d in (REP, CAL):
    for f in sorted(glob.glob(os.path.join(d, "*"))):
        if os.path.isfile(f):
            print("  %7.1f KB  %-72s" % (os.path.getsize(f) / 1024, os.path.basename(f)))
for f in (os.path.join(TGT, "00_总府皇冠改造项目_文件索引.docx"),
          os.path.join(TGT, "00_总府皇冠改造项目_文件索引.md")):
    print("  %7.1f KB  %s" % (os.path.getsize(f) / 1024, f.split("\\")[-1]))

print()
print("=" * 78)
print("二、Word 终检")
print("=" * 78)
d = Document(DOCX)
alltext = "\n".join(p.text for p in d.paragraphs) + "\n" + "\n".join(
    c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells
            if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/", "\u2013"))
EMO = ("[" + chr(92) + "U0001F300-" + chr(92) + "U0001FAFF" + chr(92) + "U00002600-" + chr(92) + "U000027BF"
       + chr(92) + "U00002B50" + chr(92) + "uFE0F" + chr(92) + "u200D" + chr(92) + "u2764" + chr(92) + "u2B06"
       + chr(92) + "u2B07" + chr(92) + "u2B05" + chr(92) + "u274C" + chr(92) + "u2705" + chr(92) + "u26A0"
       + chr(92) + "u26A1" + chr(92) + "u2139" + chr(92) + "u24C2" + chr(92) + "u2B55]")
nimg = 0
for rel in d.part.rels.values():
    if "image" in rel.reltype: nimg += 1
print("  {0:.1f} KB｜段落 {1}｜表格 {2}｜空白格 {3}｜节 {4}｜图片 {5}｜emoji {6}".format(
    os.path.getsize(DOCX) / 1024, len(d.paragraphs), len(d.tables), blank,
    len(d.sections), nimg, len(re.findall(EMO, alltext))))
for i, sec in enumerate(d.sections):
    pg = sec.footer._element.xml.count('w:instr="PAGE"')
    orient = "横" if sec.page_width > sec.page_height else "纵"
    print("   S{0} {1} {2:.0f}x{3:.0f} 页码域{4}".format(i, orient, sec.page_width.cm, sec.page_height.cm, pg))
# 目录 vs 正文（Word 内）
paras = [p.text.strip() for p in d.paragraphs]
ti = next((i for i, x in enumerate(paras) if x.replace(" ", "").endswith("目录")), 0)
toc_items = [t for t in paras[ti + 1: ti + 30] if re.match(r"^\d+\.\s", t)]
heads = [t for t in paras if re.match(r"^\d+\.\s\S", t) and t[:3].strip().rstrip(".").isdigit()]
uniq = []
for h in heads:
    if h not in uniq: uniq.append(h)
print("  目录条目 {0}｜正文标题 {1}".format(len(toc_items), len(uniq)))
print("  目录↔正文一致: {0}".format([re.sub(r"^\d+\.\s", "", x) for x in toc_items] ==
                                     [re.sub(r"^\d+\.\s", "", x) for x in uniq]))
print("  标题异常: {0}".format(sum(1 for p in d.paragraphs if not p.text.strip() and p.style.name.startswith("Heading"))))

print()
print("=" * 78)
print("三、Excel 终检")
print("=" * 78)
wb = load_workbook(XLSX, data_only=True)
print("  {0:.1f} KB｜{1} 个表：{2}".format(os.path.getsize(XLSX) / 1024, len(wb.sheetnames), "、".join(wb.sheetnames)))
xtext = ""
for ws in wb.worksheets:
    for row in ws.iter_rows(values_only=True):
        for v in row:
            if v is not None: xtext += str(v) + " "

print()
print("=" * 78)
print("四、跨文件数字一致性（模型 → Word → Excel → Markdown）")
print("=" * 78)
md = io.open(MD, encoding="utf-8").read()
def fmt(v):
    s = "%+.0f" % v if abs(v) >= 1000 else "%.0f" % v
    return s.replace("-", "\u2212")
CHECK = []
for k in ("P1", "P2", "P3", "P4"):
    r = R[k]
    npv_s = ("\u2212" if r["npv"] < 0 else "\uff0b") + "{:,.0f}".format(abs(r["npv"]))
    CHECK.append((k + " 净现值", npv_s))
    CHECK.append((k + " 投资", "{:,.0f}".format(r["owner_capex"])))
    CHECK.append((k + " IRR", "{:.2f}%".format(r["irr_pct"])))
for lbl, v in CHECK:
    a = "有" if v in alltext else "缺"
    b = "有" if v.replace(",", "") in xtext.replace(",", "") or v in xtext else "缺"
    c = "有" if v in md else "缺"
    flag = "" if (a == "有" and c == "有") else "  <<< 核查"
    print("  {0:<16} {1:<14} Word:{2}  Excel:{3}  MD:{4}{5}".format(lbl, v, a, b, c, flag))
KEY = ["11,066", "21,054", "24,119", "24,340", "9,884", "6,442.73", "5,403.53", "−416.51",
       "60,914.78", "14,382", "60,677", "2,088.85", "10,192", "25.35", "1,280", "416.29",
       "107.90", "989 间", "757", "697", "43 次", "0.0017", "2029-09-27", "−5,227",
       "209 间", "205 间", "14.69", "9.30%", "2.21%", "2.37%", "1.36%", "1,020 件", "84.22%"]
miss_w = [k for k in KEY if k not in alltext]
miss_m = [k for k in KEY if k not in md]
print("  Word 关键值缺失: {0}".format(miss_w if miss_w else "无（%d 项全中）" % len(KEY)))
print("  MD   关键值缺失: {0}".format(miss_m if miss_m else "无（%d 项全中）" % len(KEY)))

print()
print("=" * 78)
print("五、Markdown 自审")
print("=" * 78)
print("  emoji {0}｜★ {1}｜☆ {2}｜字数 {3}".format(
    len(re.findall(EMO, md)), md.count("\u2605"), md.count("\u2606"), len(md)))
lines = md.split("\n"); inb = False; nb = 0; ntab = 0
for l in lines:
    if l.strip().startswith("|"):
        if not inb: inb = True; ntab += 1; continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if all(re.match(r"^:?-{2,}:?$", c or "-") for c in cells): continue
        nb += sum(1 for c in cells if c == "")
    else: inb = False
print("  表格 {0} 个｜空白单元格 {1}".format(ntab, nb))
m = re.search(r"^## 目录\n", md, re.M); ls = md[m.end():].split("\n")
st = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\.\s", "", l).strip() for l in ls[:st] if re.match(r"^\d+\.\s", l)]
bod = [re.sub(r"^\d+\.\s", "", l[3:]).strip() for l in ls[st:] if l.startswith("## ")]
print("  目录↔正文: {0}（目录 {1}／正文 {2}）".format(toc == bod, len(toc), len(bod)))
figs = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", md)
miss_f = [rel for cap, rel in figs if not os.path.exists(os.path.join(KB, rel))]
print("  图引用 {0} 张｜缺失 {1}".format(len(figs), miss_f if miss_f else "无"))

print()
print("=" * 78)
print("六、归档检查")
print("=" * 78)
res = glob.glob(r"C:\Users\ericz\Desktop\*\u603b\u5e9c*")
print("  桌面根目录总府残留: {0}".format(len(res)))
for r in res: print("   ", r)
print("  项目文件夹总文件数: {0}".format(len([f for f in glob.glob(os.path.join(TGT, '**', '*'), recursive=True) if os.path.isfile(f)])))
print("DONE")
