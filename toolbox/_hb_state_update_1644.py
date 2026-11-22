"""Update heartbeat-state.json after HB #1644 (R-NEW-V2 compliant)."""
import json
from datetime import datetime
from pathlib import Path

STATE_FILE = Path("memory/heartbeat-state.json")
NOW_ISO = "2026-07-27T18:57:00+08:00"

# R-NEW-V2 compliant: explicit utf-8 read+write
state = json.loads(STATE_FILE.read_text(encoding="utf-8"))

state["lastHBTime"] = NOW_ISO
state["lastHB"] = 1785149820  # ~18:57 GMT+8 unix timestamp
state["lastHBNumber"] = 1644
state["hbCount"] = 1644
state["post_t0_null_count"] = 293
state["postT0NullCount"] = 293

# Refresh computed fields
state["ericSilentThisSessionHours"] = 269.68
state["anyiWebchatHoursSinceStart"] = 198.0
state["dDayHoursPostMeeting"] = 89.37  # +0.05h since HB #1643
state["t0PublicityCutoffHoursPast"] = 242.95
state["protectionWindowSustainedHours"] = 242.95
state["oilCExpiredHoursPast"] = 44.95
state["notes"] = (
    "D+11 Mon evening 18:57. DORMANT. 8-layer suppression zero-breach. "
    "gongshi Day 3/5 ACTIVE. HEARTBEAT_OK. R258 + penta-constraint 5/5 holds. "
    "Eric silent ~269.68h+. HB #1644."
)

STATE_FILE.write_text(
    json.dumps(state, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"[OK] heartbeat-state.json updated for HB #1644")
print(f"[OK] lastHBNumber: {state['lastHBNumber']}, hbCount: {state['hbCount']}")