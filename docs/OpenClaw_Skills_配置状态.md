# OpenClaw Skills 配置状态

> **更新时间**: 2026年2月27日 22:30

---

## ✅ 已配置技能 (7个)

| 技能 | 配置文件 | 状态 | 需要操作 |
|------|----------|------|----------|
| **email** | `~/.openclaw/skills/email/config.yaml` | 🟡 待配置 | 填写邮箱账号密码 |
| **calendar** | `~/.openclaw/skills/calendar/config.yaml` | 🟡 待配置 | 启用Google/Microsoft日历 |
| **github** | `~/.openclaw/skills/github/config.yaml` | 🟡 待配置 | 填写GitHub Token或运行gh auth login |
| **twitter** | `~/.openclaw/skills/twitter/config.yaml` | 🟡 待配置 | 粘贴Cookie |
| **web-search** | 无需配置 | ✅ 即用 | - |
| **jina-reader** | 无需配置 | ✅ 即用 | - |
| **second-brain** | 无需配置 | ✅ 即用 | - |

---

## 🔧 依赖安装状态

| 工具 | 状态 | 版本 | 用途 |
|------|------|------|------|
| **xreach-cli** | ✅ 已安装 | 0.3.0 | Twitter/X访问 |
| **gh CLI** | 🔄 安装中 | - | GitHub管理 |
| **Agent Reach** | ✅ 已安装 | 1.2.0 | 互联网能力 |
| **Docker** | ❌ 未安装 | - | 小红书/抖音 |

---

## 🚀 快速配置指南

### 1. GitHub (最简单)

**方式A: 使用gh CLI认证 (推荐)**
```bash
# 在终端运行
gh auth login
# 按提示完成浏览器授权
```

**方式B: 使用Token**
```bash
# 1. 访问 https://github.com/settings/tokens
# 2. 生成Personal Access Token
# 3. 编辑 ~/.openclaw/skills/github/config.yaml
# 4. 填写token和username
```

### 2. Email

```bash
# 编辑 ~/.openclaw/skills/email/config.yaml
# 填写:
# - imap.username: 你的邮箱
# - imap.password: App专用密码
# - smtp.username: 你的邮箱
# - smtp.password: App专用密码

# Gmail用户获取App密码:
# https://myaccount.google.com/apppasswords
```

### 3. Calendar

```bash
# 编辑 ~/.openclaw/skills/calendar/config.yaml
# 启用Google日历:
# google.enabled: true
# google.client_id: 你的Client ID
# google.client_secret: 你的Client Secret

# 获取OAuth凭证:
# https://console.cloud.google.com/apis/credentials
```

### 4. Twitter/X

```bash
# 1. Chrome登录Twitter (使用小号!)
# 2. 安装Cookie-Editor扩展
# 3. 导出JSON格式Cookie
# 4. 编辑 ~/.openclaw/skills/twitter/config.yaml
# 5. 粘贴到cookies字段
```

---

## 💡 使用示例

### 立即可用 (无需配置)

```bash
# Jina Reader - 读取任意网页
curl https://r.jina.ai/http://example.com

# Web Search - AI搜索
# (通过Exa API，无需配置)

# Second Brain - 本地知识管理
# (使用本地存储)
```

### 配置后可用

```bash
# GitHub
gh repo list
gh repo view owner/repo

# Twitter (xreach)
xreach search "关键词" --json
xreach tweet https://twitter.com/... --json

# Email (配置后)
# send_email(to, subject, body)
# read_inbox(limit=10)

# Calendar (配置后)
# list_events()
# create_event(title, start, end)
```

---

## 📁 相关文件

- **技能目录**: `C:\Users\Administrator\.openclaw\skills\`
- **测试脚本**: `C:\Users\Administrator\.openclaw\test-skills.sh`
- **使用文档**: 各技能目录下的 `SKILL.md`

---

**配置完成时间**: 2026-02-27 22:30  
**B166ER 协助配置**
