#!/usr/bin/env python3
"""Heartbeat atomic-tick R-NEW-V4. 2026-08-22 HB #3691."""
import json, os

PATH = r"D:\B166ER-OpenClaw\workspace\memory\heartbeat-state.json"

with open(PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

old_hb = state["hbCount"]
new_hb = old_hb + 1
new_ts = "2026-08-22T09:10:00+08:00"

new_entry = {"hb": new_hb, "ts": new_ts}
state["lastHBs"] = [new_entry] + state.get("lastHBs", [])[:2]
state["hbCount"] = new_hb
state["last_tick"] = new_ts
state["last_heartbeat_response"] = "ok_quiet"
state["post_t0_null_count"] = state.get("post_t0_null_count", 0) + 1
state["notes"] = (
    f"Sat 09:10. HB #{new_hb}, +5min after #{old_hb}. "
    f"R69 silence Day 30/30 (8d to lift 8/30 Sun). "
    f"Eric weekend rest. cron DORMANT per R65/R69/R258/R277/R282. "
    f"No mail/calendar/notifications. Sustaining minimal token tick."
)

tmp = PATH + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
os.replace(tmp, PATH)

print(f"OK HB #{new_hb} at {new_ts}")
