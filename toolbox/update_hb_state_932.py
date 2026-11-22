# -*- coding: utf-8 -*-
"""Update heartbeat-state.json for HB #932."""
import json
from datetime import datetime, timezone, timedelta

state_path = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

now = datetime(2026, 7, 22, 16, 30, 0, tzinfo=timezone(timedelta(hours=8)))
anyi_start = datetime(2026, 7, 19, 12, 33, 0, tzinfo=timezone(timedelta(hours=8)))
eric_start = datetime(2026, 7, 16, 13, 16, 0, tzinfo=timezone(timedelta(hours=8)))
t0 = datetime(2026, 7, 18, 0, 0, 0, tzinfo=timezone(timedelta(hours=8)))
d_day = datetime(2026, 7, 24, 9, 0, 0, tzinfo=timezone(timedelta(hours=8)))

def hrs(t1, t2):
    return round((t2 - t1).total_seconds() / 3600, 2)

state['hbCount'] = 932
state['lastHB'] = 932
state['lastCheck'] = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
state['silenceHours'] = hrs(eric_start, now)
state['ericActiveHours'] = hrs(anyi_start, now)
state['t0_past_hours'] = hrs(t0, now)
state['nextDDayHours'] = hrs(now, d_day)
state['mode'] = 'DORMANT'
state['nextSignificantCheck'] = '21:00 evening self-iter (~4.5h)'
state['notes'] = 'HB#932: +2.83h (afternoon transition). Wednesday 16:30. DORMANT sustained. 7/24 D-Day T-1 (~40.5h). No actionable signal. Next: 21:00 evening self-iter.'

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print('[OK] heartbeat-state.json updated: hbCount=932')
print('[OK] silence=' + str(state['silenceHours']) + 'h, anyi=' + str(state['ericActiveHours']) + 'h')
print('[OK] t0+=' + str(state['t0_past_hours']) + 'h, dday-=' + str(state['nextDDayHours']) + 'h')