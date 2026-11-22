# -*- coding: utf-8 -*-
"""Update heartbeat-state.json for HB #417 (atomic write)."""
import json, os
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)
ts_unix = int(now.timestamp())

state_path = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

state["silenceHours"] = round(state["silenceHours"] + 0.07, 2)
state["deepWorkHours"] = round(state["deepWorkHours"] + 0.10, 2)
state["hbCount"] = 417
state["lastHB"] = "#417"
state["lastChecks"]["heartbeat"] = ts_unix
state["mode"] = "silent_standby_zero_push"
state["notes"] = (
    f"#417 (silent standby). 2026-07-17 17:22 GMT+8. Eric silent ~28.10h since 7/16 13:16. "
    f"Publicity cutoff 7/18 = TOMORROW (~21h, FINAL day pre-announcement). 4-layer suppression intact. "
    f"WAIC 2026 day-1 ongoing -- non-trigger per R14. Zero push holding. R14 handoff = 100% ready."
)

# atomic write: temp + replace
tmp = state_path + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2, ensure_ascii=False)
os.replace(tmp, state_path)

print(f"OK HB #417 state updated: hbCount={state['hbCount']}, silence={state['silenceHours']}h, deepWork={state['deepWorkHours']}h")