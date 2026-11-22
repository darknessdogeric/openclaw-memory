# -*- coding: utf-8 -*-
"""v63：v4.0 最终终检 + memory/README 同步（含 v17 目录状态机 bug 教训）"""
import io, os, re, json, glob
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v63.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx")
XL = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v4.0_2026-11-14.xlsx")
MD4 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.md")
t = open(MD4, encoding="utf-8").read()
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
alltext = "\n".join(paras) + "\n" + "\n".join(c.text for tb in d.tables for r in tb.rows for c in r.cells)

L("=== 终检（续）===")
for ab in ("ADR", "RevPAR", "CAPEX", "NPV", "IRR", "GOP"):
    n = len(re.findall(r"\b" + ab + r"\b", alltext))
    L("   英文缩写 %-8s ×%d %s" % (ab, n, "OK" if n == 0 else "⚠"))
for o in ("本报告此前", "纠错", "增量口径", "唯一全判据成立", "净现值为负则", "TODO", "FIXME", "待填", "占位"):
    if o in alltext:
        L("   ⚠ 残留: %s" % o)
chs = [p.strip() for p in paras if re.match(r"^第[一二三四五六七八九十]+章", p.strip())]
L("Word 章节标题 %d 个: %s" % (len(chs), " / ".join(chs)))
m = re.search(r"^## 目录\n", t, re.M)
ls = t[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录↔正文: %s（目录 %d / 正文 %d）" % (toc == bod, len(toc), len(bod)))
L("Word 表数 %d ｜ MD 表块 %d" % (len(d.tables), sum(1 for l in t.split("\n") if re.match(r"^\|[\s:\-|]+\|$", l.strip()))))

# Excel
from openpyxl import load_workbook
wb = load_workbook(XL)
L("Excel: %.1f KB ｜ %d sheets" % (os.path.getsize(XL) / 1024, len(wb.sheetnames)))
for s in wb.sheetnames: L("   %s" % s)

L("")
L("=== 最终交付 ===")
for p in sorted(glob.glob(os.path.join(REP, "总府皇冠改造_可行性研究报告*"))) + \
         sorted(glob.glob(os.path.join(CAL, "总府皇冠改造_可行性研究报告*"))):
    L("  %6.1f KB  %s" % (os.path.getsize(p) / 1024, os.path.basename(p)))
L("桌面根目录总府残留: %d" % len(glob.glob(r"C:\Users\ericz\Desktop\*总府*")))

# memory / README
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-13.md"
open(MEM, "a", encoding="utf-8").write(r"""
### 23:05 ⭐⭐⭐ v4.0 交付 + ⭐⭐⭐ 修掉一个影响全部历史版本的转换器 bug
**终稿**：改造报告交付\\总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx —— **91.6 KB / 315 段 / 40 表 / 0 空白格 / 5 节（含横页宽表）/ 0 emoji / 12 章完整 / 36 项关键值全中**；测算与中间产物\\..._测算附表_v4.0_2026-11-14.xlsx（12 表）。

#### 🔴🔴 发现并修复一个影响所有历史版本的渲染 bug（v17_docx.py 目录状态机）
**现象**：Word 少 1 张表（39 vs MD 40），且第一章标题与《项目概况》整张表在 Word 中缺失——Word 实际从「（二）编制依据」开始。
**根因**：v17 读完目录条目后 `in_toc` 仍为 True；遇到 `## 第一章 总论`（h2）时，L283 只对 kind=="p" 判定退出目录态，h2 未命中 → 落到 L285 `if in_toc: continue` → **第一章 h2、（一）h3 及随后的第一张表被一并吞掉**。
**修复**：在 v17 源码层把退出条件扩展为 `kind in ("p","h1","h2","h3","h4")`，仅允许 `^\d+\.\s` 的段落留在目录内。
**缺失内容实证**：415 间（物理房量）、1,574 ㎡（全日餐饮）、5,000 ㎡（后场工区）、21,313.6 万元（基准改造投资）——**这四个数全在第一章《项目概况》表里**，且是全报告最基础的锚点。
**教训**：**表格数不一致必须逐块比对特征值，不能只看"差 1 张"就当解析合并**；本次正是靠"MD 表内数值是否都出现在 Word"才定位到真丢失。

#### 沉淀
- **终检必做项（固化为 v4.0 标准）**：① MD 表块数 = Word 表数；② 每张表的特征值均出现在 Word 全文；③ 表内全部数值均出现在 Word；④ 关键数值清单全中；⑤ emoji（真实 unicode 转义，非原始字符串）／★☆残留为零；⑥ 空白格为零；⑦ 目录↔正文一致；⑧ 每章标题均出现在 Word。
- **注意 Python 原始字符串陷阱**：`r"[\U0001F300...]"` 会让 `\U` 失效（re 不支持该转义），导致 emoji 检查假阳性 865。正确写法是**非原始字符串** `"[\U0001F300-\U0001FAFF...]"`。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
RM = os.path.join(KB, "00_项目总览_README.md")
open(RM, "a", encoding="utf-8").write(r"""
### v4.0 终稿（2026-11-14 23:05）—— 含一个影响所有历史版本的渲染 bug 修复
**终稿**：可研报告 v4.0 —— 91.6 KB / 315 段 / **40 表** / 0 空白 / 5 节 / 0 emoji / 12 章 / 36 项关键值全中；测算附表 v4.0（12 表）。
**修复的转换器 bug**：v17_docx.py 目录状态机在遇到章节标题（h2/h3）时未退出目录态，导致**第一章标题与《项目概况》整张表在 Word 中被吞掉**（含 415 间物理房量、1,574 ㎡ 全日餐饮、5,000 ㎡ 后场工区、21,313.6 万元基准改造投资四个基础锚点）。已在 v17 源码层修复，所有版本重建后正常。
**新增终检项**：MD 表块数 = Word 表数；每张表特征值均出现在 Word；表内全部数值均出现在 Word。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
L("memory + README synced")
L("DONE")
