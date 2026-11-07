#!/usr/bin/env python3
"""Atomic heartbeat state update - R271 enforced tmp+replace pattern."""
import json
import os
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
state_path = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

now = datetime.now(tz).isoformat(timespec='seconds')

with open(state_path, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

state['hbCount'] = 2872
state['nullCount'] = 541
state['lastDormantTick'] = now
state['lastUpdate'] = now
state['posture'] = 'DORMANT'
state['note'] = 'Tue 2026-08-11 00:59 GMT+8 post-midnight quiet-zone DORMANT sustained. HB #2872 null tick, +5m from #2871. null 540 -> 541. Eric webchat last active 22:40 Mon AHL work. R69 silence Day 10/30 active. R258 cron/webchat separation in effect.'

tmp_path = state_path + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp_path, state_path)

print(f"state.json atomic-updated: hb={state['hbCount']} null={state['nullCount']} ts={now}")
