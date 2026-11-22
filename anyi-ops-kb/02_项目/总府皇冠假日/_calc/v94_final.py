# -*- coding: utf-8 -*-
"""v94：清除 ★ 自插符号、定位并修正最后残留旧值、重建 Word、终检"""
import io, os, sys, re, json, glob, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(os.path.join(T, "v94.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
MD5 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
s = open(MD5, encoding="utf-8").read()

L("=== 定位残留 ===")
for k in ("254.7", "8.11%", "235 间", "★"):
    for m in re.finditer(re.escape(k), s):
        ln = s[:m.start()].count("\n") + 1
        L("  L%-5d %-8s | %s" % (ln, k, s[max(0, m.start()-150):m.start()+110].replace("\n", " ")))

# ① 清除 ★（自插装饰符，落在公文禁用的符号区间）
n = s.count("★")
s = s.replace("★ ", "").replace("★", "")
L("")
L("[MD] ★ 清除: %d" % n)

# ② 修正 254.7 / 8.11%（旧 B01 值）→ v87 权威值 +46.9 / 8.02%
FIX = [("| **全停业 12 月 ＋ 分区滚动开业** | **3,724.3** | **+254.7** | **8.11%** |",
        "| **全停业 12 月 ＋ 分区滚动开业** | **3,484.6** | **+46.9** | **8.02%** |"),
       ("3,724.3", "3,484.6")]
nf = 0
for a, b in FIX:
    if a in s:
        s = s.replace(a, b); nf += 1
s = s.replace("+254.7", "+46.9").replace("8.11%", "8.02%")
s = s.replace("3,724.3", "3,484.6")
L("[MD] 旧 B01 值修正: %d 处 + 全局替换" % nf)

# ③ 235 间：仅保留「由 235 间降至 209 间」的修订说明语境，其余按模型范围改写
s = s.replace("房量降至 145 至 235 间", "房量降至 145 至 209 间")
s = s.replace("在 145 至 402 间之间", "在 145 至 402 间之间")
open(MD5, "w", encoding="utf-8").write(s)

L("")
L("=== 复检 ===")
for k in ("254.7", "8.11%", "3,724.3", "★", "4,507.0", "6.10%", "6,499.1", "3,422.6", "12,610.5", "14,647.7", "4,750.9", "9.95%", "7,585.4", "9,950.5", "15.24%", "3,000 万元"):
    c = s.count(k)
    L("  %-11s %d 次 %s" % (k, c, "← 需核" if c else "OK"))
L("  235 间       %d 次（应仅存于修订说明语境）" % s.count("235 间"))
L("  2,787.2     %d 次（应仅存于修订说明语境）" % s.count("2,787.2"))

# ④ Word 重建
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
alltext = "\n".join(p.text for p in d.paragraphs) + "\n" + "\n".join(
    c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
EMO = ("[" + chr(92) + "U0001F300-" + chr(92) + "U0001FAFF" + chr(92) + "U00002600-" + chr(92) + "U000027BF"
       + chr(92) + "U00002B50" + chr(92) + "uFE0F" + chr(92) + "u200D" + chr(92) + "u2764" + chr(92) + "u2B06"
       + chr(92) + "u2B07" + chr(92) + "u2B05" + chr(92) + "u274C" + chr(92) + "u2705" + chr(92) + "u26A0"
       + chr(92) + "u26A1" + chr(92) + "u2139" + chr(92) + "u24C2" + chr(92) + "u2B55]")
L("")
L("=== Word 终检 ===")
L("  {0:.1f} KB | 段落 {1} | 表格 {2} | 空白格 {3} | 节 {4}".format(
    os.path.getsize(DOCX)/1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
for i, sec in enumerate(d.sections):
    L("   S{0} {1} {2:.0f}x{3:.0f} 页码域{4}".format(i, "横" if sec.page_width>sec.page_height else "纵",
        sec.page_width.cm, sec.page_height.cm, sec.footer._element.xml.count('w:instr="PAGE"')))
L("  emoji: {0} ｜ ★: {1} ｜ ☆: {2}".format(len(re.findall(EMO, alltext)), alltext.count("★"), alltext.count("☆")))
for ab in ("ADR", "RevPAR", "CAPEX", "NPV", "IRR", "GOP"):
    n = len(re.findall(r"\b" + ab + r"\b", alltext))
    if n: L("   ⚠ 英文缩写 {0} ×{1}".format(ab, n))
m = re.search(r"^## 目录\n", s, re.M)
ls = s[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("  目录↔正文: {0}（目录 {1} / 正文 {2}）".format(toc == bod, len(toc), len(bod)))
L("  章节 {0} ｜ 图 {1} ｜ 风险 {2} ｜ 字数 {3:,}".format(
    len(re.findall(r"^## 第", s, re.M)), len(re.findall(r"!\[", s, re.M)),
    len(re.findall(r"\| R-\d+ \|", s)), len(s)))
KEYS = ["15,064.3", "+46.9", "8.02%", "+61.0", "209 间", "+23,213.2", "−3,630.4",
        "+6,291.3", "11.41%", "6,774.1", "4,551.8", "+10,724.7", "12.52%", "45 平方米",
        "65 平方米", "50 平方米", "282 间", "230 间", "2029-03-27", "锦发改发〔2025〕30 号",
        "可分离性", "决策预研", "僵局", "顺序倒置", "R-22", "R-23"]
miss = [k for k in KEYS if k not in alltext]
L("  关键值缺失: {0}".format(miss if miss else "无（%d 项全中）" % len(KEYS)))
L("")
L("=== 交付 ===")
for p in sorted(glob.glob(os.path.join(REP, "总府皇冠改造_可行性研究报告*"))) + \
         sorted(glob.glob(os.path.join(REP, "总府皇冠改造_国际联号*"))) + \
         sorted(glob.glob(os.path.join(TGT, "测算与中间产物", "总府皇冠改造_可行性研究报告*"))):
    L("  {0:7.1f} KB  {1}".format(os.path.getsize(p)/1024, os.path.basename(p)))
L("  桌面残留: {0}".format(len(glob.glob(r"C:\Users\ericz\Desktop\*总府*"))))
L("DONE")
