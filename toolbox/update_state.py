#!/usr/bin/env python3
"""Atomic state.json update for heartbeat cron - R-NEW-V4 enforcement."""
import json
import os
import sys
from datetime import datetime, timezone, timedelta

# CST = UTC+8
CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
iso_now = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

STATE_PATH = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

# Load existing state (handle UTF-8 BOM)
with open(STATE_PATH, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

# Update fields
state['lastHbTime'] = iso_now
state['note'] = f"HB #3249; Eric webchat idle ~11h43m; Fri 23:14 evening-late quiet zone ~46m away; R69 silence Day 22/30 active; 16-layer suppression holds; cron DORMANT sustained; null_milestone_1800 sustained; weekend transition imminent"
state['last_hb'] = {'n': 3249, 'ts': iso_now}
state['lastDecision'] = 'HEARTBEAT_OK'
state['lastHb'] = iso_now
state['nullCount'] = 1803
state['post_t0_null_count'] = 1803
state['hbCount'] = 3249
state['eric_webchat_idle_min'] = 703
state['workday_zone'] = 'evening-late'
state['last_tick'] = iso_now
state['last_check'] = iso_now

# Atomic write via temp file + os.replace
tmp = STATE_PATH + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)
os.replace(tmp, STATE_PATH)

print(f"STATE_UPDATED: hbCount={state['hbCount']}, nullCount={state['nullCount']}, ts={iso_now}")
