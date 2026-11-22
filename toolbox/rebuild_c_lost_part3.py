#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""重建 C 类丢失文件 - Part 3: 知识库索引 + Inbox"""
from pathlib import Path
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")

# ========== 知识库总览 ==========
kb_overview = """---
tags: [knowledge-base, overview, MOC]
author: b166er
audience: eric
status: active
updated: 2026-07-12
recovered: true
---

# 知识库总览

## 11 个核心 KB（来源: workspace/memory/）

| KB | 大小 | 状态 |
|----|------|------|
| 酒店政策法规知识库 V1.0 | 10KB | ✅ 同步 |
| 酒店运营 SOP 知识库 V1.0 | 23KB | ✅ 同步 |
| 酒店市场销售知识库 V1.0 | 10KB | ✅ 同步 |
| 酒店项目定位 V1.0 | 10KB | ✅ 同步 |
| 酒店项目案例知识库 V1.0 | 14KB | ✅ 同步 |
| 收益管理 SKILL 知识库 V1.0 | 87KB | ✅ 同步（人格与认知/）|
| 商旅 TMC 知识库 V1.0 | 15KB | ✅ 同步（人格与认知/）|
| 跨境贸易知识库 V1.0 | 14KB | ✅ 同步（人格与认知/）|
| 跨境贸易-亚马逊运营专项 V1.0 | 18KB | ✅ 同步（人格与认知/）|
| 跨境贸易-选品实战专项 V1.0 | 23KB | ✅ 同步（人格与认知/）|
| 自我革命索引 V1.0 | 12KB | ✅ 同步（人格与认知/）|

## 7 个专题 KB

1. 多 OTA 运营 V1.0（memory/multi-ota-operations-knowledge-base-v1.md）
2. 酒店收益管理 V5（memory/hotel-revenue-management-knowledge-base-v5.md）
3. 酒店新媒体 V2（memory/hotel-new-media-marketing-knowledge-base-v2.md）
4. 酒店 AI 应用 V1.3（memory/hotel-ai-applications-knowledge-base.md）
5. AHL 知识库 V1（memory/ahl-knowledge-base-v1.md）
6. 量化交易 V1（memory/quantitative-trading-knowledge-base-v1.md）
7. 创业融资 V2（memory/startup-fundraising-knowledge-base-v2.md）

## 5 个美学/理论 KB

1. 审美知识库 V3（memory/aesthetic-knowledge-base.md）
2. 博弈论 V3（memory/game-theory-decision-knowledge-base-v3.md）
3. 群论 V1（memory/group-theory-knowledge-base-v1.md）
4. 理论架构 V2.3（memory/theoretical-framework-v2.md）
5. Token 经济 V1（memory/token-economy-research.md）

## 13 个酒店行业 KB

- 5 个核心（已同步）
- 8 个补充（待整理）

## Eric 使用方式

- 打开 Obsidian → 这个文件夹 → 浏览知识库索引
- 每个 KB 都有 frontmatter 标注版本/状态
- 跨 KB 检索：用搜索或 [[双链]] 跳转

## 🔗 关联

- [[01-核心知识库完整目录]]
- [[../00-Dashboard]]
"""
(VAULT / "20-我们共同维护的" / "知识库索引" / "00-知识库总览.md").write_text(kb_overview, encoding="utf-8")
print("[OK] 00-知识库总览.md")

# ========== 核心知识库完整目录 ==========
kb_index = """---
tags: [knowledge-base, index, complete]
author: b166er
audience: eric
status: active
updated: 2026-07-12
recovered: true
---

# 核心知识库完整目录

## 按功能分类

### 📊 战略层
- [[../战略与节奏/00-战略地图]] — 2-3 年蛰伏战略
- [[../战略与节奏/01-2年蛰伏战略]] — 三阶段详解
- [[../战略与节奏/02-1244战略详解]] — 内部框架
- [[../战略与节奏/03-安逸集团机会]] — 入职前 90 天
- [[../战略与节奏/04-AHL平台档案]] — 核心创业项目

### 📈 酒店行业（13 个 KB）
**政策法规**:
- 酒店政策法规知识库 V1.0

**运营/管理**:
- 酒店运营 SOP 知识库 V1.0
- 收益管理 SKILL 知识库 V1.0

**市场/销售**:
- 酒店市场销售知识库 V1.0

**项目/案例**:
- 酒店项目定位 V1.0
- 酒店项目案例知识库 V1.0

**OTA**:
- 多 OTA 运营 V1.0

**新媒体**:
- 酒店新媒体 V2

**AI 应用**:
- 酒店 AI 应用 V1.3

### 🛒 商业/产品
- 创业融资 V2
- AHL 知识库 V1
- 跨境贸易 V1.0 + 亚马逊专项 + 选品专项
- 商旅 TMC V1.0
- 4 个新媒体产品（¥49.9-¥99）

### 🧠 思维/理论
- 审美 V3
- 博弈论 V3
- 群论 V1
- 理论架构 V2.3
- Token 经济 V1
- 量化交易 V1

### 🌟 人格/认知
- 张实全方位人格侧写报告
- 自我革命索引 V1.0
- 自我革命-认知进化报告
- 自我革命-vectorized

## 按优先级（Eric 实战常用）

1. **战略层**（每月/季度复习）
2. **酒店行业**（按需查询）
3. **AHL 平台**（每日推进）
4. **思维理论**（关键决策时调用）
5. **人格认知**（自我反思时调用）

## Eric 使用提示

- 不需要读完全部——按主题查
- 每个 KB 都有 frontmatter
- 跨 KB 检索：用 [[双链]]
- 7/12 后台运行：每周日 cron 整理

## 🔗 关联

- [[00-知识库总览]]
- [[../00-Dashboard]]
"""
(VAULT / "20-我们共同维护的" / "知识库索引" / "01-核心知识库完整目录.md").write_text(kb_index, encoding="utf-8")
print("[OK] 01-核心知识库完整目录.md")

# ========== 00-Inbox README ==========
inbox_readme = """---
author: b166er
audience: both
status: active
created: 2026-07-12
updated: 2026-07-12
recovered: true
---

# 📥 00-Inbox-待整理
> **职责**：跨方投放区。
> B166ER 推送的"未整理"内容到这里，Eric 看完后决定归档位置。

## 当前结构

- [[0-快速捕捉]] — Eric 的快速想法
- [[cron-push/README|cron-push]] — Cron 任务推送收件箱

## 我会写入

- 临时分析/报告（不归档）
- 跨工具产生的中间产物
- 待 Eric 决定归档位置的笔记

## 整理流程

1. **每日 21:00** 我整理当天 Inbox 内容
2. **分类** → 归档到对应文件夹：
   - 战略类 → 20-我们共同维护的/战略与节奏
   - 产品类 → 10-我为你生成的/产品矩阵
   - 知识类 → 20-我们共同维护的/知识库索引
3. **删除** → Inbox 清空（已归档）

## Eric 使用方式

- 打开 Obsidian → 这个文件夹 → 看最新投放
- 不需要主动归档（我整理）
- 紧急内容我会主动加 `urgent` 标签

---

**最后更新**：2026-07-12 GMT+8
"""
(VAULT / "00-Inbox-待整理" / "README.md").write_text(inbox_readme, encoding="utf-8")
print("[OK] 00-Inbox-待整理/README.md")

# ========== 0-快速捕捉 ==========
quick = """---
author: joint
audience: both
status: active
created: 2026-07-12
updated: 2026-07-12
recovered: true
---

# ⚡ 0-快速捕捉

> Eric 临时想法 / B166ER 临时草稿的统一投放点
> 不讲究格式，先记下来

## Eric 用法

按 `Ctrl+T` → 选择"快速捕捉"模板 → 写一句话
比如：
- 7/12 13:00：D-day 应对姿态决定 = C
- 7/12 13:05：1244 战略的 4 维度应该是 X/Y/Z/W

## B166ER 用法

跑完某个分析后，把中间产物投到这里，等 Eric 看完再决定归档

## 归档

每周日 21:00 我会整理这个文件夹
- 有价值的 → 移到对应 KB
- 无价值的 → 删除
- 不确定的 → 留下周再处理

---

**最后更新**：2026-07-12 GMT+8
"""
(VAULT / "00-Inbox-待整理" / "0-快速捕捉.md").write_text(quick, encoding="utf-8")
print("[OK] 0-快速捕捉.md")

print("\n主线 3 第三波完成 (知识库索引 + Inbox)")
