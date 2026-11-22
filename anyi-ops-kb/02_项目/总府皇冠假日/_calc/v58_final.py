# -*- coding: utf-8 -*-
"""v58：v4.0 收官 —— 真实 emoji 定位与清除、占位填实措辞逐条核验、表数差异定位、终检"""
import io, os, sys, re, json, glob, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v58.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

MD4 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.md")
t = open(MD4, encoding="utf-8").read()
lines = t.split("\n")

# ① 真实 emoji（正确的 unicode 转义，非原始字符串）
EMO = ("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D"
       "\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]")
hits = []
for i, l in enumerate(lines, 1):
    for m in re.finditer(EMO, l):
        ch = m.group(0)
        hits.append((i, ch, hex(ord(ch)), l[max(0,m.start()-40):m.start()+40]))
L("=== 真实 emoji 命中 %d ===" % len(hits))
for i, ch, hx, ctx in hits:
    L("   L%d  %s (%s)  ...%s..." % (i, ch, hx, ctx.replace("\n", " ")))

# ② 占位填实结果核验
L("")
L("=== 占位填实后的表述核验 ===")
for i, l in enumerate(lines, 1):
    if "按 2026 皇冠品牌标准更新" in l or "不适用（中高端有限服务档）" in l or "未公开披露" in l and "房量" in l:
        L("   L%d | %s" % (i, l.strip()[:150]))

# ③ 表数差异定位
sep = sum(1 for l in lines if re.match(r"^\|[\s:\-|]+\|$", l.strip()))
L("")
L("=== 表结构核查 ===")
L("   分隔行（表头下横线）数: %d ｜表格块数: %d" % (sep, sum(1 for _ in re.finditer(r"(?m)^\|.*\|$\n\|[\s:\-|]+\|", t))))
L("   → v17 解析块 40 / Word 表 39：差 1 张，须定位")

# ④ 逐块解析，找出被合并或异常的空表
blocks = []
i = 0
while i < len(lines):
    if lines[i].startswith("|"):
        j = i
        while j < len(lines) and lines[j].startswith("|"): j += 1
        blk = lines[i:j]
        ncol = len(blk[0].strip().strip("|").split("|"))
        nsep = sum(1 for b in blk if re.match(r"^\|[\s:\-|]+\|$", b.strip()))
        blocks.append((i+1, j, ncol, len(blk), nsep))
        i = j
    else:
        i += 1
L("   MD 表格块 %d 个" % len(blocks))
for b in blocks:
    if b[3] <= 2 or b[4] != 1:
        L("   ⚠ 异常块 行%d-%d 列%d 行数%d 分隔行%d" % b)

# ⑤ 清除真实 emoji
if hits:
    t2 = re.sub(EMO, "", t)
    open(MD4, "w", encoding="utf-8").write(t2)
    L("[MD] 已清除真实 emoji %d 处" % len(hits))
else:
    t2 = t

# ⑥ 消防子项表内容列：把泛化措辞改为逐项准确表述
REPL = {
 "| 防火门监控系统及门禁 | 80 | 按 2026 皇冠品牌标准更新 |":
 "| 防火门监控系统及门禁 | 80 | 防火门状态监测与门禁联动控制 |",
 "| 电气火灾监控系统 | 40 | 按 2026 皇冠品牌标准更新 |":
 "| 电气火灾监控系统 | 40 | 剩余电流与测温式电气火灾监控 |",
 "| 消防报建 | 10 | 按 2026 皇冠品牌标准更新 |":
 "| 消防报建 | 10 | 消防设计审查、验收报建与资料归档 |",
 "| 消防水炮 | 10 | 按 2026 皇冠品牌标准更新 |":
 "| 消防水炮 | 10 | 增设室内消防水炮灭火系统 |",
 "| 防火卷帘系统 | 10 | 按 2026 皇冠品牌标准更新 |":
 "| 防火卷帘系统 | 10 | 防火分区卷帘与联动降落 |",
 "| 监控室机房改造 | 30 | 按 2026 皇冠品牌标准更新 |":
 "| 监控室机房改造 | 30 | 消防控制中心机房设备与装修 |",
}
n = 0
for a, b in REPL.items():
    if a in t2:
        t2 = t2.replace(a, b); n += 1
L("[MD] 消防子项内容列逐项校正:", n)
open(MD4, "w", encoding="utf-8").write(t2)

# ⑦ Excel 同步同一措辞
from openpyxl import load_workbook
XL = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v4.0_2026-11-14.xlsx")
wb = load_workbook(XL)
nx = 0
for ws in wb.worksheets:
    for rr in range(1, ws.max_row + 1):
        for cc in range(1, ws.max_column + 1):
            v = ws.cell(row=rr, column=cc).value
            if isinstance(v, str) and v.strip() == "按 2026 皇冠品牌标准更新":
                ws.cell(row=rr, column=cc).value = "按品牌标准更新"; nx += 1
wb.save(XL)
L("[XLS] 泛化措辞收敛:", nx)

# ⑧ 重建 Word
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v4.py"), "w", encoding="utf-8").write(src)
subprocess.run([r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe", os.path.join(D, "v17_docx_v4.py")],
               capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

# ⑨ 终检
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx")
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
L("")
L("=== 终检 ===")
L("%.1f KB | 段落 %d | 表格 %d | 空白格 %d | 节 %d" % (os.path.getsize(DOCX)/1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
for i, s in enumerate(d.sections):
    L("   S%d %s %.0fx%.0f 页码域%d" % (i, "横" if s.page_width>s.page_height else "纵", s.page_width.cm, s.page_height.cm, s.footer._element.xml.count('w:instr="PAGE"')))
L("emoji(真实):", len(re.findall(EMO, alltext)))
KEYS = ["427.4","72.55%","6,774.1","4,551.8","21,312.4","53.02","24,797.0","9,950.5","7,585.4",
        "71,947.5","7,768.4","4,750.9","100.32","2029-09-27","2029-03-27","六级","丽笙精选",
        "LXR","洲至奢选","柏悦","Sofitel","消防验收","不得投入使用","R-21","1,161.5","3,484.6",
        "2,871","2022","217","1.24 亿元","五条路径","2029 Q3","告知承诺","康莱德","文华东方"]
miss = [k for k in KEYS if k not in alltext]
L("关键值缺失:", miss if miss else "无（%d 项全中）" % len(KEYS))
for ab in ("ADR","RevPAR","CAPEX","NPV","IRR","GOP"):
    n = len(re.findall(r"\b%s\b" % ab, alltext))
    if n: L("   ⚠ 英文缩写 %s ×%d" % (ab, n))
for o in ("本报告此前","纠错","增量口径","净现值为负则","唯一全判据成立","4,538.7"):
    if o in alltext: L("   ⚠ 残留: %s" % o)
m = re.search(r"^## 目录\n", t2, re.M)
ls = t2[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录↔正文:", toc == bod, "| 目录", len(toc), "正文", len(bod))
L("章节数:", len(re.findall(r"^## 第", t2, re.M)))
L("DONE")
