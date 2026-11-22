#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update heartbeat-state.json atomically for HB #2738"""
import json, os, tempfile
from datetime import datetime, timezone, timedelta

state_file = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
hb_file = r"D:\B166ER-OpenClaw\workspace\memory\HEARTBEAT.md"

# Read current state
with open(state_file, 'r', encoding='utf-8-sig') as f:
    state = json.load(f)

# Read disk reality (R-NEW-V3 cross-check)
disk_size = os.path.getsize(hb_file)

# Update fields
old_hb = state['hbCount']
old_null = state['nullCount']
state['hbCount'] = 2738
state['nullCount'] = 429

# lastHB timestamp
tz_china = timezone(timedelta(hours=8))
now = datetime.now(tz_china)
state['lastHB'] = int(now.timestamp() * 1000)
state['lastUpdate'] = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
state['note'] = f"Sun 16:08 weekend-afternoon quiet zone (post-08:00) DORMANT sustained. Eric silent on cron = 589h+ sustained. R69 Day 10/30 + R266/R277 weekend + R258 cron/webchat separation all hold. 14-layer suppression zero-breach. 429th null. Last Eric webchat activity 11:15-11:39 (~4h53m ago) on hotel-classification V2 rebuild -- V2 9 slides still pending HTML/render/PNG production (production envelope outstanding). R-NEW-V3 enforced: HB #2738 appended via Python open('a') mode (NOT write/Remove-Item/git restore). state.json authoritative; disk reality={disk_size} bytes."
state['posture'] = "DORMANT"

# Atomic write via temp + rename
fd, tmp_path = tempfile.mkstemp(suffix='.json', dir=os.path.dirname(state_file))
try:
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, state_file)
    print(f"OK state.json updated: hbCount {old_hb} -> 2738, nullCount {old_null} -> 429, disk={disk_size}")
except Exception as e:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    raise e