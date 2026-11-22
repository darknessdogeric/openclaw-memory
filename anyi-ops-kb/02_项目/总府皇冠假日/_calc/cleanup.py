# -*- coding: utf-8 -*-
"""版本清理：只留上会件；旧测算移入历史版本子目录；同步 memory/README"""
import io, os, sys, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "clean.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")

# 1) 删被取代的报告
DEL = ["总府皇冠改造_整体方案报告_集团汇报件_v1.0_2026-11-13.docx",
       "总府皇冠改造_可行性研究报告_公文版_v1.0_2026-11-09.docx",
       "总府皇冠改造_立项报告_v1.0_2026-11-08.docx"]
for n in DEL:
    p = os.path.join(REP, n)
    if os.path.exists(p):
        os.remove(p); L("DEL", n.encode("unicode_escape").decode("ascii"))
for n in DEL:
    p = os.path.join(KB, n)
    if os.path.exists(p):
        os.remove(p); L("DEL-kb", n.encode("unicode_escape").decode("ascii"))

# 2) 旧测算移入历史版本目录
HIST = os.path.join(CAL, "_历史版本_2026-11-03至11-08")
os.makedirs(HIST, exist_ok=True)
for p in sorted(glob.glob(os.path.join(CAL, "*"))):
    if os.path.isdir(p):
        continue
    b = os.path.basename(p)
    if b.startswith("总府皇冠改造_立项经济测算") or b.startswith("总府皇冠改造_投资测算表") or "国际联号口径" in b:
        shutil.move(p, os.path.join(HIST, b))
        L("HIST", b.encode("unicode_escape").decode("ascii"))

# 3) 同步 memory / README
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-13.md"
open(MEM, "a", encoding="utf-8").write("""

---

## 10:15 最终版：**按《立项报告》范式**成稿（十一章 + 目录 + 公文要素）

**交付**：改造报告交付\\总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx（88.0 KB，正文 84.9 KB）

### 范式（依 Eric 指正：以《立项报告》为骨架）
公文要素：密级 + 份号 → 发文字号 → 签发人 → 标题《关于总府皇冠假日酒店改造升级项目的可行性研究报告》→ 主送「安逸酒店集团：」→ 各有关单位：→ **目录** → 正文十一章 → 附件说明 → 抄送 → 发文机关署名与成文日期 → 版记

十一章：①立项依据与项目概述 ②市场调研 ③改造必要性 ④改造可行性 ⑤改造方案比选与品牌选择 ⑥投资构成与隐性成本专项 ⑦资金来源与合作模式方向 ⑧SWOT 分析 ⑨经济测算结果 ⑩风险分析与应对 ⑪结论与建议

### 合并做法
以《可行性研究报告（公文版）》为骨架（保留其目录/十一章/公文要素/附件/抄送/落款），逐章替换为最新内容：
- 第四章（二）停业方案可行性 ← 整体方案报告的停业方案论证 3 小节（不停业不可能／半停业四条件／两方案量级对比）
- 第五章 ← 筛选框架 + 候选逐项 + 品牌选择建议 + **换牌品牌候选（成都落地状态）** + 四方向优劣 + 方向选择结论
- 第六章 ← 四个方向总投资与费用结构（新 CAPEX）
- 第九章 ← HMA 维度经济测算 6 小节（四方向表／10 年门槛复核／敏感性／与规划目标交叉验证）
- 第十章 ← 风险清单 + 24 项风险登记册
- 第十一章 ← 结论与建议

### 版本清理（避免上会时多版本并存）
- 删除：整体方案报告_集团汇报件（63.3 KB，六章版）／可行性研究报告_公文版（94.7 KB，旧数字）／立项报告_2026-11-08（75.4 KB）
- 测算与中间产物：4 份旧「立项经济测算」EXCEL（ADR 460 旧口径）+ 投资测算表 + 国际联号口径测算方法 移入 **子目录「_历史版本_2026-11-03至11-08」**
- ⭐ 保留：立项报告_集团汇报件（88.0 KB）＋ 立项方案_细项概算表（45.7 KB，12 Sheet）＋ 吸收报告 + 综合改造报告 11 部分 + 合同条款分析 + 咨询函
<!-- project: github.com/darknessdogeric/openclaw-memory -->

---
""")
RM = os.path.join(KB, "00_项目总览_README.md")
open(RM, "a", encoding="utf-8").write("""

| **立项报告（集团汇报件·最终版）** | v1.0 | docx 88.0 KB | ⭐⭐⭐⭐ **按《立项报告》范式**：红头/文号/签发人/主送「安逸酒店集团：」/**目录**/十一章/附件说明/抄送/落款/版记；内容已并入最新测算（四方向、10 年门槛复核、停业三态、一城一店核查） | ⭐ **上会件，全套只此一份** |

> ⭐ **版本说明**：改造报告交付目录现只保留上会用件；被取代的旧版报告已删除，旧测算表移入「测算与中间产物\\_历史版本_2026-11-03至11-08」。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
L("memory + README synced")

L("\n--- 最终交付清单 ---")
for f in sorted(glob.glob(os.path.join(REP, "*"))):
    L("  [报告] %-70s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
for f in sorted(glob.glob(os.path.join(CAL, "*"))):
    if os.path.isdir(f):
        L("  [测算] %-70s  <DIR>" % os.path.basename(f).encode("unicode_escape").decode("ascii"))
    else:
        L("  [测算] %-70s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
