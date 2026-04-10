# B166ER 技能激活方案
**创建**: 2026-04-06
**目标**: 充分发挥每个skill效能，避免闲置

---

## 一、技能盘点

### 1. 数据获取类 (8个)

| 技能 | 状态 | 使用频率 | 优化建议 |
|------|------|---------|---------|
| `data-acquisition` | ✅ 自动运行 | 每日2次 | 保持现状 |
| `ultimate-search` | ⚠️ 待激活 | 低 | 集成到数据采集 |
| `tavily-search` | ⚠️ 待激活 | 低 | 检查是否冗余 |
| `firecrawl-skill` | ⚠️ 待激活 | 低 | 集成到数据采集 |
| `scrapling-official` | ⚠️ 待激活 | 低 | 集成到数据采集 |
| `rss-reader` | ⚠️ 待激活 | 低 | 合并到data-acquisition |
| `web-search` | ⚠️ 待激活 | 低 | 合并到data-acquisition |
| `jina-reader` | ✅ 已用 | 中 | 保持现状 |

### 2. 知识管理类 (8个)

| 技能 | 状态 | 使用频率 | 优化建议 |
|------|------|---------|---------|
| `knowledge-base` | ✅ 已部署 | 待启用 | 尽快使用 |
| `openviking` | ✅ 运行中 | 待启用 | 尽快使用 |
| `txtai` | ✅ 已安装 | 待启用 | 尽快使用 |
| `scholar-skill` | ✅ 新安装 | 待启用 | 尽快使用 |
| `notebooklm` | ⚠️ 待激活 | 低 | 评估使用场景 |
| `secondbrain` | ⚠️ 待激活 | 低 | 评估是否需要 |
| `ontology` | ⚠️ 待激活 | 低 | 评估是否需要 |
| `memOS` | ❌ 已移除 | - | - |

### 3. 效率工具类 (10个)

| 技能 | 状态 | 使用频率 | 优化建议 |
|------|------|---------|---------|
| `proactive-agent-1-2-4` | ✅ 运行中 | 高 | 保持 |
| `self-improving` | ✅ 运行中 | 高 | 保持 |
| `cost-governor` | ✅ 已安装 | 待启用 | 尽快使用 |
| `relayplane` | ✅ 已安装 | 待启用 | 尽快使用 |
| `clawsec` | ✅ 已安装 | 低 | 提升使用频率 |
| `security-auditor` | ✅ 已安装 | 低 | 提升使用频率 |
| `evoclaw` | ✅ 已安装 | 低 | 提升使用频率 |
| `cli-anything` | ✅ 常用 | 高 | 保持 |
| `skill-creator` | ⚠️ 待激活 | 低 | 评估需求 |
| `automation-workflows` | ⚠️ 待激活 | 低 | 评估需求 |

### 4. 内容创作类 (15个)

| 技能 | 状态 | 使用频率 | 优化建议 |
|------|------|---------|---------|
| `md2wechat` | ✅ 已安装 | 待启用 | Eric需要时使用 |
| `md2ppt` | ✅ 已有 | 中 | 保持 |
| `ppt-deck-builder-pro` | ✅ 已有 | 中 | 保持 |
| `summarize` | ✅ 常用 | 高 | 保持 |
| `wewrite` | ⚠️ 待激活 | 低 | 评估需求 |
| `image-gen` | ⚠️ 待激活 | 低 | Eric需要时使用 |
| `vision-analysis` | ⚠️ 待激活 | 低 | Eric需要时使用 |
| `youtube` | ⚠️ 待激活 | 低 | 内容分析用 |
| `podcastfy` | ⚠️ 待激活 | 低 | Eric需要时使用 |
| `audiobook` | ⚠️ 待激活 | 低 | Eric需要时使用 |

### 5. 酒店行业类 (6个)

| 技能 | 状态 | 使用频率 | 优化建议 |
|------|------|---------|---------|
| `hotel-revenue-management` | ✅ 已有 | 中 | 保持 |
| `hotel-report` | ✅ 已有 | 中 | 保持 |
| `hotel-new-media` | ⚠️ 待激活 | 低 | 结合自媒体计划 |
| `hotel-private-domain` | ⚠️ 待激活 | 低 | 评估需求 |
| `business-intelligence` | ⚠️ 待激活 | 低 | Eric决策时用 |
| `price-comparison` | ⚠️ 待激活 | 低 | OTA价格监控 |

### 6. 其他工具类 (12个)

| 技能 | 状态 | 使用频率 | 优化建议 |
|------|------|---------|---------|
| `calendar` | ✅ 可用 | 低 | Eric授权后启用 |
| `email` | ✅ 可用 | 低 | Eric授权后启用 |
| `twitter` | ✅ 可用 | 低 | Eric授权后启用 |
| `xiaohongshu` | ✅ 可用 | 低 | Eric授权后启用 |
| `github` | ✅ 常用 | 高 | 保持 |
| `minimax-docx` | ✅ 常用 | 高 | 保持 |
| `minimax-pdf` | ✅ 常用 | 高 | 保持 |
| `minimax-xlsx` | ✅ 常用 | 高 | 保持 |
| `notion` | ⚠️ 待激活 | 低 | 评估需求 |
| `slack` | ⚠️ 待激活 | 低 | 评估需求 |
| `linkedin` | ⚠️ 待激活 | 低 | Eric授权后启用 |

---

## 二、激活优先级

### P0 - 立即激活（本周）

| 技能 | 激活方式 |
|------|---------|
| `knowledge-base` | 索引MEMORY.md和重要文件 |
| `openviking` | 添加Eric个人数据 |
| `txtai` | 测试向量检索 |
| `scholar-skill` | 学术研究用 |
| `cost-governor` | API成本追踪 |

### P1 - 本月激活

| 技能 | 激活方式 |
|------|---------|
| `relayplane` | 成本优化 |
| `evoclaw` | SOUL进化 |
| `hotel-new-media` | 结合自媒体计划 |
| `ultimate-search` | 集成到数据采集 |

### P2 - 择机激活

| 技能 | 触发条件 |
|------|---------|
| `image-gen` | Eric需要图片 |
| `youtube` | 视频分析 |
| `notion` | 协同需求 |
| `automation-workflows` | 批量任务需求 |

---

## 三、cron任务整合

### 当前任务（已优化）

| 任务 | 时间 | 状态 |
|------|------|------|
| 数据采集 | 8:00, 20:00 | ✅ |
| 技能扫描 | 30分钟 | ✅ |
| 每日报告 | 21:00 | ✅ |
| 知识库更新 | 每月28日 | ✅ |
| 竞品监控 | 每日 | ⏳ 待添加 |

### 待添加任务

| 任务 | 时间 | 说明 |
|------|------|------|
| 知识库索引更新 | 每周一 | 索引新文档 |
| 技能效能报告 | 每周一 | 使用情况 |
| OTA价格监控 | 每日 | 竞品数据 |

---

## 四、淘汰清单

以下技能建议淘汰（长期闲置且有替代）：

| 技能 | 原因 | 替代方案 |
|------|------|---------|
| `tavily-search` | 与ultimate-search冗余 | ultimate-search |
| `web-search` | 与jina-reader冗余 | jina-reader |
| `memOS` | 已移除 | OpenViking |
| `Scrapling` | 与firecrawl冗余 | firecrawl |

---

## 五、执行清单

### 本周执行

- [x] knowledge-base 索引 MEMORY.md ✅
- [x] knowledge-base 索引 USER.md ✅
- [x] knowledge-base 索引 SOUL.md ✅
- [x] knowledge-base 索引 IDENTITY.md ✅
- [x] knowledge-base 索引 HEARTBEAT.md ✅
- [x] knowledge-base 索引 user-knowledge-base.md ✅
- [x] knowledge-base 索引 ahl-knowledge-base-v1.md ✅
- [x] knowledge-base 索引 ota-operations-skill-v1.md ✅
- [x] knowledge-base 索引 hotel-revenue-management-knowledge-base-v3.md ✅
- [ ] openviking 添加Eric偏好数据
- [ ] txtai 测试向量检索
- [ ] cost-governor 配置API追踪
- [ ] relayplane 配置成本优化

### 本月执行

- [ ] 数据采集系统增加OTA价格监控
- [ ] scholar-skill 学术搜索测试
- [ ] hotel-new-media 评估自媒体计划需求
- [ ] 淘汰冗余技能

---

**原则**: 宁精勿多，持续使用才是正道
