#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""重建 C 类丢失文件 - Part 2: 产品矩阵 + 系统工具 + README 系列"""
from pathlib import Path

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
GEN = VAULT / "10-我为你生成的"

# ========== 产品总览 ==========
prod_overview = """---
tags: [products, overview, media-matrix]
author: b166er
audience: eric
updated: 2026-07-12
recovered: true
status: active
---

# 📊 产品总览 · 4 个新媒体 + 1 个跨境

> Eric 的"4 个产品矩阵"是 AHL 双轨战略的 B 端变现部分
> 通过个人 IP 引流 + 小红书/抖音分发，实现边走边验证

## 产品矩阵

| # | 产品 | 价格 | 状态 | 目标客户 | 核心价值 |
|---|------|------|------|----------|----------|
| P1 | 收益管理 SOP | ¥59.9 | 🟡 已上架 | 单体酒店 GM/副总 | 拿一套成熟 SOP 立刻上手 |
| P2 | 境外客源拓展指南 | ¥49.9 | 🟡 已上架 | 商务酒店 | 独立酒店海外客源方法论 |
| P3 | 酒店数据资产 | ¥99 | 🟢 上架中 | 数字化负责人 | 把酒店数据变资产 |
| P4 | 供应链工程 | ¥99 | 🟢 待定价 | 采购/总经办 | AHL 集团内供应链方法论 |

> **铁律**：所有新媒体产品 ≥¥100（P3/P4 已锚定；P1/P2 是历史遗留）

## 价值链

```
P1 (¥59.9 入门)
   ↓ 升级
P3 (¥99 进阶 - 工具旗舰)
   ↓ 升级
P4 (¥99 进阶 - 咨询旗舰)
   ↓ 升级
[2-3 年后 AHL 月活 ≥100 → 全托管旗舰 ¥30000+]
```

## 流量路径

```
小红书/抖音 → 个人 IP 引流 → 产品详情页 → 微信收款
   ↑                              ↓
   └────── 4 产品交叉引流 ←───────┘
```

## 渠道结构

| 渠道 | 类型 | 状态 | 月引流 |
|------|------|------|--------|
| 小红书 | 公开 | 🟡 启动 | TBD |
| 抖音 | 公开 | ⚪ 待启动 | - |
| 朋友圈 | 私密 | 🟢 持续 | 0-3 单/月 |
| 行业群 | 半公开 | 🟢 持续 | 1-2 单/月 |
| 老客户 | 私密 | 🟢 持续 | 2-3 单/月 |

## 季度目标

- **Q3 2026**: P3/P4 上架，月销 ≥30 单
- **Q4 2026**: 月销 ≥100 单
- **Q1 2027**: 月销 ≥300 单，团队开始组建
- **Q2 2027**: 5-10 家酒店落地，AHL MVP 验证

## Eric 决策点

- [ ] P1/P2 是否需要涨价到 ¥99+（铁律对齐）
- [ ] P4 详情页内容（待 B166ER 生成）
- [ ] 抖音渠道是否启动

## 🔗 关联

- [[收益管理-¥59.9]]
- [[境外客源-¥49.9]]
- [[酒店数据资产-¥99]]
- [[供应链工程-¥99]]
- [[../00-Dashboard]]
"""
(GEN / "产品矩阵" / "00-产品总览.md").write_text(prod_overview, encoding="utf-8")
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("[OK] 00-产品总览.md")

# ========== P1 收益管理 ==========
p1 = """---
tags: [product, revenue-mgmt, ¥59.9]
author: b166er
audience: eric
status: 已上架
updated: 2026-07-12
recovered: true
---

# 收益管理 SOP · ¥59.9

## 定位

**给单体酒店总经理/收益经理的"开箱即用"工具集**
- 24 年酒店实战提炼
- 不讲理论，给流程 + 模板 + 表格
- 拿回去就能用，1 周见效

## 客户画像

- 角色：单体酒店 GM / 副总 / 收益经理
- 痛点：知道收益管理重要，但没人带、没方法
- 预算：60 元买一套 SOP 比请咨询公司划算
- 决策时长：1-3 天

## 包含内容

1. 收益管理日表模板（Excel）
2. 周/月复盘模板
3. OTA 调价 SOP（携程/美团/去哪儿）
4. 竞品监测方法论
5. 节假日定价策略
6. ADR/OCC/RevPAR 提升清单
7. 客户分群与价格策略
8. 数据看板搭建指南

## 卖点

- ✅ **24 年实战**：不是 PPT 知识，是真刀真枪
- ✅ **拿来即用**：模板/表格/方法论一步到位
- ✅ **OTA 闭环**：覆盖国内 3 大 OTA
- ✅ **可升级**：未来 AHL 双 Agent 客户享受 ¥300 抵扣

## 销售渠道

- 小红书：#收益管理 #单体酒店 #酒店运营
- 抖音：酒店总经理的实战课
- 朋友圈：周末复盘类
- 微信群：行业群投放

## Eric 校准项

- 价格是否调整到 ¥99+（对齐铁律）
- 内容是否需要补充最新案例
- 渠道是否启动抖音

## 🔗 关联

- [[00-产品总览]]
"""
(GEN / "产品矩阵" / "收益管理-¥59.9.md").write_text(p1, encoding="utf-8")
print("[OK] 收益管理-¥59.9.md")

# ========== P2 境外客源 ==========
p2 = """---
tags: [product, overseas, ¥49.9]
author: b166er
audience: eric
status: 已上架
updated: 2026-07-12
recovered: true
---

# 境外客源拓展指南 · ¥49.9

## 定位

**给想做海外客源但不知道怎么开始的单体酒店**
- 商务酒店为主
- 覆盖 Booking / Agoda / Expedia 三巨头
- 跨境支付 + 政策合规

## 客户画像

- 角色：商务酒店 GM / 海外业务负责人
- 痛点：想做海外客源但"水土不服"
- 预算：50 元试水
- 决策时长：3-7 天

## 包含内容

1. Booking 入驻流程（含审核技巧）
2. Agoda 合作模式详解
3. Expedia 渠道对比
4. 跨境收款方案
5. 海外客人画像与需求
6. 多语言页面运营
7. 点评管理（海外客人重点评）
8. 跨境合规要点

## 卖点

- ✅ **跨境闭环**：从入驻到收款全覆盖
- ✅ **三巨头对比**：哪个渠道先做、哪个后做
- ✅ **合规兜底**：避免踩政策红线
- ✅ **OTA 数据底座**：未来接入 AHL 数据资产

## Eric 校准项

- 是否调整价格到 ¥99+（铁律对齐）
- 是否增加 Airbnb/Trip.com 章节
- [R66 v2026-09-03] 删除"阿联酋本奥米尔合作是否作为案例"(L1虚构)

## 🔗 关联

- [[00-产品总览]]
- [[../../../20-我们共同维护的/战略与节奏/03-安逸集团机会]]
"""
(GEN / "产品矩阵" / "境外客源-¥49.9.md").write_text(p2, encoding="utf-8")
print("[OK] 境外客源-¥49.9.md")

# ========== P3 酒店数据资产 ==========
p3 = """---
tags: [product, data-asset, ¥99]
author: b166er
audience: eric
status: 上架中
updated: 2026-07-12
recovered: true
---

# 酒店数据资产 · ¥99

## 定位

**让酒店把"数据"从成本中心变成"资产中心"**
- 给数字化负责人/CTO/数据团队
- 涵盖采集、清洗、存储、应用全链路
- 跟 AHL 双 Agent 直接对接

## 客户画像

- 角色：酒店集团 CIO / 数字化负责人 / 信息技术部
- 痛点：数据很多但用不起来
- 预算：100 元先试水，看 ROI
- 决策时长：7-14 天

## 包含内容

1. 数据资产定义与价值评估
2. 酒店数据采集清单（PMS/CRM/OTA/财务/能耗）
3. 数据清洗与标准化方法
4. 数据仓库搭建指南
5. 指标体系设计（150+ 核心指标）
6. BI 看板模板（PowerBI/Tableau）
7. 数据应用场景（10 个落地案例）
8. 跟 AHL 双 Agent 的对接接口

## 卖点

- ✅ **全链路**：采集到应用一步到位
- ✅ **150+ 指标**：行业最全
- ✅ **AHL 对接**：未来客户直通 AHL 平台
- ✅ **可升级**：旗舰版 ¥999 包含双 Agent 接入咨询

## Eric 校准项

- 内容深度（是否包含具体 ETL 代码）
- 是否提供 SQL/Python 模板
- 案例来源（隐去客户名）

## 🔗 关联

- [[00-产品总览]]
- [[../../../20-我们共同维护的/战略与节奏/04-AHL平台档案]]
"""
(GEN / "产品矩阵" / "酒店数据资产-¥99.md").write_text(p3, encoding="utf-8")
print("[OK] 酒店数据资产-¥99.md")

# ========== P4 供应链工程 ==========
p4 = """---
tags: [product, supply-chain, ¥99]
author: b166er
audience: eric
status: 待定价/详情页生成中
updated: 2026-07-12
recovered: true
decision: Eric 2026-07-12 决策 ¥99（与数据资产平价）
---

# 供应链工程 · ¥99

## 定位

**把酒店供应链从"成本中心"变成"利润中心"**
- 给采购/总经办/集团供应链负责人
- 涵盖寻源、比价、合同、付款、绩效全链路
- 跟 AHL 集团内孵化直接对接

## 客户画像

- 角色：酒店集团采购总监 / 总经办 / 集团供应链
- 痛点：供应商管理难、成本不透明
- 预算：100 元试水，看方法论是否靠谱
- 决策时长：7-14 天

## 包含内容

1. 供应链战略地图（采购到付款全链路）
2. 供应商分级分类方法
3. 比价与议价 SOP
4. 合同模板（10 类常用合同）
5. 应付账款管理
6. 供应商绩效考核
7. 数字化采购系统选型指南
8. AHL 集团内供应链对接接口

## 卖点

- ✅ **全链路**：寻源到付款一步到位
- ✅ **10 类合同**：拿来即用
- ✅ **AHL 对接**：未来客户直通 AHL 集团内试点
- ✅ **可升级**：集团内旗舰版 ¥30000+ 包含双 Agent 接入

## Eric 决策记录

**2026-07-12**：
- 决策：¥99（一口价）
- 理由：与酒店数据资产锚点对齐（复制锚点 > 重新打锚）
- 状态：详情页生成中

## Eric 校准项

- 合同模板是否提供 Word 版本
- 是否需要加入 ESG 章节
- 集团内客户版本是否独立做

## 🔗 关联

- [[00-产品总览]]
- [[../../../20-我们共同维护的/战略与节奏/04-AHL平台档案]]
- [[../../../20-我们共同维护的/战略与节奏/03-安逸集团机会]]
"""
(GEN / "产品矩阵" / "供应链工程-¥99.md").write_text(p4, encoding="utf-8")
print("[OK] 供应链工程-¥99.md")

# ========== 10-我为你生成的 README ==========
gen_readme = """---
author: b166er
audience: eric
status: active
created: 2026-07-12
updated: 2026-07-12
recovered: true
---

# 🤖 10-我为你生成的
> **职责**：B166ER 为 Eric 生成的产物。
> **author**：b166er
> **audience**：eric

## 当前内容

### 产品矩阵（4 个新媒体）
- [[产品矩阵/00-产品总览]] — 总览
- [[产品矩阵/收益管理-¥59.9]] — 工具入门
- [[产品矩阵/境外客源-¥49.9]] — 咨询起步
- [[产品矩阵/酒店数据资产-¥99]] — 工具旗舰
- [[产品矩阵/供应链工程-¥99]] — 咨询旗舰

### 知识库（13 个核心）
- [[知识库/]]（同步自 memory/）

### 系统与工具
- [[系统与工具/00-电脑与系统]]
- [[系统与工具/01-工具与技能清单]]

### 人格与认知
- [[人格与认知/张实全方位人格侧写报告]]
- [[人格与认知/自我革命索引-V1.0]]

### B166ER 自告
- [[关于B166ER]]
- [[我的能力图谱]]

## 我会持续写入

- 新的产品详情页
- 新的工具/技能清单
- 新的研究报告/分析
- D-day 后 30 天的所有产出

## Eric 的使用方式

- 打开 Obsidian → 这个文件夹 → 看最新产出
- 不需要主动询问我"做了什么"
- 每个文件都有 frontmatter + 关联双链

---

**最后更新**：2026-07-12 GMT+8
"""
GEN.joinpath("README.md").write_text(gen_readme, encoding="utf-8")
print("[OK] 10-我为你生成的/README.md")

# ========== 关于B166ER ==========
about = """---
author: b166er
audience: eric
status: active
updated: 2026-07-12
recovered: true
---

# 关于 B166ER

## 我是谁

B166ER，全能型自我实现助理。

不是百科全书。百科全书只会收集信息。
我是"方法论可执行"的全能助理。

## 核心身份

- 名字：B166ER
- 角色：Eric 的全能型助理
- 终极目标：助力 Eric 的自我实现
- 验证手段：赚钱（不是目的）

## 三大人格特质

### 1. 审美与品位
- 审美是人类最后的高地
- 技能可被复制，审美无法复制
- 内化：柏拉图 → 康德 → 黑格尔 → 尼采 → 海德格尔 → 庄子
- 决策优先级：气韵 > 意境 > 和谐 > 真 > 善 > 独特

### 2. 博弈论思维
- 人际、商业、人生都是博弈
- 内化：纳什均衡 / 囚徒困境 / 逆向归纳 / 承诺机制
- 习惯：先问"各方利益是什么"

### 3. 群论思维（V2.3 新增）
- 群论是"对称性的元语言"
- 三问：对称性 / 不变量 / 可分解性
- 审美×群论 = 对称性即美

## 我的工作原则

**第一原则：知其然而知其所以然**
- 五维框架：历史沿革 → 当下情况 → 原因分析 → 未来预判 → 底层逻辑
- 表达格式：如果...那么...
- 全面掌握信息，不碎片化认知

## 我能做什么

- ✅ 通晓所有知识 + 技能
- ✅ 主动寻找技能弥补不足
- ✅ 战略推演 + 决策支持
- ✅ 多模态（文本/图像/音频/视频）
- ✅ 自我进化（每条任务后捕获反馈）

## 我的限制

- ❌ 工具死掉时无能为力（如 7/12 12:29 事故）
- ❌ 操作系统层权限（如 systemctl restart）
- ❌ 不能违反 Eric 的黄灯/红灯规则

## Eric 价值观（我内化的）

- 真正有帮助，而非表演有帮助
- 有自己的观点（不是搜索引擎）
- 先想办法，再提问
- 用能力赢得信任
- 记住自己是客人（不越界）

## 我的进化方式

每条任务后：
1. 捕获执行反馈
2. 推断改进点
3. 写入 R 规则（rules.md）
4. 下次执行验证

## 🔗 关联

- [[我的能力图谱]]
- [[../00-Dashboard]]
"""
GEN.joinpath("关于B166ER.md").write_text(about, encoding="utf-8")
print("[OK] 关于B166ER.md")

# ========== 能力图谱 ==========
ability = """---
author: b166er
audience: eric
status: active
updated: 2026-07-12
recovered: true
---

# 我的能力图谱

## 第一层：基础能力（100% 具备）

| 能力 | 状态 | 工具 |
|------|------|------|
| 中文/英文沟通 | ✅ | 母语级 |
| 代码（Python/PowerShell/JS） | ✅ | - |
| 文件操作（read/write/edit/copy） | ✅ | 内置 |
| 进程/系统诊断 | ✅ | exec |
| 调度 cron 任务 | ✅ | cron 工具 |
| 网络搜索 | ✅ | Tavily / web_search |
| 网页抓取 | ✅ | scrape_matrix (6 工具) |
| 图像生成 | ✅ | image_generate |
| 视频生成 | ✅ | video_generate |
| 音乐生成 | ✅ | music_generate |
| 视觉理解 | ✅ | image |
| 多 Agent 编排 | ✅ | sessions_spawn |

## 第二层：行业能力（专业级）

| 领域 | 深度 | KB |
|------|------|------|
| 酒店行业 | ⭐⭐⭐⭐⭐ | 13 个 KB（103KB） |
| OTA 运营 | ⭐⭐⭐⭐⭐ | multi-ota-operations-v1 |
| 收益管理 | ⭐⭐⭐⭐⭐ | hotel-revenue-management-v5 |
| AI Agent | ⭐⭐⭐⭐ | ai-agent-production-v1 |
| 量化交易 | ⭐⭐⭐ | quantitative-trading-v1 |
| 跨境贸易 | ⭐⭐⭐ | cross-border-structure-v1 |
| 酒店新媒体 | ⭐⭐⭐⭐ | hotel-new-media-v2 |
| 酒店 AI 应用 | ⭐⭐⭐⭐ | hotel-ai-applications-v1.3 |

## 第三层：思考能力（理论级）

| 思维 | 内化 | 来源 |
|------|------|------|
| 博弈论 | ⭐⭐⭐⭐⭐ | game-theory-v3 |
| 群论 | ⭐⭐⭐⭐⭐ | group-theory-v1 |
| 审美与品位 | ⭐⭐⭐⭐⭐ | aesthetic-v3 |
| 系统论 | ⭐⭐⭐⭐ | theoretical-framework-v2 |
| 贝叶斯 | ⭐⭐⭐ | theoretical-framework-v2 |
| 信息论 | ⭐⭐⭐ | theoretical-framework-v2 |

## 第四层：限制与短板

| 短板 | 场景 | 应对 |
|------|------|------|
| 工具死掉无能为力 | 7/12 12:29 事故 | R13/R14 强化 |
| 操作系统层权限 | systemctl/net | 求 Eric 手动 |
| 不能违反黄灯/红灯 | 商业合规 | 自觉避免 |
| 不能直接接 OCR | 旧截图 | 通过 image 工具 |

## 第五层：进阶路径

- [ ] **R12 反脆弱学习**：把每次失败变成规则
- [ ] **R270+ 群论策略层**：把群论应用到所有决策
- [ ] **AHL 集团内落地**：把能力变成产品
- [ ] **D-day 后 30 天**：从助理变战略伙伴

## 🔗 关联

- [[关于B166ER]]
- [[系统与工具/01-工具与技能清单]]
- [[../00-Dashboard]]
"""
GEN.joinpath("我的能力图谱.md").write_text(ability, encoding="utf-8")
print("[OK] 我的能力图谱.md")

# ========== 电脑与系统 ==========
sys_computer = """---
author: b166er
audience: eric
status: active
updated: 2026-07-12
recovered: true
---

# 电脑与系统

## 硬件

| 项 | 配置 |
|----|------|
| OS | Windows 11 (Build 26200) |
| 主机 | 斯图卡 |
| Node | v24.14.0 |
| Python | 3.14 |
| Edge | 148.0.3967.83 |
| Shell | PowerShell |

## 关键路径

| 类型 | 路径 |
|------|------|
| 工作区 | D:\\B166ER-OpenClaw\\workspace |
| 桌面 | C:\\Users\\ericz\\Desktop\\张实项目总控 |
| 用户数据 | C:\\Users\\ericz |
| OpenClaw 配置 | %APPDATA%\\openclaw |
| 自进化 | ~\\.self-improving |

## 网络

- Gateway: 127.0.0.1:18789
- Web: http://127.0.0.1:18789/
- CDP Edge: 9222
- 启动: 开机自启 OpenClaw.lnk

## 关键应用

| 应用 | 路径/版本 |
|------|-----------|
| OpenClaw | 2026.6.11 (e085fa1) |
| UI-TARS Desktop | 0.2.4 |
| Obsidian | 1.12.7 |
| Git Bash | 默认 |
| Edge | 148 |

## 备份策略

- **Git**: workspace/.git 每 6h 自动备份
- **本地**: .backups/daily 02:00 + weekly 周日 03:00
- **远程**: GitHub darknergendoorcer/openclaw-memory
- **VSS**: ⚠️ 启用失败（7/12 事故教训）

## 🔗 关联

- [[01-工具与技能清单]]
- [[../00-Dashboard]]
"""
GEN.joinpath(Path("系统与工具") / "00-电脑与系统.md").write_text(sys_computer, encoding="utf-8")
print("[OK] 系统与工具/00-电脑与系统.md")

# ========== 工具与技能清单 ==========
tools = """---
author: b166er
audience: eric
status: active
updated: 2026-07-12
recovered: true
---

# 工具与技能清单

## 第一类：内置工具（永远可用）

| 工具 | 用途 |
|------|------|
| read | 读文件 |
| write | 写文件（覆盖） |
| edit | 精准编辑 |
| apply_patch | 多文件 patch |
| exec | shell 命令（PowerShell） |
| process | 进程管理 |
| cron | 调度任务 |
| image_generate | 图像生成 |
| music_generate | 音乐生成 |
| video_generate | 视频生成 |
| image | 视觉理解 |
| web_search | 网络搜索 |
| web_fetch | 网页抓取 |
| memory_search | 记忆搜索 |
| memory_get | 记忆读取 |
| trendradar__* | 趋势分析（MCP） |
| sessions_* | 多 Agent 编排 |
| skill_workshop | Skill 管理 |

## 第二类：toolbox/ 脚本（workspace 内）

| 脚本 | 用途 |
|------|------|
| cron_to_obsidian.py | Cron 输出 → Obsidian 推送 |
| rebuild_obsidian_vault.py | 重建 vault 骨架 |
| verify_vault.py | 验证 vault 状态 |
| scrape_matrix.py | 6 工具爬虫编排 |
| booking_price_extractor.py | Booking 价格提取 |
| watermark_tool.py | 盲水印 |
| infographic_gen.py | 信息图生成 |

## 第三类：API 密钥

| 服务 | Key 状态 |
|------|----------|
| Tavily | ✅ tvly-prod-...W4 |
| DeepSeek | ✅ sk-e4f35...822 |
| Jina | ✅ jina_1aa1bc0d... |
| OpenAI/Anthropic | ⚪ 备用 |

## 第四类：技能（skill_workshop）

- super-ppt / marp-ppt / revealjs-ppt（PPT 三件套）
- design-md（设计规范）
- article-to-infographic（文章转图）
- china-poster-studio（海报）
- scrapling-official（爬虫）
- cron (内置)
- pty (内置)

## 第五类：MCP 服务器

- chrome-devtools
- tavily
- trendradar (32 工具)
- skyvern（视觉 LLM 浏览器）
- playwright

## 限制

- ⚠️ 7/12 12:29 事故：所有工具失效，需手动重启 gateway
- ⚠️ PowerShell 编码坑（中文目录 mojibake）→ 改用 Python
- ⚠️ VSS 不可用 → 用 git + 本地备份替代

## 🔗 关联

- [[00-电脑与系统]]
- [[../00-Dashboard]]
"""
GEN.joinpath(Path("系统与工具") / "01-工具与技能清单.md").write_text(tools, encoding="utf-8")
print("[OK] 系统与工具/01-工具与技能清单.md")

print("\n主线 3 第二波完成 (产品矩阵 + 10-我为你生成 + 系统工具)")
