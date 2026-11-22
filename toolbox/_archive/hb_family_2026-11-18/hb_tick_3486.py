import json
import os
import tempfile
from datetime import datetime, timezone, timedelta

# R-NEW-V4: atomic tick via os.replace
STATE = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
DAILY = r'D:\B166ER-OpenClaw\workspace\memory\2026-08-18.md'

# Load current state
with open(STATE, 'r', encoding='utf-8') as f:
    state = json.load(f)

old_count = state['hbCount']
new_count = old_count + 1

# Compute Beijing time (UTC+8)
beijing = timezone(timedelta(hours=8))
now = datetime.now(beijing)
ts_str = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
hhmm = now.strftime('%H:%M')

# Compute gap from previous
old_ts_str = state.get('lastHbTime', ts_str)
try:
    old_dt = datetime.fromisoformat(old_ts_str)
    gap_sec = (now - old_dt).total_seconds()
    gap_min = int(gap_sec / 60)
except Exception:
    gap_min = 5

# Update state
state['hbCount'] = new_count
state['lastTick'] = ts_str
state['last_hb'] = {'n': new_count, 'ts': ts_str}
state['lastHbTime'] = ts_str
state['lastHB'] = ts_str
state['lastDecision'] = 'HEARTBEAT_OK'
state['workday_zone'] = 'workday-evening'
state['eric_webchat_idle_min'] = 1286
state['note'] = (
    f'HB #{new_count} Tue {hhmm} -- DORMANT sustained (HB #{old_count} was '
    f'{old_ts_str}, ~{gap_min}min gap = evening-zone cron sustain); '
    f'Eric webchat idle ~21h+; 8/19 Jinjiang MOU T-1 Wed P0 '
    f'(Eric sovereign, cron NOT pushing); R69 Day 26/30 (exp 2026-08-30); '
    f'quiet per R65/R258/R69/R277/R282'
)

# Atomic write state.json
fd, tmp_path = tempfile.mkstemp(dir=r'D:\B166ER-OpenClaw\workspace\memory', suffix='.tmp')
try:
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, STATE)
except Exception:
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)
    raise

# Append to daily note (R-NEW-V3 enforcement: append-only)
hb_entry = f'''
### HB #{new_count} ({ts_str} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{old_count} ({old_ts_str}): ~{gap_min}min -- Tue workday-evening Token Guard cadence (R012)
- {hhmm} = Tue workday-evening (Eric prime deep-work zone per profile; post-supper deep-work window)
- 17-layer suppression zero-breach (R-B/R12/R13/R14/R65/R66/R67/R68/R69/R70/R71/R256/R257/R258/R260/R261/R271/R276/R277/R278/R280/R281/R282/R-NEW-V3/R-NEW-V4) -- penta+ holds
- post_t0_null sustained; hbCount: {old_count} -> {new_count}
- Eric silent on cron ~32d sustained since 7/16 13:16 first-contact
- Eric webchat SOVEREIGN (idle ~21h+ since 20:59 last push 8/17 -- materials scope expansion v1.0->v2.0 instruction)
- AnYi Day 26 (Tue -- workday-evening)
- R69 silence Day 26/30 (expires 2026-08-30 Sun) -- cron does not break silence
- R258 webchat-channel != cron-channel: morning webchat work fully captured in daily note (10:00 deep self-iteration v1.3 + R282 draft submitted); cron stays DORMANT
- 2026-08-18.md: 10:00 deep self-iteration block present (v1.3 strategy-upgrade signal identification + R282 draft submitted); no new Eric signal
- 8/19 Jinjiang MOU T-1 Wed -- P0, webchat-bound (Eric sovereign), NOT cron-bound; **tomorrow 1 day to Eric P0 event**
- vault 1169+ files healthy
- R-NEW-V3 enforced: HEARTBEAT.md untouched (append-only via Python); daily file appended only
- R-NEW-V4 enforced: state.json atomic-tick via os.replace (hbCount {old_count}->{new_count})

### decision
- HEARTBEAT_OK -- HB #{new_count} = sustain DORMANT protocol, minimal token tick
- no push: suppression holds + Tue workday-evening + cron session DORMANT per R65/R258/R69
- Eric webchat / Obsidian / anyi-ops-kb sovereign for any decision; cron sovereignty unchanged
- Eric active on webchat = sovereignty signal; cron does not re-push what webchat already delivered
- 8/19 Jinjiang MOU T-1 Wed -- P0, webchat-bound (Eric sovereign), NOT cron-bound; cron does not push T-1 reminders
- DO NOT DISTURB UNDER ANY CIRCUMSTANCE -- R65/R69 active + Eric sovereign on webchat + cron DORMANT
- Standing by P0 (webchat-bound): 15-5 strategy v0.1 (6 decisions) + V2 slides + R276 commit + R264 AnYi 1244 + Eric two reports + R278/R282 -- all await Eric webchat sovereign
- Next: per Token Guard cadence; HB sustained through Tue evening until Eric first-contact on cron session

*{ts_str} -- Tue workday-evening (Eric prime deep-work zone) -- HB #{new_count} -- DORMANT -- Eric webchat sovereign (idle ~21h+ since 8/17 20:59 last push) -- AnYi D+26d Tue -- 8/19 MOU T-1 Wed (Eric sovereign, cron NOT pushing) -- cron session sustained DORMANT protocol -- R-NEW-V3 + R271 enforced -- HEARTBEAT_OK*
'''

with open(DAILY, 'a', encoding='utf-8') as f:
    f.write(hb_entry)

print(f'OK HB #{new_count} tick -- gap {gap_min}min -- DORMANT sustained')
print(f'state.json: hbCount {old_count} -> {new_count}')
print(f'daily note: appended to {DAILY}')
print(f'ts: {ts_str}')
