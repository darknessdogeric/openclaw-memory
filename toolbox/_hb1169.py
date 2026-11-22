# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone, timedelta

now = datetime.now(timezone(timedelta(hours=8)))
state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'

with open(state_path, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

state['lastChecks']['heartbeat'] = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
state['lastChecks']['hbCount'] = 1169
state['lastChecks']['next_significant_check'] = '21:00 R60-11 evening self-iter (~11.30h)'

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

ts = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
print('OK: HB #1169 state updated at ' + ts)
print('gap from HB #1168 (09:33): +9min')
print('next_significant_check: ' + state['lastChecks']['next_significant_check'])
