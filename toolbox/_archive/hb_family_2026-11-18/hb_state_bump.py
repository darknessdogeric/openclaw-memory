#!/usr/bin/env python3
"""Bump hbCount/nullCount/timestamps in heartbeat-state.json (R-NEW-V3 compliant)."""
import json
import time
import sys

path = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
new_hb = int(sys.argv[1]) if len(sys.argv) > 1 else None
new_null = int(sys.argv[2]) if len(sys.argv) > 2 else None

with open(path, "r", encoding="utf-8") as f:
    state = json.load(f)

if new_hb is not None:
    state["hbCount"] = new_hb
if new_null is not None:
    state["nullCount"] = new_null
state["lastChecks"]["heartbeat"] = int(time.time())

with open(path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"hbCount={state['hbCount']} nullCount={state['nullCount']} heartbeat_ts={state['lastChecks']['heartbeat']}")