# -*- coding: utf-8 -*-
"""Fix heartbeat-state.json corruption and update to HB #489"""
import json, time, re
from datetime import datetime, timezone, timedelta

path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'

with open(path, 'rb') as f:
    raw = f.read()
if raw[:3] == b'\xef\xbb\xbf':
    raw = raw[3:]
content = raw.decode('utf-8')

# Normalize to LF for safe regex replace
content_lf = content.replace('\r\n', '\n')

# Fix: after `"last_update_epoch": 1784356944\n  },` should be `,\n  `
fixed = re.sub(
    r'("last_update_epoch":\s*\d+)(\s*\}\s*,\s*)"silence_baseline"',
    r'\1,\n  "silence_baseline"',
    content_lf
)

# Validate
try:
    state = json.loads(fixed)
    print("JSON parsed successfully after fix")
except json.JSONDecodeError as e:
    print(f"JSON still broken: {e}")
    print("--- fixed content (first 800 chars) ---")
    print(fixed[:800])
    raise SystemExit(1)

# Update to HB #489
now = datetime.now(timezone(timedelta(hours=8)))
state['lastHB']['hb'] = 489
state['lastHB']['chain_hb'] = 489
state['lastHB']['ts'] = now.strftime('%Y-%m-%d %H:%M:%S GMT+8')
state['lastHB']['silence_hours'] = 41.92
state['lastHB']['mode'] = 'silent_standby_zero_push_continue'
state['lastHB']['next_cron'] = '09:00 daily checkin'
state['last_update_epoch'] = int(time.time())

# Write back without BOM, with LF (clean utf-8, R-NEW-V2 compliant)
out = json.dumps(state, ensure_ascii=False, indent=2) + '\n'
with open(path, 'wb') as f:
    f.write(b'\xef\xbb\xbf')  # keep BOM (PowerShell Get-Content displays correctly)
    f.write(out.encode('utf-8'))

print(f"Updated: HB #489, ts={state['lastHB']['ts']}, silence={state['lastHB']['silence_hours']}h")
print(f"File size: {len(out) + 3} bytes (with BOM)")