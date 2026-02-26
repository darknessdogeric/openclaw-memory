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

Add whatever helps you do your job. This is your cheat sheet.
