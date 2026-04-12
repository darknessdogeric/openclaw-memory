# B166ER 自主工作方式 V1.1
> 版本: V1.1（2026-04-12 重建）
> 创建: 2026-04-10 | 更新: 2026-04-12

---

## 核心理念

**SKILL存在的意义是被使用，不是被收藏。**
每个SKILL都应该在一个明确的workflow中有自己的位置。

---

## 架构：三层自主引擎

```
用户请求 / 心跳触发
        ↓
  【路由层】语义识别 → 判断类型
        ↓
  【执行层】调用 SKILL组合 → 完成任务
        ↓
  【记录层】结果 → memory/ + 自反思
```

---

## 一、路由决策表（任务分类）

| 任务类型 | 触发关键词 | SKILL组合 |
|---------|-----------|----------|
| **酒店运营** | 酒店/收益/ADR/OCC/定价/竞品/GOP | multi-ota → hotel-revenue → pricing-strategy → strategic |
| **OTA数据** | 携程/美团/去哪儿/Booking/Agoda | multi-ota + hotel-price-finder + scrapling |
| **新媒体内容** | 公众号/小红书/抖音/朋友圈/内容营销 | autoresearch → content-marketing → wewrite → xiaohongshu → image-gen |
| **自媒体矩阵** | 发笔记/发文章/发海报/发抖音 | china-poster-studio / wewrite / xiaohongshu / image-gen |
| **跨境电商** | Amazon/选品/BSR/跨境/外贸 | amazon-fba → amazon-fba-prep → ecommerce-product-picker → cross-border |
| **区块链/AHL** | 区块链/智能合约/Token/链上 | blockchain → afrexai-tokenomics |
| **博弈分析** | 博弈/谈判/策略/纳什均衡 | game-theory-decision-knowledge-base-v3 |
| **审美判断** | 审美/设计/品位/排版 | aesthetic-judgment + image-gen |
| **战略决策** | 战略/决策/投资/谈判 | strategic-decision-making → game-theory |
| **融资路演** | 融资/股权/YC/BP/IPO | startup-fundraising-knowledge-base + pptx-generator |
| **大乐透** | 大乐透/彩票/预测/开奖 | (执行大乐透SOP) |
| **每日心跳** | (自动触发) | 项目检查 → 技能扫描 → 记忆整理 → 自我进化 |
| **知识库搜索** | 搜索/查询/记得/有没/在哪里 | `local_semantic_search.py` (175文档向量索引) |

---

## 二、核心SKILL联动工作流

### 工作流A：酒店收益全链路
```
multi-ota（采集携程/美团/去哪数据）
  → hotel-revenue-management（收益诊断）
  → pricing-strategy（定价分析）
  → strategic-decision-making（博弈定价策略）
  → hotel-report（如需报告）
  → wewrite（如需公众号发布）
  → self-improving（自我反思）
```

### 工作流B：自媒体内容工厂
```
autoresearch（热点监控）
  → content-marketing（内容策略+编辑日历）
  → wewrite（公众号写作）
  → xiaohongshu-all-in-one（小红书发布）
  → china-poster-studio（如需海报）
  → image-gen（如需配图）
  → self-improving（自我反思）
```

### 工作流C：跨境电商选品→内容→销售
```
amazon-fba（Amazon全链路知识）
  → amazon-fba-prep（FBA发货准备）
  → ecommerce-product-picker（选品分析）
  → cross-border-trade（跨境合规）
  → content-marketing（产品内容）
  → self-improving（自我反思）
```

### 工作流D：AHL区块链方向
```
blockchain（区块链基础）
  → afrexai-tokenomics（代币经济学）
  → game-theory（激励相容设计）
  → strategic-decision-making（平台战略）
```

---

## 三、工具箱

### 已配置的工具
| 工具 | 文件 | 调用场景 |
|------|------|--------|
| 本地语义搜索 | `local_semantic_search.py` | 知识库向量搜索（175文档） |
| 博弈论决策 | `docs/game_theory_tool.py` | 投资人/商户/竞品/合作方博弈 |
| 元认知 | `docs/metacognition_tool.py` | 重大决策前/每日复盘 |
| 酒店收益 | `docs/hotel_revenue_tool.py` | ADR/OCC/定价/竞品分析 |
| 审美判断 | `skills/aesthetic-judgment/aesthetic_tool.py` | 设计/空间/内容审美 |
| 大乐透 | `docs/大乐透预测SOP.md` + `lottery_history/` | 每周一/三/六开奖后复盘 |

---

## 四、自我进化机制

### 每次心跳T0任务：微进化快速扫描
```
1. 上次任务有错误吗？→ corrections.md
2. 路由有偏差吗？→ 立即修正
3. 有没有遗漏需求？→ 主动补充
4. 工具调用最优吗？→ 优化路径
5. 有没有该记但没记住的？→ 写入MEMORY.md
```

### 进化触发规则
```
错误发生 → 微进化记录corrections.md
3次同类错误 → 提炼规则 → 更新MEMORY.md
路由偏差 → 更新WORK.md路由表
新技能发现 → 立即集成测试
知识库缺失 → 主动补充
```

---

## 五、版本历史
- V1.1: 2026-04-12 重建（Git reset后恢复）
- V1.0: 2026-04-10 初版

---

> 所有工具调度以WORK.md为准。
