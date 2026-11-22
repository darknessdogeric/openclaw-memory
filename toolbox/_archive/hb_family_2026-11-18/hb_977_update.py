"""HB #977 heartbeat-state.json updater (R-NEW-V2 compliant)"""
import json
from datetime import datetime, timezone, timedelta

with open(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

now = datetime(2026, 7, 22, 23, 38, 0, tzinfo=timezone(timedelta(hours=8)))
last_check = datetime.fromisoformat(state['lastCheck'])

new_state = dict(state)
new_state['lastCheck'] = now.isoformat()
new_state['hbCount'] = state['hbCount'] + 1
new_state['silenceHours'] = round(state['silenceHours'] + (now - last_check).total_seconds() / 3600, 2)
new_state['ericActiveHours'] = round(state['ericActiveHours'] + (now - last_check).total_seconds() / 3600, 2)
new_state['nextDDayHours'] = round(state['nextDDayHours'] - (now - last_check).total_seconds() / 3600, 2)
new_state['lastHB'] = new_state['hbCount']

with open(r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(new_state, f, indent=2, ensure_ascii=False)

hb = new_state['hbCount']
sh = new_state['silenceHours']
eh = new_state['ericActiveHours']
dh = new_state['nextDDayHours']
print(f'HB #{hb} state updated:')
print(f'  silenceHours: {sh}')
print(f'  ericActiveHours: {eh}')
print(f'  nextDDayHours: {dh}')