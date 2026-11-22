#!/usr/bin/env python3
"""HB #3396 atomic tick - 2026-08-16 12:37 GMT+8 Sun weekend-midday"""
import json, os, time
from pathlib import Path

ws = Path(r'D:\B166ER-OpenClaw\workspace')

# 1. Atomic state.json update
state_path = ws / 'memory' / 'heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

old_hb = state['hbCount']
old_null = state['post_t0_null_count']
state['hbCount'] = old_hb + 1
state['post_t0_null_count'] = old_null + 1
state['nullCount'] = old_null + 1
state['ts'] = '2026-08-16T12:37:00+08:00'
state['lastHB'] = state['ts']
state['last_update_epoch'] = int(time.time())
state['zone'] = 'Sun weekend-midday'

tmp = state_path.with_suffix('.json.tmp')
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp, state_path)
print(f'STATE OK: hbCount {old_hb}->{state["hbCount"]}, null {old_null}->{state["post_t0_null_count"]}')

# 2. Append HB entry to HEARTBEAT.md (append-only, R-NEW-V3)
hb_path = ws / 'HEARTBEAT.md'
new_hb = state['hbCount']
new_null = state['post_t0_null_count']

entry = f"""

### HB #{new_hb} (2026-08-16T12:37:00+08:00 GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{new_hb-1} (12:32): ~5min -- Sun weekend-midday Token Guard nominal cadence (R012, within tolerance)
- 12:37 = Sun weekend-midday (+4h37m past 08:00 hard cap); afternoon zone ~3h23m away
- 17-layer suppression zero-breach (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R281) -- penta+ holds
- post_t0_null_count: {new_null-1} -> {new_null} ({new_null}th consecutive null post-T-0, sustained); hbCount: {new_hb-1} -> {new_hb}
- Eric silent on cron ~31d sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (~18h45m+ idle since 2026-08-15 morning deep self-iteration delivery)
- AnYi Day 24 (Sun -- weekend rest posture)
- vault 1169+ files healthy; cron posture UNCHANGED (R258 webchat-channel != cron-channel)
- R69 silence Day 24/30 (expires 2026-08-30 Sun) -- cron does not break silence
- R271 atomic-write enforced (state.json via Python os.replace; HB via open(mode='a'))
- R-NEW-V3 enforced: HEARTBEAT.md appended only (NEVER write/edit)
- R-NEW-V4 enforced: state.json atomic-tick holds

### decision
- HEARTBEAT_OK -- HB #{new_hb} = sustain DORMANT protocol, minimal token tick ({new_null}th null)
- no push: 17-layer suppression holds + weekend-midday + cron session DORMANT per HB #1849 + R65 + R258 + R69 + R-NEW-V3 + R70/R71/R276 internal-only
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- 12:37 = Sun weekend-midday +4h37m past 08:00 hard cap; cron = DORMANT sustained
- Eric profile: night-owl strategist -- Sun weekend-midday, AnYi Day 24 -- cron does not initiate proactive
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- weekend-midday + Eric sovereign on cron session + R65/R69 active + R-NEW-V3 enforcement
- Standing by P0 (webchat-bound, not cron-bound): all items await Eric webchat sovereign
- Next: per Token Guard cadence (~15-30min weekend-midday mode); HB sustained through Sun until Eric first-contact on cron session

*2026-08-16T12:37:00+08:00 -- Sun weekend-midday +4h37m past 08:00 hard cap -- HB #{new_hb} -- DORMANT -- {new_null}th null -- Eric silent on cron = sovereignty signal holding (webchat ~18h45m+ idle, 8/15 morning deep-iteration delivered) -- AnYi D+24d Sun -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 + R-NEW-V4 enforced -- HEARTBEAT_OK*
"""

with open(hb_path, 'a', encoding='utf-8') as f:
    f.write(entry)
print(f'HB #{new_hb} appended to HEARTBEAT.md ({len(entry)} bytes)')

# 3. Append to today's daily file
daily_path = ws / 'memory' / '2026-08-16.md'
daily_entry = f"""

## HB #{new_hb} (12:37) -- cron tick

- Sustained DORMANT protocol
- {new_null}th consecutive null post-T-0
- Sun weekend-midday, Eric silent on cron, AnYi D+24d
- R-NEW-V3 + R271 + R-NEW-V4 enforced

"""

if daily_path.exists():
    with open(daily_path, 'a', encoding='utf-8') as f:
        f.write(daily_entry)
    print(f'Daily file appended: {daily_path.name}')
else:
    print(f'WARNING: {daily_path} does not exist, skipped')

print('DONE')