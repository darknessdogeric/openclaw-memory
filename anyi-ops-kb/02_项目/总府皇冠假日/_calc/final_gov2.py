# -*- coding: utf-8 -*-
import io, os, sys, re, glob
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(r"D:\B166ER-openclaw\workspace\.tmp\final_gov.log", "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

MD = os.path.join(KB, "总府皇冠改造_整体方案报告_集团汇报件_v1.0_2026-11-13.md")
t = open(MD, encoding="utf-8").read()
L("MD bytes:", len(t.encode("utf-8")))
L("--- 结构（标题）---")
for l in t.split("\n"):
    if re.match(r"^#{1,3} ", l):
        L("  " + l.encode("unicode_escape").decode("ascii")[:120])

MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-13.md"
add = """

---

## 09:30 整体方案报告改为**集团汇报件范式**（最终版）

**交付**：改造报告交付\\总府皇冠改造_整体方案报告_集团汇报件_v1.0_2026-11-13.docx（63.2 KB）
（此前两版——党政机关红头件与非公文版——均已删除，只保留本件，避免上会时版本混淆）

### 与"党政机关红头件"的差别（Eric 指正）
集团汇报件不是 GB/T 9704 的党政机关件。差别：
- 主送写作「**安逸酒店集团：**」（集团名称后加冒号），不是"安逸酒店集团决策层。"
- 正文须有**导语**：「根据集团"十五五"规划关于加快改造项目决策的要求，以及我部会同工程、财务等有关单位对总府皇冠假日酒店改造升级项目开展的论证工作，现将有关情况报告如下。」
- 正文结构改为**情况—问题—建议—请示事项**：一、项目基本情况与市场判断｜二、改造必要性｜三、论证结论与改造可行性｜四、存在的主要问题与风险｜五、下一步工作建议｜**六、请示事项**
- 结尾用「**以上报告，请审阅。**」（非"特此报告。"）
- 新增**可批复的请示事项 4 条**：认可改造必要性与主方向｜明确总府在 4.01 亿盘子中的额度与批次｜授权向消防审查机构及候选品牌方发函｜报请明确 5 项待确认参数口径
- 附件说明 4 项 + 抄送 5 单位 + 发文机关署名与成文日期 + 版记

### 结构性改进
- **补上了此前缺失的独立"改造必要性"章** —— 从《可行性研究报告（公文版）》提取完整 6 小节（规划刚性／合规刚性／品牌方刚性／房间级互证／资产与谈判刚性／必要性结论），与《整体方案报告》的最新测算数字合并成一件
- 新增「存在的主要问题与风险」章：风险清单 + 品牌落位受"一城一店"约束 + 审批路径未明 + 改造后经营执行 + 与川宾物理耦合 + 待确认参数与模型边界

### 转换过程的自造错误（均已修，记录备查）
1. 正则写在 raw string 里，Unicode 转义序列未被解释 → emoji 未删（432 个）
2. 清理用的空白匹配吞掉换行 → 标题与正文粘连、小节丢失 → 已改用仅空白字符，并加"标题完整性自检"（检测标题含竖线或加粗符即报错）
3. 章号中文（一二三）与节号数字（1.1）不匹配 → 块匹配全空、正文只剩 5.8 KB → 改为按标题关键词选取
<!-- project: github.com/darknessdogeric/openclaw-memory -->

---
"""
open(MEM, "a", encoding="utf-8").write(add)
RM = os.path.join(KB, "00_项目总览_README.md")
rm = """

| **整体方案报告（集团汇报件）** | v1.0 | docx 63.2 KB | ⭐⭐⭐ **集团汇报件范式**：主送「安逸酒店集团：」+ 导语 + 情况—问题—建议—**请示事项** + 「以上报告，请审阅。」+ 附件/抄送/版记；六章正文（含独立"改造必要性"章） | ⭐ **请示 4 项**：认可主方向 / 明确额度批次 / 授权去函 / 报请 5 项参数口径 |
"""
open(RM, "a", encoding="utf-8").write(rm)
L("memory + README synced")

for f in sorted(glob.glob(os.path.join(REP, "总府皇冠改造_整体方案报告*.docx"))):
    L("DELIVER:", os.path.basename(f).encode("unicode_escape").decode("ascii"), "%.1f KB" % (os.path.getsize(f)/1024))
