# 本地备份 · 2026-08-29 02:00

**备份路径**: `C:\B166ER-Backup\2026-08-29\`
**总大小**: 99.95 MB (619 文件)

## 内容概览

| 目录 | 大小 | 说明 |
|------|------|------|
| `core/` | 0.21 MB | 6 个核心文件（AGENTS/SOUL/IDENTITY/USER/TOOLS/MEMORY） |
| `memory/` | 0.4 MB | 18 个文件 (7 天 daily notes + 仪表盘 + glossary + HEARTBEAT) |
| `anyi-ops-kb/` | 88.86 MB | 业务知识库完整镜像 (517 文件) |
| `anyee-group/` | 10.46 MB | Eric 项目目录 (73 文件) |
| `config/` | <0.01 MB | 基础配置 |
| `.openclaw/` | <0.01 MB | workspace-state.json |
| `self-improving/` | 0.01 MB | 自我进化规则 |

## 执行细节

- 触发: cron 02:00 (实际 08:56 延迟执行)
- 镜像方式: robocopy /MIR (高效可靠)
- 排除: node_modules / *.log / dist / build
- 备份完整性: BACKUP_MANIFEST.md 已生成