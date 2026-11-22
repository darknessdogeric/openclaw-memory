"""Atomic heartbeat state updater — used by cron heartbeat polls.

Usage: python _hb_state_update.py <hb_count> <null_count> <timestamp> <note>
"""
import json
import os
import sys
import time

state_file = "memory/heartbeat-state.json"

hb = int(sys.argv[1])
null_count = int(sys.argv[2])
ts = sys.argv[3]
note = sys.argv[4]

with open(state_file, "r", encoding="utf-8") as f:
    s = json.load(f)

s["hbCount"] = hb
s["nullCount"] = null_count
s["lastHB"] = int(time.time() * 1000)
s["lastUpdate"] = ts
s["posture"] = "DORMANT"
s["note"] = note

tmp = state_file + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(s, f, ensure_ascii=False, indent=2)
os.replace(tmp, state_file)
print(f"STATE_UPDATED hb={hb} null={null_count}")
