# -*- coding: utf-8 -*-
"""v40：终稿清理 —— ① 表格「—」占位清零（保 0 空白格）② 旧判据短语改写
        ③ 请示事项补反事实基准 ④ 重出公文 Word + 终检 ⑤ memory/README 同步"""
import io, os, sys, re, json, glob, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v40.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ① 表格内「—」/「-」占位 → 不适用（逐表逐格）
lines = t.split("\n"); hdr = []; fixed = 0; in_tbl = False
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
                    rep = "不适用" if ("参数" in col or "说明" in col or col == "") else "不适用"
                    new.append(rep); fixed += 1
                else:
                    new.append(c)
            lines[i] = "| " + " | ".join(new) + " |"
        continue
    hdr = []
t = "\n".join(lines)
L("[MD] 表格占位符清理:", fixed)

# ② 旧判据短语改写（改为描述修正关系，避免读作现行结论）
t = t.replace("S7B 由唯一全判据成立方案修正为上限情景的战略期权",
              "S7B 由本报告前一稿的乐观结论修正为上限情景的战略期权")
t = t.replace("**其四，外部奢牌路径的实质门槛不是价格带，而是品牌方的出资分担比例。**",
              "**其四，外部奢牌路径的实质门槛不是价格带，而是品牌方的出资分担比例。**")
L("[MD] 旧判据短语改写:", "唯一全判据成立" not in t)

# ③ 请示事项：补入反事实基准，使请示口径与增量口径一致
old = "**二、请认可改造必要性与五星档基准方案。** 请认可"
if old in t:
    t = t.replace(old, """**二、请认可改造必要性与五星档基准方案，并认可以增量口径作为本项目的经济性评价主口径。** 需先说明：反事实不是零——不改造不是零成本基准，总府现状年经营现金流为 −1,924.0 万元，20 年 8% 折现净现值 −20,401.3 万元，且消防自动报警主机已于 2026 年 7 月全面瘫痪，继续原状经营在合规上本身不成立。请认可""")
    L("[MD] 请示二 已补反事实基准")

# ④ 重出公文 Word
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v3.py"), "w", encoding="utf-8").write(src)
PY = r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe"
subprocess.run([PY, os.path.join(D, "v17_docx_v3.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

open(MD, "w", encoding="utf-8").write(t)
L("MD bytes:", len(t.encode("utf-8")))

# ⑤ 终检
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
L("=== 终检 ===")
L("%.1f KB | 段落 %d | 表格 %d | 空白格 %d | 节 %d" % (os.path.getsize(DOCX) / 1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
for si, s in enumerate(d.sections):
    L("   S%d %s %.0fx%.0f 页码域 %d" % (si, "横" if s.page_width > s.page_height else "纵",
        s.page_width.cm, s.page_height.cm, s.footer._element.xml.count('w:instr="PAGE"')))
L("emoji:", len(re.findall("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]", alltext)))
KEYS = ["10,720", "10,192", "254 间", "208 间", "2,915", "31,727.6", "20,401.3", "14,398.4",
        "15.61%", "15.32%", "21.28%", "28.28%", "76.7", "68.4", "上限情景", "投入分担", "R-21", "R-22"]
miss = [k for k in KEYS if k not in alltext]
L("关键值缺失:", miss if miss else "无（%d 项全中）" % len(KEYS))
for o in ("唯一全判据成立", "唯一在全部判据上成立的方案是 S7B", "唯一同时满足"):
    if o in alltext: L("   ⚠ 旧判据残留: %s" % o)
for ab in ("ADR", "RevPAR", "CAPEX", "NPV", "IRR", "GOP"):
    n = len(re.findall(r"\b%s\b" % ab, alltext))
    if n: L("   ⚠ 英文缩写 %s ×%d" % (ab, n))
m = re.search(r"^## 目录\n", t, re.M)
ls = t[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录↔正文:", toc == bod, "| 目录", len(toc), "正文", len(bod))
L("交付:", [os.path.basename(x) for x in glob.glob(os.path.join(REP, "总府皇冠改造_可行性研究报告*"))],
  [os.path.basename(x) for x in glob.glob(os.path.join(CAL, "总府皇冠改造_可行性研究报告*"))])
L("桌面残留:", len(glob.glob(r"C:\Users\ericz\Desktop\*总府*")))
L("DONE")
