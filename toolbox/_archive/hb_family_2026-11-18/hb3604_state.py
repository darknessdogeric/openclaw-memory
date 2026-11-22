# -*- coding: utf-8 -*-
"""Update heartbeat-state.json for HB #3604."""
import json
from datetime import datetime, timezone, timedelta
import os

TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ)
TS_FILE = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")
EPOCH = int(NOW.timestamp())

STATE_PATH = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

with open(STATE_PATH, "r", encoding="utf-8-sig") as f:
    state = json.load(f)

state["lastHbTime"] = TS_FILE
state["last_hb"] = {"n": 3604, "ts": TS_FILE}
state["hbCount"] = 3604
state["lastDecision"] = "HEARTBEAT_OK"
state["r66_check"] = "aligned; no new Eric input; same posture +1 hb cycle"
state["r69_silence"] = "Expires 2026-08-30 Sun; 10 calendar days remain"
state["notes"] = "HB #3604 Thu 19:33. +2min from HB #3603 (tight cadence). Eric idle ~47h+. R69 T-10d (8/30 Sun). Jinjiang MOU Day 2 IN PROGRESS. 14-layer suppression holds. weekday-evening quiet zone active. No state change. Stay silent."
state["workday_zone"] = "evening-quiet"
state["zone"] = "evening-quiet"
state["anyi_day"] = 28
state["last_update_epoch"] = EPOCH

with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"heartbeat-state.json updated: HB #3604 ({TS_FILE})")
print(f"posture: {state.get('posture')}, decision: {state['lastDecision']}")