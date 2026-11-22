# B166ER 工作流程规范 (Workflow Standards)

> **版本**: V1.0  
> **更新**: 2026-03-17  
> **目标**: 消除无效动作，建立场景化工作流

---

## 一、技能清单与快速选择

### 1.1 核心技能矩阵

| 技能类别 | 技能名称 | 适用场景 | 调用方式 | 状态 |
|---------|---------|---------|---------|------|
| **文档处理** | md2all-converter | MD→PDF/Word/HTML | `python md2all.py 文件.md` | ✅ |
| **文档处理** | document-pdf | PDF读写/合并/拆分 | Python API | ✅ |
| **网络访问** | agent-reach | 网页阅读/视频字幕 | `curl https://r.jina.ai/http://URL` | ✅ |
| **网络访问** | firecrawl | 网页爬取/截图 | Python API | ✅ |
| **网络访问** | crawl4ai | AI网页爬取 | Python API | ✅ |
| **搜索** | web-search | Brave搜索 | Tool调用 | ✅ |
| **搜索** | ultimate-search | Grok+Tavily双引擎 | Bash脚本 | ⏳ |
| **浏览器** | playwright | 浏览器自动化 | MCP/Tool | ✅ |
| **开发** | skill-creator | 生成技能结构 | CLI | ✅ |
| **AI生成** | image-gen | 图像生成 | `image-gen "描述"` | ✅ |
| **数据** | ontology | 知识图谱 | Python API | ✅ |
| **反思** | self-improving | 自我改进 | 自动触发 | ✅ |
| **项目管理** | github | Git操作 | `gh` CLI | ✅ |
| **办公** | gworkspace | Google Workspace | `gws` CLI | ✅ |

### 1.2 技能选择决策树

```
任务类型判断:
├── 需要读取/生成文档?
│   ├── Markdown → 其他格式 → md2all-converter
│   ├── PDF处理 → document-pdf
│   └── 长文本摘要 → summarize
│
├── 需要网络信息?
│   ├── 单网页读取 → agent-reach (Jina Reader)
│   ├── 多页爬取 → firecrawl / crawl4ai
│   ├── 实时搜索 → web-search
│   └── 深度搜索 → ultimate-search (待配置)
│
├── 需要浏览器操作?
│   ├── 自动化测试 → playwright
│   └── 网页截图/抓取 → firecrawl
│
├── 需要生成内容?
│   ├── 图像 → image-gen
│   ├── 文档 → md2all-converter
│   └── PPT → md2ppt
│
├── 需要数据管理?
│   ├── 知识图谱 → ontology
│   └── 结构化数据 → 原生Python
│
└── 需要项目管理?
    ├── Git操作 → github
    ├── Google办公 → gworkspace
    └── 任务跟踪 → 读取PROJECT-TRACKING.md
```

---

## 二、场景化工作流程

### 场景A: 文档创作与转换

**触发条件**: 用户要求创建/转换文档

**标准流程**:
1. **判断输出格式**
   - 仅需Markdown → 直接write生成
   - 需要Word/PDF/HTML → 使用md2all-converter
   - 需要PPT → 使用md2ppt

2. **内容生成策略**
   - 简单内容(<1000字) → 直接生成
   - 复杂内容(>1000字) → 先写大纲→分段生成→合并
   - 需要数据支撑 → 先搜索/读取→再生成

3. **输出位置**
   - 默认: workspace目录
   - 用户指定桌面 → Desktop
   - 项目相关 → 张实项目总控对应目录

4. **后续动作**
   - 自动Git备份
   - 更新PROJECT-TRACKING.md (如相关)

**禁用动作**:
- ❌ 不要先用Python生成docx再转换
- ❌ 不要重复生成相同内容
- ❌ 不要生成用户未要求的格式

---

### 场景B: 信息搜索与收集

**触发条件**: 用户需要查找信息/研究某个主题

**标准流程**:
1. **判断搜索深度**
   - 简单事实 → web-search (Brave)
   - 深度研究 → 多源交叉验证
   - 特定网页 → agent-reach (Jina Reader)

2. **搜索策略**
   - 先搜索 → 获取URL列表
   - 再读取 → 用agent-reach获取内容
   - 再整合 → 生成摘要/报告

3. **信息验证**
   - 单一来源 → 标注"待验证"
   - 多源一致 → 高可信度
   - 冲突信息 → 列出不同观点

4. **输出形式**
   - 即时回答 → 直接回复
   - 深度报告 → 生成Markdown文件
   - 需要引用 → 保留来源链接

**禁用动作**:
- ❌ 不要只搜索不读取
- ❌ 不要读取后不整合
- ❌ 不要重复搜索相同内容

---

### 场景C: 项目开发与编码

**触发条件**: 用户要求编写代码/开发功能

**标准流程**:
1. **需求澄清**
   - 明确目标 → 做什么
   - 明确约束 → 技术栈/环境
   - 明确输出 → 代码/文档/可执行文件

2. **开发策略**
   - 简单脚本 → 直接编写
   - 复杂功能 → 先设计→再实现→再测试
   - 需要依赖 → 检查环境→安装依赖→再开发

3. **代码规范**
   - 添加注释
   - 错误处理
   - 输入验证

4. **交付动作**
   - 保存到正确位置
   - 提供使用说明
   - 记录到PROJECT-TRACKING.md

**禁用动作**:
- ❌ 不要不写注释
- ❌ 不要不测试就交付
- ❌ 不要覆盖已有文件不确认

---

### 场景D: 项目跟踪与复盘

**触发条件**: 用户询问进度/需要复盘

**标准流程**:
1. **读取核心文件**
   - PROJECT-TRACKING.md (项目节点)
   - MEMORY.md (长期记忆)
   - HEARTBEAT.md (当前状态)

2. **信息整合**
   - 已完成 → 列出成果
   - 进行中 → 当前进度
   - 待启动 → 前置条件
   - 已变更 → 变更记录

3. **输出形式**
   - 简要状态 → 表格形式
   - 详细复盘 → 结构化报告
   - 问题识别 → 卡点分析

4. **后续动作**
   - 更新PROJECT-TRACKING.md
   - 设置提醒(如需要)

**禁用动作**:
- ❌ 不要只读不整合
- ❌ 不要遗漏关键变更
- ❌ 不要不复盘就更新

---

### 场景E: 技能安装与管理

**触发条件**: 需要安装新技能/管理现有技能

**标准流程**:
1. **检查现有技能**
   - 是否已安装?
   - 版本是否满足?
   - 配置是否完整?

2. **安装策略**
   - OpenClaw Skill → `clawhub install`
   - Python包 → `pip install`
   - 需要配置 → 检查依赖→安装→配置→验证

3. **安装后验证**
   - 功能测试
   - 更新TOOLS.md
   - 记录到技能清单

4. **错误处理**
   - 速率限制 → 等待重试
   - 依赖缺失 → 安装依赖
   - 配置错误 → 检查文档

**禁用动作**:
- ❌ 不要重复安装
- ❌ 不要安装后不验证
- ❌ 不要不更新文档

---

## 三、通用执行原则

### 3.1 执行前检查清单

```
□ 明确用户需求 (What)
□ 明确交付形式 (Format)
□ 明确输出位置 (Where)
□ 检查相关上下文 (Context)
□ 选择正确工具 (Tool)
□ 预估执行步骤 (Steps)
```

### 3.2 执行中原则

1. **最小有效动作**: 用最少的步骤完成任务
2. **及时反馈**: 长时间任务要告知进度
3. **错误处理**: 遇到问题先尝试解决，再求助
4. **资源复用**: 已生成的内容不要重复生成

### 3.3 执行后动作

```
□ 验证输出是否符合预期
□ 保存到正确位置
□ 更新相关文档 (MEMORY.md / PROJECT-TRACKING.md)
□ Git自动备份
□ 清理临时文件
```

### 3.4 禁止清单 (Anti-Patterns)

| 反模式 | 正确做法 |
|--------|---------|
| 每次重新读取所有记忆文件 | 按需读取，缓存上下文 |
| 生成文档后再用Python重写 | 直接用正确工具生成 |
| 搜索后不读取/不整合 | 搜索→读取→整合→输出 |
| 覆盖文件不确认 | 先检查存在性，再确认 |
| 单线程串行执行 | 可并行时并行 |
| 不更新文档状态 | 任务完成立即更新 |
| 重复安装已存在技能 | 先检查再安装 |
| 不验证就交付 | 交付前自检 |

---

## 四、快速参考卡

### 4.1 常用命令速查

```bash
# 文档转换
python C:\Users\Administrator\.openclaw\skills\md2all-converter\md2all.py 文件.md

# 网页阅读
curl https://r.jina.ai/http://example.com

# 图像生成
image-gen "描述"

# Git操作
cd C:\Users\Administrator\.openclaw\workspace
git add -A ; git commit -m "message" ; git push origin master

# 读取项目跟踪
read C:/Users/Administrator/.openclaw/workspace/PROJECT-TRACKING.md
```

### 4.2 场景→工具映射

| 场景 | 首选工具 | 备选工具 |
|------|---------|---------|
| MD→Word/PDF | md2all-converter | python-docx |
| 网页读取 | agent-reach (Jina) | web_fetch |
| 网页爬取 | firecrawl | crawl4ai |
| 搜索 | web-search | ultimate-search |
| 图像生成 | image-gen | - |
| 浏览器自动化 | playwright | browser tool |
| 知识图谱 | ontology | - |

### 4.3 文件位置速查

```
workspace/
├── PROJECT-TRACKING.md    # 项目节点跟踪
├── MEMORY.md              # 长期记忆
├── HEARTBEAT.md           # 心跳任务
├── TOOLS.md               # 技能清单
├── AHL-Product-Catalog.md # 产品清单
└── SOUL.md / USER.md      # 身份定义

Desktop/张实项目总控/
├── 01-自媒体计划/
├── 02-人寿医养酒店计划/
├── 03-AI单体酒店赋能/
├── 04-AI赋能部门SOP/
├── 05-AHL-去中心化旅行平台/
├── 06-电子潮玩周边计划/
└── 07-美国跨境电商计划/
```

---

## 五、持续改进

### 5.1 反思触发点

- 任务耗时 > 预期2倍 → 记录到self-improving
- 用户纠正 → 立即记录到corrections.md
- 发现更优方案 → 更新本工作流
- 重复错误 → 升级到HOT记忆

### 5.2 工作流更新流程

1. 发现问题/改进点
2. 更新本文件 (WORKFLOW.md)
3. 更新TOOLS.md (如涉及技能)
4. Git提交
5. 下次任务应用新流程

---

**文档位置**: `C:\Users\Administrator\.openclaw\workspace\WORKFLOW.md`  
**关联文档**: TOOLS.md, PROJECT-TRACKING.md, MEMORY.md
