# OpenClaw Skills 定制化安装清单

> **来源**: https://github.com/clawdbot-ai/awesome-openclaw-skills-zh  
> **定制对象**: 酒店业AI创业者 / 张实  
> **生成时间**: 2026-02-27

---

## 🎯 为你精选的技能 (按优先级)

### 🔴 核心技能 (立即安装)

| 技能名称 | 安装命令 | 用途 |
|---------|----------|------|
| **邮件自动化** | `clawhub install email` | 自动处理商务邮件 |
| **日历管理** | `clawhub install calendar` | 管理会议和日程 |
| **Google Workspace** | `clawhub install gog` | Gmail/日历/文档 |
| **Microsoft 365** | `clawhub install mogcli` | Outlook/Teams |
| **Exa搜索** | `clawhub install exa-search` | AI语义搜索 |
| **Jina Reader** | `clawhub install jina-reader` | 网页内容提取 |
| **GitHub** | `clawhub install github` | 代码管理 |
| **第二大脑** | `clawhub install 1` | 知识管理 |

### 🟡 重要技能 (本周安装)

| 技能名称 | 安装命令 | 用途 |
|---------|----------|------|
| **Twitter/X** | `clawhub install twitter` | 社交媒体监控 |
| **LinkedIn** | `clawhub install linkedin` | B2B客户开发 |
| **小红书** | `clawhub install xiaohongshu` | 国内市场调研 |
| **抖音** | `clawhub install douyin` | 短视频分析 |
| **文件管理** | `clawhub install file-manager` | 文档自动化 |
| **系统监控** | `clawhub install system-monitor` | 服务器监控 |
| **FFmpeg** | `clawhub install ffmpeg-cli` | 视频处理 |
| **YouTube下载** | `clawhub install yt-dlp` | 视频学习 |

### 🟢 扩展技能 (按需安装)

| 类别 | 技能 | 用途 |
|------|------|------|
| **数据库** | PostgreSQL/MySQL/Redis | 数据存储 |
| **安全** | Bitwarden | 密码管理 |
| **DevOps** | Docker/Kubernetes | 部署管理 |
| **财务** | YNAB | 预算管理 |
| **健康** | Fitbit/Garmin | 健康追踪 |
| **效率** | Todoist | 任务管理 |

---

## 🚀 一键安装脚本

### 方法1: 批量安装 (推荐)

打开 PowerShell，运行：

```powershell
# 进入下载目录
cd C:\Users\Administrator\Downloads

# 执行安装脚本
.\install-awesome-skills.ps1
```

### 方法2: 单个安装

```powershell
# 核心技能
clawhub install email calendar gog mogcli github

# 搜索与信息
clawhub install exa-search jina-reader

# 社交媒体
clawhub install twitter linkedin xiaohongshu douyin

# 工具
clawhub install file-manager system-monitor ffmpeg-cli yt-dlp
```

### 方法3: 使用 clawhub 命令

```bash
# 列出所有可用技能
clawhub list

# 搜索技能
clawhub search email

# 安装技能
clawhub install [技能名]

# 更新技能
clawhub update [技能名]

# 卸载技能
clawhub remove [技能名]
```

---

## 📋 安装后配置

### 邮件管理 (email)
```bash
# 配置邮件账户
# 编辑: ~/.openclaw/skills/email/config.yaml
```

### Google Workspace (gog)
```bash
# OAuth登录
gog auth login
```

### Microsoft 365 (mogcli)
```bash
# OAuth登录
mogcli auth login
```

### Twitter/X (twitter)
```bash
# 配置Cookie
twitter configure
# 然后粘贴从Cookie-Editor导出的JSON
```

### 小红书 (xiaohongshu)
```bash
# 需要Docker运行MCP服务
xiaohongshu setup
```

---

## 💡 使用场景示例

### 场景1: 商务邮件自动化
```
你: "帮我起草一封给投资人的邮件，介绍HAL项目"
AI: 使用 email 技能生成专业邮件模板
```

### 场景2: 竞品监控
```
你: "监控Twitter上关于'直客通'的讨论"
AI: 使用 twitter + exa-search 技能抓取相关推文
```

### 场景3: 内容研究
```
你: "分析小红书上关于大理民宿的热门笔记"
AI: 使用 xiaohongshu + jina-reader 技能提取内容
```

### 场景4: 日程管理
```
你: "查看本周的会议安排"
AI: 使用 calendar 技能查询并汇总
```

### 场景5: 知识管理
```
你: "保存这个关于AI酒店的文章到我的知识库"
AI: 使用 1 (第二大脑) 技能存储和分类
```

---

## ⚙️ 自动化工作流建议

### 工作流1: 每日信息汇总
```yaml
时间: 每天早上8点
任务:
  - 检查邮件 (email)
  - 查看日程 (calendar)
  - 搜索行业新闻 (exa-search)
  - 汇总发送到微信/钉钉
```

### 工作流2: 竞品监控
```yaml
时间: 每小时
任务:
  - 搜索Twitter竞品动态 (twitter)
  - 搜索小红书行业热点 (xiaohongshu)
  - 检测到重要信息时发送通知
```

### 工作流3: 内容创作辅助
```yaml
触发: 需要创作内容时
任务:
  - 研究热门话题 (exa-search)
  - 收集素材 (jina-reader)
  - 生成初稿
  - 发布到社交媒体 (twitter/xiaohongshu)
```

---

## 🔧 故障排除

### 问题: 技能安装失败
**解决**: 检查网络连接，或稍后重试
```bash
clawhub install [技能名] --force
```

### 问题: 技能需要API Key
**解决**: 查看技能文档获取API Key
```bash
# 查看技能帮助
clawhub info [技能名]
```

### 问题: Cookie配置失败
**解决**: 使用Chrome Cookie-Editor重新导出
```bash
# 清除配置重新设置
clawhub configure [技能名] --reset
```

---

## 📚 相关文档

- **Awesome Skills列表**: https://github.com/clawdbot-ai/awesome-openclaw-skills-zh
- **OpenClaw官方**: https://clawdhub.com
- **技能文档**: 安装后使用 `clawhub info [技能名]` 查看

---

**生成时间**: 2026-02-27  
**B166ER 协助定制**
