---
title: Vault 全索引 v1.0
version: v1.0
date: 2026-09-07
author: B166ER
trigger: Eric 2026-09-07 01:04 "A 和 B 都做"
purpose: Obsidian Vault 单一入口 · 全知识网络索引
tags:
  - vault
  - 索引
  - MOC
  - 入口
---

# Vault 全索引 v1.0

> **本文件用途**：Obsidian Vault 的**单一入口**，双链所有范式/报告/数据/项目
> **Eric 痛点**：每次打开 vault 都要找 → 现在 1 处全览

---

## 一、酒店行业 · 范式入口（核心）

- [[00_报告范式_总入口_v1.0|报告范式总入口]]
- [[00_报告体系总图_v1.0|报告体系总图：信源→月报→季报→半年报]]
- [[酒店行业数据维度完整清单_v1.0_Eric出品|数据维度清单 v1.0 (Eric 出品)]]
- [[酒店行业数据维度完整清单_v2.0_B166ER对标|数据维度清单 v2.0 (B166ER 对标)]]
- [[报告模板_v2.0|报告模板 v2.0]]
- [[行业全景KB_v2.4|行业全景 KB v2.4]]

---

## 二、Dataview 查询模板（如已装 Dataview 插件）

### 2.1 全 vault 文件统计

```dataview
TABLE length(rows) as "文件数"
FROM ""
WHERE type = "markdown"
GROUP BY "全部"
```

### 2.2 最近修改的 10 个文件

```dataview
TABLE file.mtime as "修改时间"
FROM ""
SORT file.mtime DESC
LIMIT 10
```

### 2.3 所有范式文件

```dataview
LIST
FROM ""
WHERE contains(tags, "范式") OR contains(tags, "paradigm")
SORT file.ctime DESC
```

### 2.4 所有报告类文件

```dataview
LIST
FROM ""
WHERE contains(tags, "月报") OR contains(tags, "季报") OR contains(tags, "半年报")
SORT file.mtime DESC
```

### 2.5 所有 H1 2026 相关

```dataview
LIST
FROM ""
WHERE contains(file.name, "2026") OR contains(file.name, "H1")
SORT file.mtime DESC
```

---

## 三、按主题索引

### 3.1 安逸集团
- 在 KB 中：`anyi-ops-kb/00_安逸集团知识库总览.md`
- 在 Vault：`Documents/Obsidian Vault/安逸集团/`

### 3.2 酒店行业
- 范式：本 vault `00_范式与模板/`
- 数据：`01_数据池/` （如已建立）
- 报告：`02_报告/`（如已建立）

### 3.3 AI / Agent
- 在 KB 中：`anyi-ops-kb/00_全域商业市场认知/02_AI智能体/`

### 3.4 跨境与中东
- 在 KB 中：`anyi-ops-kb/00_全域商业市场认知/08_跨境_入境游/`

---

## 四、Vault 目录结构（2026-09-07 现状）

```
Documents/Obsidian Vault/
├── README.md (vault 入口)
├── 酒店行业/                       ← Eric 工作主战场
│   ├── README.md
│   └── 00_范式与模板/               ← 已建（8 个文件）
│       ├── 00_报告范式_总入口_v1.0.md
│       ├── 00_报告体系总图_v1.0.md
│       ├── README.md
│       ├── 报告体系摘要_v1.0.md
│       ├── 报告模板_v2.0.md
│       ├── 行业全景KB_v2.4.md
│       ├── 酒店行业数据维度完整清单_v1.0_Eric出品.md
│       └── 酒店行业数据维度完整清单_v2.0_B166ER对标.md
└── (其他主题待建)
```

---

## 五、Dataview 插件安装说明

1. Obsidian → Settings → Community plugins → Browse
2. 搜索 "Dataview" → Install → Enable
3. 重启 Obsidian
4. 本文件 `## 二、Dataview 查询模板` 章节的查询自动生效

---

## 六、版本历史

| 版本 | 日期 | 变更 | 作者 |
|------|------|------|------|
| v1.0 | 2026-09-07 01:04 | 首版（Vault 全索引 + Dataview 模板）| B166ER |

---

*Last updated: 2026-09-07 01:04 GMT+8 by B166ER*
*Eric 2026-09-07 01:04 指令: A 和 B 都做*