import json, pathlib

hb_path = pathlib.Path('memory/HEARTBEAT.md')
actual_size = hb_path.stat().st_size
print(f'Actual HEARTBEAT.md size: {actual_size:,} bytes')

with open(hb_path, 'r', encoding='utf-8') as f:
    content = f.read()
print(f'HB #2443 in file: {"HB #2443" in content}')
print(f'Contains my entry footer: {"HB appended via Python append (NOT write)" in content}')

state_path = pathlib.Path('memory/heartbeat-state.json')
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

prev_actual = state['maintenanceFlag'].get('actual_bytes', 1729384)

state['maintenanceFlag']['actual_bytes'] = actual_size
state['maintenanceFlag']['ceiling_bytes'] = 1572864
state['maintenanceFlag']['overage_pct'] = round((actual_size - 1572864) / 1572864 * 100, 2) if actual_size > 1572864 else 0
state['maintenanceFlag']['heartbeat_md_over_1_5mb'] = actual_size > 1572864

note_addition = f' | NOTE: HEARTBEAT.md actual size {actual_size:,} bytes (was {prev_actual:,} per stale state.json); suggests external rotation between HB #2268 and current; state.json (hbCount=2443) is source of truth'
state['notes'] = state['notes'] + note_addition

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f'Updated state.json: actual_bytes={actual_size:,}, overage_pct={state["maintenanceFlag"]["overage_pct"]}%')