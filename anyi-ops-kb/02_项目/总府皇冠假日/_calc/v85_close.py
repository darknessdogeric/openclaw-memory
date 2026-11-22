# -*- coding: utf-8 -*-
"""v85：仅修风险表列数错位并重建 Word + 终检"""
import io, os, sys, re, glob, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(os.path.join(T, "v85.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
MD5 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
s = open(MD5, encoding="utf-8").read()
before = s.count("| 产业发展部 |")
s = s.replace(" | 产业发展部 |", " |")
after = s.count("| 产业发展部 |")
L("移除多余责任方列: {0} → {1}".format(before, after))
open(MD5, "w", encoding="utf-8").write(s)

# 重建 Word
D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v5.py"), "w", encoding="utf-8").write(src)
subprocess.run([r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe", os.path.join(D, "v17_docx_v5.py")],
               capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.docx")
d = Document(DOCX)
alltext = "\n".join(p.text for p in d.paragraphs) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
EMO = ("[" + chr(92) + "U0001F300-" + chr(92) + "U0001FAFF" + chr(92) + "U00002600-" + chr(92) + "U000027BF"
       + chr(92) + "U00002B50" + chr(92) + "uFE0F" + chr(92) + "u200D" + chr(92) + "u2764" + chr(92) + "u2B06"
       + chr(92) + "u2B07" + chr(92) + "u2B05" + chr(92) + "u274C" + chr(92) + "u2705" + chr(92) + "u26A0"
       + chr(92) + "u26A1" + chr(92) + "u2139" + chr(92) + "u24C2" + chr(92) + "u2B55]")
L("")
L("=== 终检 ===")
L("{0:.1f} KB | 段落 {1} | 表格 {2} | 空白格 {3} | 节 {4}".format(os.path.getsize(DOCX)/1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
for i, sec in enumerate(d.sections):
    L("   S{0} {1} {2:.0f}x{3:.0f} 页码域{4}".format(i, "横" if sec.page_width>sec.page_height else "纵", sec.page_width.cm, sec.page_height.cm, sec.footer._element.xml.count('w:instr="PAGE"')))
L("emoji:", len(re.findall(EMO, alltext)))
KEYS = ["427.4","72.55%","6,774.1","4,551.8","15,064.3","+6,499.1","11.55%","8.11%","10,192","31,412.82",
 "11,060.0","14.92","1,147","21,448.5","282 间","230 间","65 ㎡","50 ㎡","文华东方","丽晶","康莱德","柏悦",
 "Sofitel","六善","洲至奢选","LXR","2029-03-27","建设工程消防设计审查验收管理暂行规定","58 号","锦发改发〔2025〕30 号",
 "2026-12-31","可分离性","决策预研","R-22","R-23","策展溢价指数","2,915","10,720"]
miss = [k for k in KEYS if k not in alltext]
L("关键值缺失:", miss if miss else "无（{0} 项全中）".format(len(KEYS)))
for ab in ("ADR","RevPAR","CAPEX","NPV","IRR","GOP"):
    n = len(re.findall(r"\b"+ab+r"\b", alltext))
    if n: L("   ⚠ 英文缩写 {0} ×{1}".format(ab, n))
md5 = open(MD5, encoding="utf-8").read()
m = re.search(r"^## 目录\n", md5, re.M)
ls = md5[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录↔正文: {0}（目录 {1} / 正文 {2}）".format(toc == bod, len(toc), len(bod)))
L("章节:", len(re.findall(r"^## 第", md5, re.M)), "| 图:", len(re.findall(r"!\[", md5)), "| 风险:", len(re.findall(r"\| R-\d+ \|", md5)))
L("交付:", [os.path.basename(x) for x in glob.glob(os.path.join(REP, "总府皇冠改造_可行性研究报告*"))])
L("DONE")
