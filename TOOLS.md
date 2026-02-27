# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### 运行环境偏好

**终端选择**: Git Bash (非 PowerShell)
- 原因: 更好的 Linux 命令兼容性、一致的体验
- 避免: 直接在 PowerShell 中运行 OpenClaw 命令

---

### Tavily Search API
- API Key: `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`
- 免费额度: 1000次/月
- 备用方案: 额度用完时用 Kimi 大模型联网搜索
- 安装命令: `clawhub install tavily-search`

---

### Agent Reach (互联网能力)
- **版本**: 1.2.0
- **安装位置**: C:\Python314\Lib\site-packages
- **克隆位置**: C:\Users\Administrator\Downloads\agent-reach
- **功能**: 
  - 网页阅读: `curl https://r.jina.ai/http://URL`
  - YouTube/B站字幕: `yt-dlp --dump-json "URL"`
  - RSS解析: Python feedparser
  - Twitter/小红书: 需配置Cookie (待配置)
- **使用指南**: `docs/Agent_Reach_使用指南.md`

---

### Agent Reach - 社交媒体配置状态
- **Twitter/X**: 可配置 (需安装 xreach-cli)
- **小红书**: 需Docker (未安装)
- **抖音**: 可配置 (需安装 douyin-mcp-server)
- **配置指南**: `docs/Agent_Reach_社交媒体配置指南.md`
- **状态报告**: `docs/Agent_Reach_配置状态报告.md`

---

Add whatever helps you do your job. This is your cheat sheet.
