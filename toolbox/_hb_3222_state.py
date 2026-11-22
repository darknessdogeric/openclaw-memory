# -*- coding: utf-8 -*-
"""Update state.json atomically for HB #3222 (R-NEW-V4 compliant: utf-8-sig)."""
import json
import os
from datetime import datetime, timezone, timedelta

state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
tz = timezone(timedelta(hours=8))
now = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S+08:00')

# Read existing state (preserve BOM with utf-8-sig)
with open(state_path, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

# Update fields for HB #3222
state['hbCount'] = 3222
state['lastHbTime'] = now
state['last_tick'] = now
state['last_check'] = now
state['last_hb'] = {'n': 3222, 'ts': now}
state['lastHb'] = now
state['post_t0_null_count'] = 1782
state['nullCount'] = 1782
state['eric_webchat_idle_min'] = 328  # 5h28m at HB #3222 processing time
state['note'] = f'HB 3222; Eric webchat idle ~5h28m; Fri 17:03 workday-PM; DORMANT sustained; suppression layers active; R-NEW-V3 append-only; FILE GAP drift #3218-#3221 noted'

# Atomic write: temp file then replace (R-NEW-V4)
tmp_path = state_path + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# Replace original (preserves BOM through utf-8-sig read on next load)
os.replace(tmp_path, state_path)

print('[OK] state.json updated to HB #3222')
print('[ts]', now)
print('[hbCount]', state['hbCount'])
print('[post_t0_null_count]', state['post_t0_null_count'])