# -*- coding: utf-8 -*-
"""v22 应用：替换第二、九、十二章；重建第五章比选表与结论；增风险；更新总论"""
import io, os, sys, re, json
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
LOG = open(os.path.join(T, "v22.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

sys.path.insert(0, os.path.join(KB, "_calc"))
from v22_text import CH2, CH9, CH11_NEW, CH5_NEW6

V21 = json.load(open(os.path.join(T, "v21.json"), encoding="utf-8"))
SCH = {s["key"]: s for s in V21["schemes"]}
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return ("%.2f%%" % (v * 100)) if v is not None else "无可解内部收益率"

MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v2.0_2026-11-14.md")
MD3 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ① 第二章
m = re.search(r"^## 第二章 市场分析与预测.*?(?=^## 第三章 )", t, re.M | re.S)
assert m, "未定位第二章"
t = t[:m.start()] + CH2.rstrip() + "\n\n" + t[m.end():]
L("第二章已替换")

# ② 第九章
m = re.search(r"^## 第九章 财务评价.*?(?=^## 第十章 )", t, re.M | re.S)
assert m, "未定位第九章"
t = t[:m.start()] + CH9.rstrip() + "\n\n" + t[m.end():]
L("第九章已替换")

# ③ 第五章（五）方案比选表：重建（加收入列）
m = re.search(r"^### （五）品牌方案比选.*?(?=^### （六）)", t, re.M | re.S)
if m:
    rows = ["| 方案 | 品牌标准 | 公区做法 | 房量做法 | 改造后年营业收入（万元） | 收入倍数（对改造前） | 改造投资（万元） | 全口径内部收益率 | 集团口径静态回收期 | 可行性 |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    FEAS = {"S1": "基准候选", "S2": "否决（收入仅增 8%）", "S3": "否决", "S4": "比价方案",
            "S5": "否决", "S6": "否决", "S7": "比价方案", "S7B": "唯一全判据成立", "S8": "不可行（客房面积不达标）"}
    for k in ("S1", "S2", "S3", "S4", "S5", "S6", "S7", "S7B", "S8"):
        s = SCH[k]
        b = "**" if k in ("S1", "S7B") else ""
        pbg = ("%s 年" % N(s["pb_grp"], 2)) if s["pb_grp"] else "不适用"
        rows.append("| %s | %s | %s | %s | %s%s%s | %s%s%s | %s | %s | %s | %s |" % (
            k, s["brand"], s["pub_mode"], s["room_mode"],
            b, N(s["steady_rev"]), b, b, N(s["rev_ratio"], 2), b,
            N(s["capex"]), P(s["irr20"]), pbg, FEAS[k]))
    new5 = ("### （五）品牌方案比选\n\n以下比较在第五章第一节情形一假设下成立，并按第九章分档定价口径列示。"
            "**排序同时看收入增量与投资回报两条线，不可只看其一。**\n\n" + "\n".join(rows) + "\n\n")
    t = t[:m.start()] + new5 + t[m.end():]
    L("第五章比选表已重建（9 行）")

# ④ 第五章（六）比选结论
m = re.search(r"\*\*比选结论：\*\*.*?(?=\n### （六）)", t, re.S)
if m:
    t = t[:m.start()] + CH5_NEW6.rstrip() + "\n" + t[m.end():]
    L("第五章比选结论已重写")
else:
    L("[MISS] 比选结论")

# ⑤ 第十二章
m = re.search(r"^## 第十二章 结论与建议.*", t, re.M | re.S)
assert m, "未定位第十二章"
t = t[:m.start()] + CH11_NEW.rstrip() + "\n\n"
L("第十二章已重写")

# ⑥ 第十一章 风险增项
RISK_NEW = ("| R-19 | 改造后收入未达预期（价格带低于假设或出租率不及预期） | 高 | 高 | 高 | 分档定价下 S7B 与 S1 的收入敏感性差异达 1.85 倍（14,009.8 对 10,938.7 万元），须在投资决策前完成品牌方定价意见验证 | 产业发展部 |\n"
             "| R-20 | 顶级设计型价格带无法在总府位置兑现 | 中 | 高 | 高 | 以品牌方定价意见与可比第三方成交数据双重验证；不能验证则该路径不成立，退回 S1 | 产业发展部 |")
anchor = "| R-18 | 集团与市场房价锚的差异导致测算反复 | 高 | 中 | 中 | 以集团测算底稿一次对账闭合 | 产业发展部 |"
if anchor in t:
    t = t.replace(anchor, anchor + "\n" + RISK_NEW)
    L("第十一章风险已增 R-19/R-20")
else:
    L("[MISS] R-18 锚点")

# ⑦ 总论概况表
t = t.replace("| 改造投资 | 17,995.6 至 56,850.9 万元（随情景与方案变化） |",
              "| 改造投资 | 17,995.6 至 56,850.9 万元（随情景与方案变化）；五星档基准 21,313.6 万元 |")
t = t.replace("| 项目总资金需求 | 24,515.6 至 73,150.9 万元 |",
              "| 项目总资金需求 | 24,515.6 至 73,150.9 万元；五星档基准 31,093.6 万元 |")
t = t.replace('| 主要结论 | 前置条件成立时，以"沿用皇冠 + 公区保留石材 + 不减房"为基准方案；前置条件不成立时，整体改造不成立，仅保留必要局部整改 |',
              '| 主要结论 | 前置条件成立时，以"沿用皇冠 + 公区保留石材 + 不减房"为五星档基准方案（改造后年收入为改造前的 1.61 倍）；唯"外部奢牌 + 3 改 2 + 顶级设计型价格带"在全部判据上成立，但须先验证价格带可兑现；前置条件不成立时，整体改造不成立，仅保留必要局部整改 |')

# ⑧ 第一章（三）背景补收入基线
t = t.replace('''**其四，资产处于持续失血状态。** 改造前年均经营现金流为 −1,924 万元，不改造并非零成本选择，而是持续经营性亏损。''',
              '''**其四，资产处于持续失血状态。** 改造前年均经营现金流为 −1,924 万元，不改造并非零成本选择，而是持续经营性亏损。

**其五，改造的意义必须以收入增量衡量。** 改造前年营业收入 6,774.0 万元（402 间、平均房价 363.99 元、出租率 70.78%）。改造后年收入若不超过该数，改造即失去意义。本报告在第九章以“改造后收入须高于改造前”作为贯穿判据。''')

open(MD3, "w", encoding="utf-8").write(t)
os.remove(MD)
L("MD -> v3.0, bytes:", len(t.encode("utf-8")))
h2s = re.findall(r"^## (.+)$", t, re.M)
L("章节:", len(h2s))
for h in h2s:
    L("   -", h.encode("unicode_escape").decode("ascii"))
