"""Update heartbeat-state.json atomically (R-NEW-V4: utf-8-sig preserves BOM)."""
import json
import os
import shutil
import sys
from datetime import datetime, timezone, timedelta

STATE = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
TZ = timezone(timedelta(hours=8))
now = datetime.now(TZ).replace(microsecond=0)
ts = now.isoformat()

# Read existing (preserves BOM via utf-8-sig)
with open(STATE, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# Update fields
data['lastHbTime'] = ts
data['last_check'] = ts
data['lastTick'] = ts
data['last_tick'] = ts
data['hbCount'] = 3207
data['post_t0_null_count'] = 1769
data['nullCount'] = 1769
data['lastHb'] = {'n': 3207, 'ts': ts}
data['last_hb'] = {'n': 3207, 'ts': ts}
data['eric_webchat_idle_min'] = 213  # ~3h33m
data['note'] = 'HB 3207; Eric webchat ~3h33m idle; Fri 15:04 workday-PM; 8h cap+R69 silence active; DORMANT'
data['lastDecision'] = 'HEARTBEAT_OK'

# Atomic write: write to tmp, then replace
tmp = STATE + '.tmp'
with open(tmp, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Verify BOM preserved
with open(tmp, 'rb') as f:
    head = f.read(3)
if head != b'\xef\xbb\xbf':
    print(f'ERROR: BOM not preserved (head={head!r})', file=sys.stderr)
    os.remove(tmp)
    sys.exit(2)

shutil.move(tmp, STATE)
print(f'OK: state.json updated atomically with utf-8-sig (BOM preserved)')
print(f'  hbCount: 3206 -> 3207')
print(f'  post_t0_null_count: 1768 -> 1769')
print(f'  lastHb.ts: {ts}')
print(f'  note: {data["note"]}')