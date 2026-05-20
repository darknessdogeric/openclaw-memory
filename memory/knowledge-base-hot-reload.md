# Knowledge Base Hot-Reload Index

> **目的**: 按需加载KB，避免全文加载浪费token。
> **用法**: 匹配情境 → 加载对应文件+偏移 → 获取所需章节。

## KB 分层 (HOT/WARM/COLD)

### 🔥 HOT — 每次会话相关（按需章节加载）
| KB | 文件 | 大小 | 核心章节 | 加载偏移 |
|----|------|------|---------|---------|
| 理论架构V2.2 | theoretical-framework-v2.md | ~40KB | Layer 0 调度树 + 反馈回路 | line 1-120 |
| 审美 | aesthetic-knowledge-base.md | 153.5KB | 品位决策清单 + 东方美学 | line 1-80 |
| 博弈论 | game-theory-decision-knowledge-base-v3.md | 68.9KB | 核心框架 + 决策清单 | line 1-60 |

### 🌡️ WARM — 项目/领域触发时加载
| KB | 文件 | 触发情境 |
|----|------|---------|
| 酒店全景V9.0 | hotel-industry-knowledge-base.md | 酒店运营/管理/咨询 |
| 多OTA运营V1 | multi-ota-operations-knowledge-base-v1.md | OTA/携程/美团/渠道管理 |
| 收益管理V5 | hotel-revenue-management-knowledge-base-v5.md | ADR/OCC/定价分析 |
| 创业融资V2 | startup-fundraising-knowledge-base-v2.md | 融资/BP/估值 |
| AHL V1 | ahl-knowledge-base-v1.md | AHL项目讨论 |
| 金融证券V2 | finance-securities-knowledge-base.md | 金融/证券分析 |
| AI/LLM V2 | ai-llm-knowledge-base-v2.md | AI技术选型/架构 |
| AI Agent生产 | ai-agent-production-knowledge-base-v1.md | Agent设计/部署 |
| 中美跨境 | china-us-cross-border-structure-v1.md | 跨境贸易/结构 |
| 量化交易V1 | quantitative-trading-knowledge-base-v1.md | 量化策略 |
| 研究报告标准 | research-report-standard-v1.md | 报告撰写 |
| 酒店AI应用 | hotel-ai-applications-knowledge-base.md | AI+酒店场景 |
| 酒店新媒体V2 | hotel-new-media-marketing-knowledge-base-v2.md | 营销/新媒体 |
| 酒店私域 | hotel-private-domain-membership-knowledge-base.md | 会员/私域运营 |
| 定价策略 | pricing-strategy-knowledge-base.md | 定价方法论 |
| 决策框架V1 | mental-models-decision-frameworks-v1.md | 决策辅助 |
| TOKEN经济 | token-economy-research.md | Token经济学 |

### ❄️ COLD — 极少使用/归档
| KB | 文件 | 备注 |
|----|------|------|
| 目标管理 | goal-management-knowledge-base.md | 偶尔触发 |
| 大乐透V3 | lottery-knowledge-base-v3.md | 特定指令触发 |

## 情境 → KB路由表

| 用户输入情境 | 加载KB | 章节 |
|-------------|--------|------|
| "分析竞争格局" | 博弈论V3 | 核心框架+纳什均衡 |
| "OTA/渠道运营" | 多OTA运营V1 + 收益管理V5 | 平台策略+渠道利润 |
| "评估酒店价值" | 酒店全景V9.0 + 收益管理V5 | 运营指标+RevPAR |
| "设计BP" | 创业融资V2 | 结构模板+估值方法 |
| "分析商业模式" | 决策框架V1 + 博弈论V3 | 商业模式画布+囚徒困境 |
| "AHL项目讨论" | AHL V1 + 创业融资V2 | 全部 |
| "审美/设计判断" | 审美KB | 决策清单+东方美学 |
| "定价策略" | 收益管理V5 + 定价策略 + 多OTA运营V1 | 定价方法论+竞品分析+渠道价差 |
| "写研究报告" | 研究报告标准 + 金融V2 | 结构+方法论 |
| "跨境贸易" | 中美跨境V1 | 结构+税务 |
| "AI技术架构" | AI/LLM V2 + AI Agent生产 | 架构选型+部署 |
| "量化策略" | 量化交易V1 | 全部 |
| "新媒体营销" | 酒店新媒体V2 | 渠道策略+内容 |
| "会员/私域" | 酒店私域 | 会员体系+私域工具 |
| "TOKEN经济学" | TOKEN经济 | 全部 |

## 加载规则

1. **HOT KB 默认只加载核心章节**（偏差≤120行），除非用户问题需要深入
2. **WARM KB 按需加载**（匹配到情境才加载）
3. **COLD KB 只在用户明确提及时加载**
4. **多KB加载时串行而非并行**（避免token爆炸）
5. **加载前先读KB第一段**（确认版本+结构）再决定读多少
