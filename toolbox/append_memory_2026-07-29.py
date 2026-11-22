# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r'D:\B166ER-OpenClaw\workspace\memory\2026-07-29.md')
text = """

## 🌀 21:30 涌现整理 (Cron-PUSH-Emergence)

### 关键发现 · 推送路径断裂 7 天
- **根因**: 7-22 B166ER 改 `cron_to_obsidian.py` PUSH_BASE 从 `00-Inbox-待整理/cron-push/YYYY-MM-DD/` → `50-外部接入/cron-outputs/YYYY-MM/`，但 `emergence_curator.py` 未跟随
- **影响**: 7-22 起 emergence/daily/*.md 静默 7 天（7-23~7-27 完全空白，7-28 由 hourly 涌现报告补救但不完整）
- **Eric 7-27 反馈** (过去 30 天推送全没了) 复发但根因无人察觉

### 修复动作
1. ✅ `emergence_curator.py` 改为双路径 fallback (新路径按 mtime 过滤当天 + 旧路径按目录)
2. ✅ 补做 7-22 ~ 7-29 共 7 天 MOC (49 条推送找回)
3. ✅ 7 天 MOC 全部推送到 cron-outputs (importance=high)
4. ✅ 7-29 MOC 报送到 Eric 日报面板

### 教训
- 路径变更要走两侧同步原则: 源头 (cron_to_obsidian.py) 改了，下游所有读侧 (emergence_curator / vault_index / vault_search) 必须同步审
- 7-22 改路径时只 update 了产出端和 changelog，**没有更新所有消费端** → 静默 7 天
- 这类管道断裂但脚本不报错是最难发现的 bug 类型
- 下次类似修改必须: 列出 vault 中所有引用旧路径的位置 → 全部同步

### 涌现日报
- 7-29: 6 条推送 (3 高 / 3 常), 重点 全球情报简报 + 深度自检上午 + 深度自检晚间
- 7-22~7-28 历史回填: 49 条推送全部 MOC 化
- 推送管道健康, 后续 21:30 涌现整理恢复正常
"""
with p.open('a', encoding='utf-8') as f:
    f.write(text)
print('ok, written', len(text), 'chars')
