#!/usr/bin/env python3
"""Minimal atomic heartbeat tick (R-NEW-V4). No HEARTBEAT.md write."""
import json, os
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
ts_str = now.strftime('%Y-%m-%dT%H:%M:%S') + '+08:00'

state_path = r'D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json'

with open(state_path, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

hb_count = state.get('hbCount', 0) + 1

state['hbCount'] = hb_count
state['last_tick'] = ts_str
state['last_heartbeat_response'] = 'ok_quiet'
state['last_tick_epoch'] = int(now.timestamp())

state['notes'] = (
    'Sat 12:29. HB #' + str(hb_count) + '. R69 silence Day 29/30 '
    '(8d to lift 8/30 Sun). Eric weekend rest. cron DORMANT. '
    'Sustaining minimal token tick.'
)

last_hbs = state.get('lastHBs', [])
last_hbs.append({'hb': hb_count, 'ts': ts_str})
state['lastHBs'] = last_hbs[-5:]

tmp_path = state_path + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp_path, state_path)

print('ATOMIC-TICK OK | HB #' + str(hb_count) + ' | ts=' + ts_str)
print('R-NEW-V4 enforced | notes=' + state['notes'])
