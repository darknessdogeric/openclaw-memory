from pathlib import Path

path = Path('self-improving/corrections.md')
content = path.read_text(encoding='utf-8')

r16_entry = """

---

## 2026-07-16：daily-briefing 19 天断粮 R16 KB 白名单护城河

### 事件
- 2026-06-28 后 reports/daily-briefing 停止更新 18 天
- Eric 11:06 反馈后诊断：cron 7e149123 实际每天都在跑（token 用量、success record 完整），但产物落到 memory/world-intelligence（Eric 不可见入口）
- 同步发现 6/29-7/11 共 12 份 daily-briefing 内容不存在，报告跑了，但磁盘上的产物被回收

### 根因分析
- R11 清理规则嫌疑（但未直接验证），rules.md 当前没有 R11
- 也可能是 Windows 回收 / 早期清理脚本误伤 / Cron 中途 storage 异常
- root cause 未定位 = 下次还可能再发

### 修复
- 路径修复：cron 7e149123 prompt 切换主输出到 reports/daily-briefing
- 7/12-7/16 现有 5 份直接 copy 补完（无 token 消耗）
- 6/29-7/11 在 INDEX.md 顶部记录 gap 透明说明
- 新增 R16 规则：memory/_protected_paths.json 白名单外部化

### 教训
- 决策资产不等于短期缓存：KPI 类报告、预测、仪表板 都是不可重生成的状态锚点
- 清理脚本必须加载白名单（O(0) 一次成本，避免 19 天断粮）
- repair 加 prevent 必须配对：只修一处不写规则 = 临时修复，下次再发
- Eric 11:13 反馈"断掉的这几天是不是补一补"直接触发 R16 沉淀

### 验证
- cron 7e149123 明早 08:30 自动产出 reports/daily-briefing/2026-07-17.md
- 下周一（7/21）self-improve 周期校验 _protected_paths.json 未被覆盖
- R16 需 B166ER-researcher subagent 在下次 eval 验证 KB 完整性

事故已闭环 · R16 已写入 · 19 天教训已结构化避免再发
"""

if 'R16 KB 白名单护城河' not in content:
    path.write_text(content + r16_entry, encoding='utf-8')
    print('Appended R16 entry')
else:
    print('R16 already in corrections.md')

print('Final length:', len(path.read_text(encoding='utf-8')))
