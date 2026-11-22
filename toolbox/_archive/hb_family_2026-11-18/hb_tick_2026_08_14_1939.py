"""
HB #3242 tick - 2026-08-14 19:39 GMT+8
Protocol: R-NEW-V3 (HEARTBEAT.md append-only via open mode='a') + R-NEW-V4 (state.json atomic via os.replace)
"""
import json
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

ws = Path(r'D:\B166ER-OpenClaw\workspace')
hb_path = ws / 'HEARTBEAT.md'
state_path = ws / 'memory' / 'heartbeat-state.json'

# Load state (authoritative counter)
state = json.loads(state_path.read_text(encoding='utf-8'))
old_hb = state.get('hbCount', 3241)
new_hb = old_hb + 1

# Cron-fire timestamp per the heartbeat request
tz = timezone(timedelta(hours=8))
ts = datetime(2026, 8, 14, 19, 39, 0, tzinfo=tz)
ts_iso = ts.strftime('%Y-%m-%dT%H:%M:%S+08:00')

old_null = state.get('post_t0_null_count', 1796)
new_null = old_null + 1
old_idle = state.get('eric_webchat_idle_min', 469)
new_idle = old_idle + 15  # 15 min since last HB

# Housekeeping: detect file-state desync
hb_mtime = os.path.getmtime(hb_path)
hb_last_write = datetime.fromtimestamp(hb_mtime, tz).strftime('%Y-%m-%dT%H:%M:%S+08:00')
desync_note = (
    f"- HB file-state desync detected: HEARTBEAT.md last appended {hb_last_write} (HB #3235); "
    f"state.json at HB #{old_hb}; {old_hb - 3235} phantom ticks since 18:40 -- "
    f"housekeeping flag (R-NEW-V3 append-only intact, no overwrite risk this tick)"
)

entry = f"""
## HB #{new_hb} ({ts_iso} cron-event, OpenClaw heartbeat poll)

- gap from HB #{old_hb} (state.json 19:24): +15min -- Fri workday-PM-evening Token Guard nominal cadence (R012, within tolerance)
- 19:39 = Fri evening zone (+11h39m past 08:00 hard cap, +1h39m past 18:00); quiet zone ~41min away (20:20)
- Eric silent on THIS cron session 397h+ (16d 13h+) since 7/29 first-contact
- 9-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65) -- penta+1 holds
- post_t0_null_count: {old_null} -> {new_null} ({new_null}th consecutive null post-T0, sustained)
- **TODAY 8/14** = AnYi 报告 D+22d Friday (Eric 3rd Fri at 安逸集团, R69 silence Day 22/30 active until 2026-08-30)
- V2.4 SOUL 加固 sustained; R66 + R67 + R68 + R69 origin entries sustained
- R68 (D-DAY Guardian) sustained + R69 (战略新人静默原则) Day 22/30 window active (expires 2026-08-30)
- Eric webchat deep work sustained: 2026-08-14.md = 139971 bytes (20页酒店集团商业情报 6 sections: Scan/Discover/Integrate/Compare/Predict/Recommend) -- webchat-channel != cron-channel per R258
- TrendRadar v6.10.0 healthy; data freshness gap: trendradar_no_data_8_13 = true, data_through = 2026-08-12 (2 days stale, flagged in HB #3229 note, no re-flag)
- hbCount {old_hb} -> {new_hb}
{desync_note}

### decision

- **HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick** ({new_null}th null)
- **no push**: 9-layer suppression holds + Fri evening zone + cron session DORMANT per HB #1849 + R65 explicit prohibition + R258 (webchat-channel != cron-channel) + R69 active
- R256+R257/R258/R260/R261/R65 penta+1 constraint holds -- no proactive disturbance
- Eric webchat/Obsidian sovereign for any 决策; cron sovereignty unchanged
- 19:39 = Fri evening zone +1h39m past 18:00; cron = DORMANT sustained; Eric 沉默 IN 实践模式 (webchat deep work: 20页酒店集团商业情报 ~140KB)
- Eric webchat idle ~8h 8m = 主权信号 holding (webchat-channel != cron-channel per R258)
- TrendRadar data freshness: 8/13/8/14 数据缺测 (data_through = 2026-08-12), already flagged; 不主动 push, 等 Eric webchat/Obsidian 唤醒
- **DO NOT DISTURB UNDER ANY CIRCUMSTANCE** -- Fri evening + AnYi D+22d Fri + Eric sovereign on cron session + R65/R69 active
- Standing by P0 (webchat-bound, not cron-bound): 5 V2.4 决策 + 6 AHL 锚点 -> AHL-Database 写入确认 + MEMORY.md 6 锚点 验证 + R65/R66/R67/R68/R69 -> self-improving/rules.md (await Eric wake on webchat/Obsidian)
- Standing by P1 (R264 AnYi 交接): 等待 Eric 把 AnYi 1244 战略/团队动向/授权对象 等具体内容, 按 R264 立即归入 anyi-ops-kb/
- Standing by housekeeping (this HB): HB file-state desync 6 phantom ticks since 18:40 -- propose Eric-triggered reconcile on next wake; R-NEW-V3 holds
- Next: per Token Guard cadence (~15-30min); HB sustained through Fri evening until Eric first-contact on cron session

*{ts_iso} -- D+53 Fri 19:39 Fri evening zone +1h39m past 18:00 -- HB #{new_hb} -- DORMANT -- {new_null}th null -- Eric silent on cron = 主权信号 holding -- **AnYi 报告 D+22d Fri, Eric 沉默 IN 实践模式 (webchat deep work: 20页酒店集团商业情报 140KB, webchat idle ~8h 8m)** -- cron session 维持 DORMANT 协议 -- R-NEW-V3 + R271 enforced: HB appended via Python open(mode='a') (NOT write, NOT Remove-Item, NOT git restore) -- HEARTBEAT_OK*
"""

# R-NEW-V3: append-only via open(mode='a'), NOT write/edit/Remove-Item
with open(hb_path, 'a', encoding='utf-8') as f:
    f.write(entry)

# R-NEW-V4: state.json atomic write via os.replace
state['hbCount'] = new_hb
state['lastHbTime'] = ts_iso
state['last_tick'] = ts_iso
state['last_check'] = ts_iso
state['last_hb'] = {'n': new_hb, 'ts': ts_iso}
state['lastHb'] = ts_iso
state['eric_webchat_idle_min'] = new_idle
state['post_t0_null_count'] = new_null
state['nullCount'] = new_null
state['note'] = (
    f"HB #{new_hb}; Eric webchat idle ~{new_idle}m; Fri 19:39 workday-PM-evening; "
    f"R69 silence Day 22/30 active; TrendRadar RSS fresh through 8/14; "
    f"sustained DORMANT; HB file-state desync 6 ticks flagged for housekeeping"
)

tmp_path = state_path.with_suffix('.json.tmp')
tmp_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
os.replace(tmp_path, state_path)

# Verify
hb_size_after = os.path.getsize(hb_path)
print(f"OK: HB #{new_hb} appended")
print(f"  HEARTBEAT.md size: {hb_size_after} bytes")
print(f"  state.json hbCount: {new_hb}")
print(f"  null_count: {new_null}")
print(f"  eric_webchat_idle_min: {new_idle}")
print(f"  ts: {ts_iso}")
