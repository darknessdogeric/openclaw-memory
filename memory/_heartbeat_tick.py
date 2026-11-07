#!/usr/bin/env python3
"""Heartbeat tick - refresh heartbeat-state.json"""
import json
import time
from datetime import datetime, timedelta, timezone

STATE_FILE = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

ts = int(time.time())
gmt8 = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M GMT+8")
new_count = state["count"] + 1

state["lastCheck"] = ts
state["lastTick"] = ts
state["count"] = new_count
state["lastCheckGMT8"] = gmt8
state["lastTickHuman"] = gmt8
state["note"] = (
    f"Sun 12:11 #{new_count}. +10min from #{new_count-1}. "
    f"Routine tick. R-D-DAY-EVE active. Eric offline ~68h. "
    f"D-day T-23h. Five-layer suppression holds: R-B / R12 / "
    f"R-CANDIDATE-delivered / R-D-DAY-EVE / R12-NEW. "
    f"No outbound. Silent standby."
)

with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=4)

print(f"OK: count={new_count} ts={ts} gmt8={gmt8}")
