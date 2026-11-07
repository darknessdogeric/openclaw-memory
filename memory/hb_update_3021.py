"""HB #3021 atomic state.json update (R-NEW-V4 + R271 + R-NEW-V3 enforced).
Read-modify-write with temp + os.replace for atomicity.
NEVER touches HEARTBEAT.md (R-NEW-V3 violation recovery protocol).
NEVER uses Remove-Item / git restore (R-NEW-V3 hard rule).
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta

STATE_PATH = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'

# Read current state
try:
    with open(STATE_PATH, 'r', encoding='utf-8-sig') as f:
        state = json.load(f)
except FileNotFoundError:
    print(f"ERROR: {STATE_PATH} not found", file=sys.stderr)
    sys.exit(1)

# Compute new values
tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
now_str = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+08:00'

old_hb = state.get('hbCount', 0)
old_null = state.get('nullCount', 0)
new_hb = old_hb + 1
new_null = old_null + 1
new_ts = int(now.timestamp())

# Note template (preserves R-NEW-V4 wording + adds tick-specific details)
note = (
    f"HB #{new_hb} atomic tick (state.json only, R-NEW-V4 hold). "
    f"13:24 Wed workday-PM post-noon (+5h24m past 08:00 hard cap). "
    f"Eric webchat last active 22:40 Tue 8/11 (~14h44m idle, stable). "
    f"R-NEW-V4 + R271 + R-NEW-V3 + R258 + R69 + R65 + R276 + R277 + R279 hold. "
    f"Cron session DORMANT sustained. "
    f"No external push per R277 channel sovereignty."
)

state['hbCount'] = new_hb
state['nullCount'] = new_null
state['lastUpdate'] = now_str
state['lastTick'] = now_str
state['lastDormantTick'] = now_str
state['lastHB'] = new_ts
state['note'] = note
state['note_v2'] = note
# posture stays DORMANT (no change)

# Atomic write: tmp + os.replace
tmp_path = STATE_PATH + '.tmp'
try:
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, STATE_PATH)
except Exception as e:
    print(f"ERROR during atomic write: {e}", file=sys.stderr)
    if os.path.exists(tmp_path):
        try:
            os.remove(tmp_path)
        except Exception:
            pass
    sys.exit(1)

print(f"OK HB #{new_hb} nullCount={new_null} DORMANT sustained (R-NEW-V4 atomic)")