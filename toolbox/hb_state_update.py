import json, os
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S+08:00')

path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
with open(path, 'r', encoding='utf-8') as f:
    s = json.load(f)

s['hbCount'] = s.get('hbCount', 3083) + 1
s['nullCount'] = s.get('nullCount', 751) + 1
s['lastTick'] = now
s['lastDecision'] = 'HEARTBEAT_OK'
s['last_update'] = now
s['lastHbTime'] = now

# Preserve other fields as-is (r271, r_new_v3, r258, r69_silence, anyi_day, etc.)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(s, f, ensure_ascii=False, indent=2)

print(f"Updated hbCount={s['hbCount']}, nullCount={s['nullCount']}, lastTick={now}")
