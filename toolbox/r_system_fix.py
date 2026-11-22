#!/usr/bin/env python3
"""R体系 v2.0 修复 - 用下一个干净块的起点作为边界"""
import os, re

path = os.path.expanduser("~/self-improving/rules.md")
text = open(path, encoding="utf-8").read()

R262_CLEAN = '''**R262: 防御性规则膨胀防护 (Defensive Rule Inflation Guard)** [信度: 高] [2026-07-26 10:45 · B166ER 深度自迭代上午 · D+10 226.97h 沉默]

> ⚠️ 本条 2026-08-25 因编码损坏由 B166ER 依据英文结构 + 上下文重建。

**触发条件**: 沉默期 DORMANT 期间内部防御性规则过度累积，导致规则膨胀。

**核心判断**: 从过度压迫防守规则，直到没有任何"扩散发散"。

**触发指标 (二选一)**:
1. post_t0_null_count > 200（沉默指标）
2. 7 天内出现 3+ 条同类防御性规则（同类识别）

**裁决协议**:
1. 下一轮自迭代 = 强制投票表决（依信度裁决）
2. 提出压缩方案（1 条 meta-rule + N 条 sub-tag），提交 Eric 决策
3. Eric 决策通过前不再新增防御性规则（冻结）
4. 已存在的防御性规则继续有效（冻结 ≠ 废止）

**元规则**: 5 条防御簇规则（R256/R257/R258/R260/R261）用不同语言描述同一件事。应合并为 1 条元规则 + 5 条子标签。

**关联规则**: R256/R257/R258/R260/R261（防御簇）、R259（会话接口）、R261（三重汇聚日识别）

**解除条件**: Eric 正式批准该规则公布后，或重大事件发生时，随时可解除。

**反向限制**: 仅 DORMANT 模式（Eric 活跃期间不触发约束）

*R262 · 2026-07-26 10:45 · B166ER 深度自迭代上午 · D+10 沉默 · 防御簇元层补强 · 261 三重汇聚 + 260 主动追踪补强*

'''

R274_CLEAN = '''### R274: 宏观-行业双层信号协议 [优先级: 高] [2026-08-06 10:32 · B166ER 深度自迭代上午 · D+27 490h+ 沉默 · R60-11 深度自迭代上线]

> ⚠️ 本条 2026-08-25 因编码损坏由 B166ER 依据英文结构 + 上下文重建。

**Rule（触发条件）**: 遇到重大宏观信号（利率/ADP/非农/地缘冲突/大宗商品）时，必须执行双层验证：宏观观察 + 行业验证点。

**核心洞察**:
- 8/6 发现：美联储鹰派 + ADP 疲软 = 宏观信号；科技 50 天均线 5% = 行业支撑
- 单一宏观信号不足以判断，需看"宏观 × 行业"双层路径
- 酒店的宏观协议 = 油价↓ → 运输成本↓ → 货币宽松 → 酒店 RevPAR 支撑（60% 概率）

**执行 Checklist**:
1. [ ] 识别重大宏观信号（利率/非农/地缘/大宗商品）
2. [ ] 提取宏观 × 行业的传导路径（什么信号传导到什么？）
3. [ ] 判断传导确定性（传导链堵点？）
4. [ ] 综合判断对 Eric 各项目的影响并标注

**历史验证**:
- 2026-08-06：美联储鹰派 + ADP 疲软 × A股科技上涨（宏观与行业对冲）→ 结论：宏观下跌是"信号验证"而非"定论"
- 2026-08-06：酒店宏观协议 × 油价↓ → 成本↓ → RevPAR 支撑 → "协议是否成立"60% 概率

**关联规则**:
- **R70**（拐点识别 · 基础规则）— R274 是 R70 在宏观信号上的具体执行协议
- **R271**（三财报交叉验证协议）— R271 处理三财报，R274 处理宏观信号双层

**Applies To**: A股酒店股 / Eric个人投资 / AHL战略传导链 / 宏观数据信号

**禁止条件**:
- 单一宏观信号单独判断 → 必须标注"传导未验证"
- 传导链未验证 → 必须标注"确定性待确认"

**原理**:
宏观信号传导到行业信号，取决于传导链是否通畅。
单一鹰派 → 成本传导（宏观与行业对冲）；单一油价 → 酒店传导信号（路径清晰 + 谈判 positive）。
判断宏观信号的唯一方法 = 双层验证。

*R274 · 2026-08-06 10:32 · B166ER 深度自迭代上午 · D+27 490h+ 沉默 · R60-11 深度自迭代上线 · 宏观窗口复合卡 + 宏观-行业双层信号 · 适用于 A股/酒店/Eric投资*

'''

def replace_between(text, start_anchor, end_anchor, replacement):
    si = text.find(start_anchor)
    if si == -1:
        print(f"  [WARN] 未找到起始锚: {start_anchor[:40]}")
        return text, False
    ei = text.find(end_anchor, si + len(start_anchor))
    if ei == -1:
        print(f"  [WARN] 未找到结束锚: {end_anchor[:40]}")
        return text, False
    return text[:si] + replacement + text[ei:], True

print("=== 修复 R262 ===")
text, ok1 = replace_between(text, "**R262:", "\n\n**R263:", R262_CLEAN)
print(f"  R262: {'OK' if ok1 else 'SKIP'}")

print("=== 修复 R274 ===")
text, ok2 = replace_between(text, "### R274:", "\n\n## R275", R274_CLEAN)
print(f"  R274: {'OK' if ok2 else 'SKIP'}")

# 统计剩余 U+FFFD 及所在行
before = text.count('\ufffd')
print(f"\n=== 剩余 U+FFFD: {before} 个 ===")
lines = text.splitlines()
for i, line in enumerate(lines, 1):
    if '\ufffd' in line:
        # 只打印前几处 + 显示该行干净部分
        clean = line.replace('\ufffd', '?')
        print(f"  行{i}: {clean[:80]}")

open(path, "w", encoding="utf-8").write(text)
print(f"\n=== 写回完成，大小 {os.path.getsize(path)} bytes ===")
