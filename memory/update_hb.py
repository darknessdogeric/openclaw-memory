import json
from datetime import datetime, timezone, timedelta

state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
with open(state_path, encoding='utf-8') as f:
    s = json.load(f)

s['lastChecks']['vault'] = int(datetime.now().timestamp())
s['lastChecks']['trendradar'] = int(datetime.now().timestamp())
s['EricSilenceDays'] = 6
s['vaultUpdate'] = '1301/1306 indexed'
s['AHLWindowDays'] = 33

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(s, f, indent=2, ensure_ascii=False)

print('OK')
