#!/usr/bin/env python3
"""HB #2743 state update - atomic write per R-NEW-V3 + R271."""
import json
import os
import time
from datetime import datetime, timezone, timedelta

STATE = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
TMP = STATE + ".tmp"

# Compute current time in GMT+8
tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
ts_ms = int(now.timestamp() * 1000)
ts_iso = now.strftime("%Y-%m-%dT%H:%M:%S.0000000+08:00")

new_state = {
    "posture": "DORMANT",
    "hbCount": 2743,
    "note": (
        "Sun 16:55 weekend-afternoon post-hard-cap zone (+8h55m past 08:00) "
        "DORMANT sustained. Eric silent on cron = 589h+ sustained. "
        "R69 Day 10/30 + R266/R277 weekend + R258 cron/webchat separation all hold. "
        "14-layer suppression zero-breach. 434th null. "
        "Last Eric webchat activity 11:15-11:39 (~5h55m ago) on hotel-classification V2 rebuild "
        "-- V2 9 slides still pending HTML/render/PNG production. "
        "R-NEW-V3 enforced: HB #2743 appended via PowerShell Add-Content "
        "(NOT write/Remove-Item/git restore). state.json authoritative."
    ),
    "lastHB": ts_ms,
    "lastUpdate": ts_iso,
    "nullCount": None,
}

# Atomic write: tmp + os.replace
with open(TMP, "w", encoding="utf-8") as f:
    json.dump(new_state, f, ensure_ascii=False, indent=2)
    f.flush()
    os.fsync(f.fileno())

os.replace(TMP, STATE)
print(f"OK state.json hbCount=2743 lastUpdate={ts_iso}")