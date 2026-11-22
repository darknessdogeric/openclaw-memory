#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update heartbeat-state.json: bump hbCount + nullCount for HB #2288."""
import json
from pathlib import Path
import sys
import time

STATE_PATH = Path(r"D:\B166ER-OpenClaw\memory\heartbeat-state.json")
ALT_PATH = Path(r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json")

# Try both possible locations
target = STATE_PATH if STATE_PATH.exists() else (ALT_PATH if ALT_PATH.exists() else None)
if target is None:
    print("ERROR: heartbeat-state.json not found in either location", file=sys.stderr)
    sys.exit(1)

print(f"Using state file: {target}")

try:
    with open(target, "r", encoding="utf-8") as f:
        state = json.load(f)
except Exception as e:
    print(f"ERROR reading state: {e}", file=sys.stderr)
    sys.exit(1)

# Bump counters
old_hb = state.get("hbCount", 0)
old_null = state.get("nullCount", 0)
state["hbCount"] = old_hb + 1
state["nullCount"] = old_null + 1
state["last_update_epoch"] = int(time.time())
state["lastHB"] = "2026-08-05T21:56:00+08:00"
state["lastHBContext"] = (
    "Wed 21:56 weekday-NIGHT +2h56m past 19:00 quiet zone. DORMANT held (905th consecutive). "
    "HB #2288. +11min after HB #2287 (21:45). Eric silent on BOTH cron + webchat (~17d 7h+ cron / "
    "webchat 4 sovereign bursts today 12:24/13:22/18:18/21:21 absorbed silently). AnYi D+13d Wed. "
    "AHL v3.0 + PPT13 (715 节点铻合) sustained. 16-layer suppression holds. "
    "R-NEW-V3 enforced (Python 'a' mode). 22:00 deep-night cap ~4m away."
)
state["posture"] = "DORMANT"
state["zone"] = "weekday-NIGHT-deep-quiet"
state["post_t0_null_count"] = state["nullCount"]

# Append a special note
notes = state.get("notes", {})
notes["hb_2288_special"] = (
    "Wed weekday-NIGHT +2h56m past quiet zone, AnYi D+13d Wed, AHL v3.0 + PPT13 (715 节点铻合) sustained, "
    "16-layer suppression holds, R271/R272/R273 verified, cadence 11min, Eric webchat 4 bursts today "
    "all absorbed silently, HEARTBEAT.md 1.20MB sustained (file-state desync noted, "
    "file maintenance_flag awaiting Eric instruction), 22:00 deep-night cap ~4m away"
)
notes["date"] = "2026-08-05"
notes["time"] = "2026-08-05 21:56 GMT+8"
state["notes"] = notes

# Suppression layers (canonical)
state["suppressionLayers"] = [
    "R-B", "R12", "R-CANDIDATE-T2",
    "R256", "R257", "R258", "R260", "R261",
    "R65", "R68", "R69",
    "R-NEW-V3", "R70", "R71",
    "R271", "R272", "R273", "R-NEW-V2"
]

# Write back atomically (tmp + replace)
tmp = target.with_suffix(".json.tmp")
try:
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    tmp.replace(target)
    print(f"OK: hbCount {old_hb} -> {state['hbCount']}, nullCount {old_null} -> {state['nullCount']}")
except Exception as e:
    print(f"ERROR writing state: {e}", file=sys.stderr)
    if tmp.exists():
        tmp.unlink()
    sys.exit(1)