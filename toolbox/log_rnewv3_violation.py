"""R-NEW-V3 violation #5 log append to corrections.md"""
import os
import shutil

filepath = r'D:\B166ER-OpenClaw\workspace\.self-improving\corrections.md'

entry = r"""

---

## 2026-08-22 09:51 (R-NEW-V3 第 5 次违规)

**Issue**: memory/2026-08-22.md 被 clobber 从 ~30KB (主条目 10 节 + HB #3691/#3693/#3694) → 2380 bytes (仅 HB #3695)
**Context**: HB #3695 追加时使用 Python 脚本 `open(tmp, 'a') + os.replace(tmp, filepath)` 模式
**Root Cause**:
- `open(tmp, 'a')` 创建空临时文件 + seek 至末尾 + 写入新内容 (不含原文件内容)
- `os.replace(tmp, filepath)` 是原子替换 = **用新文件替换整个旧文件** = 原内容全部丢失
- 错误模式：以为 `'a'` 模式会"先读后追加"，实际是"创建后追加"，原内容从未进入 tmp

**R-NEW-V3 历次违规历史**:
1. 早期 HEARTBEAT.md write() clobber
2. R-NEW-V2 2026-08 HEARTBEAT.md clobber
3. R-NEW-V3 HB #2157-#2244 raw log clobber (Remove-Item 误操作)
4. R-NEW-V3 #4 (重复类型)
5. **本次 — 8/22 09:51 daily file os.replace + 'a' mode 误用**

**Lesson**:
- R-NEW-V3 已记录 4 次违规历史, 仍未根除同类问题 → 升级到 **R-NEW-V3.1**
- ❌ 禁止内联实现: `open(tmp, 'a') + os.replace` 模式
- ✅ 必须三步曲: `shutil.copy(filepath, tmp) + open(tmp, 'a') + os.replace` 或更安全: `open(filepath, 'a')` 原地追加
- ✅ 工具封装: 统一 `append_file_atomic(filepath, content)` 工具函数, 禁止内联
- 教训已记入 daily file CRITICAL RECOVERY NOTE header
- clobber 快照保留: `memory/2026-08-22.md.clobbered-20260822-0951` (2380 bytes)
- 完整恢复: 从 session cache (read() 输出) 重建主条目 + 4 个 HB entry

**Applied**: 1x → R-NEW-V3.1 升级草案待 R69 解除后提交

**Eric 通知**: R69 静音期 Day 30/30, 暂不打扰 Eric; 事故已记入 daily CRITICAL RECOVERY NOTE + corrections.md; R69 解除后必须汇报 + 提交 R-NEW-V3.1 草案
"""

# Use safe direct append (R-NEW-V3.1 compliant: no os.replace)
with open(filepath, 'a', encoding='utf-8') as f:
    f.write(entry)

print(f"[ok] appended R-NEW-V3 violation #5 to corrections.md")
print(f"[ok] size: {os.path.getsize(filepath)} bytes")