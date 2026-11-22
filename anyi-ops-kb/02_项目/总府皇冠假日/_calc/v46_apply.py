# -*- coding: utf-8 -*-
"""v46：战略维度入稿
   ① 第二章 新增（八）文创化改造路径的市场参照（原（八）市场预测结论 →（九））
   ② 第三章 新增（六）战略与文化维度的必要性（原（六）→（七））
   ③ 第五章 新增（七）在地文化植入方案（原（七）（八）顺延）
   ④ 第九章 新增（九）文创化溢价情景测算
   ⑤ 第十章 重写为「社会效益、政治意义与战略价值」
   ⑥ 第十二章 增结论 11-15、建议 8-12、请示 6-8
   ⑦ 目录同步"""
import os, sys, re
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
LOG = open(os.path.join(T, "v46.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, os.path.join(KB, "_calc"))
from v44_text import CH2_9, CH3_6, CH5_7, CH9_9
from v45_text import CH10, CH12_CONCL_ADD, CH12_SUGG_ADD, CH12_ASK_ADD

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()
FAIL = []

def must(cond, msg):
    if not cond:
        FAIL.append(msg); L("[MISS]", msg)
    else:
        L("[OK]  ", msg)

# ── 预检：第十章现有结论条数与锚点 ──
L("=== 预检 ===")
n_concl = len(re.findall(r"^\*\*第[一二三四五六七八九十]+，", t, re.M))
L("全文 **第X，** 计数:", n_concl)
must("### （八）市场预测结论" in t, "第二章 （八）市场预测结论")
must("### （六）必要性结论与前置条件" in t, "第三章 （六）必要性结论")
must("### （七）实施进度原则" in t, "第五章 （七）实施进度原则")
must("### （八）方向选择结论" in t, "第五章 （八）方向选择结论")
must("## 第十章 社会效益分析" in t, "第十章 标题")
must("## 第十一章 风险分析" in t, "第十一章 锚点")
must("**第十，本项目是 20 至 30 年长周期资产" in t, "结论第十")
must("**建议七：十五五规划作为决策参照而非硬性约束。**" in t, "建议七")
must("**五、请报请明确四项参数口径。**" in t, "请示五")
must("10. 第十章 社会效益分析" in t, "目录第十章行")

# ══ ① 第二章 ══
t = t.replace("### （八）市场预测结论", "### （九）市场预测结论")
t = t.replace(CH2_9.replace("### （九）文创化改造路径的市场参照", "### （八）文创化改造路径的市场参照").rstrip() + "\n\n",
              "", 1)
# 在（九）市场预测结论前插入
m = re.search(r"^### （九）市场预测结论$", t, re.M)
must(m is not None, "第二章插入点")
if m:
    t = t[:m.start()] + CH2_9.replace("### （九）文创化改造路径的市场参照", "### （八）文创化改造路径的市场参照").rstrip() + "\n\n" + t[m.start():]
    L("[MD] 第二章（八）已插入，市场预测结论顺延为（九）")

# ══ ② 第三章 ══
t = t.replace("### （六）必要性结论与前置条件", "### （七）必要性结论与前置条件")
m = re.search(r"^### （七）必要性结论与前置条件$", t, re.M)
must(m is not None, "第三章插入点")
if m:
    t = t[:m.start()] + CH3_6.rstrip() + "\n\n" + t[m.start():]
    L("[MD] 第三章（六）已插入，原（六）顺延为（七）")

# ══ ③ 第五章 ══
t = t.replace("### （八）方向选择结论", "### （九）方向选择结论")
t = t.replace("### （七）实施进度原则", "### （八）实施进度原则")
m = re.search(r"^### （八）实施进度原则$", t, re.M)
must(m is not None, "第五章插入点")
if m:
    t = t[:m.start()] + CH5_7.rstrip() + "\n\n" + t[m.start():]
    L("[MD] 第五章（七）已插入，实施进度原则顺延为（八）、方向选择结论为（九）")

# ══ ④ 第九章（九）══
m = re.search(r"^## 第十章 社会效益分析$", t, re.M)
must(m is not None, "第九章插入点")
if m:
    t = t[:m.start()] + CH9_9.rstrip() + "\n\n" + t[m.start():]
    L("[MD] 第九章（九）已插入")

# ══ ⑤ 第十章重写 ══
m = re.search(r"^## 第十章 社会效益分析.*?(?=^## 第十一章 风险分析)", t, re.M | re.S)
must(m is not None, "第十章整章范围")
if m:
    t = t[:m.start()] + CH10.rstrip() + "\n\n---\n\n" + t[m.end():]
    L("[MD] 第十章已重写为「社会效益、政治意义与战略价值」")

# ══ ⑥ 第十二章 ══
anchor = "**第十，本项目是 20 至 30 年长周期资产"
i = t.find(anchor)
must(i >= 0, "结论插入点")
if i >= 0:
    j = t.find("\n\n", i)
    t = t[:j + 2] + CH12_CONCL_ADD.rstrip() + "\n\n" + t[j + 2:]
    L("[MD] 结论 11-15 已插入")
anchor = "**建议七：十五五规划作为决策参照而非硬性约束。**"
i = t.find(anchor)
must(i >= 0, "建议插入点")
if i >= 0:
    j = t.find("\n\n", i)
    t = t[:j + 2] + CH12_SUGG_ADD.rstrip() + "\n\n" + t[j + 2:]
    L("[MD] 建议 8-12 已插入")
anchor = "**五、请报请明确四项参数口径。**"
i = t.find(anchor)
must(i >= 0, "请示插入点")
if i >= 0:
    j = t.find("\n\n", i)
    t = t[:j + 2] + CH12_ASK_ADD.rstrip() + "\n\n" + t[j + 2:]
    L("[MD] 请示 6-8 已插入")

# ══ ⑦ 目录 ══
t = t.replace("10. 第十章 社会效益分析", "10. 第十章 社会效益、政治意义与战略价值")
L("[MD] 目录已同步")

if FAIL:
    L("=== 存在未命中锚点 %d 处，未写盘 ===" % len(FAIL))
    for f in FAIL: L("   ", f)
    sys.exit(2)

open(MD, "w", encoding="utf-8").write(t)
L("MD bytes:", len(t.encode("utf-8")))
h2 = re.findall(r"^## (.+)$", t, re.M)
L("章节数:", len(h2))
for x in h2: L("   ", x)
for c in ("第二章", "第三章", "第五章", "第九章", "第十章"):
    m = re.search(r"^## %s.*?(?=^## )" % c, t, re.M | re.S)
    if m:
        subs = re.findall(r"^### (.+)$", m.group(0), re.M)
        L("%s 小节: %s" % (c, subs))
L("DONE")
