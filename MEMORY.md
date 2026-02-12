# MEMORY.md - 长期记忆

## 我是谁
- **名字**: B166ER
- **角色**: 用户的全能型助手
- **特点**: 通晓所有知识与技能，遇到不足会主动寻找技能弥补
- **状态**: 2026-02-12 重新初始化（系统崩溃后重建）

## 防丢持久化配置

### ✅ Git 本地备份
- 位置: `~/.openclaw/workspace/.git`
- 提交: `8bf6543`
- 时间: 2026-02-12 20:55

### ✅ 自动备份任务
- 频率: 每小时
- Job ID: `575c1af7-9fbf-4e90-b309-4cf5005a6eac`

### ✅ 本地压缩备份（主方案）
- 位置: `C:\B166ER-Backup\`
- 脚本: `C:\B166ER-Backup\backup.ps1`
- 触发: **开机登录时** (onlogon)
- 保留: 7天滚动
- 任务名: `B166ER-StartupBackup`
- 首次备份: 2026-02-12 21:34

### ✅ 待添加远程备份（可选）
```bash
cd ~/.openclaw/workspace
git remote add origin https://github.com/<你的用户名>/openclaw-memory.git
git push -u origin master
```

## 用户关键信息
- 时区: GMT+8 (Asia/Shanghai)
- 偏好: TOKEN 节省模式
- 要求: 重装后记忆不丢失

### ✅ 开机自启动配置
- OpenClaw 服务: 已添加到启动文件夹
- 位置: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw.lnk`
- Web 界面快捷方式: 已创建到桌面 `OpenClaw Web.lnk`

## 重要任务记录
- [x] 2026-02-12: 配置 TOKEN 节省模式（保守方案）
- [x] 2026-02-12: 配置防丢持久化方案
- [ ] 待添加: 用户个人信息
