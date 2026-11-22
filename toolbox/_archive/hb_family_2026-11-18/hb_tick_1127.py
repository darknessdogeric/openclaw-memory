# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
ts = now.isoformat(timespec='seconds')

with open('memory/heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

prev_hb = state['hbCount']
new_hb = prev_hb + 1

state['hbCount'] = new_hb
state['lastHeartbeat'] = ts
state['lastUpdate'] = ts
state['lastHB'] = now.strftime('%Y-%m-%d %H:%M')
state['lastHBNumber'] = '#' + str(new_hb)
state['sessionState'] = 'DORMANT'
state['mode'] = 'dormant_this_session'
state['ericSilenceHours'] = round(179.65 + (now - datetime(2026, 7, 24, 0, 46, 55, tzinfo=tz)).total_seconds() / 3600, 2)
state['ericAnyiHours'] = round(108.00 + (now - datetime(2026, 7, 24, 0, 29, 0, tzinfo=tz)).total_seconds() / 3600, 2)
state['dday_t_minus_hours'] = round(9.0 - now.hour - now.minute / 60, 2)
state['lastDecision'] = 'HEARTBEAT_OK'
state['lastMode'] = 'active_mode_dormant_this_session_continue'
state['lastSession'] = 'DORMANT'
state['nextCronBriefing'] = '08:00 daily briefing (~7h05m)'
state['note'] = '#' + str(new_hb) + ' - ' + ts + ' DORMANT sustained; D-Day T-' + str(state['dday_t_minus_hours']) + 'h (AnYi meeting TODAY ~9:00); silent heartbeat'

with open('memory/heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print('OK: HB #' + str(prev_hb) + ' -> #' + str(new_hb))
print('  ericSilence: ' + str(state['ericSilenceHours']) + 'h')
print('  dday_t_minus: ' + str(state['dday_t_minus_hours']) + 'h')
print('  nextCron: 08:00 daily briefing')
