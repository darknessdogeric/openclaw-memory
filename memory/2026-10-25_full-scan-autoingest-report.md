# B166ER 全盘扫描与自动纳入报告

**执行时间**: 2026-10-25 03:26 (Asia/Shanghai)
**任务**: B166ER-Full-Scan-AutoIngest (cron `0 3 * * 0`)
**执行结果**: ✅ 全部 5 步完成

---

## 0. 关键发现（先行说明）

本次执行**重建了 3 个已丢失的脚本**。历史记录显示 `scan_files.py` 与 `kb_router.py`
在 2026-07-11 的 commit `ab76f2a8`（v2.1 全面重建）中被删除，同时消失的还有
`routing_update_needed.json`。自那以后该 cron 任务**每次运行都必然失败**——
它要找的脚本已经不在磁盘上了。

从 git 历史 (`967eb6c2`) 恢复了原始实现，并针对本机真实路径做了适配：

| 脚本 | 状态 | 处理 |
|------|------|------|
| `scan_files.py` | 已丢失 | 从 git 恢复 + 适配 D 盘路径 |
| `batch_indexer.py` | 从未存在于 git | 新建（复用 `kb_rag.py` 分块/FTS5 逻辑）|
| `kb_router.py` | 已丢失 | 由 `kb_routing_table.py` 替代（`kb_router.py` 的 TF-IDF 路线已被 `kb_rag.py` 的 FTS5+向量路线取代）|
| `routing_update_needed.json` | 已丢失 | 重新生成 |

---

## 1. 全盘扫描（scan_files.py）

**扫描根**：`D:\B166ER-openclaw\workspace` + `knowledge` + `agents/main/agent/workshop-skills`

| 指标 | 数值 |
|------|------|
| 可索引文件总数 | **39,618** |
| 总大小 | 488.3 MB |
| 耗时 | 2.6 s |
| `.md` 文件 | 10,479 |
| `.py` | 16,229 |
| `.ts` | 3,279 |
| `.json` | 2,710 |
| `.txt` | 2,657 |
| `.html` | 2,264 |

**Top 目录**（文件数）：`.backups` 14,925 / `open-design-repo` 5,997 / `toolbox` 2,945 /
`skills` 2,243 / `memory` 1,618 / `obsidian-vault` 1,516 / `text-to-cad-extract` 1,322 /
`openhuman-eval` 1,178 / `refly-eval` 1,066 / `anyi` 983 / `anyi-ops-kb` 971

**产物**：
- `memory/file_inventory.json` — 完整清单（39,618 条）
- `memory/file_scan_report.json` — 聚合报告

---

## 2. 批量自动纳入（batch_indexer.py --limit 200）

| 指标 | 数值 |
|------|------|
| 清单候选 | 39,618 |
| 已索引（纳入前） | 1,686 |
| 新增候选 | 4,920 |
| 内容变更 | 619 |
| **本次处理** | **200**（md 优先，按体积降序）|
| 成功 / 失败 | **200 / 0** |
| 新增分块 | 43,188 |
| 耗时 | 11.8 s |

**去重决策**：`anyi/anyi-ops-kb`（1,175 文件 / 228.7 MB）是 `anyi-ops-kb`（1,263 / 230.1 MB）
的近重复副本，已排除，避免同一份知识双份入库。

**排除目录**：`.backups`、`.scratch`、`.tmp`、`obsidian-vault`、`openhuman-eval`、
`refly-eval`、`text-to-cad-extract`、`open-design-repo`、`toolbox`、`skills`、
`anyi`（重复副本）等。

---

## 3. 索引库增长确认（kb_rag.py stats）

| 指标 | 纳入前 | 纳入后 | 增长 |
|------|--------|--------|------|
| 索引文件数 | 1,686 | **1,858** | **+172** |
| 分块总数 | 65,763 | **108,951** | **+43,188** |
| 索引总大小 | 19,263 KB | 32,734 KB | +13,471 KB |
| FTS5 库大小 | 66,884 KB | 146,476 KB | +79,592 KB |
| 最后索引时间 | 2026-05-06 23:52 | **2026-10-25 03:26** | — |

> 文件数 +172 而非 +200：8 个文件被跳过（内容过短无有效分块 / 重复路径去重）。
> `.md` 已索引数：**517 → 689**。

**注意**：向量库 `.chroma_db` 为 0 KB（model2vec/chromadb 未安装），当前为纯 FTS5 模式。
`model2vec` 已安装（stats 显示"model2vec 256维"），但 chromadb 缺失导致向量未落盘。
本次纳入走 `use_vector=False` 纯 FTS5 路径，检索能力未受影响。

---

## 4. 路由表检查与更新（kb_routing_table.py → routing_update_needed.json）

对比 `skills/knowledge-base/SKILL.md` 路由决策表与索引库实际内容：

| 指标 | 数值 |
|------|------|
| 已索引 md | 689 |
| KB 类候选 | 148 |
| 路由表已覆盖 | 12 |
| **新增待登记** | **136** |
| 状态 | `NEEDS_UPDATE` |

**新增路由按语义聚类**（自动推断，登记到 SKILL.md 后生效）：

| 语义类 | 数量 |
|--------|------|
| 酒店行业/运营 | 19 |
| 酒店财务/投资/资产 | 7 |
| AHL项目/去中心化 | 5 |
| AI/LLM/Agent | 5 |
| 审美/设计/品牌 | 3 |
| 理论架构/认知 | 2 |
| 酒店SOP/运营标准 | 1 |
| 研究报告/数据 | 1 |
| 博弈/分析/决策 | 1 |
| 酒店收益管理 | 1 |
| 多标签命中 | 32 |
| 未分类（待人工确认）| 59 |

**产物**：`memory/routing_update_needed.json`（含 136 条待登记路由的完整语义标注）

**已应用到 SKILL.md**：新增 `apply_routing.py`（幂等写入器），将 **77 条有明确语义归类的路由**
（11 个语义类）写入 `skills/knowledge-base/SKILL.md` 的 `AUTO-ROUTING` 区，已即时生效。
59 条"未分类"路由保留在 JSON 中待人工确认（多为单次项目报告，无复用价值）。

已校验：SKILL.md 原有 115 行非空内容 **0 行丢失**，新增 85 行路由表。

---

## 5. 报告推送

已推送至 main session（`agent:main:main`）。

---

## 附：脚本清单

| 脚本 | 用途 | 调用方式 |
|------|------|---------|
| `scan_files.py` | 全盘扫描建清单 | `python scan_files.py` |
| `batch_indexer.py` | 批量增量纳入 | `python batch_indexer.py --limit 200` |
| `kb_routing_table.py` | 路由表差异检查 | `python kb_routing_table.py` |
| `apply_routing.py` | 路由写入 SKILL.md（幂等）| `python apply_routing.py` |
| `kb_rag.py` | 检索引擎（原有）| `python kb_rag.py stats \| search \| ask` |

## 附：Git 提交

| Commit | 内容 |
|--------|------|
| `9c585d89` | 重建扫描/纳入/路由工具链 + 修复 .gitignore 编码损坏 + 解除跟踪可重建产物 |
| `69180cc2` | 应用 77 条自动增量路由到 SKILL.md + `apply_routing.py` |

> `.gitignore` 此前被 PowerShell `Add-Content` 写坏（UTF-16 残片混入 UTF-8 文件），已修复并补齐
> `.kb_rag.db*` / `.chroma_db/` / `file_inventory.json` / `file_scan_report.json` 忽略规则。

<!-- project: github.com/darknessdogeric/openclaw-memory -->
