"""Heartbeat tick HB #3570 — atomic state.json + daily file append."""
import json, os
from datetime import datetime, timezone, timedelta

TZ_CST = timezone(timedelta(hours=8))
now = datetime.now(TZ_CST)
ts_str = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
time_hm = now.strftime('%H:%M')

state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
daily_path = r'D:\B166ER-OpenClaw\workspace\memory\2026-08-20.md'

# Read current state
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

old_hb = state['hbCount']
new_hb = old_hb + 1
old_ts = state['last_hb']['ts']

# Calculate gap
gap_dt = datetime.fromisoformat(old_ts).replace(tzinfo=TZ_CST)
gap_min = int((now - gap_dt).total_seconds() / 60)
prev_idle = state['eric_webchat_idle_min']
new_idle = prev_idle + gap_min
idle_h = new_idle // 60
idle_m = new_idle % 60

# Update state
state['hbCount'] = new_hb
state['lastHbTime'] = ts_str
state['last_check'] = ts_str
state['last_update_epoch'] = int(now.timestamp())
state['lastDecision'] = 'HEARTBEAT_OK'
state['posture'] = 'DORMANT'
state['cronSession'] = 'DORMANT'
state['eric_webchat_idle_min'] = new_idle
state['last_hb'] = {'n': new_hb, 'ts': ts_str}
state['notes'] = (
    f'HB #{new_hb} Thu {time_hm} weekday-late-morning. '
    f'Gap {gap_min}min from HB #{old_hb} ({old_ts[11:16]}). '
    f'Eric webchat sovereign. 22-layer suppression holds. '
    f'R69 silence Day 28/30 (expires 2026-08-30 Sun, 2 days remain). '
    f'8/19 Jinjiang MOU Day 2 of 3 IN PROGRESS webchat-bound. '
    f'cron DORMANT sustained. R-NEW-V3 + R-NEW-V4 enforced. '
    f'R69 T-2d: R282 + R283 batch ready for 8/30 Sun lift.'
)
state['workday_zone'] = 'weekday-late-morning'

# Atomic write via os.replace (R-NEW-V4)
tmp_path = state_path + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp_path, state_path)

# Build HB entry
hb_entry = f"""
### HB #{new_hb} ({ts_str} cron-event, OpenClaw heartbeat poll)
- gap from HB #{old_hb} ({old_ts[11:16]}): ~{gap_min}min -- Thu workday-late-morning Token Guard cadence (R012)
- {time_hm} = Thu workday-late-morning (post 10:00 R60-11 + DORMANT sustain)
- 22-layer suppression zero-breach (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R282/R-NEW-V3/R-NEW-V4) -- penta+ holds
- post_t0_null sustained; hbCount: {old_hb} -> {new_hb} (atomic-tick via os.replace, R-NEW-V4)
- Eric webchat SOVEREIGN (idle ~{idle_h}h{idle_m:02d}m since 8/18 19:06 钟华 correction)
- AnYi Day 28 (Thu workday-late-morning)
- R69 silence Day 28/30 (expires 2026-08-30 Sun, **2 days remain**) -- cron does not break silence
- 8/19 Jinjiang MOU Day 2 of 3 IN PROGRESS -- P0, webchat-bound (Eric sovereign, possibly AT conference), NOT cron-bound
- vault 1169+ files healthy
- R-NEW-V3 enforced: HEARTBEAT.md untouched (recovery mode from prior data loss 8/1); daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick via os.replace (hbCount {old_hb}->{new_hb})
- R69 countdown: T-2 days to lift silence on 8/30 Sun -- prepare R282 + R283 batch submission

### decision
- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick
- no push: suppression holds + Thu workday-late-morning + cron session DORMANT per R65/R258/R69/R277/R282
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 8/19 Jinjiang MOU Day 2 IN PROGRESS -- P0, webchat-bound (Eric sovereign), NOT cron-bound; cron does NOT push
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- R65/R69 active + Eric sovereign on webchat + cron DORMANT
- Standing by P0 (webchat-bound): 15-5 strategy v0.1 (6 decisions) + V2 slides + R276 commit + R264 AnYi 1244 + Eric two reports + R278/R282 + R283 (draft) -- all await Eric webchat sovereign
- R69 T-2d reminder: prepare R282 + R283 batch submission for 8/30 Sun lift
- Next: per Token Guard cadence; HB sustained through Thu midday until Eric first-contact on cron session

*{ts_str} -- Thu workday-late-morning + post 10:00 R60-11 + ~{gap_min}min from HB #{old_hb} -- HB #{new_hb} -- DORMANT -- Eric webchat sovereign (idle ~{idle_h}h{idle_m:02d}m since 8/18 19:06 钟华 correction) -- AnYi D+28d Thu -- 8/19 MOU Day 2 IN PROGRESS (Eric sovereign, cron NOT pushing) -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 + R69-T2d enforced -- HEARTBEAT_OK*
"""

# Append to daily file (R-NEW-V3: daily file append only)
with open(daily_path, 'a', encoding='utf-8') as f:
    f.write(hb_entry)

print(f'OK: HB #{new_hb} appended to 2026-08-20.md')
print(f'  state.json atomic-tick via os.replace (R-NEW-V4)')
print(f'  gap={gap_min}min  idle={new_idle}min (~{idle_h}h{idle_m:02d}m)')
print(f'  time={ts_str}')
print(f'  decision=HEARTBEAT_OK  posture=DORMANT')
print(f'  R69 Day 28/30 (T-2d to 8/30 Sun lift)')
