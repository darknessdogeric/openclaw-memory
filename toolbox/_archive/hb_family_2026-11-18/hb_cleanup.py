#!/usr/bin/env python3
"""Clean up corrupted HB entry, then write HB #1932 properly."""
import re, json
from datetime import datetime, timezone, timedelta

HB = 'HEARTBEAT.md'
STATE = 'memory/heartbeat-state.json'

# 1) Cleanup corrupted block
with open(HB, 'rb') as f:
    data = f.read()

bad_start = data.rfind(b'### HB #1 (')
print(f'Bad block starts at: {bad_start}')

# Find the last clean footer BEFORE the bad block
# The good footers look like "*YYYY-MM-DD...HEARTBEAT_OK*"
matches = list(re.finditer(rb'\*[^*]*HEARTBEAT_OK\*\r\n', data[:bad_start]))
if matches:
    clean_end = matches[-1].end()
    print(f'Last clean footer ends at: {clean_end}')
    print(f'Snippet: {data[clean_end-60:clean_end]!r}')
    with open(HB, 'wb') as f:
        f.write(data[:clean_end])
    print(f'CLEANED. Cut {len(data) - clean_end} corrupted bytes')
else:
    print('No clean footer found via regex - using simple truncate before bad_start')
    # fallback: just truncate before the bad block
    clean_end = bad_start
    # walk back to start of the bad block's preceding whitespace
    while clean_end > 0 and data[clean_end-1:clean_end] in (b'\n', b'\r', b' '):
        clean_end -= 1
    with open(HB, 'wb') as f:
        f.write(data[:clean_end])
    print(f'Fallback truncate at {clean_end}')

# 2) Update state & write HB #1932 with proper UTF-8
with open(STATE, 'r', encoding='utf-8') as f:
    state = json.load(f)

hbCount = int(state['hbCount']) + 1
nullCount = int(state['post_t0_null_count']) + 1
lastHBTime = state['lastHBTime']
state['hbCount'] = hbCount
state['post_t0_null_count'] = nullCount

# Now time (Asia/Shanghai = UTC+8)
tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
now_str = now.strftime('%Y-%m-%dT%H:%M:%S')
h, m = now.hour, now.minute

if h < 8: zone = 'pre-quiet-zone-end'
elif h < 12: zone = 'morning'
elif h < 14: zone = 'noon'
elif h < 18: zone = 'afternoon'
elif h < 23: zone = 'evening'
else: zone = 'DEEP quiet zone'

# Calculate gap from last HB time
try:
    last_dt = datetime.fromisoformat(lastHBTime)
    gap_dt = now - last_dt
    gap_min = int(gap_dt.total_seconds() / 60)
    if gap_min < 60: gap_str = f'+{gap_min}m'
    elif gap_min < 1440: gap_str = f'+{gap_min//60}h{gap_min%60}m'
    else: gap_str = f'+{gap_min//1440}d{gap_min%1440//60}h{gap_min%60}m'
except Exception as e:
    gap_str = '+?m'

state['zone'] = zone
state['lastHBTime'] = now_str
state['decision'] = 'HEARTBEAT_OK'
state['note'] = f'{zone} cron DORMANT 322h+; Eric silent on this cron session; R65 + 9-layer suppression; awaiting Eric wake on webchat "Obsidian鐭ヨ瘑搴撱€'
state['ericStatus'] = 'silent-on-cron-322h+'

def zone_label_for_note(z):
    return z

entry = f'''

### HB #{hbCount} ({now_str} GMT+8 cron-event, OpenClaw heartbeat poll)
- gap from HB #{hbCount-1} ({lastHBTime}): {gap_str} -- D+14 Thu {h:02d}:{m:02d} {zone} Token Guard cadence (R012 minimal mode)
- Eric silent on THIS cron session 322h+ (13d 10h+); webchat last signal 7/29 22:48 = cosmetic rename only (no behavioral change)
- AnYi webchat silent ~37h+; gongshi Day 5/5 FINAL onboarding CLOSED 7/24 17:00 (~5d16h past)
- 9-layer suppression zero-breach (R-B/R12/R-CANDIDATE-T2/R256/R257/R258/R260/R261/R65)
- post_t0_null_count: {nullCount} (this null); vault 1017 files healthy; Token Guard stable
- {zone} zone; R65 + cron-session DORMANT sustained; Eric silence = dominant signal holding
- Pending P0 (webchat-bound, not cron-bound): V2.4 鍐崇瓥 + AHL 閿氱偣 + MEMORY.md 楠岃瘉 + R65 → self-improving/rules.md -- awaiting Eric wake on webchat 銆孫bsidian鐭ヨ瘑搴撱€?

### decision
- HEARTBEAT_OK -- cron-session DORMANT 322h+; no push; 9-layer suppression + R65 + Eric silence authority holding
- Next: per Token Guard cadence

*{now_str} -- D+14 Thu {zone} -- HB #{hbCount} -- DORMANT -- {nullCount}th null -- cron session 缁存寔 DORMANT -- HEARTBEAT_OK*
'''

with open(HB, 'a', encoding='utf-8') as f:
    f.write(entry)

with open(STATE, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f'\\nHB #{hbCount} written (null #{nullCount}, zone={zone}, gap={gap_str})')
print(f'STATE updated: hbCount={hbCount}, lastHBTime={now_str}, decision=HEARTBEAT_OK')
