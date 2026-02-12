# OpenClaw 技能安装记录与建议

> 记录日期: 2026-02-12  
> 记录人: B166ER  
> 明日复盘待办

---

## 一、今日已安装技能（6个）

| # | 技能名称 | 来源/路径 | 核心功能 | 适用场景 |
|---|---------|----------|----------|----------|
| 1 | **agent-council** | `skills/agent-council` | 创建自主AI代理和管理Discord频道的完整工具包 | HAL多Agent协作系统 |
| 2 | **agenticflow-skill** | `skills/agenticflow-skill` | 构建AI工作流、代理和劳动力系统的综合指南 | 民宿自动化流程设计 |
| 3 | **aisa-twitter-api** | `skills/aisa-twitter-api` | X/Twitter实时搜索，提取相关推文 | 监控酒店业趋势、竞品动态 |
| 4 | **document-pdf** | `.agents/skills/document-pdf` | PDF文档处理（提取、创建、合并等） | 商业计划书、合同处理 |
| 5 | **business-intelligence** | `.agents/skills/business-intelligence` | 商业智能、数据可视化、分析报告 | 收益管理、市场分析 |
| 6 | **secondbrain-note** | `.agents/skills/secondbrain-note` | 知识管理、笔记捕获、第二大脑构建 | 整合三大战略项目资料 |

---

## 二、安装失败的技能

| 技能名称 | 失败原因 | 后续建议 |
|---------|---------|----------|
| apple-hig | Skill not found（仓库不存在或更名） | 搜索替代iOS设计指南技能 |
| calendar-optimization | 仓库克隆超时（可能是私有仓库） | 尝试其他日程管理技能，如 `daily-planner` |

---

## 三、明日复盘要点

### 3.1 技能功能验证
- [ ] 测试 **agent-council** 的多Agent配置功能
- [ ] 验证 **agenticflow-skill** 的工作流设计流程
- [ ] 试用 **aisa-twitter-api** 搜索酒店业相关内容
- [ ] 用 **document-pdf** 处理一份现有PDF文件
- [ ] 用 **business-intelligence** 做一个简单的数据分析
- [ ] 用 **secondbrain-note** 创建一条测试笔记

### 3.2 与HAL项目结合规划
- 如何将 **agent-council** 用于HAL的"云(Yun)"和"影子(Shadow)"双Agent架构
- 用 **agenticflow-skill** 设计民宿预订的完整工作流
- **aisa-twitter-api** 监控关键词："大理民宿"、"酒店数字化"、"AI酒店"

### 3.3 可选安装技能（明日评估）

**高优先级（建议安装）**
| 技能类别 | 候选技能 | 用途 |
|---------|---------|------|
| 网页搜索/研究 | `web-search` / `tavily-search` | 深度市场调研 |
| 图像生成 | `image-generation` | 商业计划书配图 |
| 演示文稿 | `presentation` / `slides` | 融资路演PPT |
| 邮件管理 | `email` / `gmail` | 商务沟通 |

**中优先级（按需安装）**
| 技能类别 | 候选技能 | 用途 |
|---------|---------|------|
| 前端开发 | `react` / `vue` | 项目官网开发 |
| 设计工具 | `figma` / `ui-design` | App界面设计 |
| 视频制作 | `video-editing` | 项目宣传视频 |
| 社交媒体 | `linkedin` / `wechat` | 商务社交 |

---

## 四、技能使用安全提醒

根据 awesome-openclaw-skills 的官方警告：

1. **安装前检查**: 访问 ClawHub 查看 VirusTotal 安全扫描报告
2. **源码审查**: 对涉及敏感操作（支付、账号、数据）的技能，建议人工审查代码
3. **权限管理**: 技能运行时会获得完整Agent权限，谨慎授予网络/API访问权限
4. **已过滤类型**: 672个加密/区块链/金融技能已被官方过滤，建议保持警惕

---

## 五、快速参考：技能安装命令

```bash
# 使用 clawhub 安装（推荐）
npx clawhub install <skill-name> --force

# 使用 skills CLI 安装（完整路径）
npx skills add <owner/repo@skill> -y

# 搜索技能
npx skills find <关键词>

# 列出已安装
npx clawhub list
```

---

## 六、明日复核查验清单

- [ ] 6个已安装技能功能是否正常
- [ ] 是否有技能与现有工作流冲突
- [ ] 是否需要配置API Keys（如Twitter API）
- [ ] 是否需要安装额外的依赖
- [ ] 技能文档是否完整阅读
- [ ] 是否更新到主人知识库

---

**备注**: 主人已安装的 `proactive-agent-1-2-4` 和 `find-skills` 也已在工作区，明日一并复盘整合。

**下次安装建议**: 待明日复盘后，根据实际使用反馈再决定是否安装"可选技能清单"中的项目。
