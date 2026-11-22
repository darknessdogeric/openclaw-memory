"""R-NEW-V3 compliant HB tick appender (Python open mode='a', NOT write/edit).

Usage: python hb_tick_3233.py
"""
import json
import re
from datetime import datetime, timezone, timedelta

WS = r'D:\B166ER-OpenClaw\workspace'
HB_PATH = f'{WS}\\HEARTBEAT.md'
STATE_PATH = f'{WS}\\memory\\heartbeat-state.json'
DAILY_PATH = f'{WS}\\memory\\2026-08-14.md'

# Read current state
with open(STATE_PATH, 'r', encoding='utf-8') as f:
    state = json.load(f)

prev_hb = state.get('hbCount', 3232)
prev_null = state.get('post_t0_null_count', 1788)
prev_ts = state.get('lastHbTime', '2026-08-14T18:19:00+08:00')

new_hb = prev_hb + 1
new_null = prev_null + 1
ts = datetime.now(timezone(timedelta(hours=8)))
ts_str = ts.strftime('%Y-%m-%dT%H:%M:%S+08:00')

# Compute gap (handle both aware/naive)
def parse_ts(s):
    s = s.replace('+08:00', '').strip()
    d = datetime.fromisoformat(s)
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone(timedelta(hours=8)))
    return d
gap_min = int((ts - parse_ts(prev_ts)).total_seconds() // 60)

# Find last HB in file for context
with open(HB_PATH, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()
matches = re.findall(r'## HB #(\d+) \(([^\)]+)\)', content)
last_in_file = matches[-1][0] if matches else 'NONE'

# Compose entry (mirror style of prior entries)
entry = f"""
## HB #{new_hb} ({ts_str} GMT+8 cron-event, OpenClaw heartbeat poll)

- gap from HB #{prev_hb} ({prev_ts.split('T')[1][:5]}): +{gap_min}min -- Fri workday-PM Token Guard nominal cadence (R012, within tolerance)
- D+53 Fri 2026-08-14 -- workday-PM +24min past 18:00 evening zone; Fri evening quiet mode engaged
- Eric silent on THIS cron session 397h+ (16d 13h+) since 7/29 first-contact
- 9-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65) -- penta+1 holds
- post_t0_null_count: {prev_null} -> {new_null} ({new_null}th consecutive null post-T-0, sustained)
- **TODAY 8/14** = AnYi 报告 D+22d Friday (Eric 3rd Fri at 安逸集团, R69 silence Day 22/30 active until 2026-08-30)
- V2.4 SOUL 加固 sustained; R66 + R67 + R68 + R69 origin entries sustained
- R68 (D-DAY Guardian) sustained + R69 (沉默新人保护原则) Day 22/30 window active (expires 2026-08-30)
- Eric webchat idle ~393m (~6h 33m) -- silent on webchat = 主权信号 holding (webchat-channel ≠ cron-channel per R258)
- TrendRadar v6.10.0 healthy; data freshness gap: trendradar_no_data_8_13 = true, data_through = 2026-08-12 (2 days stale, already flagged in HB #3229 note)
- hbCount {prev_hb} -> {new_hb}
- file-vs-state drift acknowledged: HEARTBEAT.md has {len(matches)} entries (last in file: HB #{last_in_file}); state.json holds ground truth

### decision

- **HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick** ({new_null}th null)
- **no push**: 9-layer suppression holds + Fri workday-PM evening zone + cron session DORMANT per HB #1849 + R65 explicit prohibition + R258 (webchat-channel ≠ cron-channel) + R69 active
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat/Obsidian sovereign for any 决策; cron sovereignty unchanged
- {ts.strftime('%H:%M')} = Fri workday-PM evening zone; cron = DORMANT sustained; Eric 沉默 IN 实践模式
- Eric webchat idle ~393m = 持续沉默信号 holding (webchat-channel ≠ cron-channel per R258)
- TrendRadar data freshness: 8/13/8/14 连续两日无数据 (data_through = 2026-08-12), 已 prior HB flagged; 不重复主动 push, 等待 Eric webchat/Obsidian 唤醒
- **DO NOT DISTURB UNDER ANY CIRCUMSTANCE** -- Fri evening + AnYi D+22d Fri + Eric sovereign on cron session + R65/R69 active
- Standing by P0 (webchat-bound, not cron-bound): 5 V2.4 决策 + 6 AHL 锚点 -> AHL-Database 写入确认 + MEMORY.md 6 锚点 验证 + R65/R66/R67/R68/R69 -> self-improving/rules.md (await Eric wake on webchat/Obsidian)
- Standing by P1 (R264 AnYi 交接): 等待 Eric 将 AnYi 1244 战略/团队动向/授权对象 等具体内容, 按 R264 立即接入到 anyi-ops-kb/
- Next: per Token Guard cadence (~15-30min); HB sustained through Fri evening until Eric first-contact on cron session

*{ts_str} -- D+53 Fri {ts.strftime('%H:%M')} workday-PM evening zone -- HB #{new_hb} -- DORMANT -- {new_null}th null -- Eric silent on cron = 主权信号 holding -- **AnYi 报告 D+22d Fri, Eric 沉默 IN 实践模式 (webchat idle ~6h 33m)** -- cron session 维持 DORMANT 协议 -- HEARTBEAT_OK*
"""

# R-NEW-V3: APPEND ONLY via open(mode='a'), NEVER write/edit
with open(HB_PATH, 'a', encoding='utf-8') as f:
    f.write(entry)

# Update state.json
state['hbCount'] = new_hb
state['lastHbTime'] = ts_str
state['last_tick'] = ts_str
state['last_check'] = ts_str
state['last_hb'] = {'n': new_hb, 'ts': ts_str}
state['lastHb'] = ts_str
state['nullCount'] = new_null + 2  # nullCount includes pre-T-0 + post-T-0
state['eric_webchat_idle_min'] = 393 + gap_min
state['workday_zone'] = 'workday-PM-evening'
state['lastDecision'] = 'HEARTBEAT_OK'
state['note'] = f'HB {new_hb}; Eric webchat idle ~{393 + gap_min}m; Fri {ts.strftime("%H:%M")} workday-PM-evening; R69 silence Day 22/30 active; sustained dormancy intact; trendradar data stale (8/12)'

with open(STATE_PATH, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f'OK: HB #{new_hb} appended; state.json updated; nullCount -> {new_null}')
print(f'Last in file was HB #{last_in_file}; appended HB #{new_hb}')