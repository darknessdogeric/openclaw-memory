# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone, timedelta

state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

beijing_tz = timezone(timedelta(hours=8))
now = datetime.now(beijing_tz)
ts = int(now.timestamp())

# silence start = 2026-07-09 04:29 GMT+8
silence_start = 1752046140

state['silenceHours'] = round((ts - silence_start) / 3600, 2)
state['deepWorkHours'] = round((ts - silence_start) / 3600, 2)

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

silence_h = state['silenceHours']
print(f'silenceHours={silence_h}h ({silence_h/24:.2f} days)')
print(f'deepWorkHours={state["deepWorkHours"]}h')
print(f'hbCount={state["hbCount"]}')
print(f'Now: {now.strftime("%Y-%m-%d %H:%M:%S %Z")}')