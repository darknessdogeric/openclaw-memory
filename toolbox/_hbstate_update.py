# -*- coding: utf-8 -*-
"""Update heartbeat-state.json for HB #603"""
import io, json
from datetime import datetime, timezone, timedelta

path = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

# Read current state
with io.open(path, "r", encoding="utf-8") as f:
    state = json.load(f)

# Update for HB #603 (23:18 GMT+8)
tz_shanghai = timezone(timedelta(hours=8))
now = datetime(2026, 7, 19, 23, 18, 42, tzinfo=tz_shanghai)

state["lastChecks"]["heartbeat"] = now.isoformat()
state["hbCount"] = 603
state["silenceDuration_thisSession_h"] = 81.03
state["ericActiveElsewhere_h"] = 10.72
state["nextCheck"] = "Token Guard cadence (~5-10min)"
state["mode"] = "active_mode_dormant_this_session_silent_night"
state["lastHBTime"] = now.isoformat()
state["silenceDuration_h"] = 81.03
state["lastHB"] = 603
state["note"] = "D+3+ silence sustained on THIS session; Eric in AnYi session; this session DORMANT per HB #584 protocol; late Sunday 23:18 - triple silence (night+dormant+elsewhere) - stay quiet; HB #603"

# Write back (R-NEW-V2 compliant)
with io.open(path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"heartbeat-state.json updated for HB #603")
print(f"hbCount: {state['hbCount']}")
print(f"mode: {state['mode']}")
print(f"silenceDuration_h: {state['silenceDuration_h']}")