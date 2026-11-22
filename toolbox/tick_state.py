import json, os
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now_iso = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S+08:00')

state_path = 'memory/heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

old_hb = state['hbCount']
old_null = state['nullCount']
state['hbCount'] = 3074
state['nullCount'] = 740
state['lastTick'] = now_iso
state['lastDecision'] = 'HEARTBEAT_OK'
state['last_update'] = now_iso

# R-NEW-V4 atomic-tick: write to temp + rename
tmp_path = state_path + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp_path, state_path)

print(f'ATOMIC TICK OK: hb {old_hb}->{state["hbCount"]}, null {old_null}->{state["nullCount"]}, ts={now_iso}')