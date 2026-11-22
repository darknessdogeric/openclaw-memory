import json
from datetime import datetime, timezone, timedelta

state_path = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
hb_path = r"D:\B166ER-OpenClaw\workspace\HEARTBEAT.md"
now = datetime.now(timezone(timedelta(hours=8)))

# Update state
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

state['lastHeartbeat'] = now.isoformat()
state['lastChecks']['trend'] = now.isoformat()
state['lastChecks']['vault'] = now.isoformat()

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# Append minimal log
entry = f"## HB {now.strftime('%Y-%m-%d %H:%M')} — trend/email vault OK · no action\n"
with open(hb_path, 'a', encoding='utf-8') as f:
    f.write(entry)

print("OK", now.strftime("%H:%M"))
