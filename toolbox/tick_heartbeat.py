#!/usr/bin/env python3
"""Atomic heartbeat state tick (R-NEW-V4)"""
import json, os, time

STATE = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"
TMP = STATE + ".tmp"

with open(STATE, "r", encoding="utf-8-sig") as f:
    s = json.load(f)

s["ts"] = "2026-08-16T13:37:00+08:00"
s["lastHB"] = "2026-08-16T13:37:00+08:00"
s["hbCount"] = 3403
s["nullCount"] = 1954
s["last_update_epoch"] = int(time.time())

with open(TMP, "w", encoding="utf-8") as f:
    json.dump(s, f, indent=4, ensure_ascii=False)

# Atomic replace (os.replace is atomic on Windows)
os.replace(TMP, STATE)
print(f"OK: hb={s['hbCount']} null={s['nullCount']} ts={s['ts']}")