# -*- coding: utf-8 -*-
"""v27 修复：① 恢复被误删的（六）可保留项利用方案、（七）实施进度原则
        ② 修正被误填的 6 处单元格
        ③ 公文版式 Word 重建；终检"""
import io, os, sys, re, json, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(os.path.join(T, "v27.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, os.path.join(KB, "_calc"))

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ── 从 v19_report.py 原文取回被误删的两小节 ──
src = open(os.path.join(KB, "_calc", "v19_report.py"), encoding="utf-8").read()
i6 = src.find("### （六）可保留项利用方案")
i7 = src.find("### （七）实施进度原则")
i8 = src.find("## 第六章 投资估算与资金筹措")
assert i6 > 0 and i7 > i6 and i8 > i7, "v19 原文定位失败"
# 原文里是带 python 三引号的，做简单反转义
seg = src[i6:i8]
seg = seg.replace("\\u201c", "\u201c").replace("\\u201d", "\u201d").replace("\\u2014", "—")
seg = seg.replace("\\n", "\n")
RECOVER = seg.rstrip() + "\n\n"
L("已取回原文长度:", len(RECOVER))
L("原文小节标题:", [l for l in RECOVER.split("\n") if l.startswith("### ")])

# ── 定位当前第五章，把「（六）方向选择结论」前的「（五）」段后重新插入 ──
m5 = re.search(r"^## 第五章 .*?(?=^## 第六章 )", t, re.M | re.S)
assert m5, "未定位第五章"
ch5 = t[m5.start():m5.end()]
# 当前第五章尾部结构：...（五）品牌方案比选 ... 然后（一段被我插入的方向选择结论）
mi = ch5.find("### （六）方向选择结论")
assert mi > 0, "未定位插入的方向选择结论"
ch5_new = ch5[:mi] + RECOVER + ch5[mi:]
t = t[:m5.start()] + ch5_new + t[m5.end():]
L("[MD] 已恢复（六）（七）两小节，章内小节:",
  [l for l in ch5_new.split("\n") if l.startswith("### ")])

# ── 修正被误填的单元格：瑞吉行房量 → 未公开披露；其余"不适用"逐一检查 ──
lines = t.split("\n")
fixed = []
for i, l in enumerate(lines):
    if l.startswith("|") and "成都瑞吉酒店" in l:
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        for j, c in enumerate(cells):
            if c == "不适用":
                cells[j] = "未公开披露"
                fixed.append((i + 1, j))
        lines[i] = "| " + " | ".join(cells) + " |"
t = "\n".join(lines)
L("[MD] 瑞吉行修正:", fixed)

# ── 检查所有"不适用"出现位置 ──
for i, l in enumerate(t.split("\n"), 1):
    if l.startswith("|") and "不适用" in l:
        L("   残留不适用 L%d | %s" % (i, l[:150]))

open(MD, "w", encoding="utf-8").write(t)
L("MD bytes:", len(t.encode("utf-8")))

# ── 公文版式 Word（复用 v17）──
D = os.path.join(KB, "_calc")
s2 = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
s2 = s2.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
s2 = s2.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v3.py"), "w", encoding="utf-8").write(s2)
os.system('"%s" "%s" > "%s" 2>&1' % (
    r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe",
    os.path.join(D, "v17_docx_v3.py"), os.path.join(T, "v17v3.out")))
lg = os.path.join(T, "v17.log")
if os.path.exists(lg):
    for l in open(lg, encoding="utf-8", errors="replace").read().split("\n"):
        if l.strip():
            L(l.rstrip())
