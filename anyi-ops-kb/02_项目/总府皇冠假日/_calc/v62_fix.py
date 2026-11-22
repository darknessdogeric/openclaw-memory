# -*- coding: utf-8 -*-
"""v62：修复 v17 目录状态机吞掉第一章标题与首表的问题，并重建 v4.0 Word
   根因：in_toc=True 后遇到 h2/h3（章节标题）时未退出 TOC 状态，L285 `if in_toc: continue` 将其连同
        随后的第一张表一并跳过 —— Word 实际从「（二）编制依据」开始，缺失「第一章 总论」「（一）项目概况」
        及《项目概况》整张表（含 415 间、1,574 ㎡、5,000 ㎡、21,313.6 万元）。"""
import io, os, sys, re, json, glob, subprocess, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(os.path.join(T, "v62.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
D = os.path.join(KB, "_calc")

# ── ① 修补 v17 源码 ──
V17 = os.path.join(D, "v17_docx.py")
src = open(V17, encoding="utf-8").read()
OLD = """        if in_toc and kind == "p" and not re.match(r"^\\d+\\.\\s", val):
            in_toc = False"""
NEW = """        # 修正：目录状态须在遇到章节标题(h1/h2/h3/h4)或非目录条目段落时退出，
        # 否则 h2 章节标题与其后第一张表会被 L285 的 `if in_toc: continue` 一并吞掉
        if in_toc and kind in ("p", "h1", "h2", "h3", "h4") \\
                and not (kind == "p" and re.match(r"^\\d+\\.\\s", val)):
            in_toc = False"""
if OLD in src:
    src = src.replace(OLD, NEW)
    open(V17, "w", encoding="utf-8").write(src)
    L("[PATCH] v17 目录状态机已修复（源码级）")
elif NEW in src:
    L("[PATCH] v17 已含修复")
else:
    L("[FAIL] 未找到待修锚点"); sys.exit(2)

# ── ② 生成 v4 版转换脚本并重建 Word ──
s4 = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md",
                  "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.md")
s4 = s4.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx",
                "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v4.py"), "w", encoding="utf-8").write(s4)
subprocess.run([r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe",
                os.path.join(D, "v17_docx_v4.py")],
               capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

# ── ③ 终检 ──
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx")
MD4 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.md")
t = open(MD4, encoding="utf-8").read()
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
L("emoji(真实):", len(re.findall(EMO, alltext)))
L("含「第一章 总论」:", "第一章 总论" in alltext)
L("含「（一）项目概况」:", "（一）项目概况" in alltext)
L("含《项目概况》表首格「项目名称」:", "项目名称" in alltext)
L("此前丢失的 4 个数值: 415=%s 1574=%s 5000=%s 21313.6=%s"
  % ("415" in alltext, "1,574" in alltext, "5,000" in alltext, "21,313.6" in alltext))
KEYS = ["427.4","72.55%","6,774.1","4,551.8","21,312.4","53.02","24,797.0","9,950.5","7,585.4",
        "71,947.5","7,768.4","4,750.9","100.32","2029-09-27","2029-03-27","六级","丽笙精选",
        "LXR","洲至奢选","柏悦","Sofitel","消防验收","不得投入使用","R-21","1,161.5","3,484.6",
        "2,871","2022","217","1.24 亿元","五条路径","2029 Q3","告知承诺","康莱德","文华东方","3/5"]
miss = [k for k in KEYS if k not in alltext]
L("关键值缺失:", miss if miss else "无（%d 项全中）" % len(KEYS))
for ab in ("ADR","RevPAR","CAPEX","NPV","IRR","GOP"):
    n = len(re.findall(r"\b%s\b" % alltext))
    if n: L("   ⚠ 英文缩写 %s ×%d" % (ab, n))
for o in ("本报告此前","纠错","增量口径","唯一全判据成立"):
    if o in alltext: L("   ⚠ 残留: %s" % o)
# 章节完整性
chs = [p.strip() for p in paras if re.match(r"^第[一二三四五六七八九十]+章", p.strip())]
L("Word 内章节标题 %d 个:" % len(chs))
for c in chs: L("   %s" % c)
m = re.search(r"^## 目录\n", t, re.M)
ls = t[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录↔正文:", toc == bod, "| 目录", len(toc), "正文", len(bod))
L("DONE")
