import json
from datetime import datetime, timezone, timedelta

state_file = "D:/B166ER-OpenClaw/workspace/memory/heartbeat-state.json"
with open(state_file, 'r', encoding='utf-8') as f:
    state = json.load(f)

now = datetime.now(timezone(timedelta(hours=8)))

state['lastHeartbeat'] = now.isoformat()
state['notes'] = f"{now.strftime('%H:%M')} GMT+8 · 深夜安静时段 (23:00-08:00) · 跳过所有主动检查"

with open(state_file, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"[{now.strftime('%H:%M')}] HEARTBEAT_OK · 深夜安静时段")
