# -*- coding: utf-8 -*-
"""终检：结构 / 空白 / 术语 / 关键数字 / 旧版清理"""
import io, os, sys, re, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "verify.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return str(s).encode("unicode_escape").decode("ascii")

DOCX = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.docx")
MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.md")
from docx import Document
d = Document(DOCX)
L("=== ① 表格空白 ===")
n = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "—", "-", "／", "/"):
                n += 1
                L("  BLANK 表%d 行%d 列%d : %s" % (ti, ri, ci, " || ".join(esc(c.text.strip()[:26]) for c in row.cells)))
L("  表格 %d 个，空白格 %d" % (len(d.tables), n))

t = open(MD, encoding="utf-8").read()
L("\n=== ② 章节结构 ===")
for l in t.split("\n"):
    if re.match(r"^#{1,2} ", l):
        L("  " + esc(l[:88]))
L("  H3=%d  H4=%d" % (len([l for l in t.split("\n") if l.startswith("### ")]),
                      len([l for l in t.split("\n") if l.startswith("#### ")])))
L("\n=== ③ 残留英文缩写 ===")
for k in ("IRR","NPV","CAPEX","ADR","OCC","RevPAR","HMA","FF&E","PIP","key money",
          "MGM Collection","Kimpton","Fairmont","Autograph","Niccolo","The Temple House","Upper House"):
    if k in t: L("  [残留]", k, t.count(k))
L("  Agoda 出现:", t.count("Agoda"))
L("\n=== ④ 关键数字在位 ===")
for k in ("14,401","27,919","32,061","5.37%","3.53%","35.82","12,132","5,461","1,389","1,630",
          "67,430","25.35","35 ㎡","168 间","178 间","390 间","142 间","238 间","289 间",
          "4,019","4,142","12.7%","12.5%","4603"):
    L("  %-12s %s" % (k, "在" if k in t else "缺"))
L("\n=== ⑤ 旧数字（应为0或仅对比引用）===")
for k in ("5,495","10,520","10,686","15,420","15.99","24.73","6,857","12.0 个百分点","10.1 年"):
    L("  %-12s %d" % (k, t.count(k)))
L("\n=== ⑥ emoji / 问号占位 ===")
EMO = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
L("  emoji:", len(re.findall(EMO, t)))
L("  ?? 占位:", len(re.findall(r"\?\?", t)))
L("  未替换标记 __:", len(re.findall(r"_{3,}", t)))
bad = [l for l in t.split("\n") if l.startswith("#") and ("|" in l or "**" in l or len(l) > 95)]
L("  标题异常:", len(bad))
for b in bad[:5]: L("    !", esc(b[:100]))

# 旧版清理
L("\n=== ⑦ 旧版清理 ===")
HIST = os.path.join(CAL, "_历史版本_2026-11-03至11-08")
os.makedirs(HIST, exist_ok=True)
old_x = os.path.join(CAL, "总府皇冠改造_立项方案_细项概算表_v1.0_2026-11-13.xlsx")
if os.path.exists(old_x):
    shutil.move(old_x, os.path.join(HIST, os.path.basename(old_x))); L("  移入历史: 细项概算表 v1.0")
for n in ("总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx",):
    p = os.path.join(REP, n)
    if os.path.exists(p):
        try:
            os.remove(p); L("  删除:", n)
        except Exception as e:
            L("  [被占用，Word 正在打开，请关闭后删]", n)
lk = glob.glob(os.path.join(REP, "~$*"))
for f in lk: L("  [Word 锁文件，需手动关闭 Word 后删除]", os.path.basename(f))
L("\n=== ⑧ 最终交付 ===")
for f in sorted(glob.glob(os.path.join(REP, "*.docx"))):
    if os.path.basename(f).startswith("~$"): continue
    L("  [报告] %-70s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
for f in sorted(glob.glob(os.path.join(CAL, "*.xlsx"))):
    L("  [测算] %-70s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
L("DONE")
