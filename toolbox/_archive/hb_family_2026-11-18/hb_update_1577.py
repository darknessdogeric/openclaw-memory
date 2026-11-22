#!/usr/bin/env python3
"""HB #1577 heartbeat state update — 2026-07-27 08:29 GMT+8"""
import json
from datetime import datetime, timezone, timedelta

# Load current state
with open('memory/heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

# HB #1577 parameters
hb_time = datetime(2026, 7, 27, 8, 29, 0, tzinfo=timezone(timedelta(hours=8)))
hb_timestamp = int(hb_time.timestamp())
prev_timestamp = state['lastHB']
gap_sec = hb_timestamp - prev_timestamp
gap_min = round(gap_sec / 60, 1)

# Eric silent hours (last contact 7/16 13:16)
last_contact = datetime.fromtimestamp(state['lastContactTimestamp'], tz=timezone(timedelta(hours=8)))
silent_hours = round((hb_time - last_contact).total_seconds() / 3600, 2)

# AnYi webchat hours
anyi_since = datetime.fromisoformat(state['anyiSinceTime'])
anyi_hours = round((hb_time - anyi_since).total_seconds() / 3600, 2)

# Update state
state['lastHB'] = hb_timestamp
state['lastHBTime'] = hb_time.isoformat()
state['hbCount'] = state.get('hbCount', 1575) + 1
state['postT0NullCount'] = state.get('postT0NullCount', 226) + 1
state['ericSilentThisSessionHours'] = silent_hours
state['anyiWebchatHoursSinceStart'] = anyi_hours

notes = 'D+11 Mon morning 08:29. DORMANT. 8-layer. Triple Confluence ALL CLOSED. 7/24 D-Day PASSED +68h. HEARTBEAT_OK. HB #' + str(state['hbCount']) + '.'
state['notes'] = notes

with open('memory/heartbeat-state.json', 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print('HB #' + str(state['hbCount']) + ' registered')
print('  gap: +' + str(gap_min) + 'min from HB #' + str(state['hbCount'] - 1))
print('  Eric silent: ' + str(silent_hours) + 'h+')
print('  AnYi active: ' + str(anyi_hours) + 'h+')
print('  post_t0_null_count: ' + str(state['postT0NullCount']))
print('  notes: ' + state['notes'])
