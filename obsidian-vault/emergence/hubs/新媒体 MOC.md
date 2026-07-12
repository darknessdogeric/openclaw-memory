---
author: b166er
audience: both
type: hub
created: 2026-07-12
tags: [moc, 新媒体, 小红书, B166ER, 范式]
---

# 新媒体 MOC

> **任何视觉产出** (小红书详情图 / 海报 / PPT / 信息图) → **必读此 MOC**

## 触发场景

- Eric 说 "做小红书详情图 / 海报 / 信息图 / PPT"
- Eric 说 "做 XX 产品的小红书"
- 任何包含 "小红书 / 微信 / 微博 / 抖音" 平台的视觉产出

## 主文档

- **[[50-外部接入/B166ER-范式/README-MOC|B166ER 新媒体模板库 MOC]]** ← 必读
  - 3 大范式 (V3 Brutalist / V6 美联储 / B166ER 海报)
  - B 标严格用法 (R30)
  - 价格铁律 ¥99
  - 小红书合规铁律 (R29)
  - 标准 5 步调用流程

## 3 大范式 (按场景选)

| 范式 | 配色 | 适用 | 路径 |
|------|------|------|------|
| **V3 Brutalist** | 燕麦白 + 砖红 + 黑 | 决策类 / 采购 / 总经理 | `revenue-v3-template/` + `overseas-v3-template/` |
| **V6 美联储** | 深蓝 + 金 + 米白 | 价格突出 / 数字驱动 | `supply-chain-gen-scripts/gen_v6_fed.py` |
| **B166ER 海报** | 暗黑霓虹 | 架构图 / 概念图 | `B166ER-海报-template.html` + `B166ER-架构图-template.html` |

## 9-10 段标准结构

### V3 9 段 (收益管理)
```
p01 cover         → 封面 (品牌 + 标题 + 价格 + 4 stats)
p02 painpoints    → 6 条痛点
p03 value         → 6 条价值
p04 audience      → 5 类人群
p05 chapters      → 13 章节全景
p06 templates     → 5 档版本
p07 quotes        → 客户证言 / 对比
p08 delivery      → 交付方式
p09 cta           → 行动召唤
```

### V3 10 段 (海外客源)
```
p01-p09 同上
p10 trust         → 信任背书
```

## 渲染命令 (Edge headless)

```bash
msedge --headless --disable-gpu --hide-scrollbars \
  --screenshot=out.png --window-size=1080,1440 \
  file:///path/to/html.html
```

## 相关 MOC

- [[B166ER 知识库 MOC]] — 总索引
- [[工具-系统 MOC]] — 工具配置
- [[酒店行业 MOC]] — 酒店新媒体素材

## 相关规则

- R26 - 复用范式 > 重新发明
- R27 - 小红书 3:4 比例
- R28 - 小红书范式固定
- R29 - 小红书合规铁律
- R30 - B 标严格用法
- R31 - 模板丰富度
- R32 - 模板库调用协议 (新会话必读 MOC)

## 相关成品

- 供应链工程 V5/V6 → `obsidian-vault/10-我为你生成的/产品矩阵/酒管供应链工程-XHS/`