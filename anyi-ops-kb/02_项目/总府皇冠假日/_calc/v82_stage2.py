# -*- coding: utf-8 -*-
"""v82：v5.0 阶段二 —— 第九章整章、第十二章整章、第一章（零）、第十章（三）、插图、空白格填实、emoji 清除"""
import io, os, sys, re, json
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
LOG = open(os.path.join(T, "v82.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
MD5 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
lines = open(MD5, encoding="utf-8").read().split("\n")
FAIL = []
def find(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix):
            return i
    return -1
def put_between(a, b, content, tag):
    global lines
    i = find(a)
    if i < 0:
        FAIL.append(tag); L("[MISS]", tag); return
    j = find(b, i + 1)
    if j < 0:
        FAIL.append(tag + " end"); L("[MISS]", tag, "end"); return
    lines[i:j] = content.rstrip("\n").split("\n") + [""]
    L("[OK]  ", tag)

CH9 = open(os.path.join(KB, "_calc", "_frag", "ch9.md"), encoding="utf-8").read()
CH12 = open(os.path.join(KB, "_calc", "_frag", "ch12.md"), encoding="utf-8").read()
CH1 = open(os.path.join(KB, "_calc", "_frag", "ch1.md"), encoding="utf-8").read()
CH10ADD = open(os.path.join(KB, "_calc", "_frag", "ch10add.md"), encoding="utf-8").read()

put_between("## 第九章 财务评价", "## 第十章", CH9, "第九章整章")
put_between("## 第十二章 结论与建议", "以上报告，请审阅。", CH12, "第十二章整章")

i = find("### （一）项目概况")
if i < 0:
    FAIL.append("第一章（零）"); L("[MISS]", "第一章（零）")
else:
    lines[i:i] = CH1.rstrip("\n").split("\n") + [""]
    L("[OK]  ", "第一章（零）")

i = find("### （三）对安逸十五五战略的体现")
if i < 0:
    FAIL.append("第十章（三）"); L("[MISS]", "第十章（三）")
else:
    j = i + 1
    while j < len(lines) and not lines[j].startswith("###"):
        j += 1
    lines[j:j] = CH10ADD.rstrip("\n").split("\n")
    L("[OK]  ", "第十章（三）补充")

# ── 插图 ──
FIGS = [
 ("### （三）市场行情", "fig01_五年曲线.png", "图 1　成都五星级酒店每间可售房收入五年走势（2021—2026）"),
 ("### （五）品牌方案比选", "fig02_品牌面积与房量.png", "图 2　品牌客房面积要求 → 总府可行房量"),
 ("### （三）市场行情", "fig03_实测房价带.png", "图 3　春熙路核心商圈五星级及奢华酒店实测房价带"),
 ("### （三）净现值为正的可行路径", "fig04_净现值路径.png", "图 4　净现值转正路径分解"),
 ("### （四）停业方案", "fig05_停业方案.png", "图 5　停业方案与净现值"),
]
for header, fn, cap in FIGS:
    i = find(header)
    if i < 0:
        FAIL.append("图 " + fn); L("[MISS]", "图", fn); continue
    j = i + 1
    while j < len(lines) and not lines[j].startswith("###") and not lines[j].startswith("## "):
        j += 1
    lines[j:j] = ["![{c}](_figs/{f})".format(c=cap, f=fn), ""]
    L("[OK]  ", "插图 " + fn)

open(MD5, "w", encoding="utf-8").write("\n".join(lines))
L("")
L("阶段二完成，未命中 {0} 处".format(len(FAIL)))
for f in FAIL:
    L("   MISS:", f)
L("DONE")
