# OpenClaw Workspace Backup - 恢复指南

## 快速恢复步骤

1. **安装 OpenClaw**
   ```bash
   npm install -g openclaw
   ```

2. **克隆工作区**
   ```bash
   git clone <你的仓库地址> ~/.openclaw/workspace
   ```

3. **恢复配置**
   ```bash
   openclaw setup
   ```

4. **验证记忆**
   - 检查 `memory/` 目录
   - 检查 `MEMORY.md`

---

## 自动备份配置

备份包括：
- ✅ 所有记忆文件 (memory/*.md)
- ✅ 身份配置 (IDENTITY.md, SOUL.md, USER.md)
- ✅ 工具和技能配置 (TOOLS.md, skills/)
- ❌ 敏感凭证 (自动排除)

---

## 上次备份
- 时间: 自动维护
- 状态: 见 git log
