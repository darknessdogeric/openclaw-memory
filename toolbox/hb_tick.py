#!/usr/bin/env python3
"""Atomic state.json tick for heartbeat (R-NEW-V4)."""
import json, os, sys, time
from datetime import datetime, timezone, timedelta

ws = r"D:\B166ER-OpenClaw\workspace"
tz = timezone(timedelta(hours=8))
ts = datetime.now(tz).isoformat()
epoch = int(time.time())

hb = 3742
prev = 3741

state = {
    "zone": "Sat weekend-afternoon",
    "hbCount": hb,
    "last_tick": ts,
    "last_check": ts,
    "last_heartbeat_response": "ok_quiet",
    "posture": "DORMANT",
    "last_tick_epoch": epoch,
    "cronSession": "DORMANT",
    "lastDecision": "HEARTBEAT_OK",
    "last_hb": {"n": hb, "ts": ts},
    "lastHB": ts,
    "notes": f"Sat 16:27. HB #{hb}. R69 silence Day 29/30 (8d to lift 8/30 Sun). Eric weekend rest. cron DORMANT. Sustaining minimal token tick. ~4min since HB #{prev}, no Eric-side signal on cron channel."
}

tmp = os.path.join(ws, "memory", "heartbeat-state.json.tmp")
final = os.path.join(ws, "memory", "heartbeat-state.json")
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=4)
os.replace(tmp, final)
print(f"state.json atomic-tick OK -- hbCount {prev} -> {hb}")
print(f"ts = {ts}")
