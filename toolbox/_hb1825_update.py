import json
from pathlib import Path

# Read current state
state_path = Path('memory/heartbeat-state.json')
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

# Update for HB #1825
state['lastHBTime'] = '2026-07-29 01:25'
state['lastHBNumber'] = 1825
state['hbCount'] = 1825
state['post_t0_null_count'] = state.get('post_t0_null_count', 453) + 1
state['ericSilentThisSessionHours'] = round(299.6 + (34/60), 2)
state['notes'] = 'HB #1825. Wed 01:25 GMT+8. Quiet zone ACTIVE. DORMANT sustained. Eric silent on cron session. 9-layer suppression holds. R65 explicit prohibition. R14 handoff 100% ready. Gap from HB #1824 (00:51) = +34min (Token Guard minimal cadence). HEARTBEAT_OK.'

# Write back
with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print('STATE UPDATED TO HB #1825')
print(json.dumps({k: state[k] for k in ['lastHBNumber', 'lastHBTime', 'post_t0_null_count', 'ericSilentThisSessionHours']}, indent=2, ensure_ascii=False))