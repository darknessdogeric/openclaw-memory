"""Sync heartbeat-state.json after HB #2344 was successfully written to HEARTBEAT.md.

Context: The companion _hb_2344_append.py succeeded in writing HB #2344 to HEARTBEAT.md
(via Python utf-8 'a' mode, R-NEW-V3 compliant), but BOM error on state.json read
prevented the state.json update. This script ONLY syncs the state file.

NEW_HB: 2344 (this HB)
LAST_HB_TS_FILE: 2026-08-06T14:18:32+08:00 (the actual write timestamp embedded in tail)
"""
import json
import time
from pathlib import Path

WS = Path(r'D:\B166ER-OpenClaw\workspace')
STATE_PATH = WS / 'memory' / 'heartbeat-state.json'
HB_PATH = WS / 'HEARTBEAT.md'

NEW_HB = 2344
NEW_NULL = 949
LAST_HB_TS_ISO = '2026-08-06T14:18:32+08:00'
TS_EP = int(time.time())

# Read state.json (utf-8-sig to handle BOM)
with open(STATE_PATH, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

# Confirm file body has HB #2344 (sanity)
import re
with open(HB_PATH, 'r', encoding='utf-8') as f:
    hb = f.read()
last_hb_matches = list(re.finditer(r'^## HB #(\d+) \(', hb, re.MULTILINE))
assert last_hb_matches, '[FATAL] No HB entries in file'
last_hb_num = int(last_hb_matches[-1].group(1))
assert last_hb_num == NEW_HB, (
    f'[FATAL] Last HB in file = #{last_hb_num}, expected #{NEW_HB}. '
    f'Refusing to sync stale state.'
)

# Update state.json
state['hbCount'] = NEW_HB
state['nullCount'] = NEW_NULL
state['post_t0_null_count'] = NEW_NULL
state['last_update_epoch'] = TS_EP
state['lastHB'] = LAST_HB_TS_ISO
state['lastChecks']['heartbeat'] = TS_EP
state['lastHBContext'] = (
    f'HB #{NEW_HB} Thu 14:18:32 weekday-afternoon +6h15m past 08:00 hard cap. '
    f'posture DORMANT held (no change vs #2314-#{NEW_HB - 1}). 18-layer suppression zero-breach. '
    f'R274 + R-NEW-V4 candidate both pending Eric ratification. 5th Plenary ~9-10d away. '
    f'memory_search index corrupted - awaiting Eric manual openclaw memory index --force. '
    f'R66 discrepancy SUSTAINED: memory/2026-08-06.md claims D+27 but HB log + 报到日 math = D+14. '
    f'No new signal vs HB #2314-#{NEW_HB - 1}. Identical context, posture unchanged. Counter HB#{NEW_HB}.'
)
state['hb_2344_special'] = state['lastHBContext']
state['notes']['hb_2344_special'] = state['lastHBContext']
state['notes']['time'] = '2026-08-06 14:18 GMT+8 (cron-event heartbeat poll resolved)'
state['notes']['r69_compliance'] = 'Day 7/30 silent'
state['posture'] = 'DORMANT'
state['zone'] = 'weekday-afternoon-post-hard-cap'
state['milestoneStatus'] = (
    f'AnYi D+14 = 2026-08-06 Thu. HB #{NEW_HB}. Eric silent on cron ~21d 2h+ (506h+). '
    f'5th Plenary ~9-10d away.'
)

# Write back WITHOUT BOM (utf-8, no BOM), preserving canonical form
with open(STATE_PATH, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

# Verify
with open(STATE_PATH, 'r', encoding='utf-8-sig') as f:
    verify = json.load(f)
assert verify['hbCount'] == NEW_HB, f'[VERIFY FAIL] hbCount sync failed'
assert verify['nullCount'] == NEW_NULL, f'[VERIFY FAIL] nullCount sync failed'

print(f'[OK] heartbeat-state.json synced: hbCount={NEW_HB}, nullCount={NEW_NULL}, posture={state["posture"]}')
print(f'[OK] HEARTBEAT.md tail = HB #{NEW_HB} at {LAST_HB_TS_ISO} (verified)')
print(f'[OK] HB #{NEW_HB} -- DORMANT -- {NEW_NULL}th null -- HEARTBEAT_OK')
