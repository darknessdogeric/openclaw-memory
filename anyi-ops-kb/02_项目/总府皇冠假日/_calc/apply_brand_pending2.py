# -*- coding: utf-8 -*-
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
B = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
M = {
 "P3":"总府皇冠改造_综合改造报告_第三部分_各方向必要性与可行性_v1.0_2026-11-05.md",
 "P9":"总府皇冠改造_综合改造报告_第九部分_分品牌经营模型与规划目标校准_v1.0_2026-11-05.md",
 "P10":"总府皇冠改造_综合改造报告_第十部分_技术方案大纲与进度计划与风险登记册_v1.0_2026-11-05.md",
}
def P(k): return os.path.join(B, M[k])

E = []
E.append(("P10",
 '洲至奢选不接（品牌方接受度）** | 中 | 严重（主线品牌落空） |',
 '**品牌路径未能在 2027 H1 落地（2026-11-05 更新：品牌方接受度已解除，风险转为流程约束）** | 中 | 严重（主线品牌落空） |'))

E.append(("P10",
 '能不能把它改出来。**',
 '能不能把它改出来。**\n>\n> ⭐⭐⭐ **2026-11-05 重新分层（品牌方"待定"状态下）**：**仍为红线** = R-01 分区验收（⭐ **解除主体是消防审查机构，与品牌谈判无关，可立即问**）｜R-03 人防｜R-04 投入｜R-05 额度｜⭐ **新增 R-25：改造决策不得以"品牌已定"为前提**；**降级为待谈项** = R-06 品牌方接受（洲际已明确可配合换牌、无意见）。⭐⭐ **六条红线中与品牌相关的只剩一条，而那一条恰恰是"解耦"本身。**'))

E.append(("P9",
 '**取决于品牌方给的是委托还是特许** —— ',
 '**2026-11-05 更新：品牌方已明确可配合换牌、无意见 → "品牌路径可行"这一维度已解除**；仍待谈的只有**费率与商务条件**（委托 vs 特许），按现行流程**不可谈 → 待定** —— '))

ok = fail = 0
for k, o, n in E:
    p = P(k); t = open(p, encoding="utf-8").read(); c = t.count(o)
    if c != 1:
        print(f"  [SKIP x{c}] {k} :: {o[:50]}"); fail += 1; continue
    open(p, "w", encoding="utf-8").write(t.replace(o, n, 1)); print(f"  [OK] {k} :: {o[:50]}"); ok += 1
print(f"替换: {ok} 成功 / {fail} 未命中\n")

# 结论表插入 3 行
p = P("P10"); t = open(p, encoding="utf-8").read()
anchor = '| **6** | ⭐⭐ **六条红线里没有一条是"市场会不会来"**'
if '| **7** | ⭐⭐⭐ **2026-11-05 状态更新' in t:
    print("  [SKIP-结论已存在] P10")
elif anchor in t:
    lines = t.split("\n")
    idx = next((i for i, l in enumerate(lines) if l.startswith(anchor)), None)
    extra = [
"",
'| **7** | ⭐⭐⭐ **2026-11-05 状态更新：洲际明确"可配合换牌、无意见"** → 品牌方接受度维度已解除；但按现行流程**品牌协商不可启动 → 品牌落地路径整体"待定"**。⭐⭐ **关键解耦：改造决策不得以"品牌已定"为前提**，否则规划 2027 节点必失（新增 §10.4） |',
'| **8** | ⭐⭐⭐ **核心判断（§10.4.3）：品牌留白时应当"减房买期权"** —— 减房至 268 间 / 40 ㎡+ 是唯一能吸收未来品牌不确定性的选择：①品牌解冻时点不可控，而不减房则未来**无行使空间**（改面积须二次停业破除）②委托模式下换品牌不违约，与规划不冲突 ③风险不对称（不减房的最坏结果 = 全案重做） |',
'| **9** | ⭐⭐ **"待定"状态下现在能做的 5 件事（§10.4.4），全部不依赖品牌谈判** —— 尤以 **R-01 消防分区验收问询**为最：⭐ **它的解除主体是消防审查机构，不是品牌方**；其次为 R-03 人防、R-05 额度、品牌中立版改造范围与限额 |',
    ]
    lines[idx+1:idx+1] = extra
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    print(f"  [OK-插入结论3行] P10 @行{idx+1}")
else:
    print("  [MISS-结论锚点] P10")

# 第三部分 状态说明块
NOTE3 = """
> ### ⚠️ **2026-11-05 状态更新：品牌路径"待定"**
> **已知**：洲际已明确**可配合换牌、无意见**（口头、流程性，非书面）→ ⭐ **"品牌方接受度"这一维度已解除**；其他品牌方待谈。
> ⚠️ **但按现行流程品牌协商不可启动 → 本部分涉及品牌落地的结论整体转为"待定"。**
> ⭐⭐ **本部分的三方向"必要性"判断与"技术门槛"判断均不因此改变**（面积、消防、机电、隐蔽工程的缺口与品牌无关）；⭐ **改变的是"何时落地"与"落地代价"**：
> ① ⭐ **改造决策不得以"品牌已定"为前提**（否则规划 2027 节点必失，见第十部分 §10.4.2）；
> ② ⭐⭐ **品牌留白时应当"减房买期权"** —— 减房至 268 间 / 40 ㎡+ 是唯一能吸收未来品牌不确定性的选择（见第十部分 §10.4.3）；
> ③ ⭐ **改造按最高标准（洲际 2026 标准 + IHG 认可供应商）做**，则任何品牌落地都不需二次返工。

"""
p = P("P3"); t = open(p, encoding="utf-8").read()
if "2026-11-05 状态更新：品牌路径" in t:
    print("  [SKIP-P3说明已存在]")
else:
    lines = t.split("\n"); idx = None
    for i, l in enumerate(lines):
        if l.startswith("> **数据等级**"): idx = i; break
    if idx is None:
        for i, l in enumerate(lines):
            if l.startswith("> ") and ("数据等级" in l or "配套" in l): idx = i; break
    if idx is None:
        for i, l in enumerate(lines):
            if l.startswith("---"): idx = i; break
    if idx is None: lines.append(NOTE3)
    else: lines.insert(idx+1, NOTE3)
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    print(f"  [OK-插入P3说明] @行{idx}")

print("\n=== 校验 ===")
for k in ("P3","P9","P10"):
    t = open(P(k), encoding="utf-8").read()
    bad = [m for m in ("###FILE:","###OLD","###NEW") if m in t]
    print(f"  {k:<5} 待定 {t.count('待定'):>2} | 可配合换牌 {t.count('可配合换牌'):>2} | 减房买期权 {t.count('减房买期权'):>2} | §10.4 {t.count('10.4'):>2} | 残留 {bad if bad else '无'}")