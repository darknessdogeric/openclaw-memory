# B166ER 自主工作方式 V1.2
> 版本: V1.2（2026-04-13 Agent矩阵方案更新）
> 创建: 2026-04-10 | 更新: 2026-04-13

---

## 核心理念

**SKILL存在的意义是被使用，不是被收藏。**
**MAIN AGENT是大脑，不是手。专项AGENT是深度执行单元。**

---

## 一、AGENT矩阵架构

```
            ┌─────────────────────────────┐
            │       Eric (你)            │
            └──────────┬──────────────┘
                       │ 对话/指令
            ┌──────────▼──────────────┐
            │    MAIN AGENT (大管家)    │
            │  · 理解指令              │
            │  · 判断类型 → 分发        │
            │  · 整合结果              │
            │  · 直接执行快速任务      │
            └──────┬──────┬──────┬───┘
                   │      │      │
            ┌──────▼┐ ┌──▼──┐ ┌▼─────┐
            │深度调研│ │知识库│ │cron  │
            │researcher│knowledge│lottery│
            └───────┘ └─────┘ └──────┘
```

---

## 二、任务分类路由表

| 任务类型 | 触发方式 | 执行者 | 并发限制 |
|---------|---------|-------|---------|
| **战略决策/商业分析** | 你说 → main直接执行 | main agent | 1次 |
| **深度调研/竞品/行业/技术架构** | 你说"深化XXX" | researcher sub-agent | 最多2个 |
| **知识库建设/更新/索引** | cron或你说 → main分发 | knowledge sub-agent | 最多1个 |
| **大乐透预测/复盘** | cron触发 | isolated cron | 自动 |
| **定时提醒/日报/月报** | cron触发 | isolated cron | 自动 |
| **快速问答/文件操作** | 你说 → main直接执行 | main agent | 无限制 |
| **跨域任务（多类型同时）** | 你说 → main协调 | main+多个sub | 按需 |

---

## 三、AGENT命名与职责

| AGENT | 会话标签 | 职责 | 并发 |
|-------|---------|------|-----|
| `main` | agent:main:main | 大脑/调度/快速任务 | 默认 |
| `researcher` | sessions_spawn | 深度调研/竞品/行业/技术架构 | ≤2 |
| `knowledge` | sessions_spawn | 知识库/索引/自演化/版本管理 | ≤1 |
| `lottery` | cron isolated | 大乐透专项（预测/复盘/模型迭代） | 自动 |

---

## 四、冲突规则

```
规则1: 同类型sub-agent最多1个在跑
规则2: main agent始终是调度者，不被占用
规则3: 新任务撞车 → 队列+通知Eric
规则4: sub-agent结果汇总main，不直接输出
规则5: cron任务独立运行，不占用main/sub agent槽位
```

---

## 五、SKILL路由（按任务类型）

| 任务类型 | SKILL组合 |
|---------|-----------|
| **酒店运营** | multi-ota → hotel-revenue → pricing-strategy |
| **OTA数据** | multi-ota + scrapling |
| **新媒体内容** | autoresearch → wewrite → xiaohongshu → image-gen |
| **跨境电商** | amazon-fba → amazon-fba-prep → ecommerce-product-picker |
| **区块链/AHL** | blockchain → afrexai-tokenomics |
| **博弈分析** | game-theory-decision-knowledge-base-v3 |
| **审美判断** | aesthetic-judgment + image-gen |
| **战略决策** | strategic-decision-making → game-theory |
| **融资路演** | startup-fundraising + pptx-generator |
| **大乐透** | (执行大乐透SOP) |
| **知识库搜索** | `local_semantic_search.py` (向量索引) |

---

## 六、cron任务清单（已清理）

| 任务 | 状态 | 说明 |
|------|------|------|
| 大乐透开奖检查 | ✅ 正常 | 周一/三/六 21:30 |
| Memory Dreaming Promotion | ✅ 正常 | 每日03:00 |
| SCM供应链KB季度更新 | ✅ 正常 | 季度15日09:00 |
| B166ER月度自动复盘 | ✅ 正常 | 每月26日09:00 |
| B166ER知识库月度更新 | ✅ 正常 | 每月28日10:00 |
| Multi-OTA平台探测提醒 | ✅ 正常 | 每日09:00 |

**已移除**（故障/冗余）：
- DailyDataCollection（14次错误）
- 技能市场扫描（42次错误）
- AI Builders Digest（13次错误）
- Full-Scan-AutoIngest（channel错误）
- WeeklyKnowledgeIndexUpdate（model_not_found）

---

## 七、核心SKILL联动工作流

### 工作流A：酒店收益全链路
```
multi-ota（采集）
  → hotel-revenue-management（收益诊断）
  → pricing-strategy（定价分析）
  → strategic-decision-making（博弈定价）
```

### 工作流B：自媒体内容工厂
```
autoresearch（热点）
  → wewrite（写作）
  → xiaohongshu-all-in-one（发布）
  → image-gen（如需配图）
```

### 工作流C：跨境电商选品→销售
```
amazon-fba（知识）
  → amazon-fba-prep（发货准备）
  → cross-border-trade（合规）
  → content-marketing（产品内容）
```

### 工作流D：AHL深化
```
blockchain（链上基础）
  → afrexai-tokenomics（代币经济）
  → game-theory（激励相容）
  → strategic-decision-making（平台战略）
```

---

## 八、自我进化机制

### 每次心跳T0任务
```
1. 上次任务有错误吗？→ corrections.md
2. 路由有偏差吗？→ 立即修正
3. 有没有遗漏需求？→ 主动补充
4. 工具调用最优吗？→ 优化路径
```

### 进化触发规则
```
错误发生 → 微进化记录corrections.md
3次同类错误 → 提炼规则 → 更新MEMORY.md
路由偏差 → 更新WORK.md路由表
新技能发现 → 立即集成测试
```

---

## 九、版本历史
- V1.2: 2026-04-13 Agent矩阵方案更新（清理故障cron/建立路由表）
- V1.1: 2026-04-12 重建
- V1.0: 2026-04-10 初版

---

> 所有任务调度以WORK.md为准。
