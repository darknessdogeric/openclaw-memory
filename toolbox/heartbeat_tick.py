"""Heartbeat atomic tick per R-NEW-V4."""
import json, os, time, sys
from pathlib import Path

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace')
state_path = WORKSPACE / 'memory' / 'heartbeat-state.json'

state = json.loads(state_path.read_text(encoding='utf-8'))

old_count = state['hbCount']
new_count = old_count + 1
now_str = '2026-08-20T12:59:00+08:00'  # ~3min from HB #3570 (12:56:56)
state['hbCount'] = new_count
state['lastHbTime'] = now_str
state['last_check'] = now_str
state['last_update_epoch'] = int(time.time())
state['last_hb'] = {'n': new_count, 'ts': now_str}
state['lastDecision'] = 'HEARTBEAT_OK'

# Atomic write via os.replace (R-NEW-V4)
tmp = state_path.with_suffix('.json.tmp')
tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
os.replace(tmp, state_path)

print(f'ATOMIC_TICK: {old_count} -> {new_count}')
print(f'posture: {state.get("posture", "?")}')
print(f'lastDecision: {state["lastDecision"]}')
print(f'r69: {state.get("r69_silence", "?")}')
print(f'sovereign: {state.get("zone", "?")}')
