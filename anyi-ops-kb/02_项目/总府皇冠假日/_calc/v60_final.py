# -*- coding: utf-8 -*-
"""v60：v4.0 收官 —— ① 竞争烈度标度复原 ② 消防子项内容列具体化 ③ 定位并修复缺失的第 40 张表
        ④ 重建 Word + Excel ⑤ 终检"""
import io, os, sys, re, json, glob, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v60.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, os.path.join(KB, "_calc"))
MD4 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.md")
t = open(MD4, encoding="utf-8").read()
lines = t.split("\n")

# ① 竞争烈度行复原为 5 分制
n = 0
for i, l in enumerate(lines):
    if "竞争烈度" in l:
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if cells[0] == "竞争烈度":
            if "丽晶 2029" in l:
                cells[1], cells[2] = "3/5", "5/5"
            elif "结构性过剩" in l:
                cells[1], cells[2] = "4/5", "5/5"
            elif "连锁加速进入" in l:
                cells[1], cells[2] = "3/5", "4/5"
            else:
                cells[1], cells[2] = "3/5", "5/5"
            lines[i] = "| " + " | ".join(cells) + " |"; n += 1
L("[MD] 竞争烈度标度复原:", n)

# ② 消防子项内容列具体化（按子项名逐条）
FIRE = {
 "防火门监控系统及门禁": "防火门状态监测与门禁联动控制",
 "电气火灾监控系统": "剩余电流与测温式电气火灾监控",
 "消防报建": "消防设计审查、验收报建与资料归档",
 "消防水炮": "增设室内消防水炮灭火系统",
 "防火卷帘系统": "防火分区卷帘与联动降落",
 "监控室机房改造": "消防控制中心机房设备与装修",
}
n = 0
for i, l in enumerate(lines):
    if l.startswith("|"):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if cells and cells[0] in FIRE and "不适用" in cells:
            cells[-1] = FIRE[cells[0]]; lines[i] = "| " + " | ".join(cells) + " |"; n += 1
L("[MD] 消防子项内容列具体化:", n)

# ③ OAKS 房量
for i, l in enumerate(lines):
    if "成都 OAKS（蜀都）" in l:
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        cells[3] = "未公开披露"
        lines[i] = "| " + " | ".join(cells) + " |"
        L("[MD] OAKS 房量已填实")
        break
t = "\n".join(lines)

# ④ 定位相邻表块（无空行分隔会被并表）
blocks = []; i = 0
while i < len(lines):
    if lines[i].startswith("|"):
        j = i
        while j < len(lines) and lines[j].startswith("|"): j += 1
        blocks.append((i + 1, j, lines[i].strip().strip("|").split("|")[0].strip(), len(lines[i:j])))
        i = j
    else:
        i += 1
L("[MD] 表格块: %d" % len(blocks))
for k in range(len(blocks) - 1):
    gap = blocks[k + 1][0] - blocks[k][1]
    if gap <= 1:
        L("   ⚠ 块%d(L%d-%d 首格%s) 与 块%d(L%d) 相邻（间隔%d行）→ 合并为一张表"
          % (k + 1, blocks[k][0], blocks[k][1], blocks[k][2][:18], k + 2, blocks[k + 1][0], gap))
        # 插入空行分隔
        lines.insert(blocks[k][1], "")
        blocks = []; i = 0
        while i < len(lines):
            if lines[i].startswith("|"):
                j = i
                while j < len(lines) and lines[j].startswith("|"): j += 1
                blocks.append((i + 1, j, lines[i].strip().strip("|").split("|")[0].strip(), len(lines[i:j])))
                i = j
            else:
                i += 1
        L("   → 已插入空行分隔，表格块数 %d" % len(blocks))
        break
t = "\n".join(lines)
open(MD4, "w", encoding="utf-8").write(t)

# ⑤ Excel 同步：消防内容列 + 竞争烈度
from openpyxl import load_workbook
XL = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v4.0_2026-11-14.xlsx")
wb = load_workbook(XL)
nx = 0
for ws in wb.worksheets:
    for rr in range(1, ws.max_row + 1):
        for cc in range(1, ws.max_column + 1):
            v = ws.cell(row=rr, column=cc).value
            if isinstance(v, str) and v.strip() == "不适用":
                a = ws.cell(row=rr, column=1).value
                if isinstance(a, str) and a in FIRE:
                    ws.cell(row=rr, column=cc).value = FIRE[a]; nx += 1
wb.save(XL)
L("[XLS] 消防内容列同步:", nx)

# ⑥ 重建 Word
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v4.py"), "w", encoding="utf-8").write(src)
subprocess.run([r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe", os.path.join(D, "v17_docx_v4.py")],
               capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

# ⑦ 终检
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx")
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
EMO = ("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D"
       "\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]")
L("")
L("=== 终检 ===")
L("%.1f KB | 段落 %d | 表格 %d | 空白格 %d | 节 %d" % (os.path.getsize(DOCX)/1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
for i, s in enumerate(d.sections):
    L("   S%d %s %.0fx%.0f 页码域%d" % (i, "横" if s.page_width>s.page_height else "纵", s.page_width.cm, s.page_height.cm, s.footer._element.xml.count('w:instr="PAGE"')))
L("emoji(真实):", len(re.findall(EMO, alltext)), "| ☆:", alltext.count("☆"), "| ★:", alltext.count("★"))
KEYS = ["427.4","72.55%","6,774.1","4,551.8","21,312.4","53.02","24,797.0","9,950.5","7,585.4",
        "71,947.5","7,768.4","4,750.9","100.32","2029-09-27","2029-03-27","六级","丽笙精选",
        "LXR","洲至奢选","柏悦","Sofitel","消防验收","不得投入使用","R-21","1,161.5","3,484.6",
        "2,871","2022","217","1.24 亿元","五条路径","2029 Q3","告知承诺","康莱德","文华东方","3/5"]
miss = [k for k in KEYS if k not in alltext]
L("关键值缺失:", miss if miss else "无（%d 项全中）" % len(KEYS))
for ab in ("ADR","RevPAR","CAPEX","NPV","IRR","GOP"):
    n = len(re.findall(r"\b%s\b" % ab, alltext))
    if n: L("   ⚠ 英文缩写 %s ×%d" % (ab, n))
for o in ("本报告此前","纠错","增量口径","净现值为负则","唯一全判据成立"):
    if o in alltext: L("   ⚠ 残留: %s" % o)
m = re.search(r"^## 目录\n", t, re.M)
ls = t[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录↔正文:", toc == bod, "| 目录", len(toc), "正文", len(bod))
L("章节数:", len(re.findall(r"^## 第", t, re.M)), "| MD 表块:", len(blocks))
L("交付:", [os.path.basename(x) for x in glob.glob(os.path.join(REP, "总府皇冠改造_可行性研究报告*"))],
  [os.path.basename(x) for x in glob.glob(os.path.join(CAL, "总府皇冠改造_可行性研究报告*"))])
L("桌面残留:", len(glob.glob(r"C:\Users\ericz\Desktop\*总府*")))
L("DONE")
