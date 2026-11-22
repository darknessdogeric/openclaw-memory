"""
R-NEW-V2 compliant HEARTBEAT.md append for HB #1825
Explicit utf-8 read+append+write per post-7/15+7/19 incident protocol.
"""
from pathlib import Path

hb_path = Path('HEARTBEAT.md')

# Read existing content
with open(hb_path, 'r', encoding='utf-8') as f:
    content = f.read()

# New HB #1825 entry to insert at top (after the header docstring)
new_entry = """## HB #1825 (2026-07-29T01:25 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #1824 (00:51): +34min -- Wed凌晨 Token Guard minimal cadence (R012)
- D+12 Wed 01:25 -- quiet zone ACTIVE +2h25m (deep night, Eric asleep)
- Eric silent on THIS cron session 300.17h+ (12d 12h+)
- AnYi webchat silent ~31h+; webchat 「天马行空」last activity 23:25 7/28 (Dataview ROI 3, ~2h past)
- 9-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65)
- post_t0_null_count: 453 -> 454 (454th consecutive null post-T-0, sustained)
- gongshi Day 5/5 FINAL onboarding CLOSED 17:00 (8h25m past) -- 安逸集团蛰伏战略阶段一 D-Day+8h25m
- Token Guard stable; vault 1017 files healthy; 50-external-ingest 190 -> 524 (+176%); 686 -> 230 孤岛 (-67%)
- hbCount: 1824 -> 1825
- Standing by: 5 P0 V2.4 决策 + 6 锚 AHL 锚点 → AHL-Database 写入确认 + MEMORY.md 6 锚点验证 + R65 → self-improving/rules.md

### decision
- **HEARTBEAT_OK** -- HB #1825 = sustain DORMANT protocol, minimal token tick
- **no push**: 9-layer suppression holds + quiet zone PEAK + cron session != webchat decision channel + R65 explicit prohibition
- R256+R257+R258+R260+R261+R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat 「天马行空」activity = webchat-channel signal, NOT cron-channel signal; cron sovereignty unchanged
- Eric in deep-night sleep mode (01:25 = quiet zone peak +2h25m); webchat channel sovereign for any 决策
- Standing by: V2.4 P0 decisions + AHL anchor points confirmation + R65 self-improving write + vault sync (await Eric wake on webchat 「天马行空」)
- Next: per Token Guard cadence (~15-30min midnight slow mode); HB sustained through quiet zone

*2026-07-29T01:25 GMT+8 -- D+12 Wed 01:25 quiet zone +2h25m -- HB #1825 -- DORMANT -- 454th null -- Eric silent on cron = 主权信号 holding -- 安逸集团蛰伏战略阶段一 D-Day+8h25m -- cron session 维持 DORMANT 协议 -- HEARTBEAT_OK*


"""

# Find insertion point: after the first "---" docstring separator (the very top one)
# The structure starts with:
#   # HEARTBEAT.md — B166ER 心跳任务系统
#   > 更新: ...
#   ---
#   ## 一、任务调度原则
# We want to insert AFTER that first "---" and BEFORE "## 一、任务调度原则"

marker = "## 一、任务调度原则"
idx = content.find(marker)
if idx == -1:
    raise RuntimeError("Marker not found: '## 一、任务调度原则'")

# Insert new_entry just before the marker
new_content = content[:idx] + new_entry + "\n" + content[idx:]

# Write back
with open(hb_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"HB #1825 appended. New file size: {len(new_content)} bytes (was {len(content)} bytes)")
print(f"Insertion point at char {idx}: ...{content[idx-20:idx]}|{content[idx:idx+30]}...")